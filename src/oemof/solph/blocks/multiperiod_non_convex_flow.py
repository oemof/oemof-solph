# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for nonconvex Flow objects.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Johannes Kochems (jokochems)

SPDX-License-Identifier: MIT

"""

from pyomo.core import Binary
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import SimpleBlock


class MultiPeriodNonConvexFlow(SimpleBlock):
    r"""
    **The following sets are created:** (-> see basic sets at
        :class:`.Model` )

    A set of flows with the attribute :attr:`multiperiodnonconvex` of type
        :class:`.options.MultiPeriodNonConvex`.
    MULTIPERIOD_MIN_FLOWS
        A subset of set MULTIPERIOD_NONCONVEX_FLOWS with the attribute
        :attr:`min` being not None in the first timestep.
    MULTIPERIOD_ACTIVITYCOSTFLOWS
        A subset of set MULTIPERIOD_NONCONVEX_FLOWS with the attribute
        :attr:`activity_costs` being not None.
    MULTIPERIOD_STARTUPFLOWS
        A subset of set MULTIPERIOD_NONCONVEX_FLOWS with the attribute
        :attr:`maximum_startups` or :attr:`startup_costs`
        being not None.
    MULTIPERIOD_MAXSTARTUPFLOWS
        A subset of set MULTIPERIOD_STARTUPFLOWS with the attribute
        :attr:`maximum_startups` being not None.
    MULTIPERIOD_SHUTDOWNFLOWS
        A subset of set MULTIPERIOD_NONCONVEX_FLOWS with the attribute
        :attr:`maximum_shutdowns` or :attr:`shutdown_costs`
        being not None.
    MULTIPERIOD_MAXSHUTDOWNFLOWS
        A subset of set MULTIPERIOD_SHUTDOWNFLOWS with the attribute
        :attr:`maximum_shutdowns` being not None.
    MULTIPERIOD_MINUPTIMEFLOWS
        A subset of set MULTIPERIOD_NONCONVEX_FLOWS with the attribute
        :attr:`minimum_uptime` being not None.
    MULTIPERIOD_MINDOWNTIMEFLOWS
        A subset of set MULTIPERIOD_NONCONVEX_FLOWS with the attribute
        :attr:`minimum_downtime` being not None.
    POSITIVE_GRADIENT_FLOWS
        A subset of set MULTIPERIOD_NONCONVEX_FLOWS with the attribute
        `positive_gradient` being not None.
    NEGATIVE_GRADIENT_FLOWS
        A subset of set MULTIPERIOD_NONCONVEX_FLOWS with the attribute
        `negative_gradient` being not None.

    **The following variables are created:**

    Status variable (binary) :attr:`om.MultiPeriodNonConvexFlow.status`:
        Variable indicating if flow is >= 0 indexed by
        MULTIPERIOD_NONCONVEX_FLOWS

    Startup variable (binary) :attr:`om.MultiPeriodNonConvexFlow.startup`:
        Variable indicating startup of flow (component) indexed by
        MULTIPERIOD_STARTUPFLOWS

    Shutdown variable (binary) :attr:`om.MultiPeriodNonConvexFlow.shutdown`:
        Variable indicating shutdown of flow (component) indexed by
        MULTIPERIOD_SHUTDOWNFLOWS

    **The following constraints are created**:

    Minimum flow constraint :attr:`om.MultiPeriodNonConvexFlow.min[i,o,p,t]`
        .. math::
            flow(i, o, p, t) \geq min(i, o, t) \cdot nominal\_value \
                \cdot status(i, o, t), \\
            \forall p, t \in \textrm{TIMEINDEX}, \\
            \forall (i, o) \in \textrm{MULTIPERIOD_MIN_FLOWS}.

    Maximum flow constraint :attr:`om.MultiPeriodNonConvexFlow.max[i,o,p,t]`
        .. math::
            flow(i, o, p, t) \leq max(i, o, t) \cdot nominal\_value \
                \cdot status(i, o, t), \\
            \forall p, t \in \textrm{TIMEINDEX}, \\
            \forall (i, o) \in \textrm{MULTIPERIOD_MIN_FLOWS}.

    Startup constraint
        :attr:`om.MultiPeriodNonConvexFlow.startup_constr[i,o,t]`
            .. math::
                startup(i, o, t) \geq \
                    status(i, o, t) - status(i, o, t-1) \\
                \forall t \in \textrm{TIMESTEPS}, \\
                \forall (i,o) \in \textrm{MULTIPERIOD_STARTUPFLOWS}.

    Maximum startups constraint
        :attr:`om.MultiPeriodNonConvexFlow.max_startup_constr[i,o,t]`
            .. math::
                \sum_{t \in \textrm{TIMESTEPS}} startup(i, o, t) \leq \
                    N_{start}(i,o) \quad
                \forall (i,o) \in \textrm{MULTIPERIOD_MAXSTARTUPFLOWS}.

    Shutdown constraint
        :attr:`om.MultiPeriodNonConvexFlow.shutdown_constr[i,o,t]`
            .. math::
                shutdown(i, o, t) \geq \
                    status(i, o, t-1) - status(i, o, t) \\
                \forall t \in \textrm{TIMESTEPS}, \\
                \forall (i, o) \in \textrm{MULTIPERIOD_SHUTDOWNFLOWS}.

    Maximum shutdowns constraint
        :attr:`om.MultiPeriodNonConvexFlow.max_shutdown_constr[i,o,t]`
            .. math::
                \sum_{t \in \textrm{TIMESTEPS}} shutdown(i, o, t) \leq \
                    N_{shutdown}(i,o) \quad
                \forall (i,o) \in \textrm{MULTIPERIOD_MAXSHUTDOWNFLOWS}.

    Minimum uptime constraint
        :attr:`om.MultiPeriodNonConvexFlow.uptime_constr[i,o,t]`
            .. math::
                (status(i, o, t) - status(i, o, t-1))
                \cdot minimum\_uptime(i, o) \\
                \leq \sum_{n=0}^{minimum\_uptime-1} status(i,o,t+n) \\
                \forall p, t \in \textrm{TIMESTEPS} | \\
                t \neq \{0..minimum\_uptime\} \cup \
                \{t\_max-minimum\_uptime..t\_max\} , \\
                \forall (i,o) \in \textrm{MULTIPERIOD_MINUPTIMEFLOWS}.
                \\ \\
                status(i, o, t) = initial\_status(i, o) \\
                \forall t \in \textrm{TIMESTEPS} | \\
                t = \{0..minimum\_uptime\} \cup \
                \{t\_max-minimum\_uptime..t\_max\} , \\
                \forall (i,o) \in \textrm{MULTIPERIOD_MINUPTIMEFLOWS}.

    Minimum downtime constraint
        :attr:`om.MultiPeriodNonConvexFlow.downtime_constr[i,ot]`
            .. math::
                (status(i, o, t-1) - status(i, o, t)) \
                \cdot minimum\_downtime(i, o) \\
                \leq minimum\_downtime(i, o) \
                - \sum_{n=0}^{minimum\_downtime-1} status(i,o,t+n) \\
                \forall t \in \textrm{TIMESTEPS} | \\
                t \neq \{0..minimum\_downtime\} \cup \
                \{t\_max-minimum\_downtime..t\_max\} , \\
                \forall (i,o) \in \textrm{MULTIPERIOD_MINDOWNTIMEFLOWS}.
                \\ \\
                status(i, o, t) = initial\_status(i, o) \\
                \forall t \in \textrm{TIMESTEPS} | \\
                t = \{0..minimum\_downtime\} \cup \
                \{t\_max-minimum\_downtime..t\_max\} , \\
                \forall (i,o) \in \textrm{MULTIPERIOD_MINDOWNTIMEFLOWS}.

    Positive gradient constraint
      `om.MultiPeriodNonConvexFlow.positive_gradient_constr[i, o]`:
        .. math:: flow(i, o, p, t) \cdot status(i, o, t)
        - flow(i, o, p, t-1) \cdot status(i, o, t-1)  \geq \
          positive\_gradient(i, o, t), \\
          \forall (i, o) \in \textrm{MULTIPERIOD_POSITIVE_GRADIENT_FLOWS}, \\
          \forall p, t \in \textrm{TIMEINDEX}.

    Negative gradient constraint
      `om.MultiPeriodNonConvexFlow.negative_gradient_constr[i, o]`:
        .. math::
          flow(i, o, p, t-1) \cdot status(i, o, t-1)
          - flow(i, o, p, t) \cdot status(i, o, t) \geq \
          negative\_gradient(i, o, t), \\
          \forall (i, o) \in \textrm{MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS}, \\
          \forall t \in \textrm{TIMEINDEX}.

    _Note: The matching routine used for attributing the timesteps to the
    respective periods is not shown in the gradient equations._

    **The following parts of the objective function are created:**

    If :attr:`multiperiodnonconvex.startup_costs` is set by the user:
        .. math::
            \sum_{i, o \in \textrm{MULTIPERIOD_STARTUPFLOWS}} \sum_{p, t}
            startup(i, o, t) \
            \cdot startup\_costs(i, o, p)
            \cdot \Delta t
            \cdot (1 - DR)^{-p}

    If :attr:`multiperiodnonconvex.shutdown_costs` is set by the user:
        .. math::
            \sum_{i, o \in \textrm{MULTIPERIOD_SHUTDOWNFLOWS}}
            \sum_{p, t} shutdown(i, o, t) \
            \cdot shutdown\_costs(i, o, p)
            \cdot \Delta t
            \cdot (1 - DR)^{-p}

    If :attr:`multiperiodnonconvex.activity_costs` is set by the user:
        .. math::
            \sum_{i, o \in \textrm{MULTIPERIOD_ACTIVITYCOSTFLOWS}}
            \sum_{p, t} status(i, o, t) \
            \cdot activity\_costs(i, o, p)
            \cdot \Delta t
            \cdot (1 - DR)^{-p}

    If `nonconvex.positive_gradient["costs"]` is set by the user:
        .. math::
            \sum_{i, o \in \textrm{MULTIPERIOD_POSITIVE_GRADIENT_FLOWS}}
            \sum_{p, t} positive_gradient(i, o, t)
            \cdot positive\_gradient\_costs(i, o)
            \cdot \Delta t
            \cdot (1 - DR)^{-p}

    If `nonconvex.negative_gradient["costs"]` is set by the user:
        .. math::
            \sum_{i, o \in \textrm{MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS}}
            \sum_{p, t} negative_gradient(i, o, t)
            \cdot negative\_gradient\_costs(i, o)
            \cdot \Delta t
            \cdot (1 - DR)^{-p}

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates set, variables, constraints for all flow object with
        an attribute flow of type class:`.NonConvexFlow`.

        Parameters
        ----------
        group : list
            List of oemof.solph.NonConvexFlow objects for which
            the constraints are build.
        """
        if group is None:
            return None

        m = self.parent_block()
        # ########################## SETS #####################################
        self.MULTIPERIOD_NONCONVEX_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group]
        )

        self.MULTIPERIOD_MIN_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group
                        if g[2].min[0] is not None]
        )
        self.MULTIPERIOD_STARTUPFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].multiperiodnonconvex.startup_costs[0] is not None
                or g[2].multiperiodnonconvex.maximum_startups is not None
            ]
        )
        self.MULTIPERIOD_MAXSTARTUPFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].multiperiodnonconvex.maximum_startups is not None
            ]
        )
        self.MULTIPERIOD_SHUTDOWNFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].multiperiodnonconvex.shutdown_costs[0] is not None
                or g[2].multiperiodnonconvex.maximum_shutdowns is not None
            ]
        )
        self.MULTIPERIOD_MAXSHUTDOWNFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].multiperiodnonconvex.maximum_shutdowns is not None
            ]
        )
        self.MULTIPERIOD_MINUPTIMEFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].multiperiodnonconvex.minimum_uptime is not None
            ]
        )

        self.MULTIPERIOD_MINDOWNTIMEFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].multiperiodnonconvex.minimum_downtime is not None
            ]
        )

        self.MULTIPERIOD_ACTIVITYCOSTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].multiperiodnonconvex.activity_costs[0] is not None
            ]
        )

        self.MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if (g[2].multiperiodnonconvex.negative_gradient["ub"][0]
                    is not None)
            ]
        )

        self.MULTIPERIOD_POSITIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if (g[2].multiperiodnonconvex.positive_gradient["ub"][0]
                    is not None)
            ]
        )

        # ################### VARIABLES AND CONSTRAINTS #######################
        self.status = Var(self.MULTIPERIOD_NONCONVEX_FLOWS,
                          m.TIMESTEPS, within=Binary)

        if self.MULTIPERIOD_STARTUPFLOWS:
            self.startup = Var(self.MULTIPERIOD_STARTUPFLOWS,
                               m.TIMESTEPS, within=Binary)

        if self.MULTIPERIOD_SHUTDOWNFLOWS:
            self.shutdown = Var(self.MULTIPERIOD_SHUTDOWNFLOWS,
                                m.TIMESTEPS, within=Binary)

        if self.MULTIPERIOD_POSITIVE_GRADIENT_FLOWS:
            self.positive_gradient = Var(
                self.MULTIPERIOD_POSITIVE_GRADIENT_FLOWS,
                m.TIMESTEPS
            )

        if self.MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS:
            self.negative_gradient = Var(
                self.MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS,
                m.TIMESTEPS
            )

        def _minimum_flow_rule(block, i, o, p, t):
            """Rule definition for MILP minimum flow constraints."""
            expr = (
                self.status[i, o, t]
                * m.flows[i, o].min[t]
                * m.flows[i, o].nominal_value
                <= m.flow[i, o, p, t]
            )
            return expr

        self.min = Constraint(
            self.MULTIPERIOD_MIN_FLOWS, m.TIMEINDEX, rule=_minimum_flow_rule
        )

        def _maximum_flow_rule(block, i, o, p, t):
            """Rule definition for MILP maximum flow constraints."""
            expr = (
                self.status[i, o, t]
                * m.flows[i, o].max[t]
                * m.flows[i, o].nominal_value
                >= m.flow[i, o, p, t]
            )
            return expr

        self.max = Constraint(
            self.MULTIPERIOD_MIN_FLOWS, m.TIMEINDEX, rule=_maximum_flow_rule
        )

        def _startup_rule(block, i, o, t):
            """Rule definition for startup constraint of
            multiperiodnonconvex flows."""
            if t > m.TIMESTEPS[1]:
                expr = (
                    self.startup[i, o, t]
                    >= self.status[i, o, t] - self.status[i, o, t - 1]
                )
            else:
                expr = (
                    self.startup[i, o, t]
                    >= self.status[i, o, t]
                    - m.flows[i, o].multiperiodnonconvex.initial_status
                )
            return expr

        self.startup_constr = Constraint(
            self.MULTIPERIOD_STARTUPFLOWS, m.TIMESTEPS, rule=_startup_rule
        )

        def _max_startup_rule(block, i, o):
            """Rule definition for maximum number of start-ups."""
            lhs = sum(self.startup[i, o, t] for t in m.TIMESTEPS)
            return lhs <= m.flows[i, o].multiperiodnonconvex.maximum_startups

        self.max_startup_constr = Constraint(
            self.MULTIPERIOD_MAXSTARTUPFLOWS, rule=_max_startup_rule
        )

        def _shutdown_rule(block, i, o, t):
            """Rule definition for shutdown constraints of
            multiperiodnonconvex flows."""
            if t > m.TIMESTEPS[1]:
                expr = (
                    self.shutdown[i, o, t]
                    >= self.status[i, o, t - 1] - self.status[i, o, t]
                )
            else:
                expr = (
                    self.shutdown[i, o, t]
                    >= m.flows[i, o].multiperiodnonconvex.initial_status
                    - self.status[i, o, t]
                )
            return expr

        self.shutdown_constr = Constraint(
            self.MULTIPERIOD_SHUTDOWNFLOWS, m.TIMESTEPS, rule=_shutdown_rule
        )

        def _max_shutdown_rule(block, i, o):
            """Rule definition for maximum number of start-ups."""
            lhs = sum(self.shutdown[i, o, t] for t in m.TIMESTEPS)
            return lhs <= m.flows[i, o].multiperiodnonconvex.maximum_shutdowns

        self.max_shutdown_constr = Constraint(
            self.MULTIPERIOD_MAXSHUTDOWNFLOWS, rule=_max_shutdown_rule
        )

        def _min_uptime_rule(block, i, o, t):
            """
            Rule definition for min-uptime constraints of
            multiperiodnonconvex flows.
            """
            if (
                m.flows[i, o].multiperiodnonconvex.max_up_down
                <= t
                <= (m.TIMESTEPS[-1]
                    - m.flows[i, o].multiperiodnonconvex.max_up_down)
            ):
                expr = 0
                expr += (
                    self.status[i, o, t] - self.status[i, o, t - 1]
                ) * m.flows[i, o].multiperiodnonconvex.minimum_uptime
                expr += -sum(
                    self.status[i, o, t + u]
                    for u in range(
                        0, m.flows[i, o].multiperiodnonconvex.minimum_uptime
                    )
                )
                return expr <= 0
            else:
                expr = 0
                expr += self.status[i, o, t]
                expr += -m.flows[i, o].multiperiodnonconvex.initial_status
                return expr == 0

        self.min_uptime_constr = Constraint(
            self.MULTIPERIOD_MINUPTIMEFLOWS, m.TIMESTEPS, rule=_min_uptime_rule
        )

        def _min_downtime_rule(block, i, o, t):
            """
            Rule definition for min-downtime constraints of
            multiperiodnonconvex flows.
            """
            if (
                m.flows[i, o].multiperiodnonconvex.max_up_down
                <= t
                <= (m.TIMESTEPS[-1]
                    - m.flows[i, o].multiperiodnonconvex.max_up_down)
            ):
                expr = 0
                expr += (
                    self.status[i, o, t - 1] - self.status[i, o, t]
                ) * m.flows[i, o].multiperiodnonconvex.minimum_downtime
                expr += -m.flows[i, o].multiperiodnonconvex.minimum_downtime
                expr += sum(
                    self.status[i, o, t + d]
                    for d in range(
                        0, m.flows[i, o].multiperiodnonconvex.minimum_downtime
                    )
                )
                return expr <= 0
            else:
                expr = 0
                expr += self.status[i, o, t]
                expr += -m.flows[i, o].multiperiodnonconvex.initial_status
                return expr == 0

        self.min_downtime_constr = Constraint(
            self.MULTIPERIOD_MINDOWNTIMEFLOWS, m.TIMESTEPS,
            rule=_min_downtime_rule
        )

        def _positive_gradient_flow_rule(block):
            """Rule definition for positive gradient constraint."""
            for i, o in self.MULTIPERIOD_POSITIVE_GRADIENT_FLOWS:
                for index in range(1, len(m.TIMEINDEX) + 1):
                    if m.TIMEINDEX[index][1] > 0:
                        lhs = (
                            m.flow[i, o, m.TIMEINDEX[index][0],
                                   m.TIMEINDEX[index][1]]
                            * self.status[i, o, m.TIMEINDEX[index][1]]
                            - m.flow[i, o, m.TIMEINDEX[index - 1][0],
                                     m.TIMEINDEX[index - 1][1]]
                            * self.status[i, o, m.TIMEINDEX[index - 1][1]]
                        )
                        rhs = self.positive_gradient[i, o,
                                                     m.TIMEINDEX[index][1]]
                        self.positive_gradient_constr.add(
                            (i, o, m.TIMEINDEX[index][0],
                             m.TIMEINDEX[index][1]),
                            lhs <= rhs
                        )
                    else:
                        pass  # return(Constraint.Skip)

        self.positive_gradient_constr = Constraint(
            self.MULTIPERIOD_POSITIVE_GRADIENT_FLOWS, m.TIMEINDEX,
            noruleinit=True
        )
        self.positive_gradient_build = BuildAction(
            rule=_positive_gradient_flow_rule
        )

        def _negative_gradient_flow_rule(block):
            """Rule definition for negative gradient constraint."""
            for i, o in self.MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS:
                for index in range(1, len(m.TIMEINDEX) + 1):
                    if m.TIMEINDEX[index][1] > 0:
                        lhs = (
                            m.flow[i, o, m.TIMEINDEX[index - 1][0],
                                   m.TIMEINDEX[index - 1][1]]
                            * self.status[i, o, m.TIMEINDEX[index - 1][1]]
                            - m.flow[i, o, m.TIMEINDEX[index][0],
                                     m.TIMEINDEX[index][1]]
                            * self.status[i, o, m.TIMEINDEX[index][1]]
                        )
                        rhs = self.negative_gradient[i, o,
                                                     m.TIMEINDEX[index][1]]
                        self.negative_gradient_constr.add(
                            (i, o, m.TIMEINDEX[index][0],
                             m.TIMEINDEX[index][1]),
                            lhs <= rhs
                        )
                    else:
                        pass  # return(Constraint.Skip)

        self.negative_gradient_constr = Constraint(
            self.MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS, m.TIMEINDEX,
            noruleinit=True
        )
        self.negative_gradient_build = BuildAction(
            rule=_negative_gradient_flow_rule
        )

    def _objective_expression(self):
        r"""Objective expression for nonconvex flows."""
        if not hasattr(self, "MULTIPERIOD_NONCONVEX_FLOWS"):
            return 0

        m = self.parent_block()

        startup_costs = 0
        shutdown_costs = 0
        activity_costs = 0
        gradient_costs = 0

        if self.MULTIPERIOD_STARTUPFLOWS:
            for i, o in self.MULTIPERIOD_STARTUPFLOWS:
                if (m.flows[i, o].multiperiodnonconvex.startup_costs[0]
                        is not None):
                    startup_costs += sum(
                        self.startup[i, o, t]
                        * m.flows[i, o].multiperiodnonconvex.startup_costs[p]
                        * m.objective_weighting[t]
                        * ((1 + m.discount_rate) ** -p)
                        for p, t in m.TIMEINDEX
                    )
            self.startup_costs = Expression(expr=startup_costs)

        if self.MULTIPERIOD_SHUTDOWNFLOWS:
            for i, o in self.MULTIPERIOD_SHUTDOWNFLOWS:
                if (m.flows[i, o].multiperiodnonconvex.shutdown_costs[0]
                        is not None):
                    shutdown_costs += sum(
                        self.shutdown[i, o, t]
                        * m.flows[i, o].multiperiodnonconvex.shutdown_costs[p]
                        * m.objective_weighting[t]
                        * ((1 + m.discount_rate) ** -p)
                        for p, t in m.TIMEINDEX
                    )
            self.shutdown_costs = Expression(expr=shutdown_costs)

        if self.MULTIPERIOD_ACTIVITYCOSTFLOWS:
            for i, o in self.MULTIPERIOD_ACTIVITYCOSTFLOWS:
                if (m.flows[i, o].multiperiodnonconvex.activity_costs[0]
                        is not None):
                    activity_costs += sum(
                        self.status[i, o, t]
                        * m.flows[i, o].multiperiodnonconvex.activity_costs[p]
                        * m.objective_weighting[t]
                        * ((1 + m.discount_rate) ** -p)
                        for p, t in m.TIMEINDEX
                    )

            self.activity_costs = Expression(expr=activity_costs)

        if self.MULTIPERIOD_POSITIVE_GRADIENT_FLOWS:
            for i, o in self.MULTIPERIOD_POSITIVE_GRADIENT_FLOWS:
                if (
                    (m.flows[i, o].multiperiodnonconvex
                        .positive_gradient["ub"][0])
                    is not None
                ):
                    gradient_costs += sum(
                        self.positive_gradient[i, o, p, t]
                        * (m.flows[i, o].multiperiodnonconvex
                           .positive_gradient["costs"])
                        * m.objective_weighting[t]
                        * ((1 + m.discount_rate) ** -p)
                        for p, t in m.TIMEINDEX
                    )

        if self.MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS:
            for i, o in self.MULTIPERIOD_NEGATIVE_GRADIENT_FLOWS:
                if (
                    (m.flows[i, o].multiperiodnonconvex
                        .negative_gradient["ub"][0])
                    is not None
                ):
                    gradient_costs += sum(
                        self.negative_gradient[i, o, p, t]
                        * (m.flows[i, o].multiperiodnonconvex
                           .negative_gradient["costs"])
                        * m.objective_weighting[t]
                        * ((1 + m.discount_rate) ** -p)
                        for p, t in m.TIMEINDEX
                    )

            self.gradient_costs = Expression(expr=gradient_costs)

        return startup_costs + shutdown_costs + activity_costs + gradient_costs
