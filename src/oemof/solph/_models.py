# -*- coding: utf-8 -*-

"""Solph Optimization Models.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Saeed Sayadi
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""
import logging
import warnings
from logging import getLogger

from pyomo import environ as po
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality
from pyomo.opt import SolverFactory

from oemof.solph import processing
from oemof.solph.buses._bus import BusBlock
from oemof.solph.components._transformer import TransformerBlock
from oemof.solph.flows._invest_non_convex_flow_block import (
    InvestNonConvexFlowBlock,
)
from oemof.solph.flows._investment_flow_block import InvestmentFlowBlock
from oemof.solph.flows._non_convex_flow_block import NonConvexFlowBlock
from oemof.solph.flows._simple_flow_block import SimpleFlowBlock
from oemof.solph._plumbing import sequence

# imports for CellularModel
from oemof.solph.components.experimental._cell_connector import CellConnector
import itertools
from oemof.tools import debugging


class LoggingError(BaseException):
    """Raised when the wrong logging level is used."""

    pass


class BaseModel(po.ConcreteModel):
    """The BaseModel for other solph-models (Model, MultiPeriodModel, etc.)

    Parameters
    ----------
    energysystem : EnergySystem object
        Object that holds the nodes of an oemof energy system graph
    constraint_groups : list (optional)
        Solph looks for these groups in the given energy system and uses them
        to create the constraints of the optimization problem.
        Defaults to `Model.CONSTRAINTS`
    objective_weighting : array like (optional)
        Weights used for temporal objective function
        expressions. If nothing is passed `timeincrement` will be used which
        is calculated from the freq length of the energy system timeindex or
        can be directly passed as a sequence.
    auto_construct : boolean
        If this value is true, the set, variables, constraints, etc. are added,
        automatically when instantiating the model. For sequential model
        building process set this value to False
        and use methods `_add_parent_block_sets`,
        `_add_parent_block_variables`, `_add_blocks`, `_add_objective`

    Attributes
    ----------
    timeincrement : sequence
        Time increments.
    flows : dict
        Flows of the model.
    name : str
        Name of the model.
    es : solph.EnergySystem
        Energy system of the model.
    meta : `pyomo.opt.results.results_.SolverResults` or None
        Solver results.
    dual : `pyomo.core.base.suffix.Suffix` or None
        Store the dual variables of the model if pyomo suffix is set to IMPORT
    rc : `pyomo.core.base.suffix.Suffix` or None
        Store the reduced costs of the model if pyomo suffix is set to IMPORT
    """

    # The default list of constraint groups to be used for a model.
    CONSTRAINT_GROUPS = []

    def __init__(self, energysystem, **kwargs):
        """Initialize a BaseModel, using its energysystem as well as
        optional kwargs for specifying the timeincrement, objective_weigting
        and constraint groups."""
        super().__init__()

        # Check root logger. Due to a problem with pyomo the building of the
        # model will take up to a 100 times longer if the root logger is set
        # to DEBUG

        if getLogger().level <= 10 and kwargs.get("debug", False) is False:
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

        self.name = kwargs.get("name", type(self).__name__)
        self.es = energysystem
        self.timeincrement = kwargs.get("timeincrement", self.es.timeincrement)

        self.objective_weighting = kwargs.get(
            "objective_weighting", self.timeincrement
        )

        self._constraint_groups = type(self).CONSTRAINT_GROUPS + kwargs.get(
            "constraint_groups", []
        )

        self._constraint_groups += [
            i
            for i in self.es.groups
            if hasattr(i, "CONSTRAINT_GROUP")
            and i not in self._constraint_groups
        ]

        self.flows = self.es.flows()

        self.solver_results = None
        self.dual = None
        self.rc = None

        if kwargs.get("auto_construct", True):
            self._construct()

    def _construct(self):
        """Construct a BaseModel by adding parent block sets and variables
        as well as child blocks and variables to it."""
        self._add_parent_block_sets()
        self._add_parent_block_variables()
        self._add_child_blocks()
        self._add_objective()

    def _add_parent_block_sets(self):
        """Method to create all sets located at the parent block, i.e. in the
        model itself, as they are to be shared across all model components.
        See the class :py:class:~oemof.solph.models.Model for the sets created.
        """
        pass

    def _add_parent_block_variables(self):
        """Method to create all variables located at the parent block,
        i.e. the model itself as these variables  are to be shared across
        all model components.
        See the class :py:class:~oemof.solph._models.Model
        for the `flow` variable created.
        """
        pass

    def _add_child_blocks(self):
        """Method to add the defined child blocks for components that have
        been grouped in the defined constraint groups. This collects all the
        constraints from the component blocks and adds them to the model.
        """
        for group in self._constraint_groups:
            # create instance for block
            block = group()
            # Add block to model
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
        return processing.results(self)

    def solve(self, solver="cbc", solver_io="lp", **kwargs):
        r"""Takes care of communication with solver to solve the model.

        Parameters
        ----------
        solver : string
            solver to be used e.g. "cbc", "glpk","gurobi","cplex"
        solver_io : string
            pyomo solver interface file format: "lp","python","nl", etc.
        \**kwargs : keyword arguments
            Possible keys can be set see below:

        Other Parameters
        ----------------
        solve_kwargs : dict
            Other arguments for the pyomo.opt.SolverFactory.solve() method
            Example : {"tee":True}
        cmdline_options : dict
            Dictionary with command line options for solver e.g.
            {"mipgap":"0.01"} results in "--mipgap 0.01"
            \{"interior":" "} results in "--interior"
            \Gurobi solver takes numeric parameter values such as
            {"method": 2}
        """
        solve_kwargs = kwargs.get("solve_kwargs", {})
        solver_cmdline_options = kwargs.get("cmdline_options", {})

        opt = SolverFactory(solver, solver_io=solver_io)
        # set command line options
        options = opt.options
        for k in solver_cmdline_options:
            options[k] = solver_cmdline_options[k]

        solver_results = opt.solve(self, **solve_kwargs)

        status = solver_results["Solver"][0]["Status"]
        termination_condition = solver_results["Solver"][0][
            "Termination condition"
        ]

        if status == "ok" and termination_condition == "optimal":
            logging.info("Optimization successful...")
        else:
            msg = (
                "Optimization ended with status {0} and termination "
                "condition {1}"
            )
            warnings.warn(
                msg.format(status, termination_condition), UserWarning
            )
        self.es.results = solver_results
        self.solver_results = solver_results

        return solver_results

    def relax_problem(self):
        """Relaxes integer variables to reals of optimization model self."""
        relaxer = RelaxIntegrality()
        relaxer._apply_to(self)

        return self


class Model(BaseModel):
    """An  energy system model for operational and/or investment
    optimization.

    Parameters
    ----------
    energysystem : EnergySystem object
        Object that holds the nodes of an oemof energy system graph
    constraint_groups : list
        Solph looks for these groups in the given energy system and uses them
        to create the constraints of the optimization problem.
        Defaults to `Model.CONSTRAINT_GROUPS`


    **The following basic sets are created**:

    NODES
        A set with all nodes of the given energy system.

    TIMESTEPS
        A set with all timesteps of the given time horizon.

    FLOWS
        A 2 dimensional set with all flows. Index: `(source, target)`

    **The following basic variables are created**:

    flow
        Flow from source to target indexed by FLOWS, TIMESTEPS.
        Note: Bounds of this variable are set depending on attributes of
        the corresponding flow object.

    """

    CONSTRAINT_GROUPS = [
        BusBlock,
        TransformerBlock,
        InvestmentFlowBlock,
        SimpleFlowBlock,
        NonConvexFlowBlock,
        InvestNonConvexFlowBlock,
    ]

    def __init__(self, energysystem, **kwargs):
        super().__init__(energysystem, **kwargs)

    def _add_parent_block_sets(self):
        """Add all basic sets to the model, i.e. NODES, TIMESTEPS and FLOWS."""
        # set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.es.nodes])

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
        indexed by FLOWS and TIMESTEPS."""
        self.flow = po.Var(self.FLOWS, self.TIMESTEPS, within=po.Reals)

        for o, i in self.FLOWS:
            if self.flows[o, i].nominal_value is not None:
                if self.flows[o, i].fix[self.TIMESTEPS.at(1)] is not None:
                    for t in self.TIMESTEPS:
                        self.flow[o, i, t].value = (
                            self.flows[o, i].fix[t]
                            * self.flows[o, i].nominal_value
                        )
                        self.flow[o, i, t].fix()
                else:
                    for t in self.TIMESTEPS:
                        self.flow[o, i, t].setub(
                            self.flows[o, i].max[t]
                            * self.flows[o, i].nominal_value
                        )

                    if not self.flows[o, i].nonconvex:
                        for t in self.TIMESTEPS:
                            self.flow[o, i, t].setlb(
                                self.flows[o, i].min[t]
                                * self.flows[o, i].nominal_value
                            )
                    elif (o, i) in self.UNIDIRECTIONAL_FLOWS:
                        for t in self.TIMESTEPS:
                            self.flow[o, i, t].setlb(0)
            else:
                if (o, i) in self.UNIDIRECTIONAL_FLOWS:
                    for t in self.TIMESTEPS:
                        self.flow[o, i, t].setlb(0)


