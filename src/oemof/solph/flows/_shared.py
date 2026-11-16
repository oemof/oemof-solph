# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for Flow objects with investment but without nonconvex option.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Dylan Pulver
SPDX-FileCopyrightText: Syed Inayatullah

SPDX-License-Identifier: MIT

"""

from pyomo.core import Binary
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import Set
from pyomo.core import Var

from oemof.solph._plumbing import valid_sequence


def _gradient_limit(flow, direction):
    """Gradient limit of a non-convex flow.

    The limit can be given in the `NonConvex` attribute or on the flow
    itself. Both cannot be given at the same time (see
    :class:`~oemof.solph.flows.Flow`). `direction` is "positive" or
    "negative".
    """
    attribute = f"{direction}_gradient_limit"
    limit = getattr(flow.nonconvex, attribute)
    if limit is None:
        limit = getattr(flow, attribute)
    return limit


def sets_for_non_convex_flows(block, group):
    r"""Creates all sets for non-convex flows.

    MIN_FLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute `min`
        being not None in the first timestep.
    ACTIVITYCOSTFLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute
        `activity_costs` being not None.
    INACTIVITYCOSTFLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute
        `inactivity_costs` being not None.
    STARTUPFLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute
        `maximum_startups` or `startup_costs`
        being not None.
    MAXSTARTUPFLOWS
        A subset of set STARTUPFLOWS with the attribute
        `maximum_startups` being not None.
    SHUTDOWNFLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute
        `maximum_shutdowns` or `shutdown_costs`
        being not None.
    MAXSHUTDOWNFLOWS
        A subset of set SHUTDOWNFLOWS with the attribute
        `maximum_shutdowns` being not None.
    MINUPTIMEFLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute
        `minimum_uptime` being > 0.
    MINDOWNTIMEFLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute
        `minimum_downtime` being > 0.
    POSITIVE_GRADIENT_FLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute
        `positive_gradient_limit` being not None, given in `NonConvex` or
        on the flow.
    NEGATIVE_GRADIENT_FLOWS
        A subset of set FIXED_CAPACITY_NONCONVEX_FLOWS with the attribute
        `negative_gradient_limit` being not None, given in `NonConvex` or
        on the flow.
    """
    block.MIN_FLOWS = Set(
        initialize=[(g[0], g[1]) for g in group if g[2].minimum is not None]
    )
    block.STARTUPFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.startup_costs is not None
            or g[2].nonconvex.maximum_startups is not None
        ]
    )
    block.MAXSTARTUPFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.maximum_startups is not None
        ]
    )
    block.SHUTDOWNFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.shutdown_costs is not None
            or g[2].nonconvex.maximum_shutdowns is not None
        ]
    )
    block.MAXSHUTDOWNFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.maximum_shutdowns is not None
        ]
    )
    block.MINUPTIMEFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.minimum_uptime.max() > 0
        ]
    )
    block.MINDOWNTIMEFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.minimum_downtime.max() > 0
        ]
    )
    block.NEGATIVE_GRADIENT_FLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if _gradient_limit(g[2], "negative") is not None
        ]
    )
    block.POSITIVE_GRADIENT_FLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if _gradient_limit(g[2], "positive") is not None
        ]
    )
    block.ACTIVITYCOSTFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.activity_costs is not None
        ]
    )

    block.INACTIVITYCOSTFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.inactivity_costs is not None
        ]
    )


def variables_for_non_convex_flows(block):
    r"""
    :math:`Y_{startup}` (binary) `NonConvexFlowBlock.startup`:
        Variable indicating startup of flow (component) indexed by
        STARTUPFLOWS

    :math:`Y_{shutdown}` (binary) `NonConvexFlowBlock.shutdown`:
        Variable indicating shutdown of flow (component) indexed by
        SHUTDOWNFLOWS

    Gradient limits need no extra variables. They are written directly in
    terms of the flow and the status variables, see
    :py:func:`shared_constraints_for_non_convex_flows`.
    """
    m = block.parent_block()

    if block.STARTUPFLOWS:
        block.startup = Var(block.STARTUPFLOWS, m.TIMESTEPS, within=Binary)

    if block.SHUTDOWNFLOWS:
        block.shutdown = Var(block.SHUTDOWNFLOWS, m.TIMESTEPS, within=Binary)


def _previous_status(block, i, o, t):
    """Status of a flow in the time step before `t`.

    Before the first time step of the optimisation horizon, the flow is
    assumed to have been in its `initial_status`. This is the same
    convention that the startup and shutdown constraints use.
    """
    m = block.parent_block()
    if t > m.TIMESTEPS.at(1):
        return block.status[i, o, t - 1]
    return m.flows[i, o].nonconvex.initial_status


def _min_downtime_constraint(block):
    r"""
    .. math::
        (Y_{status}(t-1) - Y_{status}(t)) \
        \cdot t_{down,minimum} \\
        \leq t_{down,minimum} \
        - \sum_{n=0}^{t_{down,minimum}-1} Y_{status}(t+n) \\
        \forall t \in \textrm{TIMESTEPS}, \\
        \forall (i,o) \in \textrm{MINDOWNTIMEFLOWS}.

    where :math:`Y_{status}(-1) := Y_{status,0}`, the `initial_status`
    of the flow.
    """
    m = block.parent_block()

    def min_downtime_rule(_, i, o, t):
        """
        Rule definition for min-downtime constraints of non-convex flows.
        """
        expr = 0
        expr += (
            _previous_status(block, i, o, t) - block.status[i, o, t]
        ) * m.flows[i, o].nonconvex.minimum_downtime[t]
        expr += -m.flows[i, o].nonconvex.minimum_downtime[t]
        expr += sum(
            block.status[i, o, d]
            for d in range(
                t,
                min(
                    t + m.flows[i, o].nonconvex.minimum_downtime[t],
                    len(m.TIMESTEPS),
                ),
            )
        )
        return expr <= 0

    return Constraint(
        block.MINDOWNTIMEFLOWS, m.TIMESTEPS, rule=min_downtime_rule
    )


def _min_uptime_constraint(block):
    r"""
    .. math::
        (Y_{status}(t)-Y_{status}(t-1)) \cdot L(t) \\
        \leq \sum_{n=0}^{L(t)-1} Y_{status}(t+n) \\
        \forall t \in \textrm{TIMESTEPS}, \\
        \forall (i,o) \in \textrm{MINUPTIMEFLOWS},

    with :math:`L(t) = \min(t_{up,minimum}, |\textrm{TIMESTEPS}| - t)`,
    the number of time steps of the uptime window that lie within the
    optimisation horizon. Near the end of the horizon, a start-up
    requires the flow to stay on until the last time step.

    :math:`Y_{status}(-1) := Y_{status,0}`, the `initial_status`
    of the flow.
    """
    m = block.parent_block()

    def _min_uptime_rule(_, i, o, t):
        """
        Rule definition for min-uptime constraints of non-convex flows.
        """
        window = range(
            t,
            min(
                t + m.flows[i, o].nonconvex.minimum_uptime[t],
                len(m.TIMESTEPS),
            ),
        )
        expr = 0
        expr += (
            block.status[i, o, t] - _previous_status(block, i, o, t)
        ) * len(window)
        expr += -sum(block.status[i, o, u] for u in window)
        return expr <= 0

    return Constraint(block.MINUPTIMEFLOWS, m.TIMESTEPS, rule=_min_uptime_rule)


def _shutdown_constraint(block):
    r"""
    .. math::
        Y_{shutdown}(t) \geq Y_{status}(t-1) - Y_{status}(t) \\
        \forall t \in \textrm{TIMESTEPS}, \\
        \forall \textrm{SHUTDOWNFLOWS}.
    """
    m = block.parent_block()

    def _shutdown_rule(_, i, o, t):
        """Rule definition for shutdown constraints of non-convex flows."""
        previous = _previous_status(block, i, o, t)
        return block.shutdown[i, o, t] >= previous - block.status[i, o, t]

    return Constraint(block.SHUTDOWNFLOWS, m.TIMESTEPS, rule=_shutdown_rule)


def _startup_constraint(block):
    r"""
    .. math::
        Y_{startup}(t) \geq Y_{status}(t) - Y_{status}(t-1) \\
        \forall t \in \textrm{TIMESTEPS}, \\
        \forall \textrm{STARTUPFLOWS}.
    """
    m = block.parent_block()

    def _startup_rule(_, i, o, t):
        """Rule definition for startup constraint of nonconvex flows."""
        previous = _previous_status(block, i, o, t)
        return block.startup[i, o, t] >= block.status[i, o, t] - previous

    return Constraint(block.STARTUPFLOWS, m.TIMESTEPS, rule=_startup_rule)


def _max_startup_constraint(block):
    r"""
    .. math::
        \sum_{t \in \textrm{TIMESTEPS}} Y_{startup}(t) \leq \
            N_{start}(i,o)\\
        \forall (i,o) \in \textrm{MAXSTARTUPFLOWS}.
    """
    m = block.parent_block()

    def _max_startup_rule(_, i, o):
        """Rule definition for maximum number of start-ups."""
        lhs = sum(block.startup[i, o, t] for t in m.TIMESTEPS)
        return lhs <= m.flows[i, o].nonconvex.maximum_startups

    return Constraint(block.MAXSTARTUPFLOWS, rule=_max_startup_rule)


def _max_shutdown_constraint(block):
    r"""
    .. math::
        \sum_{t \in \textrm{TIMESTEPS}} Y_{startup}(t) \leq \
            N_{shutdown}(i,o)\\
        \forall (i,o) \in \textrm{MAXSHUTDOWNFLOWS}.
    """
    m = block.parent_block()

    def _max_shutdown_rule(_, i, o):
        """Rule definition for maximum number of start-ups."""
        lhs = sum(block.shutdown[i, o, t] for t in m.TIMESTEPS)
        return lhs <= m.flows[i, o].nonconvex.maximum_shutdowns

    return Constraint(block.MAXSHUTDOWNFLOWS, rule=_max_shutdown_rule)


def _factors_for_gradient_terms(block, i, o, t):
    r"""Factors used in the gradient terms between `t-1` and `t`.

    Returns a tuple `(capacity, previous_on, on, ratio)`: the capacity
    at `t`, the status at `t-1` and at `t` multiplied by that capacity,
    and the capacity at `t-1` divided by the capacity at `t`. The
    gradient limits are multiplied by these factors.

    Returns `None` if no gradient limit is set up for `t`. This is the
    case if the capacity at `t` is zero, and for investment flows if the
    capacity can change between `t-1` and `t`.
    """
    m = block.parent_block()
    period_of_step = m.es.capacity_period_of_timestep(t)
    period_of_previous_step = m.es.capacity_period_of_timestep(t - 1)

    if m.flows[i, o].investment is not None:
        if period_of_step != period_of_previous_step:
            return None
        return (
            block.invest[i, o, period_of_step],
            block.status_nominal[i, o, t - 1],
            block.status_nominal[i, o, t],
            1,
        )

    capacity = m.flows[i, o].nominal_capacity[period_of_step]
    if capacity == 0:
        return None
    return (
        capacity,
        block.status[i, o, t - 1] * capacity,
        block.status[i, o, t] * capacity,
        m.flows[i, o].nominal_capacity[period_of_previous_step] / capacity,
    )


def shared_constraints_for_non_convex_flows(block):
    r"""
    positive_gradient_constr
        .. math::
            P(t) - P(t-1) \leq
            (G_{up}(t) - S_{up}(t)) \cdot P_{nom} \cdot Y_{status}(t-1)
            + E_{up}(t) \cdot P_{nom} \cdot Y_{status}(t)
            + (S_{up}(t) - E_{up}(t)) \cdot P_{nom}, \\
            \forall t \in \textrm{TIMESTEPS} \setminus \{0\}, \\
            \forall (i, o) \in \textrm{POSITIVE\_GRADIENT\_FLOWS}

        with :math:`S_{up}(t) = \max(G_{up}(t), f_{min}(t))` and
        :math:`E_{up}(t) = \min(S_{up}(t), G_{up}(t) + f_{min}(t-1))`.

        While the flow stays on, it can rise by at most
        :math:`G_{up}(t) \cdot P_{nom}` from one time step to the next.
        A start-up can reach :math:`S_{up}(t) \cdot P_{nom}`, so a
        start-up to the minimum load is always possible. Shut-downs are
        not restricted by this constraint.

    negative_gradient_constr
        .. math::
            P(t-1) - P(t) \leq
            (G_{down}(t) - S_{down}(t)) \cdot P_{nom} \cdot Y_{status}(t)
            + E_{down}(t) \cdot P_{nom} \cdot Y_{status}(t-1)
            + (S_{down}(t) - E_{down}(t)) \cdot P_{nom}, \\
            \forall t \in \textrm{TIMESTEPS} \setminus \{0\}, \\
            \forall (i, o) \in \textrm{NEGATIVE\_GRADIENT\_FLOWS}

        with :math:`S_{down}(t) = \max(G_{down}(t), f_{min}(t-1))` and
        :math:`E_{down}(t) = \min(S_{down}(t), G_{down}(t) + f_{min}(t))`.

        While the flow stays on, it can fall by at most
        :math:`G_{down}(t) \cdot P_{nom}` from one time step to the next.
        A shut-down is possible from :math:`S_{down}(t) \cdot P_{nom}` or
        less, so a shut-down from the minimum load is always possible.
        Start-ups are not restricted by this constraint.

    Here, :math:`G_{up}` and :math:`G_{down}` are the
    `positive_gradient_limit` and the `negative_gradient_limit`, given in
    the `NonConvex` attribute or on the flow, and :math:`f_{min}` is the
    `minimum` of the flow. Both constraints are linear. For each
    combination of the status in `t-1` and `t`, they allow exactly the
    changes described above. The
    terms with :math:`E_{up}` and :math:`E_{down}` give a tighter LP
    relaxation than the form
    :math:`G_{up} \cdot Y_{status}(t-1) + S_{up} \cdot (1 - Y_{status}(t-1))`
    without changing the set of feasible integer solutions.

    For investment flows, :math:`P_{nom} \cdot Y_{status}` is the
    variable `status_nominal`. If the nominal capacity changes between
    `t-1` and `t`, :math:`f_{min}(t-1)` is multiplied by the ratio of the
    capacities at `t-1` and `t`. For investment flows, no gradient limit
    is set up for the first time step after an investment time.

    Also creates:

    * :py:func:`startup_constraint`
    * :py:func:`max_startup_constraint`
    * :py:func:`shutdown_constraint`
    * :py:func:`max_shutdown_constraint`
    * :py:func:`min_uptime_constraint`
    * :py:func:`min_downtime_constraint`
    """
    m = block.parent_block()

    block.startup_constr = _startup_constraint(block)
    block.max_startup_constr = _max_startup_constraint(block)
    block.shutdown_constr = _shutdown_constraint(block)
    block.max_shutdown_constr = _max_shutdown_constraint(block)
    block.min_uptime_constr = _min_uptime_constraint(block)
    block.min_downtime_constr = _min_downtime_constraint(block)

    def _positive_gradient_rule(_, i, o, t):
        """Rule definition for positive gradient constraint."""
        if t == m.TIMESTEPS.first():
            return Constraint.Skip
        factors = _factors_for_gradient_terms(block, i, o, t)
        if factors is None:
            return Constraint.Skip
        capacity, previous_on, on, ratio = factors

        flow = m.flows[i, o]
        limit = _gradient_limit(flow, "positive")[t]
        startup_limit = max(limit, flow.minimum[t])
        off_reduction = min(startup_limit, limit + flow.minimum[t - 1] * ratio)

        lhs = m.flow[i, o, t] - m.flow[i, o, t - 1]
        rhs = (
            (limit - startup_limit) * previous_on
            + off_reduction * on
            + (startup_limit - off_reduction) * capacity
        )
        return lhs <= rhs

    block.positive_gradient_constr = Constraint(
        block.POSITIVE_GRADIENT_FLOWS,
        m.TIMESTEPS,
        rule=_positive_gradient_rule,
    )

    def _negative_gradient_rule(_, i, o, t):
        """Rule definition for negative gradient constraint."""
        if t == m.TIMESTEPS.first():
            return Constraint.Skip
        factors = _factors_for_gradient_terms(block, i, o, t)
        if factors is None:
            return Constraint.Skip
        capacity, previous_on, on, ratio = factors

        flow = m.flows[i, o]
        limit = _gradient_limit(flow, "negative")[t]
        shutdown_limit = max(limit, flow.minimum[t - 1] * ratio)
        off_reduction = min(shutdown_limit, limit + flow.minimum[t])

        lhs = m.flow[i, o, t - 1] - m.flow[i, o, t]
        rhs = (
            (limit - shutdown_limit) * on
            + off_reduction * previous_on
            + (shutdown_limit - off_reduction) * capacity
        )
        return lhs <= rhs

    block.negative_gradient_constr = Constraint(
        block.NEGATIVE_GRADIENT_FLOWS,
        m.TIMESTEPS,
        rule=_negative_gradient_rule,
    )


def maximum_flow_constraint(block):
    r"""
    .. math::
        P(t) \leq max(i, o, t) \cdot P_{nom} \
            \cdot status(t), \\
        \forall t \in \textrm{TIMESTEPS}, \\
        \forall (i, o) \in \textrm{FIXED_CAPACITY_NONCONVEX_FLOWS}.
    """
    m = block.parent_block()

    def _maximum_flow_rule(_, i, o, t):
        """Rule definition for MILP maximum flow constraints."""
        expr = (
            block.status_nominal[i, o, t] * m.flows[i, o].maximum[t]
            >= m.flow[i, o, t]
        )
        return expr

    return Constraint(block.MIN_FLOWS, m.TIMESTEPS, rule=_maximum_flow_rule)


def minimum_flow_constraint(block):
    r"""
    .. math::
        P(t) \geq min(i, o, t) \cdot P_{nom} \
            \cdot Y_{status}(t), \\
        \forall (i, o) \in \textrm{FIXED_CAPACITY_NONCONVEX_FLOWS}, \\
        \forall t \in \textrm{TIMESTEPS}.
    """
    m = block.parent_block()

    def _minimum_flow_rule(_, i, o, t):
        """Rule definition for MILP minimum flow constraints."""
        expr = (
            block.status_nominal[i, o, t] * m.flows[i, o].minimum[t]
            <= m.flow[i, o, t]
        )
        return expr

    return Constraint(block.MIN_FLOWS, m.TIMESTEPS, rule=_minimum_flow_rule)


def startup_costs(block):
    r"""
    .. math::
        \sum_{i, o \in STARTUPFLOWS} \sum_t  Y_{startup}(t) \
        \cdot c_{startup}
    """
    startup_costs = 0

    if block.STARTUPFLOWS:
        m = block.parent_block()

        for i, o in block.STARTUPFLOWS:
            if valid_sequence(
                m.flows[i, o].nonconvex.startup_costs, len(m.TIMESTEPS)
            ):
                startup_costs += sum(
                    block.startup[i, o, t]
                    * m.flows[i, o].nonconvex.startup_costs[t]
                    for t in m.TIMESTEPS
                )

        block.startup_costs = Expression(expr=startup_costs)

    return startup_costs


def shutdown_costs(block):
    r"""
    .. math::
        \sum_{SHUTDOWNFLOWS} \sum_t Y_{shutdown}(t) \
        \cdot c_{shutdown}
    """
    shutdown_costs = 0

    if block.SHUTDOWNFLOWS:
        m = block.parent_block()

        for i, o in block.SHUTDOWNFLOWS:
            if valid_sequence(
                m.flows[i, o].nonconvex.shutdown_costs,
                len(m.TIMESTEPS),
            ):
                shutdown_costs += sum(
                    block.shutdown[i, o, t]
                    * m.flows[i, o].nonconvex.shutdown_costs[t]
                    * m.tsam_weighting[t]
                    for t in m.TIMESTEPS
                )

        block.shutdown_costs = Expression(expr=shutdown_costs)

    return shutdown_costs


def activity_costs(block):
    r"""
    .. math::
        \sum_{ACTIVITYCOSTFLOWS} \sum_t Y_{status}(t) \
        \cdot c_{activity}
    """
    activity_costs = 0

    if block.ACTIVITYCOSTFLOWS:
        m = block.parent_block()

        for i, o in block.ACTIVITYCOSTFLOWS:
            if valid_sequence(
                m.flows[i, o].nonconvex.activity_costs,
                len(m.TIMESTEPS),
            ):
                activity_costs += sum(
                    block.status[i, o, t]
                    * m.flows[i, o].nonconvex.activity_costs[t]
                    * m.tsam_weighting[t]
                    for t in m.TIMESTEPS
                )

        block.activity_costs = Expression(expr=activity_costs)

    return activity_costs


def inactivity_costs(block):
    r"""
    .. math::
        \sum_{INACTIVITYCOSTFLOWS} \sum_t (1 - Y_{status}(t)) \
        \cdot c_{inactivity}
    """
    inactivity_costs = 0

    if block.INACTIVITYCOSTFLOWS:
        m = block.parent_block()

        for i, o in block.INACTIVITYCOSTFLOWS:
            if valid_sequence(
                m.flows[i, o].nonconvex.inactivity_costs,
                len(m.TIMESTEPS),
            ):
                inactivity_costs += sum(
                    (1 - block.status[i, o, t])
                    * m.flows[i, o].nonconvex.inactivity_costs[t]
                    * m.tsam_weighting[t]
                    for t in m.TIMESTEPS
                )

        block.inactivity_costs = Expression(expr=inactivity_costs)

    return inactivity_costs
