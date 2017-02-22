# -*- coding: utf-8 -*-
"""
Module to collect useful functions for economic calculation.

"""

def annuity(capex, n, wacc):
    """
    """
    return capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)