class CellularModel(po.ConcreteModel):
    """
    bla bla bla

    Parameters
    ----------
    EnergyCells: dict
        Dictionary where key is the upmost EnergyCell ("parent cell")
        containing all other cell instances (from a model point of view) and
        value is a list containing all EnergyCell objects (from an object point
        of view).
    Connections: set
        A set of tuples, where each tuple is created as (CellConnector1,
        CellConnector2, loss_factor).
        Connections are established symmetrically, so loss_factor is applied in
        both directions. See equation (x) for usage of loss_factor. Use
        `auto_connect=False` to prevent automatic connection of CellConnectors.
    """

    # TODO: Fill this
    # TODO: Adjust this to new BaseModel and Model code!
    # TODO: Remove redundancies by inheriting from BaseModel or Model

    CONSTRAINT_GROUPS = [
        BusBlock,
        TransformerBlock,
        InvestmentFlowBlock,
        SimpleFlowBlock,
        NonConvexFlowBlock,
        InvestNonConvexFlowBlock,
    ]

    def __init__(self, EnergyCells, Connections, **kwargs):
        super().__init__()

        # Check root logger. Due to a problem with pyomo the building of the
        # model will take up to a 100 times longer if the root logger is set
        # to DEBUG

        if getLogger().level <= 10 and kwargs.get("debug", False) is False:
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

        ##########################  Arguments #################################
        self.name = kwargs.get("name", type(self).__name__)

        # get the parent energy cell
        self.es = list(EnergyCells.keys())[0]

        # get all child energy cells
        self.ec = EnergyCells[self.es]

        # get the cell connection object
        self.CONNECTIONS = Connections

        # add all groups together
        self.groups = {}
        self.groups.update(self.es.groups)
        for cell in self.ec:
            for group_name, components in cell.groups.items():
                if group_name not in self.groups.keys():
                    self.groups.update({group_name: components})
                else:
                    try:
                        self.groups[group_name].update(components)
                    except:
                        msg = (
                            "Couldn't add components {0} to the already"
                            " existing set \n\n {1}".format(
                                components, self.groups[group_name]
                            )
                        )
                        raise Warning(msg)
        # Add time increment (no idea what it does)
        self.timeincrement = kwargs.get("timeincrement", self.es.timeincrement)

        # Set objective weighting (no idea what it does)
        self.objective_weighting = kwargs.get(
            "objective_weighting", self.timeincrement
        )

        # Create constraint groups of all groups-objects to _constraint_groups
        self._constraint_groups = type(self).CONSTRAINT_GROUPS + kwargs.get(
            "constraint_groups", []
        )
        self._constraint_groups += [
            i
            for i in self.groups
            if hasattr(i, "CONSTRAINT_GROUP")
            and i not in self._constraint_groups
        ]

        # add flows to the model
        self.flows = self.es.flows()
        for cell in self.ec:
            for io, f in cell.flows().items():
                if io not in self.flows.keys():
                    self.flows.update({io: f})
                else:
                    msg = (
                        "Two flows with identical input-ouput are tried to"
                        " be added to the CellularModel. {}".format({io: f})
                    )
                    raise Warning(msg)

        # create solver attributes
        self.solver_results = None
        self.dual = None
        self.rc = None

        # start construction of the model (if set to auto_construct)
        if kwargs.get("auto_construct", True):
            self._construct()

        # start connecting of cells (turn off with auto_connect=False)
        if kwargs.get("auto_connect", True):
            self._auto_connect()

    def _construct(self):
        "This is basically copy-pasted from the Model class"
        self._add_parent_block_sets()
        self._add_parent_block_variables()
        self._add_child_blocks()
        self._add_objective()

    def _add_parent_block_sets(self):
        """Method to create all sets located at the parent block, i.e. in the
        model itself, as they are to be shared across all model components.
        See the class :py:class:~oemof.solph.models.Model for the sets created.
        """
        # collect all nodes from the child cells
        self.nodes = self.es.nodes
        for cell in self.ec:
            for node in cell.nodes:
                if node not in self.nodes:
                    self.nodes.append(node)
                else:
                    msg = (
                        "Two nodes of identical name are tried to be added"
                        " to `CellularModel.nodes`: {}".format(node)
                    )
                    raise Warning(msg)
        # create set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.nodes])

        if self.es.timeincrement is None:
            msg = (
                "The EnergySystem needs to have a valid 'timeincrement' "
                "attribute to build a model."
            )
            raise AttributeError(msg)

        # create pyomo set for timesteps and timepoints of optimization problem
        self.TIMESTEPS = po.Set(
            initialize=range(len(self.es.timeincrement)), ordered=True
        )
        self.TIMEPOINTS = po.Set(
            initialize=range(len(self.es.timeincrement) + 1), ordered=True
        )

        # get previous timesteps
        previous_timesteps = [x - 1 for x in self.TIMESTEPS]
        previous_timesteps[0] = self.TIMESTEPS.last()
        self.previous_timesteps = dict(zip(self.TIMESTEPS, previous_timesteps))

        # create pyomo set for all flows in the energy system graph
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
        """Method to create all variables located at the parent block,
        i.e. the model itself as these variables  are to be shared across
        all model components.
        See the class :py:class:~oemof.solph._models.Model
        for the `flow` variable created.
        """
        # TODO: what does this do?
        self.flow = po.Var(self.FLOWS, self.TIMESTEPS, within=po.Reals)
        for (o, i) in self.FLOWS:
            if self.flows[o, i].nominal_value is not None:
                if self.flows[o, i].fix[self.TIMESTEPS.at(1)] is not None:
                    # if nominal_value and fix is given,
                    # set flow to fix * nominal value
                    for t in self.TIMESTEPS:
                        self.flow[o, i, t].value = (
                            self.flows[o, i].fix[t]
                            * self.flows[o, i].nominal_value
                        )
                        self.flow[o, i, t].fix()
                else:
                    # if max is set, set that as upper bound
                    for t in self.TIMESTEPS:
                        self.flow[o, i, t].setub(
                            self.flows[o, i].max[t]
                            * self.flows[o, i].nominal_value
                        )

                    # TODO: why is that check necessary?
                    # set min value (if nonconvex isn't set) as lower bound
                    if not self.flows[o, i].nonconvex:
                        for t in self.TIMESTEPS:
                            self.flow[o, i, t].setlb(
                                self.flows[o, i].min[t]
                                * self.flows[o, i].nominal_value
                            )
                    # TODO: what does this do?
                    elif (o, i) in self.UNIDIRECTIONAL_FLOWS:
                        for t in self.TIMESTEPS:
                            self.flow[o, i, t].setlb(0)
            else:
                # restrict flow values to >0 if unidirectional
                if (o, i) in self.UNIDIRECTIONAL_FLOWS:
                    for t in self.TIMESTEPS:
                        self.flow[o, i, t].setlb(0)

    def _add_child_blocks(self):
        """Method to add the defined child blocks for components that have
        been grouped in the defined constraint groups. This collects all the
        constraints from the component blocks and adds them to the model.
        """
        for group in self._constraint_groups:
            # create instance for block from _constraint_groups
            block = group()
            # add block to model
            self.add_component(str(block), block)
            # create the constraints of the block
            block._create(group=self.groups.get(group))

    def _add_objective(self, sense=po.minimize, update=False):
        """Method to sum up all objective expressions from the child blocks
        that have been created. This method looks for `_objective_expression`
        attribute in the block definition and will call this method to add
        their return value to the objective function.
        """
        if update:
            self.del_component("objective")

        expr = 0
        # TODO: for distributed optimization, this needs to be fitted!
        # TODO: is it necessary to add an _objective_expression to the
        # CellConnectorBlock?
        # TODO: Check if component_data_objects contains all relevant
        # objects from the child-cells

        # get the objective function expression from each block
        for block in self.component_data_objects():
            if hasattr(block, "_objective_expression"):
                expr += block._objective_expression()

        self.objective = po.Objective(sense=sense, expr=expr)

    def _auto_connect(self):
        self._check_orphaned_connectors()
        self._check_max_power_compliance()
        self._mirror_connections()
        self._connect_cells()

    def _check_orphaned_connectors(self):
        """
        Check if there are orphaned (unused) connectors and hand out a warning
        if not.
        """
        # create set containing Connectors in use
        cell_connector_set = set(
            [
                x
                for x in itertools.chain.from_iterable(self.CONNECTIONS)
                if isinstance(x, CellConnector)
            ]
        )
        # create set containing all Connectors
        all_cell_connectors = set(self.CellConnectorBlock.CELLCONNECTORS)
        # set comparison for fast calculation of orphans
        orphaned_connectors = all_cell_connectors - cell_connector_set

        if orphaned_connectors:
            # only entered if there are orphaned Connectors
            msg = (
                "A CellConnector is designed to always be connected to one other "
                "CellConnector. The following CellConnector(s) are not connected "
                "to a counterpart: {0}. If this is intended and you know what you "
                "are doing, you can ignore or disable the SuspiciousUsageWarning."
            )
            warnings.warn(
                msg.format(orphaned_connectors),
                debugging.SuspiciousUsageWarning,
            )

    def _check_max_power_compliance(self):
        """
        Check if max_power values comply and hand out an error if not.
        """
        for con in self.CONNECTIONS:
            if not con[0].max_power == con[1].max_power:
                msg = (
                    "Two connected CellConnectors need to have the same max_power "
                    "value. The following values where set:\n"
                    "{0}: {1}\n"
                    "{2}: {3}"
                )
                raise ValueError(
                    msg.format(
                        con[0].label,
                        con[0].max_power,
                        con[1].label,
                        con[1].max_power,
                    )
                )

    def _mirror_connections(self):
        """
        For convenience, users only need to add (cc1, cc2, lf) to connect two
        CellConnectors. This creates the opposite connection (cc2, cc1, lf).
        """
        complete_connections = set()
        for con in self.CONNECTIONS:
            # add original connection
            complete_connections.add(con)
            # add mirrored connection
            complete_connections.add((con[1], con[0], con[2]))
        self.CONNECTIONS = complete_connections

    def _connect_cells(self):
        """
        This function actually connects the cells by equating the flows of
        the CellConnectors.

        TODO: When building the distributed model, this needs to stay in
        the main problem as complicating constraint.
        """
        # connection_block = po.Block()
        # self.add_component("ConnectionBlock", connection_block)

        def _equate_CellConnector_flows_rule(self, cc1, cc2, lf, t):
            lhs = self.flow[cc1, cc1.input_bus, t]
            rhs = (1 - lf) * self.flow[cc2.output_bus, cc2, t]
            return lhs == rhs

        self.equate_CellConnector_flows = po.Constraint(
            self.CONNECTIONS,
            self.TIMESTEPS,
            rule=_equate_CellConnector_flows_rule,
        )

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
        return processing.results(self)

    def solve(self, solver="cbc", solver_io="lp", **kwargs):
        r"""Takes care of communication with solver to solve the model.

        Parameters
        ----------
        solver : string
            solver to be used e.g. "cbc", "glpk","gurobi","cplex"
        solver_io : string
            pyomo solver interface file format: "lp","python","nl", etc.
        \**kwargs : keyword arguments
            Possible keys can be set see below:

        Other Parameters
        ----------------
        solve_kwargs : dict
            Other arguments for the pyomo.opt.SolverFactory.solve() method
            Example : {"tee":True}
        cmdline_options : dict
            Dictionary with command line options for solver e.g.
            {"mipgap":"0.01"} results in "--mipgap 0.01"
            \{"interior":" "} results in "--interior"
            \Gurobi solver takes numeric parameter values such as
            {"method": 2}
        """
        solve_kwargs = kwargs.get("solve_kwargs", {})
        solver_cmdline_options = kwargs.get("cmdline_options", {})

        opt = SolverFactory(solver, solver_io=solver_io)
        # set command line options
        options = opt.options
        for k in solver_cmdline_options:
            options[k] = solver_cmdline_options[k]

        solver_results = opt.solve(self, **solve_kwargs)

        status = solver_results["Solver"][0]["Status"]
        termination_condition = solver_results["Solver"][0][
            "Termination condition"
        ]

        if status == "ok" and termination_condition == "optimal":
            logging.info("Optimization successful...")
        else:
            msg = (
                "Optimization ended with status {0} and termination "
                "condition {1}"
            )
            warnings.warn(
                msg.format(status, termination_condition), UserWarning
            )
        self.es.results = solver_results
        self.solver_results = solver_results

        return solver_results

    def relax_problem(self):
        """Relaxes integer variables to reals of optimization model self."""
        relaxer = RelaxIntegrality()
        relaxer._apply_to(self)

        return self
