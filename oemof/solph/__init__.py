"""


"""
from collections import abc, UserList
import warnings
import pandas as pd
import pyomo.environ as pyomo
from pyomo.opt import SolverFactory
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality
import oemof.network as on
from oemof.solph import constraints as cblocks
from oemof.core import energy_system as oces

###############################################################################
#
# Solph Functions
#
###############################################################################

def Sequence(sequence_or_scalar):
    """ Tests if an object is sequence (except string) or scalar and returns
    a the original sequence if object is a sequence and a 'emulated' sequence
    object of class _Sequence if object is a scalar or string.

    Parameters
    ----------
    sequence_or_scalar : array-like or scalar (None, int, etc.)

    Examples
    --------
    >>> Sequence([1,2])
    [1, 2]

    >>> x = Sequence(10)
    >>> x[0]
    10

    >>> x[10]
    10
    >>> print(x)
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    """
    if ( isinstance(sequence_or_scalar, abc.Iterable) and not
         isinstance(sequence_or_scalar, str) ):
       return sequence_or_scalar
    else:
       return _Sequence(default=sequence_or_scalar)

###############################################################################
#
# Solph Classes
#
###############################################################################

class _Sequence(UserList):
    """ Emulates a list whose length is not known in advance.

    Parameters
    ----------
    source:
    default:


    Examples
    --------
    >>> s = _Sequence(default=42)
    >>> len(s)
    0
    >>> s[2]
    42
    >>> len(s)
    3
    >>> s[0] = 23
    >>> s
    [23, 42, 42]

    """
    def __init__(self, *args, **kwargs):
        self.default = kwargs["default"]
        super().__init__(*args)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            return self.data[key]

    def __setitem__(self, key, value):
        try:
            self.data[key] = value
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            self.data[key] = value


class Flow:
    """
    Define a flow between two nodes.

    Parameters
    ----------
    summed_max : float
        Specific maximum value summed over all timesteps. Will be multiplied
        with the nominal_value to get the absolute limit. If investment is set
        the summed_max will be multiplied with the nominal_value_variable.
    summed_min : float
        see above

    """
    def __init__(self, *args, **kwargs):
        """
        """
        # TODO: Check if we can inherit form pyomo.core.base.var _VarData
        # then we need to create the var object with
        # pyomo.core.base.IndexedVarWithDomain before any Flow is created.
        # E.g. create the variable in the energy system and populate with
        # information afterwards when creating objects.

        self.nominal_value = kwargs.get('nominal_value')
        self.min = Sequence(kwargs.get('min', 0))
        self.max = Sequence(kwargs.get('max', 1))
        self.actual_value = Sequence(kwargs.get('actual_value'))
        self.variable_costs = Sequence(kwargs.get('variable_costs'))
        self.fixed_costs = kwargs.get('fixed_costs')
        self.summed_max = kwargs.get('summed_max')
        self.summed_min = kwargs.get('summed_min')
        self.fixed = kwargs.get('fixed', False)
        self.investment = kwargs.get('investment')
        if self.fixed:
            warnings.warn(
                "Values for min/max will be ignored if fixed is True.",
                SyntaxWarning)
            self.min = Sequence(0)
            self.max = Sequence(1)
        if self.investment and self.nominal_value is not None:
            self.nominal_value = None
            warnings.warn(
                "Using the investment object the nominal_value is set to None.",
                SyntaxWarning)


Bus = on.Bus


class Investment:
    """
    Parameters
    ----------
    maximum : float
        Maximum of the additional invested capacity
    epc : float
        Equivalent periodical costs for the investment, if period is one
        year these costs are equal to the equivalent annual costs.

    """
    def __init__(self, maximum=float('+inf'), epc=None):
        self.maximum = maximum
        self.epc = epc


