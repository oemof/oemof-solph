"""
The solph-package contains funtionalities for creating and solving an
optimizaton problem. The problem is created from oemof base classes.
Solph depends on pyomo.

"""
import pyomo.environ as pyomo
import oemof.network as on


###############################################################################
#
# Classes
#
###############################################################################

class Flow:
    def __init__(self, *args, **kwargs):
        """
        """
        self.min = kwargs.get('nominal_value')
        self.max = kwargs.get('variable_costs')
        self.actual_value = kwargs.get('actual_value')
        self.nominal_value = kwargs.get('nominal_value')
        self.variable_costs =  kwargs.get('variable_costs')
        self.fixed_costs = kwargs.get('fixed_costs')
        self.summed = kwargs.get('summed')
        self.fixed = kwargs.get('fixed')


# TODO: create solph sepcific energysystem subclassed from core energy system
class EnergySystem:

    def __init__(self):
        """
        """
        pass

# import bus
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
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factors = kwargs.get('conversion_factors')



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
# Solph Optimization Model
#
###############################################################################

class OptimizationModel(pyomo.ConcreteModel):
    """ Creates Pyomo model of the energy system.

    Parameters
    ----------
    es : object of Solph - EnergySystem Class


    """
    def __init__(self, es):
        super().__init__()

        self.es = es

        self.relaxed = getattr(es.simulation, "relaxed", False)

        def is_investment_flow(source, target):
            component = next(filter( lambda x: not isinstance(Bus, x),
                                     (source, target)))
            return getattr(component, "investment", False)

        # edges dictionary with tuples as keys and flows as values
        self.non_investment_flows = {
                (str(source), str(target)): source.outputs[target]
                for source in es.nodes
                for target in source.outputs
                if not is_investment_flow(source, target) }

        # pyomo Set for all edges as tuples
        self.FLOWS = pyomo.Set(initialize=self.flows.keys, ordered=True)

        #
        self.investment_flows = {
                (str(source), str(target)): source.outputs[target]
                for source in es.nodes
                for target in source.outputs
                if is_investment_flow(source, target) }

        #
        if self.investment_flows:
            self.INVESTMENT_FLOWS = pyomo.Set(
                initialize=self.investment_flows.keys(), ordered=True)

        # pyomo set for timesteps of optimization problem
        self.TIMESTEPS = pyomo.Set(initialize=es.time_index.values,
                                   ordered=True)

        # non-negative pyomo variable for all existing flows in energysystem
        self.flow = pyomo.Var(self.FLOWS, self.TIMESTEPS,
                              within=pyomo.NonNegativeReals)

        for (o, i) in self.FLOWS:
            for t in self.TIMESTEPS:
                # upper bound of flow variable
                self.flow[o, i, t].set_lb(self.flows[o, i].max[t] *
                                          self.flows[o, i].nominal_value)
                # lower bound of flow variable
                self.flow[o, i, t].set_ub(self.flows[o, i].min[t] *
                                          self.flows[o, i].nominal_value)
                # pre - optimizide value of flow
                self.flow[o, i, t].value = self.flows[o, i].actual_value[t]

                # fix variable if flow is fixed
                if self.flows[o, i].fix:
                     self.flow[o, i, t].fix()


        def _investment_bounds(self, o, i):
            return (0, self.flows[o, i].investment.maximum)

        self.investment = pyomo.Var(self.INVESTMENT_FLOWS,
                                    bounds=_investment_bounds,
                                    within=pyomo.NonNegativeReals)

        def _summed_flow_limit(self, o, i):
            """ pyomo rule
            """
            return (
                sum(self.flow[o, i, t] for t in self.TIMESTEPS)
                    <= self.flows[o, i].summed
            )
        self.summed_flow_limit = pyomo.Constraint(self.FLOWS,
                                                  rule=_summed_flow_limit)



###############################################################################
#
# Solph grouping functions
#
###############################################################################

def investment_grouping(node):
    if hasattr(node, "investment"):
        return Investment
    return None


subsets = [investment_grouping]


if __name__ == "__main__":

    b = Bus(label="el")

    so = Source(outputs={b: Flow(actual_value=[10, 5, 10], fixed=True, investment=Investment(maximum=1000))},
               )
    si = Sink(inputs={b: Flow(min=[0,0,0], max=[0.1, 0.2, 0.9],
                             nominal_value=10, fixed=True)})

