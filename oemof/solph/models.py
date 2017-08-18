# -*- coding: utf-8 -*-
"""

"""

from collections import UserDict, UserList
from itertools import groupby
import pyomo.environ as po
from pyomo.opt import SolverFactory
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality

from .network import Storage
from oemof.solph import blocks
from oemof.solph import network
from .options import Investment
from .plumbing import sequence
from ..outputlib import result_dictionary
import logging

# #############################################################################
#
# Solph Optimization Models
#
# #############################################################################

<<<<<<< 1506a7c3dae200f5283308aa69acc2b05e4aaba5

=======
>>>>>>> Add draft for expansion model example
class ExpansionModel(po.ConcreteModel):
    """ An energy system model for optimized capacity expansion.
    """

    CONSTRAINT_GROUPS = [blocks.ExpansionFlow,
                         blocks.Flow,
                         blocks.Bus,
                         blocks.LinearTransformer]

    def __init__(self, es, **kwargs):
        super().__init__()

        # ########################  Arguments #################################

        self.name = kwargs.get('name', 'ExpansionModel')
        self.es = es

        self.period_increment = sequence(kwargs.get('period_increment', 1))

        # TODO: Create timeincrement based on timeindex
        self.timeincrement = kwargs.get('timeincrement', sequence(1))

        self._constraint_groups = (ExpansionModel.CONSTRAINT_GROUPS +
                                   kwargs.get('constraint_groups', []))

        # dictionary with all flows containing flow objects as values und
        # tuple of string representation of oemof nodes (predecessor, successor)
        self.flows = es.flows()

        # ###########################  SETS  ##################################
        # set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.es.nodes])

        # pyomo set for timeindex of optimization problem
        # dict helper: {'year1': 0, 'year2': 1, ...}
        d = dict(zip(self.es.timeindex.keys(),
                     range(len(self.es.timeindex))))

        self.TIMEINDEX = po.Set(
            initialize=list(zip(
                [d[a] for a in es.timeindex for t in es.timeindex[a]],
                range(len([t  for a in es.timeindex for t in es.timeindex[a]])))),
                                ordered=True)

        self.TIMESTEPS = range(len([t  for a in es.timeindex
                                       for t in es.timeindex[a]]))
        # pyomo set for all flows in the energy system graph
        self.FLOWS = po.Set(initialize=self.flows.keys(),
                            ordered=True, dimen=2)

        self.PERIODS =  po.Set(initialize=range(len(es.timeindex)),
                               ordered=True)

        self.PERIOD_TIMESTEPS = {
            d[a]: self.TIMESTEPS[d[a]*len(es.timeindex[a]):
                                 (1+d[a])*len(es.timeindex[a])]
                for a in es.timeindex}

        self.flow = po.Var(self.FLOWS, self.TIMEINDEX,
                           within=po.NonNegativeReals)

        # ########################### CONSTRAINTS #############################
        # loop over all constraint groups to add constraints to the model
        for group in self._constraint_groups:
            # create instance for block
            block = group()
            # Add block to model

            self.add_component(str(block), block)
            # create constraints etc. related with block for all nodes
            # in the group
            block._create(group=self.es.groups.get(group))

        # ########################### Objective ###############################

        self.objective_function()


    def system_constraints(self):
        """
        """
        buses = [n for n in self.es.nodes
                 if isinstance(n, network.Bus) and n.sector == 'electricity']

        P = {n:[i for i in n.inputs] for n in buses}
        #S = {n:[i for i in n.outputs] for n in buses}

        # TODO: Calculate System Demand (SD), System Peak Load (SPL)
        SPL = 100 # self.es.SPL
        SD = 120  # self.es.SD
        SE = 1000 # self.es.SEL

        def _capacity_margin_rule(model):
            """ Eq. 14 [1]
            """
            for a, t in self.TIMEINDEX:
                lhs = 0
                rhs = 0
                for n in buses:
                    lhs += sum(self.ExpansionFlow.expanded_flow[p,n,a] *
                               self.flows[p,n].nominal_value *
                               self.flows[p,n].system_potential['capacity']
                               for p in P[n]
                               if (p,n) in self.ExpansionFlow.EXPANSION_FLOWS)
                rhs = SPL * self.es.capacity_margin
                self.capacity_margin.add((a,t), lhs >= rhs)
        self.capacity_margin = po.Constraint(self.TIMEINDEX, noruleinit=True)
        self.capacity_margin_build = po.BuildAction(rule=_capacity_margin_rule)

        def _reserve_margin_rule(model):
            """ Eq. 15 [1]
            """
            # TODO: add
            for a, t in  self.TIMEINDEX:
                lhs = 0
                rhs = 0
                for n in buses:
                    lhs += sum(self.ExpansionFlow.reserve_flow[p,n,a,t] *
                               self.flows[p,n].system_potential['reserve']
                               for p in P[n]
                               if (p,n) in self.ExpansionFlow.EXPANSION_FLOWS)
                rhs = SD * self.es.reserve_margin
                self.reserve_margin.add((a,t), lhs >= rhs)
        self.reserve_margin = po.Constraint(self.TIMEINDEX, noruleinit=True)
        self.reserve_margin_build = po.BuildAction(rule=_reserve_margin_rule)

        def _system_inertia_rule(model):
            """ Eq. 16 [1]
            """
            # TODO: add
            for a, t in self.TIMEINDEX:
                lhs = 0
                rhs = 0
                for n in buses:
                    lhs += sum(self.ExpansionFlow.active_flow[p,n,a,t] *
                               self.flows[p,n].nominal_value *
                               self.flows[p, n].system_potential['inertia']
                               for p in P[n]
                               if (p,n) in self.ExpansionFlow.EXPANSION_FLOWS)
                rhs = SD * self.es.reserve_margin
                self.system_inertia.add((a,t), lhs >= rhs)
        self.system_inertia = po.Constraint(self.TIMEINDEX, noruleinit=True)
        self.system_inertia_build = po.BuildAction(rule=_system_inertia_rule)

        def _system_emission_rule(model):
            """ Eq. 17 [1]
            """
            # TODO: add
            for a, t in self.TIMEINDEX:
                lhs = 0
                rhs = 0
                for n in buses:
                    lhs += sum(self.flow[p,n,a,t] *
                               self.flows[p,n].emission
                               for p in P[n])
                rhs = SE
                self.emissions.add((a,t), lhs <= rhs)
        self.emissions = po.Constraint(self.TIMEINDEX, noruleinit=True)
        self.emissions_build = po.BuildAction(rule=_system_emission_rule)



    def objective_function(self, sense=po.minimize, update=False):
        """
        """
        if update:
            self.del_component('objective')

        expr = 0

        # Expression for investment flows
        for block in self.component_data_objects():
            if hasattr(block, '_objective_expression'):
                expr += block._objective_expression()

        self.objective = po.Objective(sense=sense, expr=expr)

