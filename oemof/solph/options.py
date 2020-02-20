# -*- coding: utf-8 -*-

"""Optional classes to be added to a network class.
This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/options.py

SPDX-License-Identifier: MIT
"""

from oemof.solph.plumbing import sequence


class Investment:
    """
    Parameters
    ----------
    maximum : float
        Maximum of the additional invested capacity
    minimum : float
        Minimum of the additional invested capacity
    ep_costs : float
        Equivalent periodical costs for the investment, if period is one
        year these costs are equal to the equivalent annual costs.
    existing : float
        Existing / installed capacity. The invested capacity is added on top
        of this value.

    """
    def __init__(self, maximum=float('+inf'), minimum=0, ep_costs=0,
                 existing=0):
        self.maximum = maximum
        self.minimum = minimum
        self.ep_costs = ep_costs
        self.existing = existing


class NonConvex:
    """
    Parameters
    ----------
    startup_costs : numeric (sequence or scalar)
        Costs associated with a start of the flow (representing a unit).
    shutdown_costs : numeric (sequence or scalar)
        Costs associated with the shutdown of the flow (representing a unit).
    activity_costs : numeric (sequence or scalar)
        Costs associated with the active operation of the flow, independently
        from the actual output.
    minimum_uptime : numeric (1 or positive integer)
        Minimum time that a flow must be greater then its minimum flow after
        startup. Be aware that minimum up and downtimes can contradict each
        other and may lead to infeasible problems.
    minimum_downtime : numeric (1 or positive integer)
        Minimum time a flow is forced to zero after shutting down.
        Be aware that minimum up and downtimes can contradict each
        other and may to infeasible problems.
    maximum_startups : numeric (0 or positive integer)
        Maximum number of start-ups.
    maximum_shutdowns : numeric (0 or positive integer)
        Maximum number of shutdowns.
    initial_status : numeric (0 or 1)
        Integer value indicating the status of the flow in the first time step
        (0 = off, 1 = on). For minimum up and downtimes, the initial status
        is set for the respective values in the edge regions e.g. if a
        minimum uptime of four timesteps is defined, the initial status is
        fixed for the four first and last timesteps of the optimization period.
        If both, up and downtimes are defined, the initial status is set for
        the maximum of both e.g. for six timesteps if a minimum downtime of
        six timesteps is defined in addition to a four timestep minimum uptime.
    """
    def __init__(self, **kwargs):
        scalars = ['minimum_uptime', 'minimum_downtime', 'initial_status',
                   'maximum_startups', 'maximum_shutdowns']
        sequences = ['startup_costs', 'shutdown_costs', 'activity_costs']
        defaults = {'initial_status': 0}

        for attribute in set(scalars + sequences + list(kwargs)):
            value = kwargs.get(attribute, defaults.get(attribute))
            setattr(self, attribute,
                    sequence(value) if attribute in sequences else value)

        self._max_up_down = None

    def _calculate_max_up_down(self):
        """
        Calculate maximum of up and downtime for direct usage in constraints.

        The maximum of both is used to set the initial status for this
        number of timesteps within the edge regions.
        """
        if self.minimum_uptime is not None and self.minimum_downtime is None:
            max_up_down = self.minimum_uptime
        elif self.minimum_uptime is None and self.minimum_downtime is not None:
            max_up_down = self.minimum_downtime
        else:
            max_up_down = max(self.minimum_uptime, self.minimum_downtime)

        self._max_up_down = max_up_down

    @property
    def max_up_down(self):
        """Compute or return the _max_up_down attribute."""
        if self._max_up_down is None:
            self._calculate_max_up_down()

        return self._max_up_down
