# -*- coding: utf-8 -*-

"""Constraints to relate variables in an existing model.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po


def equate_variables(model, var1, var2, factor1=1, name=None):
    r"""
    Adds a constraint to the given model that sets two variables to equal adaptable by a factor.

    Parameters
    ----------
    var1 : pyomo.environ.Var
        First variable, to be set to equal with Var2 and multiplied with
        factor1.
    var2 : pyomo.environ.Var
        Second variable, to be set equal to (Var1 * factor1).
    factor1 : float
        Factor to define the proportion between the variables.
    name : str
        Optional name for the equation e.g. in the LP file. By default the
        name is: equate + string representation of var1 and var2.
    model : oemof.solph._models.Model
        Model to which the constraint is added.


    **The following constraints are build:**

    .. math:: var_1 \cdot factor_1 = var_1

    The symbols used are defined as follows (with Variables (V) and Parameters (P)):

    +------------------+---------------------+------+------------------------------------------------------------------------------------------------------------------------------------------------+
    | symbol           | attribute           | type | explanation                                                                                                                                    |
    +==================+=====================+======+================================================================================================================================================+
    | :math:`var_1`    | pyomo.environ.Var`  | V    | First variable, to be set to equal with :math:`var_2` and :math:`var_1` multiplied with :math:`factor_1`                                       |
    +------------------+---------------------+------+------------------------------------------------------------------------------------------------------------------------------------------------+
    | :math:`var_2`    | pyomo.environ.Var`  | V    | Second variable, to be set equal to :math:`var_1 \cdot factor_1`                                                                               |
    +------------------+---------------------+------+------------------------------------------------------------------------------------------------------------------------------------------------+
    | :math:`factor_1` | `float`             | P    | Factor to define the proportion between the variables. The default value is 1.                                                                 |
    +------------------+---------------------+------+------------------------------------------------------------------------------------------------------------------------------------------------+
    | name             | `str`               | P    | | Optional name for the equation e.g. in the LP file.                                                                                          |
    |                  |                     |      | | By default the name is: equate + string representation of :math:`var_1` and :math:`var_2`.                                                   |
    +------------------+---------------------+------+------------------------------------------------------------------------------------------------------------------------------------------------+
    | model            | `oemof.solph.Model` | P    | Model to which the constraint is added                                                                                                         |
    +------------------+---------------------+------+------------------------------------------------------------------------------------------------------------------------------------------------+

    Examples
    --------
    The following example shows how to define a transmission line in the
    investment mode by connecting both investment variables. Note that the
    equivalent periodical costs (epc) of the line are 40. You could also add
    them to one line and set them to 0 for the other line.

    >>> import pandas as pd
    >>> from oemof import solph
    >>> date_time_index = pd.date_range('1/1/2012', periods=6, freq='h')
    >>> energysystem = solph.EnergySystem(
    ...     timeindex=date_time_index,
    ...     infer_last_interval=False,
    ... )
    >>> bel1 = solph.buses.Bus(label='electricity1')
    >>> bel2 = solph.buses.Bus(label='electricity2')
    >>> energysystem.add(bel1, bel2)
    >>> energysystem.add(solph.components.Converter(
    ...    label='powerline_1_2',
    ...    inputs={bel1: solph.flows.Flow()},
    ...    outputs={bel2: solph.flows.Flow(
    ...        nominal_capacity=solph.Investment(ep_costs=20))}))
    >>> energysystem.add(solph.components.Converter(
    ...    label='powerline_2_1',
    ...    inputs={bel2: solph.flows.Flow()},
    ...    outputs={bel1: solph.flows.Flow(
    ...        nominal_capacity=solph.Investment(ep_costs=20))}))
    >>> om = solph.Model(energysystem)
    >>> line12 = energysystem.groups['powerline_1_2']
    >>> line21 = energysystem.groups['powerline_2_1']
    >>> solph.constraints.equate_variables(
    ...    om,
    ...    om.InvestmentFlowBlock.invest[line12, bel2, 0],
    ...    om.InvestmentFlowBlock.invest[line21, bel1, 0])
    """  # noqa: E501
    if name is None:
        name = "_".join(["equate", str(var1), str(var2)])

    def equate_variables_rule(m):
        return var1 * factor1 == var2

    setattr(model, name, po.Constraint(rule=equate_variables_rule))
