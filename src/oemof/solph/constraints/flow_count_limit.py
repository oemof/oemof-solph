# -*- coding: utf-8 -*-

"""Constraints to limit active (nonconvex) Flows.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po


def limit_active_flow_count(
    model, constraint_name, flows, lower_limit=0, upper_limit=None
):
    r"""
    Set limits (lower and/or upper) for the number of concurrently
    active NonConvex flows. The flows are given as a list.

    Total actual counts after optimization can be retrieved
    calling the `oemof.solph.Model.$(constraint_name)_count()`.

    Parameters
    ----------
    model: oemof.solph.Model
        Model to which constraints are added
    constraint_name: string
        name for the constraint
    flows: list of flows
        flows (have to be NonConvex) in the format [(in, out)]
    lower_limit: integer
        minimum number of active flows in the list
    upper_limit: integer
        maximum number of active flows in the list

    Returns
    -------
    the updated model

    Note
    ----
    SimpleFlowBlock objects required to be NonConvex


    **Constraint:**

    .. math:: N_{X,min} \le \sum_{n \in F} X_n(t)
                        \le N_{X,max} \forall t \in T

    With `F` being the set of considered flows and
    `T` being the set of time steps.

    The symbols used are defined as follows
    (with Variables (V) and Parameters (P)):

    +-------------------+------+--------------------------------------------------------------+
    | symbol            | type | explanation                                                  |
    +===================+======+==============================================================+
    | :math:`X_n(t)`    | V    | status (0 or 1) of the flow :math:`n` at time step :math:`t` |
    +-------------------+------+--------------------------------------------------------------+
    | :math:`N_{X,min}` | P    | lower_limit                                                  |
    +-------------------+------+--------------------------------------------------------------+
    | :math:`N_{X,max}` | P    | upper_limit                                                  |
    +-------------------+------+--------------------------------------------------------------+
    """  # noqa: E501

    # number of concurrent active flows
    setattr(model, constraint_name, po.Var(model.TIMESTEPS))

    for t in model.TIMESTEPS:
        getattr(model, constraint_name)[t].setlb(lower_limit)
        getattr(model, constraint_name)[t].setub(upper_limit)

    attrname_constraint = constraint_name + "_constraint"

    def _flow_count_rule(m):
        for ts in m.TIMESTEPS:
            lhs = sum(
                m.NonConvexFlowBlock.status[fi, fo, ts] for fi, fo in flows
            )
            rhs = getattr(model, constraint_name)[ts]
            expr = lhs == rhs
            if expr is not True:
                getattr(m, attrname_constraint).add(ts, expr)

    setattr(
        model,
        attrname_constraint,
        po.Constraint(model.TIMESTEPS, noruleinit=True),
    )
    setattr(
        model,
        attrname_constraint + "_build",
        po.BuildAction(rule=_flow_count_rule),
    )

    return model


def limit_active_flow_count_by_keyword(
    model, keyword, lower_limit=0, upper_limit=None
):
    r"""
    This wrapper for limit_active_flow_count allows to set limits
    to the count of concurrently active flows by using a keyword
    instead of a list. The constraint will be named $(keyword)_count.

    Parameters
    ----------
    model: oemof.solph.Model
        Model to which constraints are added
    keyword: string
        keyword to consider (searches all NonConvexFlows)
    lower_limit: integer
        minimum number of active flows having the keyword
    upper_limit: integer
        maximum number of active flows having the keyword

    Returns
    -------
    the updated model

    See Also
    --------
    limit_active_flow_count
    """
    flows = []
    for i, o in model.NonConvexFlowBlock.NONCONVEX_FLOWS:
        if hasattr(model.flows[i, o], keyword):
            flows.append((i, o))

    return limit_active_flow_count(
        model,
        keyword,
        flows=flows,
        lower_limit=lower_limit,
        upper_limit=upper_limit,
    )
