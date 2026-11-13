# -*- coding: utf-8 -*-

"""Constraints to relate variables in an existing model.

SPDX-FileCopyrightText: jnnr

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po
from collections.abc import Iterable

from oemof.network import Node

from oemof.solph import Model


def equate_flows(
    model: Model | po.ConcreteModel,
    flows1: Iterable[tuple[Node, Node]],
    flows2: Iterable[tuple[Node, Node]],
    factor1: float = 1,
    name: str = "equate_flows",
):
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
    model : oemof.solph.Model or pyomo.environ.ConcreteModel
        Model to which the constraint is added.
    flows1 : Iterable of tuples
        First group of flows. The iterable must contain tuples of Nodes. The
        Nodes within the tuples are expected to represent `(source, target)`,
        like a key of `model.flows`. The iterable must be re-iterable (like a
        `list` or `dict`).
    flows2 : Iterable of tuples
        Second group of flows. See `flows1` for a description.
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
    model: Model | po.ConcreteModel,
    keyword1: str,
    keyword2: str,
    factor1: float = 1,
    name: str = "equate_flows",
):
    r"""
    This wrapper for equate_flows allows to equate groups of flows by using a
    keyword instead of a list of flows.

    Parameters
    ----------
    model: oemof.solph.Model or po.environ.ConcreteModel
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
            if keyword in model.flows[i, o].custom_properties:
                flows[n].append((i, o))

    return equate_flows(model, flows[0], flows[1], factor1=factor1, name=name)
