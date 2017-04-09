# -*- coding: utf-8 -*-
"""Optional classes to be added to a network class.
"""


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
