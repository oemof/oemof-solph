# -*- coding: utf-8 -*-

"""Optional classes to be added to a network class.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: jmloenneberga

SPDX-License-Identifier: MIT

"""

from oemof.solph._plumbing import sequence


class Investment:
    """Defines an Investment object holding all the specifications needed
    for investment modeling.

    Parameters
    ----------
    maximum : float, :math:`P_{invest,max}` or :math:`E_{invest,max}`
        Maximum of the additional invested capacity
    minimum : float, :math:`P_{invest,min}` or :math:`E_{invest,min}`
        Minimum of the additional invested capacity. If `nonconvex` is `True`,
        `minimum` defines the threshold for the invested capacity.
    ep_costs : float, :math:`c_{invest,var}`
        Equivalent periodical costs for the investment per flow capacity.
    existing : float, :math:`P_{exist}` or :math:`E_{exist}`
        Existing / installed capacity. The invested capacity is added on top
        of this value. Not applicable if `nonconvex` is set to `True`.
    nonconvex : bool
        If `True`, a binary variable for the status of the investment is
        created. This enables additional fix investment costs (*offset*)
        independent of the invested flow capacity. Therefore, use the `offset`
        parameter.
    offset : float, :math:`c_{invest,fix}`
        Additional fix investment costs. Only applicable if `nonconvex` is set
        to `True`.


    For the variables, constraints and parts of the objective function, which
    are created, see
    :py:class:`~oemof.solph.blocks.investment_flow.InvestmentFlow`,
    :py:class:`~oemof.solph.components.generic_storage.GenericInvestmentStorageBlock`
    :py:class:`~oemof.solph.custom.sink_dsm.SinkDSMOemofInvestmentBlock`,
    :py:class:`~oemof.solph.custom.sink_dsm.SinkDSMDLRInvestmentBlock` and
    :py:class:`~oemof.solph.custom.sink_dsm.SinkDSMDIWInvestmentBlock`.

    """  # noqa: E501

    def __init__(
        self,
        maximum=float("+inf"),
        minimum=0,
        ep_costs=0,
        existing=0,
        nonconvex=False,
        offset=0,
        custom_attributes=None,
    ):
        if custom_attributes is None:
            custom_attributes = {}
        self.maximum = maximum
        self.minimum = minimum
        self.ep_costs = ep_costs
        self.existing = existing
        self.nonconvex = nonconvex
        self.offset = offset

        for attribute in custom_attributes.keys():
            value = custom_attributes.get(attribute)
            setattr(self, attribute, value)

        self._check_invest_attributes()
        self._check_invest_attributes_maximum()
        self._check_invest_attributes_offset()

    def _check_invest_attributes(self):
        if (self.existing != 0) and (self.nonconvex is True):
            e1 = (
                "Values for 'offset' and 'existing' are given in"
                " investement attributes. \n These two options cannot be "
                "considered at the same time."
            )
            raise AttributeError(e1)

    def _check_invest_attributes_maximum(self):
        if (self.maximum == float("+inf")) and (self.nonconvex is True):
            e2 = (
                "Please provide an maximum investment value in case of"
                " nonconvex investemnt (nonconvex=True), which is in the"
                " expected magnitude."
                " \nVery high maximum values (> 10e8) as maximum investment"
                " limit might lead to numeric issues, so that no investment"
                " is done, although it is the optimal solution!"
            )
            raise AttributeError(e2)

    def _check_invest_attributes_offset(self):
        if (self.offset != 0) and (self.nonconvex is False):
            e3 = (
                "If `nonconvex` is `False`, the `offset` parameter will be"
                " ignored."
            )
            raise AttributeError(e3)


class NonConvex:
    """Defines a NonConvex object holding all the specifications for NonConvex
    Flows, i.e. Flows with binary variables associated to them.

    Parameters
    ----------
    startup_costs : numeric (iterable or scalar)
        Costs associated with a start of the flow (representing a unit).
    shutdown_costs : numeric (iterable or scalar)
        Costs associated with the shutdown of the flow (representing a unit).
    activity_costs : numeric (iterable or scalar)
        Costs associated with the active operation of the flow, independently
        from the actual output.
    inactivity_costs : numeric (iterable or scalar)
        Costs associated with not operating the flow.
    minimum_uptime : numeric (1 or positive integer)
        Minimum time that a flow must be greater then its minimum flow after
        startup. Be aware that minimum up and downtimes can contradict each
        other and may lead to infeasible problems.
    minimum_downtime : numeric (1 or positive integer)
        Minimum time a flow is forced to zero after shutting down.
        Be aware that minimum up and downtimes can contradict each
        other and may to infeasible problems.
    maximum_startups : numeric (0 or positive integer)
        Maximum number of start-ups in the optimization timeframe.
    maximum_shutdowns : numeric (0 or positive integer)
        Maximum number of shutdowns in the optimization timeframe.
    initial_status : numeric (0 or 1)
        Integer value indicating the status of the flow in the first time step
        (0 = off, 1 = on). For minimum up and downtimes, the initial status
        is set for the respective values in the edge regions e.g. if a
        minimum uptime of four timesteps is defined, the initial status is
        fixed for the four first and last timesteps of the optimization period.
        If both, up and downtimes are defined, the initial status is set for
        the maximum of both e.g. for six timesteps if a minimum downtime of
        six timesteps is defined in addition to a four timestep minimum uptime.
    negative_gradient_limit : numeric (iterable, scalar or None)
        the normed *upper bound* on the positive difference
        (`flow[t-1] < flow[t]`) of two consecutive flow values.
    positive_gradient_limit : numeric (iterable, scalar or None)
            the normed *upper bound* on the negative difference
            (`flow[t-1] > flow[t]`) of two consecutive flow values.
    """

    def __init__(
        self,
        initial_status=0,
        minimum_uptime=0,
        minimum_downtime=0,
        maximum_startups=None,
        maximum_shutdowns=None,
        startup_costs=None,
        shutdown_costs=None,
        activity_costs=None,
        inactivity_costs=None,
        negative_gradient_limit=None,
        positive_gradient_limit=None,
        custom_attributes=None,
    ):
        if custom_attributes is None:
            custom_attributes = {}

        self.initial_status = initial_status
        self.minimum_uptime = minimum_uptime
        self.minimum_downtime = minimum_downtime
        self.maximum_startups = maximum_startups
        self.maximum_shutdowns = maximum_shutdowns

        self.startup_costs = sequence(startup_costs)
        self.shutdown_costs = sequence(shutdown_costs)
        self.activity_costs = sequence(activity_costs)
        self.inactivity_costs = sequence(inactivity_costs)
        self.negative_gradient_limit = sequence(negative_gradient_limit)
        self.positive_gradient_limit = sequence(positive_gradient_limit)

        for attribute, value in custom_attributes.items():
            setattr(self, attribute, value)

        self._max_up_down = None

    @property
    def max_up_down(self):
        """Return maximum of minimum_uptime and minimum_downtime.

        The maximum of both is used to set the initial status for this
        number of time steps within the edge regions.
        """

        return max(self.minimum_uptime, self.minimum_downtime)