class OperationalModel(po.ConcreteModel):
    """ An energy system model for operational simulation with optimized
    dispatch.

    Parameters
    ----------
    es : EnergySystem object
        Object that holds the nodes of an oemof energy system graph
    constraint_groups : list
        Solph looks for these groups in the given energy system and uses them
        to create the constraints of the optimization problem.
        Defaults to :const:`OperationalModel.CONSTRAINTS`

    **The following sets are created**:

    NODES :
        A set with all nodes of the given energy system.

    TIMESTEPS :
        A set with all timesteps of the given time horizon.

    FLOWS :
        A 2 dimensional set with all flows. Index: `(source, target)`

    NEGATIVE_GRADIENT_FLOWS :
        A subset of set FLOWS with all flows where attribute
        `negative_gradient` is set.

    POSITIVE_GRADIENT_FLOWS :
        A subset of set FLOWS with all flows where attribute
        `positive_gradient` is set.

    **The following variables are created**:

    flow
        Flow from source to target indexed by FLOWS, TIMESTEPS.
        Note: Bounds of this variable are set depending on attributes of
        the corresponding flow object.

    negative_flow_gradient :
        Difference of a flow in consecutive timesteps if flow is reduced
        indexed by NEGATIVE_GRADIENT_FLOWS, TIMESTEPS.

    positive_flow_gradient :
        Difference of a flow in consecutive timesteps if flow is increased
        indexed by NEGATIVE_GRADIENT_FLOWS, TIMESTEPS.

    """
    CONSTRAINT_GROUPS = [blocks.Bus, blocks.LinearTransformer,
                         blocks.LinearN1Transformer,
                         blocks.VariableFractionTransformer,
                         blocks.Storage, blocks.InvestmentFlow,
                         blocks.InvestmentStorage, blocks.Flow,
                         blocks.BinaryFlow, blocks.DiscreteFlow]

    def __init__(self, es, **kwargs):
        super().__init__()

        # ########################  Arguments #################################

        self.name = kwargs.get('name', 'OperationalModel')
        self.es = es
        self.timeindex = es.timeindex
        self.timesteps = range(len(self.timeindex))
        self.timeincrement = sequence(self.timeindex.freq.nanos / 3.6e12)

        self._constraint_groups = (OperationalModel.CONSTRAINT_GROUPS +
                                   kwargs.get('constraint_groups', []))

        # dictionary with all flows containing flow objects as values und
        # tuple of string representation of oemof nodes (source, target)
        self.flows = es.flows()


        # ###########################  SETS  ##################################
        # set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.es.nodes])

        # dict helper: {'period1': 0, 'period2': 1, ...}
        periods = getattr(es.timeindex, 'year')
        d = dict(zip(set(periods),
                     range(len(set(periods)))))

        # pyomo set for timesteps of optimization problem
        self.TIMEINDEX = po.Set(
            initialize=list(zip([d[a] for a in periods],
                                range(len(es.timeindex)))),
                                ordered=True)

        self.PERIODS = po.Set(initialize=range(len(set(periods))))

        self.TIMESTEPS = po.Set(initialize=self.timesteps, ordered=True)

        # TODO: Make this robust
        self.PERIOD_TIMESTEPS = {a: range( int( len(self.TIMESTEPS) /
                                                len(self.PERIODS) )
                                         )
                                 for a in self.PERIODS}
        # previous timesteps
        previous_timesteps = [x - 1 for x in self.timesteps]
        previous_timesteps[0] = self.timesteps[-1]

        self.previous_timesteps = dict(zip(self.TIMESTEPS, previous_timesteps))
        # self.PREVIOUS_TIMESTEPS = po.Set(self.TIMESTEPS,
        #                            initialize=dict(zip(self.TIMESTEPS,
        #                                                previous_timesteps)))

        # pyomo set for all flows in the energy system graph
        self.FLOWS = po.Set(initialize=self.flows.keys(),
                            ordered=True, dimen=2)

        self.NEGATIVE_GRADIENT_FLOWS = po.Set(
            initialize=[(n, t) for n in self.es.nodes
                        for (t, f) in n.outputs.items()
                        if f.negative_gradient[0] is not None],
            ordered=True, dimen=2)

        self.POSITIVE_GRADIENT_FLOWS = po.Set(
            initialize=[(n, t) for n in self.es.nodes
                        for (t, f) in n.outputs.items()
                        if f.positive_gradient[0] is not None],
            ordered=True, dimen=2)

        # ######################### FLOW VARIABLE #############################

        # non-negative pyomo variable for all existing flows in energysystem
        self.flow = po.Var(self.FLOWS, self.TIMEINDEX,
                           within=po.NonNegativeReals)

        # loop over all flows and timesteps to set flow bounds / values
        for (o, i) in self.FLOWS:
            for a, t in self.TIMEINDEX:
                if self.flows[o, i].actual_value[t] is not None and (
                        self.flows[o, i].nominal_value is not None):
                    # pre- optimized value of flow variable
                    self.flow[o, i, a, t].value = (
                        self.flows[o, i].actual_value[t] *
                        self.flows[o, i].nominal_value)
                    # fix variable if flow is fixed
                    if self.flows[o, i].fixed:
                        self.flow[o, i, a, t].fix()

                if self.flows[o, i].nominal_value is not None and (
                        self.flows[o, i].binary is None):
                    # upper bound of flow variable
                    self.flow[o, i, a, t].setub(self.flows[o, i].max[t] *
                                             self.flows[o, i].nominal_value)
                    # lower bound of flow variable
                    self.flow[o, i, a, t].setlb(self.flows[o, i].min[t] *
                                             self.flows[o, i].nominal_value)

        self.positive_flow_gradient = po.Var(self.POSITIVE_GRADIENT_FLOWS,
                                             self.TIMESTEPS,
                                             within=po.NonNegativeReals)

        self.negative_flow_gradient = po.Var(self.NEGATIVE_GRADIENT_FLOWS,
                                             self.TIMESTEPS,
                                             within=po.NonNegativeReals)

        # ########################### CONSTRAINTS #############################
        # loop over all constraint groups to add constraints to the model
        for group in self._constraint_groups:
            # create instance for block
            block = group()
            # Add block to model
            self.add_component(str(block), block)
            # create constraints etc. related with block for all nodes
            # in the group
            block._create(group=self.es.groups.get(group))

        # ########################### Objective ###############################
        self.objective_function()

    def objective_function(self, sense=po.minimize, update=False):
        """
        """
        if update:
            self.del_component('objective')

        expr = 0

        # Expression for investment flows
        for block in self.component_data_objects():
            if hasattr(block, '_objective_expression'):
                expr += block._objective_expression()

        self.objective = po.Objective(sense=sense, expr=expr)

    def receive_duals(self):
        """ Method sets solver suffix to extract information about dual
        variables from solver. Shadow prices (duals) and reduced costs (rc) are
        set as attributes of the model.

        """
        # shadow prices
        self.dual = po.Suffix(direction=po.Suffix.IMPORT)
        # reduced costs
        self.rc = po.Suffix(direction=po.Suffix.IMPORT)

    def results(self):
        """ Returns a nested dictionary of the results of this optimization
        """
