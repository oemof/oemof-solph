# -*- coding: utf-8 -*-

"""Module to collect useful functions for economic calculation.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/tools/economics.py

SPDX-License-Identifier: MIT
"""


def annuity(capex, n, wacc, u=None, cost_decrease=0):
    """Calculates the annuity of an initial investment 'capex', considering the 
    cost of capital 'wacc' during a project horizon 'n'

    In case of a single initial investment, the employed formula reads:

    .. math::
    annuity = capex \cdot \frac{(wacc \cdot (1+wacc)^n)}
              {((1 + wacc)^n - 1)}
    
    In case of repeated investments (due to replacements) at fixed intervals 
    'u', the formula yields:

    .. math::
    annuity = capex \cdot \frac{(wacc \cdot (1+wacc)^n)}
              {((1 + wacc)^n - 1)} \cdot \left( 
              \frac{1 - \left( \frac{(1-cost\_decrease)}
              {(1+wacc)} \right)^n}
              {1 - \left( \frac{(1-cost\_decrease)}{(1+wacc)}
              \right)^u} \right)

    Parameters
    ----------
    capex : float
        Capital expenditure for first investment. Net Present Value (NPV) or
        Net Present Cost (NPC) of investment
    n : int
        Horizon of the analysis, or number of years the annuity wants to be 
        obtained for (n>=1)
    wacc : float
        Weighted average cost of capital (0<wacc<1)
    u : int
        Lifetime of the investigated investment. Might be smaller than the 
        analysis horizon, 'n', meaning it will have to be replaced. 
        Takes value 'n' if not specified otherwise (u>=1)
    cost_decrease : float
        Annual rate of cost decrease (due to, e.g., price experience curve). 
        This only influences the result for investments corresponding to 
        replacements, whenever u<n. 
        Takes value 0, if not specified otherwise (0<cost_decrease<1)
    Returns
    -------
    float 
        annuity
    """ 
    if u is None:
        u = n
        
    if ((n < 1) or (wacc < 0 or wacc > 1) or (u < 1) or
            (cost_decrease < 0 or cost_decrease > 1)):
        raise ValueError("Input arguments for 'annuity' out of bounds!")

    return (
        capex * (wacc*(1+wacc)**n) / ((1 + wacc)**n - 1) *
        ((1 - ((1-cost_decrease)/(1+wacc))**n) /
         (1 - ((1-cost_decrease)/(1+wacc))**u)))
