# -*- coding: utf-8 -*-

"""Constraints that are shared between non-convex flows.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Johannes Kochems (jokochems)
SPDX-FileCopyrightText: Saeed Sayadi
SPDX-FileCopyrightText: Pierre-François Duc

SPDX-License-Identifier: MIT

"""
from pyomo.core import Binary
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import Set
from pyomo.core import Var


def add_sets_for_non_convex_flows_to_block(block, group):
    block.MIN_FLOWS = Set(
        initialize=[(g[0], g[1]) for g in group if g[2].min[0] is not None]
    )
    block.STARTUPFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.startup_costs[0] is not None
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
            if g[2].nonconvex.shutdown_costs[0] is not None
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
            if g[2].nonconvex.minimum_uptime is not None
        ]
    )
    block.MINDOWNTIMEFLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.minimum_downtime is not None
        ]
    )
    block.NEGATIVE_GRADIENT_FLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.negative_gradient["ub"][0] is not None
        ]
    )
    block.POSITIVE_GRADIENT_FLOWS = Set(
        initialize=[
            (g[0], g[1])
            for g in group
            if g[2].nonconvex.positive_gradient["ub"][0] is not None
        ]
    )


def add_variables_for_non_convex_flows_to_block(block):
    m = block.parent_block()

    if block.STARTUPFLOWS:
        block.startup = Var(block.STARTUPFLOWS, m.TIMESTEPS, within=Binary)

    if block.SHUTDOWNFLOWS:
        block.shutdown = Var(block.SHUTDOWNFLOWS, m.TIMESTEPS, within=Binary)

    if block.POSITIVE_GRADIENT_FLOWS:
        block.positive_gradient = Var(
            block.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS
        )

    if block.NEGATIVE_GRADIENT_FLOWS:
        block.negative_gradient = Var(
            block.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS
        )


def startup_costs(block):
    r"""
    :param block:
    :return:

    If `nonconvex.startup_costs` is set by the user:
    .. math::
        \sum_{i, o \in STARTUPFLOWS} \sum_t  startup(i, o, t) \
        \cdot startup\_costs(i, o)
    """
    _startup_costs = 0

    if block.STARTUPFLOWS:
        m = block.parent_block()

        for i, o in block.STARTUPFLOWS:
            if m.flows[i, o].nonconvex.startup_costs[0] is not None:
                _startup_costs += sum(
                    block.startup[i, o, t]
                    * m.flows[i, o].nonconvex.startup_costs[t]
                    for t in m.TIMESTEPS
                )
        block.startup_costs = Expression(expr=_startup_costs)

    return _startup_costs


def shutdown_costs(block):
    r"""
    :param block:
    :return:

    If `nonconvex.shutdown_costs` is set by the user:
    .. math::
        \sum_{i, o \in SHUTDOWNFLOWS} \sum_t shutdown(i, o, t) \
        \cdot shutdown\_costs(i, o)
    """
    _shutdown_costs = 0

    if block.SHUTDOWNFLOWS:
        m = block.parent_block()

        for i, o in block.SHUTDOWNFLOWS:
            if m.flows[i, o].nonconvex.shutdown_costs[0] is not None:
                _shutdown_costs += sum(
                    block.shutdown[i, o, t]
                    * m.flows[i, o].nonconvex.shutdown_costs[t]
                    for t in m.TIMESTEPS
                )
        block.shutdown_costs = Expression(expr=_shutdown_costs)

    return _shutdown_costs


def _time_step_allows_flexibility(t, max_up_down, last_step):
    return max_up_down <= t <= last_step - max_up_down


def min_downtime_constraint(block):
    """Factory function for minimum downtime (on non-convex flows)"""
    m = block.parent_block()

    def _min_downtime_rule(_, i, o, t):
        """
        Rule definition for min-downtime constraints of non-convex flows.
        """
        if _time_step_allows_flexibility(
            t, m.flows[i, o].nonconvex.max_up_down, m.TIMESTEPS[-1]
        ):
            expr = 0
            expr += (
                block.status[i, o, t - 1] - block.status[i, o, t]
            ) * m.flows[i, o].nonconvex.minimum_downtime
            expr += -m.flows[i, o].nonconvex.minimum_downtime
            expr += sum(
                block.status[i, o, t + d]
                for d in range(0, m.flows[i, o].nonconvex.minimum_downtime)
            )
            return expr <= 0
        else:
            expr = 0
            expr += block.status[i, o, t]
            expr += -m.flows[i, o].nonconvex.initial_status
            return expr == 0

    return Constraint(
        block.MINDOWNTIMEFLOWS, m.TIMESTEPS, rule=_min_downtime_rule
    )


def min_uptime_constraint(block):
    """Factory function for minimum uptime (on non-convex flows)"""
    m = block.parent_block()

    def _min_uptime_rule(_, i, o, t):
        """
        Rule definition for min-uptime constraints of non-convex flows.
        """
        if _time_step_allows_flexibility(
            t, m.flows[i, o].nonconvex.max_up_down, m.TIMESTEPS[-1]
        ):
            expr = 0
            expr += (
                block.status[i, o, t] - block.status[i, o, t - 1]
            ) * m.flows[i, o].nonconvex.minimum_uptime
            expr += -sum(
                block.status[i, o, t + u]
                for u in range(0, m.flows[i, o].nonconvex.minimum_uptime)
            )
            return expr <= 0
        else:
            expr = 0
            expr += block.status[i, o, t]
            expr += -m.flows[i, o].nonconvex.initial_status
            return expr == 0

    return Constraint(block.MINUPTIMEFLOWS, m.TIMESTEPS, rule=_min_uptime_rule)


