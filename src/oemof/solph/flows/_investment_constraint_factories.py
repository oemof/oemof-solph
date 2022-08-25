# -*- coding: utf-8 -*-

"""Constraints that are shared between investment flows.

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


def minimum_investment_constraint(block):
    """Constraint factory for a minimum investment"""
    m = block.parent_block()

    def _min_invest_rule(_, i, o):
        """Rule definition for applying a minimum investment"""
        expr = (
            m.flows[i, o].investment.minimum * block.invest_status[i, o]
            <= block.invest[i, o]
        )
        return expr

    return Constraint(block.NON_CONVEX_INVESTFLOWS, rule=_min_invest_rule)


def maximum_investment_constraint(block):
    """Constraint factory for a maximum investment"""
    m = block.parent_block()

    def _max_invest_rule(_, i, o):
        """Rule definition for applying a minimum investment"""
        expr = block.invest[i, o] <= (
            m.flows[i, o].investment.maximum * block.invest_status[i, o]
        )
        return expr

    return Constraint(block.NON_CONVEX_INVESTFLOWS, rule=_max_invest_rule)
