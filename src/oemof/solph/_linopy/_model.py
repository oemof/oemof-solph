# -*- coding: utf-8 -*-

"""The linopy model of a solph energy system.

SPDX-License-Identifier: MIT
"""

import linopy
import numpy as np
import pandas as pd
import xarray as xr

from oemof.solph._linopy._data import to_array
from oemof.solph._linopy._registry import get_builder
from oemof.solph._models import Model

INF = float("inf")


class LinopyModel:
    """An energy system optimisation model built with linopy.

    Experimental. Builds the same optimisation problem as
    :class:`oemof.solph.Model` from the same
    :class:`~oemof.solph.EnergySystem`, but with linopy instead of Pyomo:
    variables and constraints are created as arrays, one container per
    kind, which makes building and handing the model to a solver much
    faster.

    Parameters
    ----------
    energysystem : EnergySystem
        The energy system to optimise.
    constraint_groups : list, optional
        Additional constraint groups (block classes), as for
        :class:`oemof.solph.Model`. Each needs a builder registered with
        :func:`~oemof.solph._linopy.register_builder`.
    auto_construct : bool
        Build the model on instantiation (default True).

    Attributes
    ----------
    linopy : linopy.Model
        The underlying linopy model. Custom constraints are added here.
    flow : linopy.Variable
        All flows, with dimensions ("flow", "timestep"). The position of a
        flow along "flow" is :meth:`flow_position`.
    """

    BACKEND = "linopy"
    CONSTRAINT_GROUPS = list(Model.CONSTRAINT_GROUPS)

    def __init__(
        self,
        energysystem,
        *,
        constraint_groups=None,
        auto_construct=True,
    ):
        self.es = energysystem
        self.timeincrement = self.es.timeincrement

        if constraint_groups is None:
            constraint_groups = []
        self._constraint_groups = type(self).CONSTRAINT_GROUPS + list(
            constraint_groups
        )
        self._constraint_groups += [
            i
            for i in self.es.groups
            if hasattr(i, "CONSTRAINT_GROUP")
            and i not in self._constraint_groups
        ][::-1]

        self.flows = self.es.flows()
        self.dual = None
        self.rc = None

        self.linopy = linopy.Model()
        self._objective_added = False
        self._objective_constant = 0.0
        self._objective_terms = {}
        self._var_meta = {}
        self._expressions = {}
        self._result_vars = {}
        self._solver_results = None
        self.solver_return = None
        self.solver = None

        if auto_construct:
            self._construct()

    # ------------------------------------------------------------------
    # construction
    # ------------------------------------------------------------------

    def _construct(self):
        self._add_parent_block_sets()
        self._add_parent_block_variables()
        self._add_child_blocks()
        self._add_objective()

    def _add_parent_block_sets(self):
        """Time sets, capacity periods and the flow index."""
        es = self.es
        self.nodes = list(es.nodes)

        if es.timeincrement is None:
            msg = (
                "The EnergySystem needs to have a valid 'timeincrement' "
                "attribute to build a model."
            )
            raise AttributeError(msg)

        n_steps = len(es.timeincrement)
        self.TIMESTEPS = range(n_steps)
        self.TIMEPOINTS = range(n_steps + 1)
        self.timestep_index = pd.RangeIndex(n_steps, name="timestep")
        self.timepoint_index = pd.RangeIndex(n_steps + 1, name="timepoint")
        self.timeincrement_array = to_array(
            es.timeincrement, n_steps, name="timeincrement"
        )

        if es.transitional_single_period:
            period_of_timestep = np.zeros(n_steps, dtype=np.int64)
        else:
            period_of_timestep = np.concatenate(
                [
                    np.full(len(cp), k, dtype=np.int64)
                    for k, cp in enumerate(es.capacity_periods)
                ]
            )[:n_steps]
        self.period_of_timestep = period_of_timestep
        n_periods = int(period_of_timestep.max()) + 1 if n_steps else 1
        self.CAPACITY_PERIODS = range(n_periods)
        self.capacity_period_index = pd.RangeIndex(
            n_periods, name="capacity_period"
        )
        self.TIMESTEPS_IN_PERIOD = {
            p: list(np.flatnonzero(period_of_timestep == p))
            for p in self.CAPACITY_PERIODS
        }

        self.TSAM_MODE = es.tsa_parameters is not None
        if self.TSAM_MODE:
            msg = (
                "Energy systems with tsa_parameters (solph's tsam mode) are "
                "not supported by the linopy backend yet."
            )
            raise NotImplementedError(msg)
        self.tsam_weighting = np.ones(n_steps)

        self.FLOWS = list(self.flows.keys())
        self._flow_position = {k: i for i, k in enumerate(self.FLOWS)}
        self.flow_entity_index = pd.RangeIndex(len(self.FLOWS), name="flow")

    def _add_parent_block_variables(self):
        """The flow variable with its bounds, as in
        :meth:`oemof.solph.Model._add_parent_block_variables`."""
        n_flows, n_steps = len(self.FLOWS), len(self.TIMESTEPS)
        lower = np.full((n_flows, n_steps), -INF)
        upper = np.full((n_flows, n_steps), INF)
        # flows with `fix`: Pyomo fixes them, which makes them constants
        self._fixed_flows = np.zeros(n_flows, dtype=bool)
        p_of_t = self.period_of_timestep
        n_periods = len(self.CAPACITY_PERIODS)

        for k, (i, o) in enumerate(self.FLOWS):
            flow = self.flows[i, o]
            if flow.nominal_capacity is not None:
                nominal = to_array(
                    flow.nominal_capacity, n_periods, name="nominal_capacity"
                )[p_of_t]
                if flow.fix is not None:
                    fixed = to_array(flow.fix, n_steps, name="fix") * nominal
                    lower[k] = fixed
                    upper[k] = fixed
                    self._fixed_flows[k] = True
                else:
                    upper[k] = (
                        to_array(flow.maximum, n_steps, name="maximum")
                        * nominal
                    )
                    if not flow.nonconvex:
                        lower[k] = (
                            to_array(flow.minimum, n_steps, name="minimum")
                            * nominal
                        )
                    elif not flow.bidirectional:
                        lower[k] = 0
            elif not flow.bidirectional:
                lower[k] = 0

        self.flow = self.add_variables(
            "flow",
            entities=self.FLOWS,
            entity_dim="flow",
            index="timestep",
            lower=lower,
            upper=upper,
        )

    def _add_child_blocks(self):
        """Run the builder of every constraint group that has members."""
        for group in self._constraint_groups:
            members = self.es.groups.get(group)
            if not members:
                continue
            # groups are sets: sort for a deterministic model
            members = sorted(members, key=_member_key)
            builder = get_builder(group)
            if builder is None:
                msg = (
                    f"{group.__name__} is not supported by the linopy "
                    f"backend yet (used by {len(members)} member(s), e.g. "
                    f"{_describe(members[0])})."
                )
                raise NotImplementedError(msg)
            builder(self, members)

    def _add_objective(self):
        """Sum the objective terms the builders contributed."""
        terms = [t for t in self._objective_terms.values() if t is not None]
        if not terms:
            # a model without costs: feasibility only
            total = 0 * self.flow.sum() if self.FLOWS else None
        else:
            total = terms[0]
            for term in terms[1:]:
                total = total + term
        if total is not None:
            self.linopy.add_objective(total, sense="min", overwrite=True)
        self._objective_added = True

    # ------------------------------------------------------------------
    # API for builders
    # ------------------------------------------------------------------

    def flow_position(self, source, target):
        """Position of the flow (source, target) along the "flow" dim."""
        return self._flow_position[source, target]

    def flow_var(self, source, target):
        """The linopy variable slice of one flow, dimension "timestep".

        Meant for custom constraints, e.g.
        ``model.linopy.add_constraints(model.flow_var(a, b) <= 5)``.
        """
        return self.flow.isel(
            flow=self.flow_position(source, target), drop=True
        )

    def coords_for(self, index):
        """Coordinate index for an index kind used in :meth:`add_variables`."""
        return {
            "timestep": self.timestep_index,
            "timepoint": self.timepoint_index,
            "capacity_period": self.capacity_period_index,
        }[index]

    def add_variables(
        self,
        name,
        *,
        entities=None,
        entity_dim=None,
        index=None,
        lower=-INF,
        upper=INF,
        binary=False,
        integer=False,
    ):
        """Add a variable container and remember its result layout.

        Parameters
        ----------
        name : str
            linopy name. ``"<Block>.<var>"`` for block variables; the part
            after the last dot is the key in :class:`~oemof.solph.Results`,
            matching the Pyomo variable names.
        entities : list, optional
            The flows (as (source, target)) or nodes the variable is
            defined for. They become the result columns.
        entity_dim : str
            Dimension name for the entities. Must be unique per kind of
            subset (e.g. "flow", "invest_flow"), so that xarray never
            aligns two different subsets.
        index : {"timestep", "timepoint", "capacity_period", None}
        lower, upper : float or numpy.ndarray
            Bounds, broadcastable to (entities, index).
        """
        coords = []
        if entities is not None:
            coords.append(pd.RangeIndex(len(entities), name=entity_dim))
        if index is not None:
            coords.append(self.coords_for(index))
        kwargs = {}
        if not binary or np.ndim(lower) > 0 or np.ndim(upper) > 0:
            # binaries take bounds only to fix them (0 or 1)
            if binary:
                lower = 0 if np.ndim(lower) == 0 else lower
                upper = 1 if np.ndim(upper) == 0 else upper
            kwargs["lower"] = self._bound(lower, coords)
            kwargs["upper"] = self._bound(upper, coords)
        var = self.linopy.add_variables(
            coords=coords or None,
            name=name,
            binary=binary,
            integer=integer,
            **kwargs,
        )
        key = name.split(".")[-1]
        self._result_vars.setdefault(key, []).append(
            (name, list(entities) if entities is not None else None, index)
        )
        self._var_meta[name] = (
            list(entities) if entities is not None else None,
            entity_dim,
            index,
        )
        return var

    @staticmethod
    def _bound(value, coords):
        if np.ndim(value) == 0:
            return float(value)
        value = np.asarray(value, dtype=float)
        if not coords:
            return float(value)
        shape = tuple(len(c) for c in coords)
        value = np.broadcast_to(value, shape)
        return xr.DataArray(
            value,
            coords={c.name: c for c in coords},
            dims=[c.name for c in coords],
        )

    def add_constraints(self, name, lhs, sign=None, rhs=None):
        """Add a constraint container (thin wrapper, for naming)."""
        if sign is None:
            return self.linopy.add_constraints(lhs, name=name)
        return self.linopy.add_constraints(lhs, sign, rhs, name=name)

    def add_masked_constraints(self, name, lhs, sign, rhs, mask):
        """Add constraints only where `mask` (an array over the dims of
        `lhs`) is True, like rules returning Constraint.Skip in Pyomo."""
        dims = [d for d in lhs.dims if d != "_term"]
        mask = xr.DataArray(
            np.asarray(mask, dtype=bool),
            dims=dims,
            coords={d: lhs.coords[d] for d in dims if d in lhs.coords},
        )
        return self.linopy.add_constraints(
            lhs, sign, rhs, name=name, mask=mask
        )

    def add_objective_term(self, name, expression):
        """Contribute a (scalar) expression to the objective.

        The objective is the sum of all terms, as the Pyomo backend sums the
        `_objective_expression` of every block.
        """
        if expression is None:
            return
        if hasattr(expression, "ndim") and expression.ndim > 0:
            expression = expression.sum()
        # linopy objectives take no constant: keep it apart and add it to
        # the reported objective value, as the Pyomo objective includes it
        const = float(np.asarray(expression.const).sum())
        if const != 0:
            expression = expression - const
            self._objective_constant += const
        self._objective_terms[name] = expression

    def add_expression(self, name, expression):
        """Keep a named (scalar) expression, e.g. the investment costs of a
        block or the total of an integral limit. ``model.<name>()`` returns
        its value after solving, as for a Pyomo Expression."""
        self._expressions[name] = expression
        return expression

    def expression(self, name):
        """The named expression added with :meth:`add_expression`."""
        return self._expressions[name]

    def entity_labels(self, quantity, entity):
        """Labels of one entity of a variable, along its index.

        `quantity` is ``model.flow`` (entity = (source, target)) or a block
        variable as ``model.<Block>.<variable>`` (entity = node or flow).
        """
        if isinstance(quantity, _VariableView):
            return quantity.variable.labels.values[quantity._position[entity]]
        if quantity is self.flow or getattr(quantity, "name", None) == "flow":
            return self.flow.labels.values[self.flow_position(*entity)]
        msg = (
            "Expected model.flow or a block variable such as "
            "model.GenericStorageBlock.storage_content."
        )
        raise TypeError(msg)

    @property
    def objective_terms(self):
        """The objective contributions by block, as a dict."""
        return dict(self._objective_terms)

    def __getattr__(self, name):
        # model.<Block>.<variable>[keys]: read access to block variables by
        # the same keys as in the Pyomo model, e.g.
        # model.InvestmentFlowBlock.invest[source, target, period]
        if name.startswith("_") or "_var_meta" not in self.__dict__:
            raise AttributeError(name)
        if name in self.__dict__.get("_expressions", {}):
            return _ExpressionView(self.__dict__["_expressions"][name])
        prefix = name + "."
        if any(v.startswith(prefix) for v in self.__dict__["_var_meta"]):
            return _BlockView(self, name)
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}"
        )

    # ------------------------------------------------------------------
    # solving
    # ------------------------------------------------------------------

    def solve(
        self,
        solver="cbc",
        solver_io=None,
        allow_nonoptimal=False,
        duals=False,
        solve_kwargs=None,
        cmdline_options=None,
    ):
        """Solve the model; same arguments as :meth:`oemof.solph.Model.solve`.

        Parameters
        ----------
        solver : str
            Any solver linopy supports ("highs", "cbc", "gurobi", ...).
        solver_io : str, optional
            linopy's ``io_api`` ("direct", "lp", "mps"). Defaults to
            "direct" for solvers with an in-memory interface, else "lp".
        allow_nonoptimal : bool
            Warn instead of raising if no optimal solution is found.
        duals : bool
            Receive duals of the bus balances and reduced costs.
        solve_kwargs : dict
            ``{"tee": True}`` shows the solver log; other keys are passed
            to linopy's ``Model.solve``.
        cmdline_options : dict
            Solver options, passed to the solver by name.

        Returns
        -------
        Results
        """
        from oemof.solph._linopy._solve import solve

        return solve(
            self,
            solver=solver,
            solver_io=solver_io,
            allow_nonoptimal=allow_nonoptimal,
            duals=duals,
            solve_kwargs=solve_kwargs,
            cmdline_options=cmdline_options,
        )

    def relax_problem(self):
        """Relax integer and binary variables to continuous ones, as
        :meth:`oemof.solph.Model.relax_problem`."""
        for name in list(self.linopy.integers) + list(self.linopy.binaries):
            self.linopy.variables[name].relax()
        return self

    def results(self):
        """Deprecated, as :meth:`oemof.solph.Model.results`."""
        import warnings

        from oemof.solph import processing

        warnings.warn(
            "Model.results() is deprecated."
            + " Please use results returned by Model.solve().",
            FutureWarning,
        )
        return processing.results(self)

    @property
    def objective(self):
        """The objective; ``model.objective()`` returns its value, as for a
        Pyomo objective. Only exists once the model is constructed."""
        if not self._objective_added:
            raise AttributeError("The objective has not been added yet.")
        return _Objective(self.linopy, self._objective_constant)

    @property
    def solver_results(self):
        """Deprecated, as :attr:`oemof.solph.Model.solver_results`."""
        import warnings

        warnings.warn(
            "'solver_results' attribute is deprecated and will be removed in "
            "a future version. Use the 'solver' attribute of the Results "
            "object or 'solver_return' if you need the original return "
            "object.",
            FutureWarning,
            stacklevel=2,
        )
        return self._solver_results

    def receive_duals(self):
        """Deprecated, as :meth:`oemof.solph.Model.receive_duals`."""
        import warnings

        warnings.warn(
            "Model.receive_duals() is deprecated. Use "
            "Model.solve(duals=True) instead.",
            FutureWarning,
        )
        self._receive_duals()

    def _receive_duals(self):
        """Receive bus duals and reduced costs with the next solve."""
        self.dual = True
        self.rc = True

    # ------------------------------------------------------------------
    # results
    # ------------------------------------------------------------------

    def _result_duals(self):
        """Bus balance duals as a DataFrame (columns: buses)."""
        if "BusBlock.balance" not in self.linopy.constraints:
            return pd.DataFrame()
        values = np.asarray(
            self.linopy.constraints["BusBlock.balance"].dual.values
        )
        return pd.DataFrame(
            values.T,
            index=self._row_index("timestep", values.shape[1]),
            columns=pd.Index(self.balance_buses),
        )

    def _bus_duals(self):
        """Bus balance duals as {bus: array over timesteps}."""
        frame = self._result_duals()
        return {bus: frame[bus].to_numpy() for bus in frame.columns}

    def _result_reduced_costs(self):
        """Reduced costs of the flow variable, columns (source, target)."""
        from oemof.solph._linopy._solve import reduced_costs

        rc = reduced_costs(self)
        labels = self.flow.labels.values
        values = np.vectorize(lambda lab: rc.get(lab, np.nan))(labels)
        # as in the Pyomo backend, where fixed flows are constants
        values[self._fixed_flows] = 0.0
        return pd.DataFrame(
            values.T,
            index=self._row_index("timestep", values.shape[1]),
            columns=self._columns(self.FLOWS),
        )

    def _results_dataframe(self):
        """All variable values as the long table that
        :func:`oemof.solph.processing.create_dataframe` builds for Pyomo
        models, so that :func:`~oemof.solph.processing.results` and
        :mod:`~oemof.solph.views` work unchanged."""
        frames = []
        for key, containers in self._result_vars.items():
            for name, entities, index in containers:
                if entities is None:
                    continue
                values = np.asarray(
                    self.linopy.variables[name].solution.values
                ).reshape(len(entities), -1)
                n_rows = values.shape[1]
                tuples = [
                    e if isinstance(e, tuple) else (e,) for e in entities
                ]
                timesteps = np.arange(n_rows) if index is not None else [0]
                frame = pd.DataFrame(
                    {
                        "oemof_tuple": [
                            t for t in tuples for _ in range(len(timesteps))
                        ],
                        "timestep": np.tile(timesteps, len(entities)),
                        "variable_name": key,
                        "value": values.ravel(),
                    }
                )
                frames.append(frame)
        if not frames:
            return pd.DataFrame(
                columns=["oemof_tuple", "timestep", "variable_name", "value"]
            )
        df = pd.concat(frames, ignore_index=True)
        df["pyomo_tuple"] = None
        df = df.sort_values(
            ["oemof_tuple", "timestep"], ascending=[True, True]
        )
        return df.dropna(subset=["value"])

    def _row_index(self, index, n_rows):
        timeindex = self.es.timeindex
        if index == "timestep":
            if timeindex is not None and len(timeindex) > n_rows:
                return timeindex[:n_rows]
            return pd.RangeIndex(n_rows)
        if index == "timepoint":
            if timeindex is not None and len(timeindex) >= n_rows:
                return timeindex[:n_rows]
            return pd.RangeIndex(n_rows)
        return pd.RangeIndex(n_rows)

    @staticmethod
    def _columns(entities):
        if entities and isinstance(entities[0], tuple):
            return pd.MultiIndex.from_tuples(entities)
        return pd.Index(entities)

    def _result_keys(self):
        return set(self._result_vars)

    def _result_frame(self, key):
        """Solution of all containers named `key` as one DataFrame, laid out
        like :meth:`oemof.solph.Results.get` does for the Pyomo backend."""
        frames = []
        for name, entities, index in self._result_vars[key]:
            values = np.asarray(self.linopy.variables[name].solution.values)
            if entities is None:
                values = values.reshape((1,) + values.shape)
                entities = [None]
            if index is None:
                frame = pd.DataFrame(
                    values.reshape(1, -1), columns=self._columns(entities)
                )
            else:
                values = values.reshape(len(entities), -1)
                frame = pd.DataFrame(
                    values.T,
                    index=self._row_index(index, values.shape[1]),
                    columns=self._columns(entities),
                )
            frames.append(frame)
        return pd.concat(frames, axis=1)


