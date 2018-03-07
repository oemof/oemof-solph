# -*- coding: utf-8 -*-

"""Module to collect useful functions for economic calculation.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/tools/economics.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from collections import namedtuple


def annuity(capex, n, wacc):
    """Calculate the annuity.

    annuity = capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)

    Parameters
    ----------
    capex : float
        Capital expenditure (NPV of investment)
    n : int
        Number of years that the investment is used (economic lifetime)
    wacc : float
        Weighted average cost of capital

    Returns
    -------
    float : annuity

    """
    return capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)


LCOE = namedtuple('LCOE', ['invest', 'opex', 'fuel_cost'])


def lcoe(energy_output, annualized_investment, opex, fuel_costs=0.0):
    """
    Calculates levelized cost of energy (electricity)

    lcoe = (annualized_investment + opex + fuel_costs) / energy_output

    LCOE are split into "invest", "opex" and "fuel_cost".

    Parameters
    ----------
    energy_output: float
        Energy output per year
    annualized_investment: float
        Investment per year
    opex: float
        OPEX (maintaing costs) per year
    fuel_costs: float
        Fuel costs per year

    Returns
    -------
    LCOE (collections.namedtuple):
        LCOE is split up into its different parts (invest, opex, fuel). Total
        LCOE is given by: LCOE_total = sum(LCOE)
    """
    if energy_output == 0.0:
        return None
    return LCOE(
        *map(
            lambda x: x / energy_output,
            [annualized_investment, opex, fuel_costs]
        )
    )
