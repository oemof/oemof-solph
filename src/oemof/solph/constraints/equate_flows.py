# -*- coding: utf-8 -*-

"""Constraints to relate variables in an existing model.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po


def equate_flows(model, flows1, flows2, factor1=1, name="equate_flows"):
    r"""
    Adds a constraint to the given model that sets the sum of two groups of
    flows equal or proportional by a factor.
    """
    def _equate_flow_groups_rule(m):
        for ts in m.TIMESTEPS:
            sum1_t = sum(
                m.flow[fi, fo, ts] for fi, fo in flows1
            )
            sum2_t = sum(
                m.flow[fi, fo, ts] for fi, fo in flows2
            )
            expr = sum1_t * factor1 == sum2_t
            if expr is not True:
                getattr(m, name).add(ts, expr)

    setattr(
        model,
        name,
        po.Constraint(model.TIMESTEPS, noruleinit=True),
    )
    setattr(
        model,
        name + "_build",
        po.BuildAction(rule=_equate_flow_groups_rule),
    )


def equate_flows_by_keyword(model, keyword1, keyword2, factor1=1, name="equate_flows"):
    r"""
    This wrapper for equate_flows allows to equate groups of flows by using a keyword
    instead of a list of flows.
    """
    flows = {}
    for n, keyword in enumerate([keyword1, keyword2]):
        flows[n] = []
        for (i, o) in model.flows:
            if hasattr(model.flows[i, o], keyword):
                flows[n].append((i, o))

    return equate_flows(
        model,
        flows[0],
        flows[1],
        factor1=factor1,
        name=name
    )
