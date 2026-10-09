# -*- coding: utf-8 -*-

"""Solph Optimization Models.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Saeed Sayadi
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Lennart Schürmann

SPDX-License-Identifier: MIT

"""

import logging
import warnings
from collections import namedtuple
from logging import getLogger

from pyomo import environ as po
from pyomo.contrib import appsi
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality
from pyomo.opt import SolverFactory

from oemof.solph import EnergySystem, processing
from oemof.solph.buses._bus import BusBlock
from oemof.solph.components._converter import ConverterBlock
from oemof.solph.flows._invest_non_convex_flow_block import (
    InvestNonConvexFlowBlock,
)
from oemof.solph.flows._investment_flow_block import InvestmentFlowBlock
from oemof.solph.flows._non_convex_flow_block import NonConvexFlowBlock
from oemof.solph.flows._simple_flow_block import SimpleFlowBlock

from ._results import Results


class LoggingError(BaseException):
    """Raised when the wrong logging level is used."""

    pass


class Model(po.ConcreteModel):
    """An energy system model for operational and/or investment
    optimization.

    Parameters
    ----------
    energysystem : EnergySystem object
        Object that holds the nodes of an oemof energy system graph.
    constraint_groups : list
        Solph looks for these groups in the given energy system and uses them
        to create the constraints of the optimization problem.
        Defaults to `Model.CONSTRAINT_GROUPS`
    auto_construct : boolean
        If this value is true, the set, variables, constraints, etc. are added,
        automatically when instantiating the model. For sequential model
        building process set this value to False
        and use methods `_add_parent_block_sets`,
        `_add_parent_block_variables`, `_add_blocks`, `_add_objective`

    Attributes
    ----------
    timeincrement : sequence
        Time increments
    flows : dict
        Flows of the model
    name : str
        Name of the model
    es : solph.EnergySystem
        Energy system of the model
    meta : `pyomo.opt.results.results_.SolverResults` or None
        Solver results
    dual : `pyomo.core.base.suffix.Suffix` or None
        Store the dual variables of the model if pyomo suffix is set to IMPORT
    rc : `pyomo.core.base.suffix.Suffix` or None
        Store the reduced costs of the model if pyomo suffix is set to IMPORT


    **The following basic sets are created**:

    NODES
        A set with all nodes of the given energy system.

    TIMESTEPS
        A set with all timesteps of the given time horizon.

    CAPACITY_PERIODS
        A set with all investment periods of the given time horizon.

    TIMEINDEX
        A set with all time indices of the given time horizon, whereby
        time indices are defined as a tuple consisting of the period and the
        timestep. E.g. (2, 10) would be timestep 10 (which is exactly the same
        as in the TIMESTEPS set) and which is in period 2.

    FLOWS
        A 2 dimensional set with all flows. Index: `(source, target)`

    **The following basic variables are created**:

    flow
        Flow from source to target indexed by FLOWS, TIMEINDEX.
        Note: Bounds of this variable are set depending on attributes of
        the corresponding flow object.

    """

    CONSTRAINT_GROUPS = [
        BusBlock,
        ConverterBlock,
        InvestmentFlowBlock,
        SimpleFlowBlock,
        NonConvexFlowBlock,
        InvestNonConvexFlowBlock,
    ]

    # TODO: add missing solvers
    _APPSI_SOLVER = {
        "highs": (appsi.solvers.Highs, "highs_options"),
        "cbc": (appsi.solvers.Cbc, "cbc_options"),
        "gurobi": (appsi.solvers.Gurobi, "gurobi_options"),
    }

    def __init__(
        self,
        energysystem: EnergySystem,
        *,
        constraint_groups: list[po.ScalarBlock] = None,
        auto_construct: bool = True,
        debug: bool = False,
    ):
        super().__init__()

        # Check root logger. Due to a problem with pyomo the building of the
        # model will take up to a 100 times longer if the root logger is set
        # to DEBUG

        if getLogger().level <= 10 and debug is False:
            msg = (
                "The root logger level is 'DEBUG'.\nDue to a communication "
                "problem between solph and the pyomo package,\nusing the "
                "DEBUG level will slow down the modelling process by the "
                "factor ~100.\nIf you need the debug-logging you can "
                "initialise the Model with 'debug=True`\nYou should only do "
                "this for small models. To avoid the slow-down use the "
                "logger\nfunction of oemof.tools (read docstring) or "
                "change the level of the root logger:\n\nimport logging\n"
                "logging.getLogger().setLevel(logging.INFO)"
            )
            raise LoggingError(msg)

        # ########################  Arguments #################################

        self.es = energysystem
        self.timeincrement = self.es.timeincrement

        if constraint_groups is None:
            constraint_groups = []

        self._constraint_groups = (
            type(self).CONSTRAINT_GROUPS + constraint_groups
        )

        self._constraint_groups += [
            i
            for i in self.es.groups
            if hasattr(i, "CONSTRAINT_GROUP")
            and i not in self._constraint_groups
        ][::-1]  # invert to add constraints of subnodes first

        self.flows = self.es.flows()

        self.solver_results = None
        self.dual = None
        self.rc = None

        if auto_construct is True:
            self._construct()

    def _construct(self):
        """Construct a Model by adding parent block sets and variables
        as well as child blocks and variables to it.
        """
        self._add_parent_block_sets()
        self._add_parent_block_variables()
        self._add_child_blocks()
        self._add_objective()

    def _add_parent_block_sets(self):
        """Add all basic sets to the model, i.e. NODES, TIMESTEPS and FLOWS.
        Also create sets CAPACITY_PERIODS and TIMEINDEX used for
        formulti-period models.
        """
        self.nodes = list(self.es.nodes)

        # create set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.nodes])

        if self.es.timeincrement is None:
            msg = (
                "The EnergySystem needs to have a valid 'timeincrement' "
                "attribute to build a model."
            )
            raise AttributeError(msg)

        # pyomo set for timesteps of optimization problem
        self.TIMESTEPS = po.Set(
            initialize=range(len(self.es.timeincrement)), ordered=True
        )
        self.TIMEPOINTS = po.Set(
            initialize=range(len(self.es.timeincrement) + 1), ordered=True
        )

        if self.es.transitional_single_period:
            self.TIMEINDEX = po.Set(
                initialize=list(
                    zip(
                        [0] * len(self.es.timeincrement),
                        range(len(self.es.timeincrement)),
                    )
                ),
                ordered=True,
            )
            self.CAPACITY_PERIODS = po.Set(initialize=[0], ordered=True)
        else:
            nested_list = [
                [k] * len(self.es.capacity_periods[k])
                for k in range(len(self.es.capacity_periods))
            ]
            flattened_list = [
                item for sublist in nested_list for item in sublist
            ]
            self.TIMEINDEX = po.Set(
                initialize=list(
                    zip(flattened_list, range(len(self.es.timeincrement)))
                ),
                ordered=True,
            )
            self.CAPACITY_PERIODS = po.Set(
                initialize=sorted(
                    list(set(range(len(self.es.capacity_periods))))
                ),
                ordered=True,
            )

        # (Re-)Map timesteps to periods
        timesteps_in_period = {p: [] for p in self.CAPACITY_PERIODS}
        for p, t in self.TIMEINDEX:
            timesteps_in_period[p].append(t)
        self.TIMESTEPS_IN_PERIOD = timesteps_in_period

        # Set up disaggregated timesteps from original timeseries
        self.TSAM_MODE = False
        if self.es.tsa_parameters is None:
            self.tsam_weighting = [1] * len(self.timeincrement)
        else:
            self.TSAM_MODE = True

            # Construct weighting from occurrences and order
            self.tsam_weighting = list(
                self.es.tsa_parameters[p]["occurrences"][k]
                for p in self.CAPACITY_PERIODS
                for k in range(len(self.es.tsa_parameters[p]["occurrences"]))
                for _ in range(self.es.tsa_parameters[p]["timesteps"])
            )
            self.CLUSTERS = po.Set(
                initialize=list(
                    range(
                        sum(
                            len(self.es.tsa_parameters[p]["order"])
                            for p in self.CAPACITY_PERIODS
                        )
                    )
                )
            )
            self.CLUSTERS_OFFSET = po.Set(
                initialize=list(
                    range(
                        sum(
                            len(self.es.tsa_parameters[p]["order"])
                            for p in self.CAPACITY_PERIODS
                        )
                        + 1
                    )
                )
            )
            self.TYPICAL_CLUSTERS = po.Set(
                initialize=[
                    (p, i)
                    for p in self.CAPACITY_PERIODS
                    for i in range(
                        len(self.es.tsa_parameters[p]["occurrences"])
                    )
                ]
            )

            self.TIMEINDEX_CLUSTER = self.get_cluster_index("order", 0)
            self.TIMEINDEX_TYPICAL_CLUSTER = self.get_cluster_index(
                "occurrences", 0
            )
            self.TIMEINDEX_TYPICAL_CLUSTER_OFFSET = self.get_cluster_index(
                "occurrences", 1
            )

        # previous timesteps
        previous_timesteps = [x - 1 for x in self.TIMESTEPS]
        previous_timesteps[0] = self.TIMESTEPS.last()

        self.previous_timesteps = dict(zip(self.TIMESTEPS, previous_timesteps))

        # pyomo set for all flows in the energy system graph
        self.FLOWS = po.Set(
            initialize=self.flows.keys(), ordered=True, dimen=2
        )

        self.BIDIRECTIONAL_FLOWS = po.Set(
            initialize=[k for (k, v) in self.flows.items() if v.bidirectional],
            ordered=True,
            dimen=2,
            within=self.FLOWS,
        )

        self.UNIDIRECTIONAL_FLOWS = po.Set(
            initialize=[
                k for (k, v) in self.flows.items() if not v.bidirectional
            ],
            ordered=True,
            dimen=2,
            within=self.FLOWS,
        )

    def _add_parent_block_variables(self):
        """Add the parent block variables, which is the `flow` variable,
        indexed by FLOWS and TIMEINDEX."""
        self.flow = po.Var(self.FLOWS, self.TIMESTEPS, within=po.Reals)

        for o, i in self.FLOWS:
            if self.flows[o, i].nominal_capacity is not None:
                if self.flows[o, i].fix is not None:
                    for p, timesteps in self.TIMESTEPS_IN_PERIOD.items():
                        for t in timesteps:
                            self.flow[o, i, t].value = (
                                self.flows[o, i].fix[t]
                                * self.flows[o, i].nominal_capacity[p]
                            )
                            self.flow[o, i, t].fix()
                else:
                    for p, timesteps in self.TIMESTEPS_IN_PERIOD.items():
                        for t in timesteps:
                            self.flow[o, i, t].setub(
                                self.flows[o, i].maximum[t]
                                * self.flows[o, i].nominal_capacity[p]
                            )
                    if not self.flows[o, i].nonconvex:
                        for p, timesteps in self.TIMESTEPS_IN_PERIOD.items():
                            for t in timesteps:
                                self.flow[o, i, t].setlb(
                                    self.flows[o, i].minimum[t]
                                    * self.flows[o, i].nominal_capacity[p]
                                )
                    elif (o, i) in self.UNIDIRECTIONAL_FLOWS:
                        for p, timesteps in self.TIMESTEPS_IN_PERIOD.items():
                            for t in timesteps:
                                self.flow[o, i, t].setlb(0)
            else:
                if (o, i) in self.UNIDIRECTIONAL_FLOWS:
                    for p, timesteps in self.TIMESTEPS_IN_PERIOD.items():
                        for t in timesteps:
                            self.flow[o, i, t].setlb(0)

    def _add_child_blocks(self):
        """Method to add the defined child blocks for components that have
        been grouped in the defined constraint groups. This collects all the
        constraints from the buses, components and flows blocks
        and adds them to the model.
        """
        for group in self._constraint_groups:
            block = group()
            self.add_component(str(block), block)

            # create constraints etc. related with block for all nodes
            # in the group
            block._create(group=self.es.groups.get(group))

    def _add_objective(self, sense=po.minimize, update=False):
        """Method to sum up all objective expressions from the child blocks
        that have been created. This method looks for `_objective_expression`
        attribute in the block definition and will call this method to add
        their return value to the objective function.
        """
        if update:
            self.del_component("objective")

        expr = 0

        for block in self.component_data_objects():
            if hasattr(block, "_objective_expression"):
                expr += block._objective_expression()

        self.objective = po.Objective(sense=sense, expr=expr)

    def receive_duals(self):
        """Method sets solver suffix to extract information about dual
        variables from solver. Shadow prices (duals) and reduced costs (rc) are
        set as attributes of the model.
        """
        # shadow prices
        self.dual = po.Suffix(direction=po.Suffix.IMPORT)
        # reduced costs
        self.rc = po.Suffix(direction=po.Suffix.IMPORT)

    def results(self):
        """Returns a nested dictionary of the results of this optimization.
        See the processing module for more information on results extraction.
        """
        warnings.warn(
            "Model.results() is deprecated."
            + " Please use results returned by Model.solve().",
            FutureWarning,
        )
        return processing.results(self)

    def solve_appsi(
        self,
        solver_info,
        solver=appsi.solvers.Cbc,
        solver_options="cbc_options",
        cmdline_options=None,
        solve_kwargs=None,
    ):
        """Solve the model with a Pyomo APPSI solver.

        Parameters
        ----------
        solver_info : callable
            Factory used to create the common solver return object.
        solver : type
            APPSI solver class (a subclass of
            ``pyomo.contrib.appsi.base.Solver``) to instantiate.
        solver_options : str
            Name of the solver attribute that receives ``cmdline_options``.
        cmdline_options : dict
            Solver-specific options passed to the APPSI solver.
        solve_kwargs : dict
            Solve options. Currently, ``tee=True`` enables solver output.

        Returns
        -------
        solver_info
            Solver status and APPSI result metadata. Variable values are
            loaded when an optimal solution or a feasible incumbent exists.
        """
        # TODO: Implement option to handle unknown solver names defined by user
        opt = solver()
        opt.config.load_solution = False

        if solve_kwargs.get("tee"):
            opt.config.stream_solver = True

        setattr(opt, solver_options, cmdline_options)

        appsi_results = opt.solve(self)
        tc = appsi_results.termination_condition

        # TODO: Handle solver results depending on solver class
        solver_results = {
            "termination_condition": tc.name,
            "best_feasible_objective": appsi_results.best_feasible_objective,
            "best_objective_bound": appsi_results.best_objective_bound,
            "wallclock_time": appsi_results.wallclock_time,
        }

        optimal = tc == appsi.base.TerminationCondition.optimal

        # TODO: check if valid for all solver
        if optimal or appsi_results.best_feasible_objective is not None:
            appsi_results.solution_loader.load_vars()

        return solver_info(
            optimal=optimal,
            termination_condition=tc,
            status=tc.value,
            solver_results=solver_results,
        )

    def solve_factory(
        self, solver_info, solver, solver_io, solve_kwargs, cmdline_options
    ):
        """Solve the model with Pyomo's ``SolverFactory`` interface.

        Parameters
        ----------
        solver_info : callable
            Factory used to create the common solver return object.
        solver : str
            Name of the solver registered with ``SolverFactory``.
        solver_io : str
            Solver interface or file format passed to ``SolverFactory``.
        solve_kwargs : dict
            Keyword arguments forwarded to the solver's ``solve`` method.
        cmdline_options : dict
            Solver options added to the solver object's ``options`` mapping.

        Returns
        -------
        solver_info
            Solver status and the Pyomo ``SolverResults`` object.
        """
        opt = SolverFactory(solver, solver_io=solver_io)

        # set command line options
        options = opt.options
        for k in cmdline_options:
            options[k] = cmdline_options[k]

        factory_results = opt.solve(self, **solve_kwargs)

        status = factory_results.Solver.Status
        message = factory_results.Solver.Termination_condition

        return solver_info(
            optimal=status == "ok" and message == "optimal",
            termination_condition=message,
            status=factory_results.Solver.Status,
            solver_results=factory_results,
        )

    def _get_solve_function(self, solver: str, interface: str):
        """Function to return the correct solve function (`solve_factory`,
        `solve_appsi`) based on solver and interface selection of the user in
        the `solve` function.
        """
        if interface == "auto":
            if solver in self._APPSI_SOLVER:
                msg = f"'appsi' interface selected by default for '{solver}'."
                logging.info(msg)
                return self.solve_appsi
            else:
                msg = (
                    f"Solver '{solver}' is not supported by 'appsi' interface."
                    f" Using pyomos 'SolverFactory' as fallback (slower for"
                    f" repeated solves)."
                )
                logging.info(msg)
                return self.solve_factory
        elif interface == "solverfactory":
            return self.solve_factory
        elif interface == "appsi":
            if solver in self._APPSI_SOLVER:
                return self.solve_appsi
            else:
                msg = (
                    f"Solver '{solver}' is not supported by 'appsi' interface,"
                    f" which is set explicitly. A generic implementation is"
                    f" tested. If this fails, set the interface to 'auto' or"
                    f" 'solverfactory', or use a different solver."
                )
                raise UserWarning(msg)
                # TODO: Implement forced appsi usage
        else:
            msg = (
                f"The selected interface '{interface}' is not supported. "
                f"Please use one of the following: 'auto', 'solverfactory', "
                f"'appsi'."
            )
            raise ValueError(msg)

    def solve(
        self,
        solver: str = "cbc",
        solver_io: str = "lp",  # TODO: only relevant for SolverFactory
        interface: str = "auto",
        allow_nonoptimal: bool = False,
        solve_kwargs: None | dict = None,
        cmdline_options: None | dict = None,
    ) -> Results | dict:
        r"""Takes care of communication with solver to solve the model.

        Parameters
        ----------
        solver : string
            solver to be used e.g. "cbc", "glpk", "gurobi", "cplex".
        solver_io : string
            pyomo solver interface file format: "lp", "python", "nl", etc.
        interface : str
            interface to use: "auto", "solverfactory", "appsi".
        allow_nonoptimal : bool
            False: If no optimal solution is found, an error will be risen.
            True: If no optimal solution is found, a warning is issued and
            the solver metadata is returned instead of a ``Results`` object.
            A feasible incumbent may be loaded for APPSI solvers.
        solve_kwargs : dict
            Additional arguments for the solver's ``solve`` method, e.g.
            ``{"tee": True}``. APPSI solvers currently use ``tee`` to enable
            solver output; other arguments are forwarded by the
            ``SolverFactory`` path.
        cmdline_options : dict
            Solver-specific options. APPSI solvers receive these through
            their options attribute; ``SolverFactory`` solvers receive them
            through their ``options`` mapping. For example,
            ``{"mipgap": 0.01}`` sets a MIP gap, while Gurobi accepts numeric
            parameters such as ``{"method": 2}``.

        Returns
        -------
        Results or dict
            An optimal solve returns a ``Results`` object. If
            ``allow_nonoptimal=True`` and the solver is non-optimal, a warning
            is issued and its solver metadata is returned instead.

        Raises
        ------
        RuntimeError
            If the solver does not return an optimal solution and
            ``allow_nonoptimal`` is false.
        """
        if solve_kwargs is None:
            solve_kwargs = {}
        if cmdline_options is None:
            cmdline_options = {}
        solver_info = namedtuple(  # defines return object for solve functions
            "SolverReturn",
            ["optimal", "solver_results", "termination_condition", "status"],
        )

        solve_function = self._get_solve_function(
            solver=solver, interface=interface
        )

        solve_function(
            solver_info=solver_info,
            solver=solver,
            solver_io=None if solve_function == self.solve_appsi else "lp",
            solve_kwargs=solve_kwargs,
            cmdline_options=cmdline_options,
        )

        if solver in self._APPSI_SOLVER:
            solver_class, solver_options = self._APPSI_SOLVER.get(solver, None)

            solver_return = self.solve_appsi(
                solver_info=solver_info,
                solver_class=solver_class,
                solver_options=solver_options,
                solve_kwargs=solve_kwargs,
                cmdline_options=cmdline_options,
            )
        else:
            solver_return = self.solve_factory(
                solver_info=solver_info,
                solver=solver,
                solver_io=solver_io,
                solve_kwargs=solve_kwargs,
                cmdline_options=cmdline_options,
            )

        self.es.results = solver_return.solver_results
        self.solver_results = solver_return.solver_results

        if solver_return.optimal:
            msg = "Optimization successful."
            logging.info(msg)
        else:
            msg = (
                f"The solver did not return an optimal solution. "
                f"Instead the optimization ended with\n"
                f"       - status: {solver_return.status}\n"
                f"       - termination condition: "
                f"{solver_return.termination_condition.name}"
            )

            if allow_nonoptimal:
                warnings.warn(msg, UserWarning)
                return solver_return.solver_results
            else:
                raise RuntimeError(msg)

        return Results(self)

    def relax_problem(self):
        """Relaxes integer variables to reals of optimization model self."""
        relaxer = RelaxIntegrality()
        relaxer._apply_to(self)

        return self

    def get_timestep_from_tsam_timestep(self, p, ik, g):
        """Return original timestep from cluster-based timestep"""
        t = (
            p * len(self.TIMESTEPS_IN_PERIOD[p])
            + ik * self.es.tsa_parameters[p]["timesteps"]
            + g
        )
        return t

    def get_cluster_index(self, cluster_type, offset):
        """
        Return cluster index for original or typical periods with or
        without offset
        """
        return [
            (p, k, t)
            for p in range(len(self.es.tsa_parameters))
            for k in range(len(self.es.tsa_parameters[p][cluster_type]))
            for t in range(self.es.tsa_parameters[p]["timesteps"] + offset)
        ]
