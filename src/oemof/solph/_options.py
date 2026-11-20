# -*- coding: utf-8 -*-

"""Optional classes to be added to a network class.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Malte Fritz
SPDX-FileCopyrightText: Jonas Freißmann

SPDX-License-Identifier: MIT

"""

from warnings import warn

from oemof.tools import debugging

from oemof.solph._plumbing import sequence


class Investment:
    """Defines an Investment object holding all the specifications needed
    for investment modeling.

    Parameters
    ----------
    maximum : float, :math:`P_{invest,max}(p)` or :math:`E_{invest,max}(p)`
        Maximum of the additional invested capacity;
        defined per period p for a multi-period model.
    minimum : float, :math:`P_{invest,min}(p)` or :math:`E_{invest,min}(p)`
        Minimum of the additional invested capacity. If `nonconvex` is `True`,
        `minimum` defines the threshold for the invested capacity;
        defined per period p for a multi-period model.
    ep_costs : float, :math:`c_{invest,var}`
        Equivalent periodical costs or investment expenses for the investment
        per flow or storage capacity, i.e. annuities for investments already
        calculated.
    existing : float, :math:`P_{exist}` or :math:`E_{exist}`
        Existing / installed capacity. The invested capacity is added on top
        of this value. Hence, existing capacities come at no additional costs.
        Not applicable if `nonconvex` is set to `True`.
    nonconvex : bool
        If `True`, a binary variable for the status of the investment is
        created. This enables additional fix investment costs (*offset*)
        independent of the invested flow capacity. Therefore, use the `offset`
        parameter.
    offset : float, :math:`c_{invest,fix}`
        Additional fixed investment costs. Only applicable if `nonconvex` is
        set to `True`.
    lifetime : int, :math:`l` (experimental)
        Lifetime of newly invested capacity (given capacity periods)


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
        lifetime=None,
        custom_attributes=None,  # To be removed for versions >= v0.7
        custom_properties=None,
    ):
        # --- BEGIN: The following code can be removed for versions >= v0.7 ---
        if custom_attributes is not None:
            msg = (
                "For backward compatibility,"
                + " the option custom_attributes overwrites the option"
                + " custom_properties."
                + " Both options cannot be set at the same time."
            )
            if custom_properties is not None:
                raise AttributeError(msg)
            else:
                warn(msg, FutureWarning)
            for attribute in custom_attributes.keys():
                value = custom_attributes.get(attribute)
                setattr(self, attribute, value)

            custom_properties = custom_attributes
        # --- END ---
        self.custom_properties = custom_properties
        self.maximum = maximum
        self.minimum = minimum
        self.ep_costs = ep_costs
        self.existing = existing
        self.nonconvex = nonconvex
        self.offset = offset
        self.lifetime = lifetime

        self._check_invest_attributes()
        self._check_invest_attributes_maximum()
        self._check_invest_attributes_offset()
        self._check_invest_attributes_nonconvex()
        self._check_nonconvex()

    @property
    def ep_costs(self):
        return self._ep_costs

    @ep_costs.setter
    def ep_costs(self, value):
        self._ep_costs = sequence(value)

    @property
    def existing(self):
        return self._existing

    @existing.setter
    def existing(self, value):
        self._existing = sequence(value)

    @property
    def maximum(self):
        return self._maximum

    @maximum.setter
    def maximum(self, value):
        self._maximum = sequence(value)

    @property
    def minimum(self):
        return self._minimum

    @minimum.setter
    def minimum(self, value):
        self._minimum = sequence(value)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = sequence(value)

    @property
    def lifetime(self):
        return self._lifetime

    @lifetime.setter
    def lifetime(self, value):
        self._lifetime = sequence(value)

    def relevant_periods(
        self,
        period: int,
    ) -> list[int]:
        rv = []
        for p in range(period):
            if not self.lifetime or self.lifetime[p] + p > period:
                rv.append(p)
        rv.append(period)
        return rv

    def _check_invest_attributes(self):
        """Throw an error if existing is other than 0 and nonconvex is True"""
        if (self.existing != 0) and (self.nonconvex is True):
            e1 = (
                "Values for 'offset' and 'existing' are given in"
                " investement attributes. \n These two options cannot be "
                "considered at the same time."
            )
            raise AttributeError(e1)

    def _check_invest_attributes_maximum(self):
        """Throw an error if maximum is infinite and nonconvex is True"""
        if (self.maximum[0] == float("+inf")) and (self.nonconvex is True):
            e2 = (
                "Please provide a maximum investment value in case of"
                " nonconvex investment (nonconvex=True), which is in the"
                " expected magnitude."
                " \nVery high maximum values (> 10e8) as maximum investment"
                " limit might lead to numeric issues, so that no investment"
                " is done, although it is the optimal solution!"
            )
            raise AttributeError(e2)

    def _check_invest_attributes_offset(self):
        """Throw an error if offset is given without nonconvex=True"""
        if (self.offset[0] != 0) and (self.nonconvex is False):
            e3 = (
                "If `nonconvex` is `False`, the `offset` parameter will be"
                " ignored."
            )
            raise AttributeError(e3)

    def _check_invest_attributes_nonconvex(self):
        """Throw an error if nonconvex is not of type boolean."""
        if not isinstance(self.nonconvex, bool):
            e5 = (
                "The `nonconvex` parameter of the `Investment` class has to be"
                + f" of type boolean, not {type(self.nonconvex)}."
            )
            raise AttributeError(e5)

    def _check_nonconvex(self):
        """Checking for unnecessary setting of nonconvex"""
        if self.nonconvex:
            if (self.minimum.min() == 0) and (self.offset.min() == 0):
                msg = (
                    "It is not necessary to set the investment to `nonconvex` "
                    "if `minimum` and `offset` are 0.\n"
                    "This can lead to the `invest_status` variable becoming "
                    "1, even if the `nominal_capacity` is optimized to 0."
                )
                warn(msg, debugging.SuspiciousUsageWarning)


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
    minimum_uptime : numeric or list of numeric (1 or positive integer)
        Minimum number of time steps that a flow must be greater then its
        minimum flow after startup. Be aware that minimum up and downtimes
        can contradict each other and may lead to infeasible problems.
    minimum_downtime : numeric or list of numeric (1 or positive integer)
        Minimum number of time steps a flow is forced to zero after
        shutting down. Be aware that minimum up and downtimes can
        contradict each other and may to infeasible problems.
    maximum_startups : numeric (0 or positive integer)
        Maximum number of start-ups in the optimization timeframe.
    maximum_shutdowns : numeric (0 or positive integer)
        Maximum number of shutdowns in the optimization timeframe.
    initial_status : numeric (0 or 1)
        Integer value indicating the status of the flow in the first time step
        (0 = off, 1 = on). For minimum up and downtimes, the initial status
        is set for the respective values in the beginning e.g. if a
        minimum uptime of four timesteps is defined and the initial status is
        set to one, the initial status is fixed for the four first timesteps
        of the optimization period. Otherwise if the initial status is set to
        zero and the first timesteps are fixed for the number of minimum
        downtime steps.
    negative_gradient_limit : numeric (iterable, scalar or None)
        the normed *upper bound* on the decrease
        (`flow[t-1] > flow[t]`) of two consecutive flow values while the
        flow stays on. A shut-down is possible from the larger of this
        limit and the minimum load.
    positive_gradient_limit : numeric (iterable, scalar or None)
        the normed *upper bound* on the increase
        (`flow[t-1] < flow[t]`) of two consecutive flow values while the
        flow stays on. A start-up can reach the larger of this limit and
        the minimum load.
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
        custom_attributes=None,  # To be removed for versions >= v0.7
        custom_properties=None,
    ):
        # --- BEGIN: The following code can be removed for versions >= v0.7 ---
        if custom_attributes is not None:
            msg = (
                "For backward compatibility,"
                + " the option custom_attributes overwrites the option"
                + " custom_properties."
                + " Both options cannot be set at the same time."
            )
            if custom_properties is not None:
                raise AttributeError(msg)
            else:
                warn(msg, FutureWarning)
            for attribute in custom_attributes.keys():
                value = custom_attributes.get(attribute)
                setattr(self, attribute, value)

            custom_properties = custom_attributes
        # --- END ---
        self.custom_properties = custom_properties

        self.initial_status = initial_status
        self.minimum_uptime = minimum_uptime
        self.minimum_downtime = minimum_downtime
        self.maximum_startups = maximum_startups
        self.maximum_shutdowns = maximum_shutdowns

        self.startup_costs = startup_costs
        self.shutdown_costs = shutdown_costs
        self.activity_costs = activity_costs
        self.inactivity_costs = inactivity_costs
        self.negative_gradient_limit = negative_gradient_limit
        self.positive_gradient_limit = positive_gradient_limit

        if initial_status == 0:
            self.first_flexible_timestep = self.minimum_downtime[0]
        else:
            self.first_flexible_timestep = self.minimum_uptime[0]

    @property
    def activity_costs(self):
        return self._activity_costs

    @activity_costs.setter
    def activity_costs(self, value):
        self._activity_costs = sequence(value)

    @property
    def inactivity_costs(self):
        return self._inactivity_costs

    @inactivity_costs.setter
    def inactivity_costs(self, value):
        self._inactivity_costs = sequence(value)

    @property
    def minimum_downtime(self):
        return self._minimum_downtime

    @minimum_downtime.setter
    def minimum_downtime(self, value):
        self._minimum_downtime = sequence(value)

    @property
    def minimum_uptime(self):
        return self._minimum_uptime

    @minimum_uptime.setter
    def minimum_uptime(self, value):
        self._minimum_uptime = sequence(value)

    @property
    def negative_gradient_limit(self):
        return self._negative_gradient_limit

    @negative_gradient_limit.setter
    def negative_gradient_limit(self, value):
        self._negative_gradient_limit = sequence(value)

    @property
    def positive_gradient_limit(self):
        return self._positive_gradient_limit

    @positive_gradient_limit.setter
    def positive_gradient_limit(self, value):
        self._positive_gradient_limit = sequence(value)

    @property
    def shutdown_costs(self):
        return self._shutdown_costs

    @shutdown_costs.setter
    def shutdown_costs(self, value):
        self._shutdown_costs = sequence(value)

    @property
    def startup_costs(self):
        return self._startup_costs

    @startup_costs.setter
    def startup_costs(self, value):
        self._startup_costs = sequence(value)
