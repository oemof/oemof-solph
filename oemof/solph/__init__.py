"""
The solph-package contains funtionalities for creating and solving an
optimizaton problem. The problem is created from oemof base classes.
Solph depend on pyomo.

"""

class Flow:
    def __init__(self, actual_value, nominal_value, variable_costs, min, max,
                 fixed_costs, summed_min, summed_max):
        """

        """
        self.min = min
        self.max = max
        self.actual_value = actual_value
        self.nominal_value = nominal_value
        self.variable_costs =  variable_costs
        self.fixed_costs = fixed_costs
        self.summed_min = summed_min
        self.summed_max =  summed_min