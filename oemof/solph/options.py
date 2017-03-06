# -*- coding: utf-8 -*-
"""Optional classes to be added to a network class.
"""


class Investment:
    """
    Parameters
    ----------
    maximum : float
        Maximum of the additional invested capacity
    minimum : float
        Minimum of the addtional invested capacity
    ep_costs : float
        Equivalent periodical costs for the investment, if period is one
        year these costs are equal to the equivalent annual costs.

    """
    def __init__(self, maximum=float('+inf'), minimum=0, ep_costs=0):
        self.maximum = maximum
        self.minimum = minimum
        self.ep_costs = ep_costs


class BinaryFlow:
    """
    Parameters
    ----------
    startup_costs : numeric
        Costs associated with a start of the flow (representing a unit).
    shutdown_costs : numeric
        Costs associated with the shutdown of the flow (representing a until).
    minimum_uptime : numeric
        Minimum time that a flow must be greater then its minimum flow after
        startup.
    minimum_downtime : numeric
        Minimum time a flow is forced to zero after shutting down.
    initial_status : numeric (0 or 1)
        Integer value indicating the status of the flow in the first time step
        (0 = off, 1 = on).
    """
    def __init__(self, **kwargs):
        # super().__init__(self, **kwargs)
        self.startup_costs = kwargs.get('startup_costs')
        self.shutdown_costs = kwargs.get('shutdown_costs')
        self.minimum_uptime = kwargs.get('minimum_uptime')
        self.minimum_downtime = kwargs.get('minimum_downtime')
        self.initial_status = kwargs.get('initial_status', 0)


class DiscreteFlow:
    """
    Parameters
    ----------
    integers : boolean
        Specify domain of flow variable: If True, flow is forced to integer
        values.
    """
    def __init__(self, **kwargs):
        # super().__init__(self, **kwargs)
        self.integers = kwargs.get('integers', True)
