"""
The solph-package contains funtionalities for creating and solving an
optimizaton problem. The problem is created from oemof base classes.
Solph depends on pyomo.

"""
import oemof.network as on



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
        super().__init__()
        self.investment = kwargs.get('investment')

class Source(on.Source):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.investment = kwargs.get('investment')


class LinearTransformer(on.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.conversion_factors = kwargs.get('conversion_factors')
        self.investment = kwargs.get('investment')


class Storage(on.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.nominal_capacity = kwargs.get('nominal_capacity')
        self.maximum_nominal_capacity = kwargs.get('maximum_nominal_capacity')
        self.initial_capacity = kwargs.get('initial_capacity', 0)
        self.capacity_loss = kwargs.get('capacity_loss', 0)
        self.nominal_input_capacity_ratio = kwargs.get('nominal_input_capacity_ratio', 0.2)
        self.nominal_output_capacity_ratio = kwargs.get('nominal_input_capacity_ratio', 0.2)
        self.inflow_conversion_factor = kwargs.get('inflow_conversion_factor', 1)
        self.outflow_conversion_factor = kwargs.get('outflow_conversion_factor', 1)
        self.investment = kwargs.get('investment')

if __name__ == "__main__":

    b = Bus(label="el")

    so = Source(outputs={b: Flow(actual_value=[10, 5, 10], fixed=True)},
               investement=Investment(maximum=1000))
    si = Sink(inputs={b: Flow(min=[0,0,0], max=[0.1, 0.2, 0.9],
                             nominal_value=10, fixed=True)})

