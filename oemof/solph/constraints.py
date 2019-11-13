# -*- coding: utf-8 -*-

"""Additional constraints to be used in an oemof energy model.
This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/constraints.py

SPDX-License-Identifier: MIT
"""

import pyomo.environ as po
from oemof.solph.plumbing import sequence


def investment_limit(model, limit=None):
    """ Set an absolute limit for the total investment costs of an investment
    optimization problem:

    .. math:: \sum_{investment\_costs} \leq limit

    Parameters
    ----------
    model : oemof.solph.Model
        Model to which the constraint is added
    limit : float
        Absolute limit of the investment (i.e. RHS of constraint)
    """

    def investment_rule(m):
        expr = 0

        if hasattr(m, "InvestmentFlow"):
            expr += m.InvestmentFlow.investment_costs

        if hasattr(m, "GenericInvestmentStorageBlock"):
            expr += m.GenericInvestmentStorageBlock.investment_costs
        return expr <= limit

    model.investment_limit = po.Constraint(rule=investment_rule)

    return model


def emission_limit(om, flows=None, limit=None):
    """
    Short handle for generic_integral_limit() with keyword="emission_factor".

    Note
    ----
    Flow objects required an attribute "emission_factor"!

    """
    generic_integral_limit(om,
                           keyword='emission_factor',
                           flows=flows,
                           limit=limit)


def generic_integral_limit(om, keyword, flows=None, limit=None):
    """Set a global limit for flows weighted by attribute called keyword.
    The attribute named by keyword has to be added
    to every flow you want to take into account.

    Total value of keyword attributes after optimization can be retrieved
    calling the :attr:`om.oemof.solph.Model.integral_limit_${keyword}()`.

    Parameters
    ----------
    om : oemof.solph.Model
        Model to which constraints are added.
    flows : dict
        Dictionary holding the flows that should be considered in constraint.
        Keys are (source, target) objects of the Flow. If no dictionary is
        given all flows containing the keyword attribute will be
        used.
    keyword : attribute to consider
    limit : numeric
        Absolute limit of keyword attribute for the energy system.

    Note
    ----
    Flow objects required an attribute named like keyword!

    **Constraint:**

    .. math:: \sum_{i \in F_E} \sum_{t \in T} P_i(t) \cdot w_i(t)
               \cdot \tau(t) \leq M


    With `F_I` being the set of flows considered for the integral limit and
    `T` being the set of time steps.

    The symbols used are defined as follows
    (with Variables (V) and Parameters (P)):

    ================ ==== =====================================================
    math. symbol     type explanation
    ================ ==== =====================================================
    :math:`P_n(t)`   V    power flow :math:`n` at time step :math:`t`
    :math:`w_N(t)`   P    weight given to Flow named according to `keyword`
    :math:`\tau(t)`  P    width of time step :math:`t`
    :math:`L`        P    global limit given by keyword `limit`

    """
    if flows is None:
        flows = {}
        for (i, o) in om.flows:
            if hasattr(om.flows[i, o], keyword):
                flows[(i, o)] = om.flows[i, o]

    else:
        for (i, o) in flows:
            if not hasattr(flows[i, o], keyword):
                raise AttributeError(
                    ('Flow with source: {0} and target: {1} '
                     'has no attribute {2}.').format(
                        i.label, o.label, keyword))

    limit_name = "integral_limit_"+keyword

    setattr(om, limit_name, po.Expression(
        expr=sum(om.flow[inflow, outflow, t]
                 * om.timeincrement[t]
                 * sequence(getattr(flows[inflow, outflow], keyword))[t]
                 for (inflow, outflow) in flows
                 for t in om.TIMESTEPS)))

    setattr(om, limit_name+"_constraint", po.Constraint(
        expr=(getattr(om, limit_name) <= limit)))

    return om


def equate_variables(model, var1, var2, factor1=1, name=None):
    r"""
    Adds a constraint to the given model that set two variables to equal
    adaptable by a factor.

    **The following constraints are build:**

      .. math::
        var\textit{1} \cdot factor\textit{1} = var\textit{2}

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
    model : oemof.solph.Model
        Model to which the constraint is added.

    Examples
    --------
    The following example shows how to define a transmission line in the
    investment mode by connecting both investment variables. Note that the
    equivalent periodical costs (epc) of the line are 40. You could also add
    them to one line and set them to 0 for the other line.

    >>> import pandas as pd
    >>> from oemof import solph
    >>> date_time_index = pd.date_range('1/1/2012', periods=5, freq='H')
    >>> energysystem = solph.EnergySystem(timeindex=date_time_index)
    >>> bel1 = solph.Bus(label='electricity1')
    >>> bel2 = solph.Bus(label='electricity2')
    >>> energysystem.add(bel1, bel2)
    >>> energysystem.add(solph.Transformer(
    ...    label='powerline_1_2',
    ...    inputs={bel1: solph.Flow()},
    ...    outputs={bel2: solph.Flow(
    ...        investment=solph.Investment(ep_costs=20))}))
    >>> energysystem.add(solph.Transformer(
    ...    label='powerline_2_1',
    ...    inputs={bel2: solph.Flow()},
    ...   outputs={bel1: solph.Flow(
    ...       investment=solph.Investment(ep_costs=20))}))
    >>> om = solph.Model(energysystem)
    >>> line12 = energysystem.groups['powerline_1_2']
    >>> line21 = energysystem.groups['powerline_2_1']
    >>> solph.constraints.equate_variables(
    ...    om,
    ...    om.InvestmentFlow.invest[line12, bel2],
    ...    om.InvestmentFlow.invest[line21, bel1])
    """
    if name is None:
        name = '_'.join(["equate", str(var1), str(var2)])

    def equate_variables_rule(m):
        return var1 * factor1 == var2
    setattr(model, name, po.Constraint(rule=equate_variables_rule))
