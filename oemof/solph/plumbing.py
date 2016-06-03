# -*- coding: utf-8 -*-
"""

"""
from collections import UserDict, UserList
import pyomo.environ as po
from pyomo.opt import SolverFactory
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality
from oemof.solph import blocks
from .network import Sink, Source, Storage
from .options import Investment


# #############################################################################
#
# Solph Optimization Models
#
# #############################################################################

# TODO: Add an nice capacity expansion model ala temoa/osemosys ;)

class ExpansionModel(po.ConcreteModel):
    """ An energy system model for optimized capacity expansion.
    """
    def __init__(self):
        super().__init__()


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
    timeindex : DatetimeIndex

    """
    CONSTRAINT_GROUPS = [blocks.Bus, blocks.LinearTransformer,
                         blocks.Storage, blocks.InvestmentFlow,
                         blocks.InvestmentStorage, blocks.Flow,
                         blocks.Discrete]

    def __init__(self, es, **kwargs):
        super().__init__()

        # ########################  Arguments #################################

        self.name = kwargs.get('name', 'OperationalModel')
        self.es = es
        self.timeindex = kwargs.get('timeindex')
        self.timesteps = range(len(self.timeindex))
        self.timeincrement = self.timeindex.freq.nanos / 3.6e12  # hours

        self._constraint_groups = OperationalModel.CONSTRAINT_GROUPS
        self._constraint_groups.extend(kwargs.get('constraint_groups', []))

        # dictionary with all flows containing flow objects as values und
        # tuple of string representation of oemof nodes (source, target)
        self.flows = {(source, target): source.outputs[target]
                      for source in es.nodes
                      for target in source.outputs}

        # ###########################  SETS  ##################################
        # set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.es.nodes])

        # pyomo set for timesteps of optimization problem
        self.TIMESTEPS = po.Set(initialize=self.timesteps, ordered=True)

        # previous timesteps
        previous_timesteps = [x - 1 for x in self.timesteps]
        previous_timesteps[0] = self.timesteps[-1]

        self.previous_timesteps = dict(zip(self.TIMESTEPS, previous_timesteps))
        # self.PREVIOUS_TIMESTEPS = po.Set(self.TIMESTEPS,
        #                            initialize=dict(zip(self.TIMESTEPS,
        #                                                previous_timesteps)))

        # indexed index set for inputs of nodes (nodes as indices)
        self.INPUTS = po.Set(self.NODES, initialize={
            n: [i for i in n.inputs] for n in self.es.nodes
            if not isinstance(n, Source)
            }
        )

        # indexed index set for outputs of nodes (nodes as indices)
        self.OUTPUTS = po.Set(self.NODES, initialize={
            n: [o for o in n.outputs] for n in self.es.nodes
            if not isinstance(n, Sink)
            }
        )

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
        self.flow = po.Var(self.FLOWS, self.TIMESTEPS,
                           within=po.NonNegativeReals)

        # loop over all flows and timesteps to set flow bounds / values
        for (o, i) in self.FLOWS:
            for t in self.TIMESTEPS:
                if self.flows[o, i].actual_value[t] is not None and (
                        self.flows[o, i].nominal_value is not None):
                    # pre- optimized value of flow variable
                    self.flow[o, i, t].value = (
                        self.flows[o, i].actual_value[t] *
                        self.flows[o, i].nominal_value)
                    # fix variable if flow is fixed
                    if self.flows[o, i].fixed:
                        self.flow[o, i, t].fix()

                if self.flows[o, i].nominal_value is not None:
                    # upper bound of flow variable
                    self.flow[o, i, t].setub(self.flows[o, i].max[t] *
                                             self.flows[o, i].nominal_value)
                    # lower bound of flow variable
                    self.flow[o, i, t].setlb(self.flows[o, i].min[t] *
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
        r""" Method sets solver suffix to extract information about dual
        variables from solver. Shadowprices (duals) and reduced costs (rc) are
        set as attributes of the model.

        """
        self.dual = po.Suffix(direction=po.Suffix.IMPORT)
        # reduced costs
        self.rc = po.Suffix(direction=po.Suffix.IMPORT)

    def results(self):
        """ Returns a nested dictionary of the results of this optimization
        model.

        The dictionary is keyed by the :class:`Entities
        <oemof.core.network.Entity>` of the optimization model, that is
        :meth:`om.results()[s][t] <OptimizationModel.results>`
        holds the time series representing values attached to the edge (i.e.
        the flow) from `s` to `t`, where `s` and `t` are instances of
        :class:`Entity <oemof.core.network.Entity>`.

        Time series belonging only to one object, like e.g. shadow prices of
        commodities on a certain :class:`Bus
        <oemof.core.network.entities.Bus>`, dispatch values of a
        :class:`DispatchSource
        <oemof.core.network.entities.components.sources.DispatchSource>` or
        storage values of a
        :class:`Storage
        <oemof.core.network.entities.components.transformers.Storage>` are
        treated as belonging to an edge looping from the object to itself.
        This means they can be accessed via
        :meth:`om.results()[object][object] <OptimizationModel.results>`.

        Other result from the optimization model can be accessed like
        attributes of the flow, e.g. the invest variable for capacity
        of the storage 'stor' can be accessed like:

        :attr:`om.results()[stor][stor].invest` attribute

        For the investment flow of a 'tranfsformer' trsf to the bus 'bel' this
        can be accessed with:

        :attr:`om.results()[trsf][bel].invest` attribute

        The value of the objective function is stored under the
        :attr:`om.results().objective` attribute.

        Note that the optimization model has to be solved prior to invoking
        this method.
        """
        # TODO: Maybe make the results dictionary a proper object?

        result = UserDict()
        result.objective = self.objective()
        for i,o in self.flows:

            result[i] = result.get(i, UserDict())
            result[i][o] = UserList([self.flow[i, o, t].value
                                     for t in self.TIMESTEPS])

            if isinstance(i, Storage):
                if i.investment is None:
                    result[i][i] = UserList(
                        [self.Storage.capacity[i, t].value
                         for t in self.TIMESTEPS])
                else:
                    result[i][i] = UserList(
                        [self.InvestmentStorage.capacity[i, t].value
                         for t in self.TIMESTEPS])

            if isinstance(self.flows[i,o].investment, Investment):
                setattr(result[i][o], 'invest',
                        self.InvestmentFlow.invest[i,o].value)
                if isinstance(i, Storage):
                    setattr(result[i][i], 'invest',
                            self.InvestmentStorage.invest[i].value)

        # TODO: extract duals for all constraints ?

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
        solve_kwargs : dict
            Other arguments for the pyomo.opt.SolverFactory.solve() method
            Example : {"tee":True}
        cmdline_options : dict
            Dictionary with command line options for solver e.g.
            {"mipgap":"0.01"} results in "--mipgap 0.01"
            {"interior":" "} results in "--interior"

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

        return results

    def relax_problem(self):
        """ Relaxes integer variables to reals of optimization model self
        """
        relaxer = RelaxIntegrality()
        relaxer._apply_to(self)

        return self