class Sink(on.Sink):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Source(on.Source):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class LinearTransformer(on.Transformer):
    """
    Parameters
    ----------

    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of timehorizon for simulation.

    Examples
    --------
    >>> bel = Bus()
    >>> bth = Bus()
    >>> trsf = LinearTransformer(conversion_factors={bel: 0.4,
    ...                                              bth: [1, 2, 3]})
    >>> trsf.conversion_factors[bel][3]
    0.4

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factors = {k: Sequence(v)
            for k,v in kwargs.get('conversion_factors').items()}


class Storage(on.Transformer):
    """

    Parameters
    ----------
    nominal_capacity : numeric
        Absolute nominal capacity of the storage
    nominal_input_capacity_ratio :  numeric
        Ratio between the nominal inflow of the storage and its capacity.
    nominal_output_capacity_ratio : numeric
        Ratio between the nominal outflow of the storage and its capacity.
        Note: This ratio is used to create the Flow object for the outflow
        and set its nominal value of the storage in the constructor.
    nominal_input_capacity_ratio : numeric
        see: nominal_output_capacity_ratio
    initial_capacity : numeric
        The capacity of the storage in the first (and last) timestep of
        optimization.
    capacity_loss : numeric (sequence or scalar)
        The relativ loss of the storage capacity from between two consecutive
        timesteps.
    inflow_conversion_factor : numeric (sequence or scalar)
        The relative conversion factor, i.e. efficiency associated with the
        inflow of the storage.
    outflow_conversion_factor : numeric (sequence or scalar)
        see: inflow_conversion_factor
    capacity_min : numeric (sequence or scalar)
        The normend minimum capacity of the storage, e.g. a value between 0,1.
        To use different values in every timesteps use a sequence of values.
    capacity_max : numeric (sequence or scalar)
        see: capacity_min

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nominal_capacity = kwargs.get('nominal_capacity')
        self.nominal_input_capacity_ratio = kwargs.get(
            'nominal_input_capacity_ratio', 0.2)
        self.nominal_output_capacity_ratio = kwargs.get(
            'nominal_output_capacity_ratio', 0.2)
        self.initial_capacity = kwargs.get('initial_capacity', 0)
        self.capacity_loss = Sequence(kwargs.get('capacity_loss', 0))
        self.inflow_conversion_factor = Sequence(
            kwargs.get(
                'inflow_conversion_factor', 1))
        self.outflow_conversion_factor = Sequence(
            kwargs.get(
                'outflow_conversion_factor', 1))
        self.capacity_max = Sequence(kwargs.get('capacity_max', 1))
        self.capacity_min = Sequence(kwargs.get('capacity_min', 0))
        self.investment = kwargs.get('investment')
        # Check investment
        if self.investment and self.nominal_capacity is not None:
            self.nominal_capacity = None
            warnings.warn(
                "Using the investment object the nominal_capacity is set to" +
                "None.", SyntaxWarning)
        # Check input flows for nominal value
        for flow in self.inputs.values():
            if flow.nominal_value is not None:
                storage_nominal_value_warning('output')
            if self.nominal_capacity is None:
                flow.nominal_value = None
            else:
                flow.nominal_value = (self.nominal_input_capacity_ratio *
                                      self.nominal_capacity)
            if self.investment:
                flow.investment = Investment()
        # Check output flows for nominal value
        for flow in self.outputs.values():
            if flow.nominal_value is not None:
                storage_nominal_value_warning('input')
            if self.nominal_capacity is None:
                flow.nominal_value = None
            else:
                flow.nominal_value = (self.nominal_output_capacity_ratio *
                                      self.nominal_capacity)
            if self.investment:
                flow.investment = Investment()


def storage_nominal_value_warning(flow):
    msg = ("The nominal_value should not be set for {0} flows of storages." +
           "The value will be overwritten by the product of the " +
           "nominal_capacity and the nominal_{0}_capacity_ratio.")
    warnings.warn(msg.format(flow), SyntaxWarning)


###############################################################################
#
# Solph Optimization Models
#
###############################################################################

# TODO: Add an nice capacity expansion model ala temoa/osemosys ;)
class ExpansionModel(pyomo.ConcreteModel):
    """ An energy system model for optimized capacity expansion.
    """
    def __init__(self, es):
        super().__init__()