<<<<<<< HEAD
        # TODO: Make the results dictionary a proper object?
        result = UserDict()
        result.objective = self.objective()
        investment = UserDict()
        for i, o in self.flows:

            result[i] = result.get(i, UserDict())
            result[i][o] = UserList([self.flow[i, o, a, t].value
                                     for a, t in self.TIMEINDEX])

            if isinstance(i, Storage):
                if i.investment is None:
                    result[i][i] = UserList(
                        [self.Storage.capacity[i, t].value
                         for t in self.TIMESTEPS])
                else:
                    result[i][i] = UserList(
                        [self.InvestmentStorage.capacity[i, t].value
                         for t in self.TIMESTEPS])

            if isinstance(self.flows[i, o].investment, Investment):
                setattr(result[i][o], 'invest',
                        self.InvestmentFlow.invest[i, o].value)
                investment[(i, o)] = self.InvestmentFlow.invest[i, o].value
                if isinstance(i, Storage):
                    setattr(result[i][i], 'invest',
                            self.InvestmentStorage.invest[i].value)
                    investment[(i, i)] = self.InvestmentStorage.invest[i].value
        # add results of dual variables for balanced buses
        if hasattr(self, "dual"):
            # grouped = [(b1, [(b1, 0), (b1, 1)]), (b2, [(b2, 0), (b2, 1)])]
            #import pdb; pdb.set_trace()
            grouped = groupby(sorted(self.Bus.balance.iterkeys()),
                              lambda pair: pair[0])

            for bus, timesteps in grouped:
                result[bus] = result.get(bus, UserDict())
                result[bus][bus] = [self.dual[self.Bus.balance[bus, a, t]]
                                    for _, a, t in timesteps]

        result.investment = investment
