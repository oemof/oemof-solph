# -*- coding: utf-8 -*-

"""Constraints to relate variables in an existing model.

SPDX-FileCopyrightText: jnnr

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po


def equate_flows(model, flows1, flows2, factor1=1, name="equate_flows"):
    r"""
    Adds a constraint to the given model that sets the sum of two groups of
    flows equal or proportional by a factor for each timestep.

    **The following constraints are built:**

        .. math::
          \text{factor\_1} \cdot
          \sum_{\text{flow in flows1}} \text{flow}_{t}  =
          \sum_{\text{flow in flows2}} \text{flow}_t \forall t

    Parameters
    ----------
    model : oemof.solph.Model
        Model to which the constraint is added.
    flows1 : iterable
        First group of flows, to be set to equal with Var2 and multiplied with
        factor1.
    flows2 : iterable
        Second group of flows, to be set equal to (Var1 * factor1).
    factor1 : numeric, default=1
        Factor to define the proportion between the two groups.
    name : str, default='equate_flows'
        Name for the equation e.g. in the LP file.

    Returns
    -------
    the updated model.
    """

    def _equate_flow_groups_rule(m):
        for ts in m.TIMESTEPS:
            sum1_t = sum(m.flow[fi, fo, ts] for fi, fo in flows1)
            sum2_t = sum(m.flow[fi, fo, ts] for fi, fo in flows2)
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

    return model


def equate_flows_by_keyword(
    model, keyword1, keyword2, factor1=1, name="equate_flows"
):
    r"""
    This wrapper for equate_flows allows to equate groups of flows by using a
    keyword instead of a list of flows.

    Parameters
    ----------
    model: oemof.solph.Model
        Model to which constraints are added.
    keyword1: string
        keyword to consider (searches all Flows).
    keyword2: string
        keyword to consider (searches all Flows).
    factor1 : numeric, default=1
        Factor to define the proportion between the two groups.
    name : str, default='equate_flows'
        Name for the equation e.g. in the LP file.

    Returns
    -------
    the updated model

    See Also
    --------
    equate_flows(model, flows1, flows2,
                 factor1=1, name="equate_flows")
    """
    flows = {}
    for n, keyword in enumerate([keyword1, keyword2]):
        flows[n] = []
        for i, o in model.flows:
            if hasattr(model.flows[i, o], keyword):
                flows[n].append((i, o))

    return equate_flows(model, flows[0], flows[1], factor1=factor1, name=name)
