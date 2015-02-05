#!/usr/bin/python
# -*- coding: utf-8 -*-


def crf_calc(lifetime, wacc, cost_opt=True):
    r'''Returns the Capital Recovery Factor (CRF) using the
    Weighted Average Cost of Capital (WACC)

    Parameters
    ----------
    liftime : integer
        years of liftime
    wacc : float
        Weighted Average Cost of Capital [1]_
    cost_opt : boolean
        True if optimisation is set to "cost minimisation" (default: True).

    Returns
    -------
    crf : float
        Capital Recovery Factor (CRF) [2]_

    Notes
    -----
    Formular to calculate the Capital Recovery Factor:

    .. math::
        crf=\frac{wacc\cdot\left(1+wacc\right)^{lifetime}}{
        \left(\left(1+wacc\right)^{lifetime}\right)-1}

       \lim\limits _{wacc\to0}crf=\frac{1}{lifetime}


    References
    ----------

    .. [1]
        `WACC <http://en.wikipedia.org/wiki/Weighted_average_cost_of_capital>`_
    .. [2] `CRF <http://en.wikipedia.org/wiki/Capital_recovery_factor>`_

    '''

    if wacc != 0 and cost_opt:
        crf = (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)
    else:
        crf = 1 / lifetime
    return crf