=======

        result = result_dictionary.result_dict(self)
>>>>>>> dev

        return result

    def solve(self, solver='glpk', solver_io='lp', **kwargs):
        r""" Takes care of communication with solver to solve the model.

        Parameters
        ----------
        solver : string
            solver to be used e.g. "glpk","gurobi","cplex"
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
            {"interior":" "} results in "--interior"
            Gurobi solver takes numeric parameter values such as
            {"method": 2}

        """
        solve_kwargs = kwargs.get('solve_kwargs', {})
        solver_cmdline_options = kwargs.get("cmdline_options", {})

        opt = SolverFactory(solver, solver_io=solver_io)
        # set command line options
        options = opt.options
        for k in solver_cmdline_options:
            options[k] = solver_cmdline_options[k]

        results = opt.solve(self, **solve_kwargs)

        status = results["Solver"][0]["Status"].key
        termination_condition = \
            results["Solver"][0]["Termination condition"].key

        if status == "ok" and termination_condition == "optimal":
            logging.info("Optimization successful...")
            self.solutions.load_from(results)
            # storage results in result dictionary of energy system
            self.es.results = self.results()
            self.es.results.objective = self.objective()
            self.es.results.solver = results
        elif status == "ok" and termination_condition == "unknown":
            logging.warning("Optimization with unknown termination condition."
                            + " Writing output anyway...")
            self.solutions.load_from(results)
            # storage results in result dictionary of energy system
            self.es.results = self.results()
            self.es.results.objective = self.objective()
            self.es.results.solver = results
        elif status == "warning" and termination_condition == "other":
            logging.warning("Optimization might be sub-optimal."
                            + " Writing output anyway...")
            self.solutions.load_from(results)
            # storage results in result dictionary of energy system
            self.es.results = self.results()
            self.es.results.objective = self.objective()
            self.es.results.solver = results
        else:
            # storage results in result dictionary of energy system
            self.es.results = self.results()
            self.es.results.objective = self.objective()
            self.es.results.solver = results
            logging.error(
                "Optimization failed with status %s and terminal condition %s"
                % (status, termination_condition))

        return results

    def relax_problem(self):
        """Relaxes integer variables to reals of optimization model self."""
        relaxer = RelaxIntegrality()
        relaxer._apply_to(self)

        return self