def shutdown_constraint(block):
    """Factory function for shutdowns (on non-convex flows)"""
    m = block.parent_block()

    def _shutdown_rule(_, i, o, t):
        """Rule definition for shutdown constraints of non-convex flows."""
        if t > m.TIMESTEPS[1]:
            expr = (
                block.shutdown[i, o, t]
                >= block.status[i, o, t - 1] - block.status[i, o, t]
            )
        else:
            expr = (
                block.shutdown[i, o, t]
                >= m.flows[i, o].nonconvex.initial_status
                - block.status[i, o, t]
            )
        return expr

    return Constraint(block.SHUTDOWNFLOWS, m.TIMESTEPS, rule=_shutdown_rule)


def startup_constraint(block):
    """Factory function for startups (of non-convex flows)"""
    m = block.parent_block()

    def _startup_rule(_, i, o, t):
        """Rule definition for startup constraint of nonconvex flows."""
        if t > m.TIMESTEPS[1]:
            expr = (
                block.startup[i, o, t]
                >= block.status[i, o, t] - block.status[i, o, t - 1]
            )
        else:
            expr = (
                block.startup[i, o, t]
                >= block.status[i, o, t]
                - m.flows[i, o].nonconvex.initial_status
            )
        return expr

    return Constraint(block.STARTUPFLOWS, m.TIMESTEPS, rule=_startup_rule)


def max_startup_constraint(block):
    """Factory function for maximum number of startups

    Will only run if startup_constraint is also defined.
    """
    m = block.parent_block()

    def _max_startup_rule(_, i, o):
        """Rule definition for maximum number of start-ups."""
        lhs = sum(block.startup[i, o, t] for t in m.TIMESTEPS)
        return lhs <= m.flows[i, o].nonconvex.maximum_startups

    return Constraint(block.MAXSTARTUPFLOWS, rule=_max_startup_rule)


def max_shutdown_constraint(block):
    """Factory function for maximum number of startups

    Will only run if shutdown_constraint is also defined.
    """
    m = block.parent_block()

    def _max_shutdown_rule(_, i, o):
        """Rule definition for maximum number of start-ups."""
        lhs = sum(block.shutdown[i, o, t] for t in m.TIMESTEPS)
        return lhs <= m.flows[i, o].nonconvex.maximum_shutdowns

    return Constraint(block.MAXSHUTDOWNFLOWS, rule=_max_shutdown_rule)


def maximum_flow_constraint(block):
    """Factory function for maximum of flows"""
    m = block.parent_block()

    def _maximum_flow_rule(_, i, o, t):
        """Rule definition for MILP maximum flow constraints."""
        expr = (
            block.status_nominal[i, o, t] * m.flows[i, o].max[t]
            >= m.flow[i, o, t]
        )
        return expr

    return Constraint(block.MIN_FLOWS, m.TIMESTEPS, rule=_maximum_flow_rule)


def minimum_flow_constraint(block):
    """Factory function for minimum of flows"""
    m = block.parent_block()

    def _minimum_flow_rule(_, i, o, t):
        """Rule definition for MILP minimum flow constraints."""
        expr = (
            block.status_nominal[i, o, t] * m.flows[i, o].min[t]
            <= m.flow[i, o, t]
        )
        return expr

    return Constraint(block.MIN_FLOWS, m.TIMESTEPS, rule=_minimum_flow_rule)


def add_constraints_to_non_convex_block(block):
    m = block.parent_block()

    block.startup_constr = startup_constraint(block)
    block.max_startup_constr = max_startup_constraint(block)
    block.shutdown_constr = shutdown_constraint(block)
    block.max_shutdown_constr = max_shutdown_constraint(block)
    block.min_uptime_constr = min_uptime_constraint(block)
    block.min_downtime_constr = min_downtime_constraint(block)

    def _positive_gradient_flow_rule(_):
        """Rule definition for positive gradient constraint."""
        for i, o in block.POSITIVE_GRADIENT_FLOWS:
            for t in m.TIMESTEPS:
                if t > 0:
                    lhs = (
                        m.flow[i, o, t] * block.status[i, o, t]
                        - m.flow[i, o, t - 1] * block.status[i, o, t - 1]
                    )
                    rhs = block.positive_gradient[i, o, t]
                    block.positive_gradient_constr.add((i, o, t), lhs <= rhs)
                else:
                    pass  # return(Constraint.Skip)

    block.positive_gradient_constr = Constraint(
        block.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
    )
    block.positive_gradient_build = BuildAction(
        rule=_positive_gradient_flow_rule
    )

    def _negative_gradient_flow_rule(_):
        """Rule definition for negative gradient constraint."""
        for i, o in block.NEGATIVE_GRADIENT_FLOWS:
            for t in m.TIMESTEPS:
                if t > 0:
                    lhs = (
                        m.flow[i, o, t - 1] * block.status[i, o, t - 1]
                        - m.flow[i, o, t] * block.status[i, o, t]
                    )
                    rhs = block.negative_gradient[i, o, t]
                    block.negative_gradient_constr.add((i, o, t), lhs <= rhs)
                else:
                    pass  # return(Constraint.Skip)

    block.negative_gradient_constr = Constraint(
        block.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
    )
    block.negative_gradient_build = BuildAction(
        rule=_negative_gradient_flow_rule
    )
