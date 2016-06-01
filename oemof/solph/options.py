# -*- coding: utf-8 -*-
"""

"""

class Investment:
    """
    Parameters
    ----------
    maximum : float
        Maximum of the additional invested capacity
    ep_costs : float
        Equivalent periodical costs for the investment, if period is one
        year these costs are equal to the equivalent annual costs.

    """
    def __init__(self, maximum=float('+inf'), ep_costs=None):
        self.maximum = maximum
        self.ep_costs = ep_costs

class Discrete:
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_costs = kwargs.get('start_costs')
        self.minimum_uptime = kwargs.get('minimum_uptime')
        self.minimum_downtime = kwargs.get('minimum_downtime')