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
        Mininm of the addtional invested capacity
    ep_costs : float
        Equivalent periodical costs for the investment, if period is one
        year these costs are equal to the equivalent annual costs.
    invest_costs : float
        Specific investmet costs, if ep_cost are to be calculated
        (do not set 'ep_costs' then)
    wacc : float
        Weighted average cost of capital to be used in ep_costs calculation
    lifetime : float
        Lifetime of component/flow investment to be used in ep_costs
        calculation

    """
    def __init__(self, maximum=float('+inf'), minimum=0, invest_costs=None,
                 ep_costs=None, wacc=0.08, lifetime=20):
        self.maximum = maximum
        self.minimum = minimum
        self.wacc = wacc
        self.lifetime = lifetime
        self.invest_costs = invest_costs
        self.ep_costs = ep_costs
        self._calc_ep_costs()

    def _calc_ep_costs(self):
        """
        """
        if self.invest_costs is None:
            if self.ep_costs is None:
                self.ep_costs = 0
        else:
            if self.ep_costs is None:
                self.ep_costs = (self.invest_costs *
                    (self.wacc * (1 + self.wacc) ** self.lifetime) /
                        ((1 + self.wacc) ** self.lifetime - 1))
            else:
                logging.info('Attribute ep_costs already set.' +
            'Recalculating ep_costs based on invest_costs, wacc and lifetime!')
                self.ep_costs = (self.invest_costs *
                    (self.wacc * (1 + self.wacc) ** self.lifetime) /
                        ((1 + self.wacc) ** self.lifetime - 1))


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
        Specify domain of flow variable: If True, flow is force to integer
        values.
    """
    def __init__(self, **kwargs):
        # super().__init__(self, **kwargs)
        self.integers = kwargs.get('integers', True)
