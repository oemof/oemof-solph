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
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import SimpleBlock


class MultiPeriodNonConvexFlow(SimpleBlock):
    r"""
    **The following sets are created:** (-> see basic sets at
        :class:`.Model` )

    A set of flows with the attribute :attr:`nonconvex` of type
        :class:`.options.NonConvex` and the attribute :attr:`multiperiod`.
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

    **The following variables are created:**

    Status variable (binary) :attr:`om.NonConvexFlow.status`:
        Variable indicating if flow is >= 0 indexed by
        MULTIPERIOD_NONCONVEX_FLOWS

    Startup variable (binary) :attr:`om.NonConvexFlow.startup`:
        Variable indicating startup of flow (component) indexed by
        MULTIPERIOD_STARTUPFLOWS

    Shutdown variable (binary) :attr:`om.NonConvexFlow.shutdown`:
        Variable indicating shutdown of flow (component) indexed by
        MULTIPERIOD_SHUTDOWNFLOWS

    **The following constraints are created**:

    Minimum flow constraint :attr:`om.NonConvexFlow.min[i,o,p,t]`
        .. math::
            flow(i, o, p, t) \geq min(i, o, t) \cdot nominal\_value \
                \cdot status(i, o, p, t), \\
            \forall p, t \in \textrm{TIMEINDEX}, \\
            \forall (i, o) \in \textrm{MULTIPERIOD_MIN_FLOWS}.

    Maximum flow constraint :attr:`om.NonConvexFlow.max[i,o,p,t]`
        .. math::
            flow(i, o, p, t) \leq max(i, o, t) \cdot nominal\_value \
                \cdot status(i, o, p, t), \\
            \forall p, t \in \textrm{TIMEINDEX}, \\
            \forall (i, o) \in \textrm{MULTIPERIOD_MIN_FLOWS}.

    Startup constraint :attr:`om.NonConvexFlow.startup_constr[i,o,p,t]`
        .. math::
            startup(i, o, p, t) \geq \
                status(i, o, p, t) - status(i, o, p, t-1) \\
            \forall p, t \in \textrm{TIMEINDEX}, \\
            \forall (i,o) \in \textrm{MULTIPERIOD_STARTUPFLOWS}.

    Maximum startups constraint
        :attr:`om.NonConvexFlow.max_startup_constr[i,o,p,t]`
            .. math::
                \sum_{p, t \in \textrm{TIMEINDEX}} startup(i, o, p, t) \leq \
                    N_{start}(i,o) \quad
                \forall (i,o) \in \textrm{MULTIPERIOD_MAXSTARTUPFLOWS}.

    Shutdown constraint :attr:`om.NonConvexFlow.shutdown_constr[i,o,p,t]`
        .. math::
            shutdown(i, o, p, t) \geq \
                status(i, o, p, t-1) - status(i, o, p, t) \\
            \forall p, t \in \textrm{TIMEINDEX}, \\
            \forall (i, o) \in \textrm{MULTIPERIOD_SHUTDOWNFLOWS}.

    Maximum shutdowns constraint
        :attr:`om.NonConvexFlow.max_startup_constr[i,o,p,t]`
            .. math::
                \sum_{p, t \in \textrm{TIMEINDEX}} shutdown(i, o, p, t) \leq \
                    N_{shutdown}(i,o) \quad
                \forall (i,o) \in \textrm{MULTIPERIOD_MAXSHUTDOWNFLOWS}.

    Minimum uptime constraint :attr:`om.NonConvexFlow.uptime_constr[i,o,p,t]`
        .. math::
            (status(i, o, p, t) - status(i, o, p, t-1))
            \cdot minimum\_uptime(i, o) \\
            \leq \sum_{n=0}^{minimum\_uptime-1} status(i,o,t+n) \\
            \forall p, t \in \textrm{TIMEINDEX} | \\
            t \neq \{0..minimum\_uptime\} \cup \
            \{t\_max-minimum\_uptime..t\_max\} , \\
            \forall (i,o) \in \textrm{MULTIPERIOD_MINUPTIMEFLOWS}.
            \\ \\
            status(i, o, p, t) = initial\_status(i, o) \\
            \forall p, t \in \textrm{TIMEINDEX} | \\
            t = \{0..minimum\_uptime\} \cup \
            \{t\_max-minimum\_uptime..t\_max\} , \\
            \forall (i,o) \in \textrm{MULTIPERIOD_MINUPTIMEFLOWS}.

    Minimum downtime constraint
        :attr:`om.NonConvexFlow.downtime_constr[i,o,pt]`
            .. math::
                (status(i, o, p, t-1) - status(i, o, p, t)) \
                \cdot minimum\_downtime(i, o) \\
                \leq minimum\_downtime(i, o) \
                - \sum_{n=0}^{minimum\_downtime-1} status(i,o,p,t+n) \\
                \forall p, t \in \textrm{TIMEINDEX} | \\
                t \neq \{0..minimum\_downtime\} \cup \
                \{t\_max-minimum\_downtime..t\_max\} , \\
                \forall (i,o) \in \textrm{MULTIPERIOD_MINDOWNTIMEFLOWS}.
                \\ \\
                status(i, o, p, t) = initial\_status(i, o) \\
                \forall p, t \in \textrm{TIMEINDEX} | \\
                t = \{0..minimum\_downtime\} \cup \
                \{t\_max-minimum\_downtime..t\_max\} , \\
                \forall (i,o) \in \textrm{MULTIPERIOD_MINDOWNTIMEFLOWS}.

    **The following parts of the objective function are created:**

    If :attr:`nonconvex.startup_costs` is set by the user:
        .. math::
            \sum_{i, o \in \textrm{MULTIPERIOD_STARTUPFLOWS}} \sum_{p, t}
            startup(i, o, p, t) \
            \cdot startup\_costs(i, o, p)
            \cdot \Delta t
            \cdot (1 - DR)^{-p}

    If :attr:`nonconvex.shutdown_costs` is set by the user:
        .. math::
            \sum_{i, o \in MULTIPERIOD_SHUTDOWNFLOWS}
            \sum_{p, t} shutdown(i, o, p, t) \
            \cdot shutdown\_costs(i, o, p)
            \cdot \Delta t
            \cdot (1 - DR)^{-p}

    If :attr:`nonconvex.activity_costs` is set by the user:
        .. math::
            \sum_{i, o \in MULTIPERIOD_ACTIVITYCOSTFLOWS}
            \sum_{p, t} status(i, o, p, t) \
            \cdot activity\_costs(i, o, p)
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
                if g[2].nonconvex.startup_costs[0] is not None
                or g[2].nonconvex.maximum_startups is not None
            ]
        )
        self.MULTIPERIOD_MAXSTARTUPFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.maximum_startups is not None
            ]
        )
        self.MULTIPERIOD_SHUTDOWNFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.shutdown_costs[0] is not None
                or g[2].nonconvex.maximum_shutdowns is not None
            ]
        )
        self.MULTIPERIOD_MAXSHUTDOWNFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.maximum_shutdowns is not None
            ]
        )
        self.MULTIPERIOD_MINUPTIMEFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.minimum_uptime is not None
            ]
        )

        self.MULTIPERIOD_MINDOWNTIMEFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.minimum_downtime is not None
            ]
        )

        self.MULTIPERIOD_ACTIVITYCOSTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.activity_costs[0] is not None
            ]
        )

        # ################### VARIABLES AND CONSTRAINTS #######################
        self.status = Var(self.MULTIPERIOD_NONCONVEX_FLOWS,
                          m.TIMEINDEX, within=Binary)

        if self.MULTIPERIOD_STARTUPFLOWS:
            self.startup = Var(self.MULTIPERIOD_STARTUPFLOWS,
                               m.TIMEINDEX, within=Binary)

        if self.MULTIPERIOD_SHUTDOWN:
            self.shutdown = Var(self.MULTIPERIOD_SHUTDOWN,
                                m.TIMEINDEX, within=Binary)

        def _minimum_flow_rule(block, i, o, p, t):
            """Rule definition for MILP minimum flow constraints."""
            expr = (
                self.status[i, o, p, t]
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
                self.status[i, o, p, t]
                * m.flows[i, o].max[t]
                * m.flows[i, o].nominal_value
                >= m.flow[i, o, p, t]
            )
            return expr

        self.max = Constraint(
            self.MULTIPERIOD_MIN_FLOWS, m.TIMEINDEX, rule=_maximum_flow_rule
        )

        def _startup_rule(block, i, o, p, t):
            """Rule definition for startup constraint of nonconvex flows."""
            if t > m.TIMEINDEX[1][1]:
                expr = (
                    self.startup[i, o, p, t]
                    >= self.status[i, o, p, t] - self.status[i, o, p, t - 1]
                )
            else:
                expr = (
                    self.startup[i, o, p, t]
                    >= self.status[i, o, p, t]
                    - m.flows[i, o].nonconvex.initial_status
                )
            return expr

        self.startup_constr = Constraint(
            self.MULTIPERIOD_STARTUPFLOWS, m.TIMEINDEX, rule=_startup_rule
        )

        def _max_startup_rule(block, i, o):
            """Rule definition for maximum number of start-ups."""
            lhs = sum(self.startup[i, o, p, t] for p, t in m.TIMEINDEX)
            return lhs <= m.flows[i, o].nonconvex.maximum_startups

        self.max_startup_constr = Constraint(
            self.MULTIPERIOD_MAXSTARTUPFLOWS, rule=_max_startup_rule
        )

        def _shutdown_rule(block, i, o, p, t):
            """Rule definition for shutdown constraints of nonconvex flows."""
            if t > m.TIMEINDEX[1][1]:
                expr = (
                    self.shutdown[i, o, p, t]
                    >= self.status[i, o, p, t - 1] - self.status[i, o, p, t]
                )
            else:
                expr = (
                    self.shutdown[i, o, p, t]
                    >= m.flows[i, o].nonconvex.initial_status
                    - self.status[i, o, p, t]
                )
            return expr

        self.shutdown_constr = Constraint(
            self.MULTIPERIOD_SHUTDOWN, m.TIMEINDEX, rule=_shutdown_rule
        )

        def _max_shutdown_rule(block, i, o):
            """Rule definition for maximum number of start-ups."""
            lhs = sum(self.shutdown[i, o, p, t] for p, t in m.TIMEINDEX)
            return lhs <= m.flows[i, o].nonconvex.maximum_shutdowns

        self.max_shutdown_constr = Constraint(
            self.MULTIPERIOD_MAXSHUTDOWNFLOWS, rule=_max_shutdown_rule
        )

        def _min_uptime_rule(block, i, o, p, t):
            """
            Rule definition for min-uptime constraints of nonconvex flows.
            """
            if (
                m.flows[i, o].nonconvex.max_up_down
                <= t
                <= m.TIMEINDEX[-1][1] - m.flows[i, o].nonconvex.max_up_down
            ):
                expr = 0
                expr += (
                    self.status[i, o, p, t] - self.status[i, o, p, t - 1]
                ) * m.flows[i, o].nonconvex.minimum_uptime
                expr += -sum(
                    self.status[i, o, p, t + u]
                    for u in range(0, m.flows[i, o].nonconvex.minimum_uptime)
                )
                return expr <= 0
            else:
                expr = 0
                expr += self.status[i, o, p, t]
                expr += -m.flows[i, o].nonconvex.initial_status
                return expr == 0

        self.min_uptime_constr = Constraint(
            self.MULTIPERIOD_MINUPTIMEFLOWS, m.TIMEINDEX, rule=_min_uptime_rule
        )

        def _min_downtime_rule(block, i, o, p, t):
            """
            Rule definition for min-downtime constraints of nonconvex flows.
            """
            if (
                m.flows[i, o].nonconvex.max_up_down
                <= t
                <= m.TIMEINDEX[-1][1] - m.flows[i, o].nonconvex.max_up_down
            ):
                expr = 0
                expr += (
                    self.status[i, o, p, t - 1] - self.status[i, o, p, t]
                ) * m.flows[i, o].nonconvex.minimum_downtime
                expr += -m.flows[i, o].nonconvex.minimum_downtime
                expr += sum(
                    self.status[i, o, p, t + d]
                    for d in range(0, m.flows[i, o].nonconvex.minimum_downtime)
                )
                return expr <= 0
            else:
                expr = 0
                expr += self.status[i, o, p, t]
                expr += -m.flows[i, o].nonconvex.initial_status
                return expr == 0

        self.min_downtime_constr = Constraint(
            self.MULTIPERIOD_MINDOWNTIMEFLOWS, m.TIMEINDEX,
            rule=_min_downtime_rule
        )

        # TODO: Add gradient constraints for nonconvex block / flows

    def _objective_expression(self):
        r"""Objective expression for nonconvex flows."""
        if not hasattr(self, "MULTIPERIOD_NONCONVEX_FLOWS"):
            return 0

        m = self.parent_block()

        startup_costs = 0
        shutdown_costs = 0
        activity_costs = 0

        if self.MULTIPERIOD_STARTUPFLOWS:
            for i, o in self.MULTIPERIOD_STARTUPFLOWS:
                if m.flows[i, o].nonconvex.startup_costs[0] is not None:
                    startup_costs += sum(
                        self.startup[i, o, p, t]
                        * m.flows[i, o].nonconvex.startup_costs[p]
                        * m.objective_weighting[t]
                        * ((1 + m.discount_rate) ** -p)
                        for p, t in m.TIMEINDEX
                    )
            self.startup_costs = Expression(expr=startup_costs)

        if self.MULTIPERIOD_SHUTDOWN:
            for i, o in self.MULTIPERIOD_SHUTDOWN:
                if m.flows[i, o].nonconvex.shutdown_costs[0] is not None:
                    shutdown_costs += sum(
                        self.shutdown[i, o, p, t]
                        * m.flows[i, o].nonconvex.shutdown_costs[p]
                        * m.objective_weighting[t]
                        * ((1 + m.discount_rate) ** -p)
                        for p, t in m.TIMEINDEX
                    )
            self.shutdown_costs = Expression(expr=shutdown_costs)

        if self.MULTIPERIOD_ACTIVITYCOSTFLOWS:
            for i, o in self.MULTIPERIOD_ACTIVITYCOSTFLOWS:
                if m.flows[i, o].nonconvex.activity_costs[0] is not None:
                    activity_costs += sum(
                        self.status[i, o, p, t]
                        * m.flows[i, o].nonconvex.activity_costs[p]
                        * m.objective_weighting[t]
                        * ((1 + m.discount_rate) ** -p)
                        for p, t in m.TIMEINDEX
                    )

            self.activity_costs = Expression(expr=activity_costs)

        return startup_costs + shutdown_costs + activity_costs
