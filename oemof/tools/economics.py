# -*- coding: utf-8 -*-

"""Module to collect useful functions for economic calculation.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/tools/economics.py

SPDX-License-Identifier: GPL-3.0-or-later
"""


def annuity(capex, n, wacc, **kwargs):
    """Calculate the annuity.

    In case of a single initial investment:

    annuity = capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)
    
    or in case of repeated investments at fixed intervals 'u'
        with decreasing costs 'cost_decrease':

    annuity = capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)*
              ((1-((1-cost_decrease)/(1+wacc))**n)/
              (1-((1-cost_decrease)/(1+wacc))**u)))

    Parameters
    ----------
    capex : float
        Capital expenditure for first investment (NPV of investment)
    n : int
        Number of years investigated; might be an integer multiple of technical
        lifetime (u) in case of repeated investments; in case of a single
        investment n must equal u (economic lifetime)
    wacc : float
        Weighted average cost of capital
    u : int
        Number of years that a single investment is used, i.e. the technical
        lifetime of a single investment
    cost_decrease : float
        Annual rate of cost_decrease for repeated investments; takes the value '0'
        if not set otherwise, that is in case of a single investment or in case
        of no cost decrease for repeated investments

    Returns
    -------
    float : annuity

    """ 
    u  = kwargs.get('u', n)
    cost_decrease = kwargs.get('cost_decrease', 0)

    return (capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)*
                    ((1-((1-cost_decrease)/(1+wacc))**n)/
                    (1-((1-cost_decrease)/(1+wacc))**u)))
