"""


"""
from collections import abc, UserList, UserDict
from itertools import chain
import warnings
import pandas as pd
import pyomo.environ as po
from pyomo.opt import SolverFactory
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality
import oemof.network as on
from oemof.solph import blocks
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
    actual_value : float or array-like
        Specific value for the flow variable. Will be multiplied with the
        nominal_value to get the absolute value. If fixed is True the flow
        variable will be fixed to actual_value * nominal_value.

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
    pass

class Source(on.Source):
    pass



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
        self.initial_capacity = kwargs.get('initial_capacity')
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
class ExpansionModel(po.ConcreteModel):
    """ An energy system model for optimized capacity expansion.
    """
    def __init__(self, es):
        super().__init__()



class OperationalModel(po.ConcreteModel):
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

    CONSTRAINT_GROUPS = [blocks.Bus, blocks.LinearTransformer,
                         blocks.Storage, blocks.InvestmentFlow,
                         blocks.InvestmentStorage, blocks.Flow]

    def __init__(self, es, *args, **kwargs):
        super().__init__()

        ##########################  Arguments #################################

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
        #self.PREVIOUS_TIMESTEPS = po.Set(self.TIMESTEPS,
        #                            initialize=dict(zip(self.TIMESTEPS,
        #                                                previous_timesteps)))

        # indexed index set for inputs of nodes (nodes as indices)
        self.INPUTS = po.Set(self.NODES, initialize={
            n: [i for i in n.inputs] for n in self.es.nodes
                                     if not isinstance(n, on.Source)
            }
        )

        # indexed index set for outputs of nodes (nodes as indices)
        self.OUTPUTS = po.Set(self.NODES, initialize={
            n: [o for o in n.outputs] for n in self.es.nodes
                                      if not isinstance(n, on.Sink)
            }
        )

        # pyomo set for all flows in the energy system graph
        self.FLOWS = po.Set(initialize=self.flows.keys(),
                               ordered=True, dimen=2)

        # ######################## FLOW VARIABLE #############################

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

        ############################# CONSTRAINTS #############################
        # loop over all constraint groups to add constraints to the model
        for group in self._constraint_groups:
            # create instance for block
            block = group()
            # Add block to model
            self.add_component(str(block), block)
            # create constraints etc. related with block for all nodes
            # in the group
            block._create(group=self.es.groups.get(group))

        ############################# Objective ###############################
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

        The value of the objective function is stored under the
        :attr:`om.results().objective` attribute.

        Note that the optimization model has to be solved prior to invoking
        this method.
        """
        # TODO: Maybe make the results dictionary a proper object?

        # TODO: Do we need to store invested capacity / flow etc
        #       e.g. max(results[node][o]) will give the newly invested nom val
        result = UserDict()
        result.objective = self.objective()
        for node in self.es.nodes:
            if node.outputs:
                result[node] = result.get(node, UserDict())
            for o in node.outputs:
                result[node][o] = [self.flow[node, o, t].value
                                   for t in self.TIMESTEPS]
            for i in node.inputs:
                result[i] = result.get(i, UserDict())
                result[i][node] = [self.flow[i, node, t].value
                                   for t in self.TIMESTEPS]
        # TODO: This is just a fast fix for now. Change this once structure is
        #       finished (remove check for hasattr etc.)
            if isinstance(node, Storage):
                result[node] = result.get(node, UserDict())
                if hasattr(self.Storage, 'capacity'):
                    value = [
                        self.Storage.capacity[node, t].value
                             for t in self.TIMESTEPS]
                else:
                    value = [
                        self.InvestmentStorage.capacity[node, t].value
                            for t in self.TIMESTEPS]
                result[node][node] = value


        # TO
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

###############################################################################
#
# Solph grouping functions
#
###############################################################################
def constraint_grouping(node):
    if isinstance(node, on.Bus):
        return blocks.Bus
    if isinstance(node, LinearTransformer):
        return blocks.LinearTransformer
    if isinstance(node, Storage) and isinstance(node.investment, Investment):
        return blocks.InvestmentStorage
    if isinstance(node, Storage):
        return blocks.Storage


def investment_key(n):
    for f in n.outputs.values():
        if f.investment is not None:
            return blocks.InvestmentFlow

def investment_flows(n):
    return set(chain( ((n, t, f) for (t, f) in n.outputs.items()
                                 if f.investment is not None),
                      ((s, n, f) for (s, f) in n.inputs.items()
                                 if f.investment is not None)))

def merge_investment_flows(n, group):
    return group.union(n)

investment_flow_grouping = oces.Grouping(
    key=investment_key,
    value=investment_flows,
    merge=merge_investment_flows)

def standard_flow_key(n):
    for f in n.outputs.values():
        if f.investment is None:
            return blocks.Flow

def standard_flows(n):
    return [(n, t, f) for (t, f) in n.outputs.items()
            if f.investment is None]

def merge_standard_flows(n, group):
    group.extend(n)
    return group

standard_flow_grouping = oces.Grouping(
    key=standard_flow_key,
    value=standard_flows,
    merge=merge_standard_flows)

GROUPINGS = [constraint_grouping, investment_flow_grouping,
             standard_flow_grouping]

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