class OperationalModel(pyomo.ConcreteModel):
    """ An energy system model for operational simulation with optimized
    distpatch.

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

    CONSTRAINT_GROUPS = [cblocks.BusBalance, cblocks.LinearRelation,
                         cblocks.StorageBalance, cblocks.InvestmentFlow]

    OBJECTIVE_GROUPS = [cblocks.VariableCosts]

    def __init__(self, es, *args, **kwargs):
        super().__init__()

        ##########################  Arguments#  ###############################

        self.name = kwargs.get('name', 'OperationalModel')
        self.es = es
        self.timeindex = kwargs.get('timeindex')
        self.timesteps = range(len(self.timeindex))
        self.timeincrement = self.timeindex.freq.nanos / 3.6e12  # hours
        # TODO Use solph groups and add user defined groups ????
        # self._constraint_groups = OperationalModel.CONSTRAINT_GROUPS
        # self._constraint_groups.add(kwargs.get('constraint_groups', []))
        constraint_groups = kwargs.get('constraint_groups',
                                       OperationalModel.CONSTRAINT_GROUPS)
        # dictionary with all flows containing flow objects as values und
        # tuple of string representation of oemof nodes (source, target)
        self.flows = {(str(source), str(target)): source.outputs[target]
                      for source in es.nodes
                      for target in source.outputs}

        # ###########################  SETS  ##################################
        # set with all nodes
        self.NODES = pyomo.Set(initialize=[str(n) for n in self.es.nodes])

        # pyomo set for timesteps of optimization problem
        self.TIMESTEPS = pyomo.Set(initialize=self.timesteps,
                                   ordered=True)

        previous_timesteps_list = [x - 1 for x in self.timesteps]
        previous_timesteps_list[0] = len(self.timesteps) - 1

        self.previous_timestep = dict(zip(self.timesteps,
                                          previous_timesteps_list))
        print('wer', self.previous_timestep)

        # indexed index set for inputs of nodes (nodes as indices)
        self.INPUTS = pyomo.Set(self.NODES, initialize={
            str(n): [str(i) for i in n.inputs]
                     for n in self.es.nodes
                     if not isinstance(n, on.Source)
            }
        )

        # indexed index set for outputs of nodes (nodes as indices)
        self.OUTPUTS = pyomo.Set(self.NODES, initialize={
            str(n): [str(o) for o in n.outputs]
                     for n in self.es.nodes
                     if not isinstance(n, on.Sink)
            }
        )

        # pyomo set for all flows in the energy system graph
        self.FLOWS = pyomo.Set(initialize=self.flows.keys(),
                               ordered=True, dimen=2)

        # set for all flows for which fixed osts are set
        self.FIXEDCOST_FLOWS = pyomo.Set(
            initialize=[(str(n), str(t)) for n in self.es.nodes
                                         for (t,f) in n.outputs.items()
                                         if f.fixed_costs is not None and
                                         f.nominal_value is not None],
            ordered=True, dimen=2)

        # set for all flows with an global limit on the flow over time
        self.UB_LIMIT_FLOWS = pyomo.Set(
            initialize=[(str(n), str(t)) for n in self.es.nodes
                        for (t, f) in n.outputs.items()
                        if f.summed_max is not None and
                        f.nominal_value is not None],
            ordered=True, dimen=2)

        self.LB_LIMIT_FLOWS = pyomo.Set(
            initialize=[(str(n), str(t)) for n in self.es.nodes
                        for (t, f) in n.outputs.items()
                        if f.summed_min is not None and
                        f.nominal_value is not None],
            ordered=True, dimen=2)
        # ######################## FLOW VARIABLE #############################

        # non-negative pyomo variable for all existing flows in energysystem
        self.flow = pyomo.Var(self.FLOWS, self.TIMESTEPS,
                              within=pyomo.NonNegativeReals)

        # loop over all flows and timesteps to set flow bounds / values
        for (o, i) in self.FLOWS:
            for t in self.TIMESTEPS:
                if self.flows[o, i].actual_value[t] is not None:
                    # pre- optimized value of flow variable
                    self.flow[o, i, t].value = self.flows[o, i].actual_value[t]
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

        # constraint to bound the sum of a flow over all timesteps
        self.flow_sum_max = pyomo.Constraint(self.UB_LIMIT_FLOWS,
                                             noruleinit=True)
        self.flow_sum_min = pyomo.Constraint(self.LB_LIMIT_FLOWS,
                                             noruleinit=True)

        def _flow_summed_max_rule(model):
            for i, o in self.UB_LIMIT_FLOWS:
                lhs = sum(self.flow[i, o, t] * self.timeincrement
                          for t in self.TIMESTEPS)
                rhs = (self.flows[i, o].summed_max *
                       self.flows[i, o].nominal_value)
                self.flow_sum_max.add((i, o), lhs <= rhs)

        def _flow_summed_min_rule(model):
            for i, o in self.LB_LIMIT_FLOWS:
                lhs = sum(self.flow[i, o, t] * self.timeincrement
                          for t in self.TIMESTEPS)
                rhs = (self.flows[i, o].summed_min *
                       self.flows[i, o].nominal_value)
                self.flow_sum_min.add((i, o), lhs >= rhs)

        self.flow_sum_maxCon = pyomo.BuildAction(rule=_flow_summed_max_rule)
        self.flow_sum_minCon = pyomo.BuildAction(rule=_flow_summed_min_rule)

        ############################# CONSTRAINTS #############################
        # loop over all constraint groups to add constraints to the model
        for group in constraint_groups:
            # create instance for block
            block = group()
            # Add block to model
            self.add_component(str(block), block)
            # create constraints etc. related with block for all nodes
            # in the group
            block._create(group=self.es.groups.get(group))

        ############################# Objective ###############################
        self.objective_function()


    def objective_function(self, sense=pyomo.minimize, update=False):
        """
        """
        if update:
            self.del_component('objective')

        expr = 0

        for group in OperationalModel.OBJECTIVE_GROUPS:
            expr += group(self, self.es.groups.get(group))

        # Expression for fixed costs associated the the nominal value of flow
        expr += sum(self.flows[i, o].nominal_value *
                    self.flows[i, o].fixed_costs
                    for i, o in self.FIXEDCOST_FLOWS)

        # Expression for investment flows
        for block in self.component_data_objects():
            if isinstance(block, cblocks.InvestmentFlow) and \
                    hasattr(block, 'INVESTMENT_FLOWS'):
                expr += block._objective_expression()


        self.objective = pyomo.Objective(sense=sense, expr=expr)

    def receive_duals(self):
        r""" Method sets solver suffix to extract information about dual
        variables from solver. Shadowprices (duals) and reduced costs (rc) are
        set as attributes of the model.

        """
        self.dual = pyomo.Suffix(direction=pyomo.Suffix.IMPORT)
        # reduced costs
        self.rc = pyomo.Suffix(direction=pyomo.Suffix.IMPORT)

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

        return results

    def relax_problem(self):
        """ Relaxes integer variables to reals of optimization model self
        """
        relaxer = RelaxIntegrality()
        relaxer._apply_to(self)

        return self

###############################################################################
#
# Solph grouping functions
#
###############################################################################
def constraint_grouping(node):
    if isinstance(node, on.Bus) and 'balance' in str(node):
        return cblocks.BusBalance
    if isinstance(node, LinearTransformer):
        return cblocks.LinearRelation
    if isinstance(node, Storage):
        return cblocks.StorageBalance


def investment_key(n):
    for f in n.outputs.values():
        if f.investment is not None:
            return cblocks.InvestmentFlow

def investment_flows(n):
     return [(n, t, f) for (t, f) in n.outputs.items()
             if f.investment is not None]

def merge_investment_flows(n, group):
     group.extend(n)
     return group

investment_grouping = oces.Grouping(
    key=investment_key,
    value=investment_flows,
    merge=merge_investment_flows)

def variable_costs_key(n):
    for f in n.outputs.values():
        if f.variable_costs[0] is not None:
            return cblocks.VariableCosts

def variable_costs_flows(n):
     return [(n, t, f) for (t, f) in n.outputs.items()
             if f.variable_costs[0] is not None]

def merge_variable_costs_flows(n, group):
     group.extend(n)
     return group

variable_costs_grouping = oces.Grouping(
    key=variable_costs_key,
    value=variable_costs_flows,
    merge=merge_variable_costs_flows)

GROUPINGS = [constraint_grouping, investment_grouping, variable_costs_grouping]

""" list:  Groupings needed on an energy system for it to work with solph.

