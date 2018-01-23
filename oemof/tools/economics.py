# -*- coding: utf-8 -*-

"""Module to collect useful functions for economic calculation.

Copyright (c) 2014-2018 Cord Kaldemeyer, Simon Hilpert, Stefan Günther,
                        Uwe Krien

SPDX-License-Identifier: GPL-3.0-or-later
"""


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
