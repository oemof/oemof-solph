# -*- coding: utf-8 -*-

"""Module to collect useful functions for economic calculation.
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"


def annuity(capex, n, wacc):
    """
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
    float

    """
    return capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)
