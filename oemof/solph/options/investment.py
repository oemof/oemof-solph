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