TODO: Maybe move this to the module docstring? It shoule be somewhere prominent
      so solph user's immediately see that they need to use :const:`GROUPINGS`
      when they want to create an energy system for use with solph.

If you want to use solph on an energy system, you need to create it with these
groupings specified like this:

    .. code-block: python

    from oemof.network import EnergySystem
    import solph

    energy_system = EnergySystem(groupings=solph.GROUPINGS)

"""

###############################################################################
#
# Examples
#
###############################################################################

if __name__ == "__main__":
    from oemof.core import energy_system as oces

    es = oces.EnergySystem(groupings=GROUPINGS,
                           time_idx=[1,2,3])

    lt = len(es.time_idx)

    bel = Bus(label="el_balance")
    bcoal = Bus(label="coalbus")

    so = Source(label="coalsource",
                outputs={bcoal: Flow()})

    wind = Source(label="wind", outputs={
        bel:Flow(actual_value=[1, 1, 2],
                 nominal_value=2,
                 fixed_costs=25,
                 investment=Investment(maximum=100, epc=200))
        }
    )

    si = Sink(label="sink", inputs={bel: Flow(max=[0.1, 0.2, 0.9],
                                              nominal_value=10, fixed=True,
                                              actual_value=[1, 2, 3])})

    trsf = LinearTransformer(label='trsf', inputs={bcoal:Flow()},
                             outputs={bel:Flow(nominal_value=10,
                                               fixed_costs=5,
                                               variable_costs=10,
                                               summed_max=4,
                                               summed_min=2)},
                             conversion_factors={bel: 0.4})
    stor = Storage(label="stor", inputs={bel: Flow()}, outputs={bel:Flow()},
                   nominal_capacity=50, inflow_conversion_factor=0.9,
                   outflow_conversion_factor=0.8, initial_capacity=0.5,
                   capacity_loss=0.001)

    date_time_index = pd.date_range('1/1/2011', periods=3, freq='60min')
    om = OperationalModel(es, timeindex=date_time_index)
    om.solve(solve_kwargs={'tee': True})
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})
    #om.pprint()