class _BlockView:
    """The variables of one block, addressed as in the Pyomo model."""

    def __init__(self, model, block):
        self._model = model
        self._block = block

    def __getattr__(self, name):
        full = f"{self._block}.{name}"
        if full not in self._model._var_meta:
            raise AttributeError(f"{self._block} has no variable {name!r}")
        return _VariableView(self._model, full)


class _VariableView:
    """Index a linopy variable by node keys and time, as a Pyomo Var."""

    def __init__(self, model, name):
        self._model = model
        self._name = name
        self._entities, self._entity_dim, self._index = model._var_meta[name]
        self._position = {e: k for k, e in enumerate(self._entities or [])}

    @property
    def variable(self):
        """The linopy variable."""
        return self._model.linopy.variables[self._name]

    def __getitem__(self, key):
        key = key if isinstance(key, tuple) else (key,)
        selection = {}
        if self._index is not None:
            *key, step = key
            selection[self._model.coords_for(self._index).name] = step
        if self._entities is not None:
            entity = tuple(key) if len(key) > 1 else key[0]
            selection[self._entity_dim] = self._position[entity]
        return self.variable.isel(selection)


class _ExpressionView:
    """A named expression; calling it gives its value after solving."""

    def __init__(self, expression):
        self.expression = expression

    def __call__(self):
        return float(self.expression.solution)


class _Objective:
    """Callable stand-in for a Pyomo objective: ``objective()`` is its
    value."""

    def __init__(self, linopy_model, constant=0.0):
        self._model = linopy_model
        self._constant = constant

    def __call__(self):
        return self._model.objective.value + self._constant

    @property
    def expression(self):
        return self._model.objective.expression


def _member_key(member):
    if isinstance(member, tuple):
        return tuple(str(getattr(m, "label", m)) for m in member[:2])
    return (str(getattr(member, "label", member)),)


def _describe(member):
    if isinstance(member, tuple) and len(member) == 3:
        return f"flow {member[0].label!s} -> {member[1].label!s}"
    return repr(getattr(member, "label", member))
