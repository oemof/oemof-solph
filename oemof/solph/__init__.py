"""


"""
from collections import abc, UserList

import pyomo.environ as pyomo
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality
import oemof.network as on
from oemof.solph import constraints as cblocks

###############################################################################
#
# Functions
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
# Classes
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
    """
    def __init__(self, *args, **kwargs):
        # TODO: Check if we can inherit form pyomo.core.base.var _VarData
        # then we need to create the var object with
        # pyomo.core.base.IndexedVarWithDomain before any Flow is created.
        # E.g. create the variable in the energy system and populate with
        # information afterwards when creating objects.

        self.nominal_value = kwargs.get('nominal_value')
        self.min = Sequence(kwargs.get('min', 0))
        self.max = Sequence(kwargs.get('max', 1))
        self.actual_value = Sequence(kwargs.get('actual_value'))
        self.variable_costs = Sequence(kwargs.get('variable_costs', 999))
        self.fixed_costs = kwargs.get('fixed_costs')
        self.summed = kwargs.get('summed')
        self.fixed = kwargs.get('fixed', False)



# TODO: create solph sepcific energysystem subclassed from core energy system
class EnergySystem:
    """
    """
    def __init__(self, *args, **kwargs):

        super().__init__( *args, **kwargs)
        #self.flow_var = IndexedVarWithDomain()
        self.timeindex = kwargs.get('timeindex')
        self.increment = kwargs.get('increment', 1)


Bus = on.Bus


class Investment:
    """
    """
    def __init__(self, maximum=float('+inf')):
        self.maximum = maximum


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
            for k,v in kwargs.get('conversion_factors', {}).items()}


class Storage(on.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nominal_capacity = kwargs.get('nominal_capacity')
        self.initial_capacity = kwargs.get('initial_capacity', 0)
        self.capacity_loss = kwargs.get('capacity_loss', 0)
        self.nominal_input_capacity_ratio = kwargs.get(
            'nominal_input_capacity_ratio', 0.2)
        self.nominal_output_capacity_ratio = kwargs.get(
            'nominal_input_capacity_ratio', 0.2)
        self.inflow_conversion_factor = kwargs.get(
            'inflow_conversion_factor', 1)
        self.outflow_conversion_factor = kwargs.get(
            'outflow_conversion_factor', 1)


###############################################################################
#
# Solph Optimization Models
#
###############################################################################

# TODO: Create Investment model
class ExpansionModel(pyomo.ConcreteModel):
    """ An energy system model for optimized capacity expansion.
    """
    def __init__(self, es):
        super().__init__()

        self.es = es

        self.time_increment = 1

        self.periods = 1

        # edges dictionary with tuples as keys and non investment flows as
        # values
        self.non_investment_flows = {
                (str(source), str(target)): source.outputs[target]
                    for source in es.nodes
                    for target in source.outputs
                    if not getattr(source.outputs[target], "investment", False)
                }


class OperationalModel(pyomo.ConcreteModel):
    """ An energy system model for operational simulation with optimized
    distpatch.

    Parameters
    ----------

    es : EnergySystem object
    constraint_groups: list
        Solph looks for these groups in the given energy system and uses them
        to create the constraints of the optimization problem.
        Defaults to :const:`OperationalModel.CONSTRAINTS`
    objective_groups:
        Solph looks for these groups in the given energy system and uses them
        to create the objective expression.
        Defaults to :const:`OperationalModel.OBJECTIVES`

    objective_groups:
        Solph looks for these groups in the given energy system and uses them
        to create the objective expression.
        Defaults to :const:`OperationalModel.OBJECTIVES`
    """


    CONSTRAINT_GROUPS = [cblocks.BusBalance, cblocks.LinearRelation]
    OBJECTIVE_GROUPS = [cblocks.outflowcosts]


    def __init__(self, es, *args, **kwargs):

        super().__init__()


        # name of the optimization model
        self.name = 'OperationalModel'

        constraint_groups = kwargs.get('constraint_groups',
                                       OperationalModel.CONSTRAINT_GROUPS)
        objective_groups = kwargs.get('objective_groups',
                                      OperationalModel.OBJECTIVE_GROUPS)

        # TODO : move time-increment to energy system class
        # specified time_increment (time-step width)
        self.time_increment = 2

        self.es = es
        # TODO: Move code below somewhere to grouping in energysystem class (@gnn)
        # remove None key from dictionary to avoid errors
        self.es.groups = {k: v for k, v in self.es.groups.items()
                          if k is not None}

        self.flows = {(str(source), str(target)): source.outputs[target]
                      for source in es.nodes
                      for target in source.outputs}

        # set with all components
        self.COMPONENTS = pyomo.Set(initialize=[str(n)
                                                for n in self.es.nodes])

        # indexed index set for inputs of components (components as indices)
        self.INPUTS = pyomo.Set(self.COMPONENTS, initialize={
            str(c): [str(i) for i in c.inputs.keys()]
                     for c in self.es.nodes if not isinstance(c, on.Source)
            }
        )

        # indexed index set for outputs of components (components as indices)
        self.OUTPUTS = pyomo.Set(self.COMPONENTS, initialize={
            str(c): [str(o) for o in c.outputs.keys()]
                     for c in self.es.nodes if not isinstance(c, on.Sink)
            }
        )


        # pyomo set for timesteps of optimization problem
        self.TIMESTEPS = pyomo.Set(initialize=range(len(es.time_idx)),
                                   ordered=True)

        # pyomo set for all flows in the energy system graph
        self.FLOWS = pyomo.Set(initialize=self.flows.keys(),
                               ordered=True, dimen=2)

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


        # loop over all constraint groups to add constraints to the model
        for group in constraint_groups:
            # create instance for block
            block = group()
            # add block to model
            self.add_component(str(group), block)
            # create constraints etc. related with block for all nodes
            # in the group
            block._create(nodes=self.es.groups[group])


        # loop over all objective groups to add objective exprs to objective

        self.add_objective(groups=objective_groups)


    def add_objective(self, groups, sense=pyomo.minimize,
                      name='objective'):
        """
        """
        setattr(self, name, pyomo.Objective(sense=sense, expr=0))

        for group in groups:
             self.objective.expr += group(self, self.es.groups.get(group))



        # This is for integer problems, migth be usefull but can be moved somewhere else
        # Ignore this!!!
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
# TODO: Make investment grouping work with (node does not hold 'investment' but the flows do)
def investment_grouping(node):
    if hasattr(node, "investment"):
        return Investment

def constraint_grouping(node):
    if isinstance(node, on.Bus) and 'el' in str(node):
        return cblocks.BusBalance
    if isinstance(node, on.Transformer):
        return cblocks.LinearRelation

def objective_grouping(node):
    if isinstance(node, on.Transformer):
        return cblocks.outflowcosts

GROUPINGS = [constraint_grouping, investment_grouping, objective_grouping]
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

    es = oces.EnergySystem(groupings=[constraint_grouping, objective_grouping],
                           time_idx=[1,2,3])

    lt = len(es.time_idx)

    bel = Bus(label="el")
    # TODO: Resolve error by 'unsused' busses??
    #bth = Bus(label="th")

    bcoal = Bus(label="coalbus")

    so = Source(label="coalsource",
                outputs={bcoal: Flow()})

    wind = Source(label="wind", outputs={bel:Flow(actual_value=[1,3,10],
                                                  nominal_value=10,
                                                  fixed=True)})

    si = Sink(label="sink", inputs={bel: Flow(max=[0.1, 0.2, 0.9],
                                              nominal_value=10, fixed=True,
                                              actual_value=[1, 2, 3])})

    trsf = LinearTransformer(label='trsf', inputs={bcoal:Flow()},
                             outputs={bel:Flow(nominal_value=10),
                                      bcoal:Flow(min=[0.5, 0.4, 0.4],
                                                 max=[1, 1, 1],
                                                 nominal_value=30)},
                             conversion_factors={bel: _Sequence(default=0.4),
                                                 bcoal:  _Sequence(default=0.5)})

    om = OperationalModel(es)

    om.pprint()



