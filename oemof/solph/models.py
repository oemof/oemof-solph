# -*- coding: utf-8 -*-
"""Creating models with their general sets, variables, constraints and parts
of the objective function.
"""

import pyomo.environ as po
from pyomo.opt import SolverFactory
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality
from oemof.solph import blocks, core
from .plumbing import sequence
from ..outputlib import result_dict

class DispatchModel(core.BaseModel):
    """ An energy system model for operational simulation with optimized
    dispatch. This class subclasses from BaseModel. See this class for more
    information on class attributes etc.

    **The following additioanl sets are created**

    NEGATIVE_GRADIENT_FLOWS :
        A subset of set FLOWS with all flows where attribute
        `negative_gradient` is set.

    POSITIVE_GRADIENT_FLOWS :
        A subset of set FLOWS with all flows where attribute
        `positive_gradient` is set.

    **The following additional variables are created**:

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
                         blocks.Storage, blocks.Flow]

    def __init__(self, es, **kwargs):
        super().__init__()


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


    def add_flow(self):
        """
        """
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

                    # upper bound of flow variable
                    self.flow[o, i, a, t].setub(self.flows[o, i].max[t] *
                                             self.flows[o, i].nominal_value)
                    # lower bound of flow variable
                    self.flow[o, i, a, t].setlb(self.flows[o, i].min[t] *
                                             self.flows[o, i].nominal_value)

        self.positive_flow_gradient = po.Var(self.POSITIVE_GRADIENT_FLOWS,
                                             self.TIMEINDEX,
                                             within=po.NonNegativeReals)

        self.negative_flow_gradient = po.Var(self.NEGATIVE_GRADIENT_FLOWS,
                                             self.TIMEINDEX,
                                             within=po.NonNegativeReals)


# *************************** depreceaded **********************************

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
    timeindex : pandas DatetimeIndex
        The time index will be used to calculate the timesteps and the
        time increment for the optimization model.
    timesteps : sequence (optional)
        Timesteps used in the optimization model. If provided as list or
        pandas.DatetimeIndex the sequence will be used to index the time
        dependent variables, constraints etc. If not provided we will try to
        compute this sequence from attr:`timeindex`.
    timeincrement : float or list of floats (optional)
        Time increment used in constraints and objective expressions.
        If type is 'float', will be converted internally to
        solph.plumbing.Sequence() object for time dependent time increment.
        If a list is provided this list will be taken. Default is calculated
        from timeindex if provided.

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
        self.timeindex = kwargs.get('timeindex', es.timeindex)
        self.timesteps = kwargs.get('timesteps', range(len(self.timeindex)))
        self.timeincrement = kwargs.get('timeincrement',
                                        self.timeindex.freq.nanos / 3.6e12)

        self.period_type = kwargs.get('period_type', 'year')
        # convert to sequence object for time dependent timeincrement
        self.timeincrement = sequence(self.timeincrement)


        if self.timesteps is None:
            raise ValueError("Missing timesteps!")
        self._constraint_groups = (OperationalModel.CONSTRAINT_GROUPS +
                                   kwargs.get('constraint_groups', []))

        # dictionary with all flows containing flow objects as values und
        # tuple of string representation of oemof nodes (source, target)
        self.flows = es.flows()


        # ###########################  SETS  ##################################
        # set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.es.nodes])

        # dict helper: {'period1': 0, 'period2': 1, ...}
        periods = getattr(es.timeindex, self.period_type)
        d = dict(zip(set(periods),range(len(set(periods)))))

        # TODO: claculate period incerment based on  d
        self.periodincrement = sequence(1)

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

        result = result_dict(self)

        return result

    def solve(self, solver='cbc', solver_io='lp', **kwargs):
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

        self.solutions.load_from(results)

        # storage optimization results in result dictionary of energysystem
        self.es.results = self.results()
        self.es.results.objective = self.objective()
        self.es.results.solver = results

        return results

    def relax_problem(self):
        """ Relaxes integer variables to reals of optimization model self
        """
        relaxer = RelaxIntegrality()
        relaxer._apply_to(self)

        return self
