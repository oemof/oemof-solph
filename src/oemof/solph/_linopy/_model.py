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
        self._objective_terms = {}
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
        if not binary:
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

    def add_objective_term(self, name, expression):
        """Contribute a (scalar) expression to the objective.

        The objective is the sum of all terms, as the Pyomo backend sums the
        `_objective_expression` of every block.
        """
        if expression is None:
            return
        if hasattr(expression, "ndim") and expression.ndim > 0:
            expression = expression.sum()
        self._objective_terms[name] = expression

    @property
    def objective_terms(self):
        """The objective contributions by block, as a dict."""
        return dict(self._objective_terms)

    # ------------------------------------------------------------------
    # results
    # ------------------------------------------------------------------

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


def _member_key(member):
    if isinstance(member, tuple):
        return tuple(str(getattr(m, "label", m)) for m in member[:2])
    return (str(getattr(member, "label", member)),)


def _describe(member):
    if isinstance(member, tuple) and len(member) == 3:
        return f"flow {member[0].label!s} -> {member[1].label!s}"
    return repr(getattr(member, "label", member))
