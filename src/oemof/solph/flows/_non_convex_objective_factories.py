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
from pyomo.core import Expression


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
