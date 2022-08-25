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
from pyomo.core import Constraint


def min_downtime_constraint(block):
    """Factory function for minimum downtime (on non-convex flows)"""
    m = block.parent_block()

    def _min_downtime_rule(_, i, o, t):
        """
        Rule definition for min-downtime constraints of non-convex flows.
        """
        if (
            m.flows[i, o].nonconvex.max_up_down
            <= t
            <= m.TIMESTEPS[-1] - m.flows[i, o].nonconvex.max_up_down
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
        if (
            m.flows[i, o].nonconvex.max_up_down
            <= t
            <= m.TIMESTEPS[-1] - m.flows[i, o].nonconvex.max_up_down
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
