# -*- coding: utf-8 -*-

"""Limits for investments.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po


def investment_limit(model, limit=None):
    r"""Set an absolute limit for the total investment costs of an investment
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


def additional_investment_flow_limit(model, keyword, limit=None):
    r"""
    Global limit for investment flows weighted by an attribute keyword.

    This constraint is only valid for Flows not for components such as an
    investment storage.

    The attribute named by keyword has to be added to every Investment
    attribute of the flow you want to take into account.
    Total value of keyword attributes after optimization can be retrieved
    calling the :attr:`oemof.solph.Model.invest_limit_${keyword}()`.

    .. math:: \sum_{i \in IF}  P_i \cdot w_i \leq limit

    With `IF` being the set of InvestmentFlows considered for the integral
    limit.

    The symbols used are defined as follows
    (with Variables (V) and Parameters (P)):

    +---------------+-------------------------------+------+--------------------------------------------------------------+
    | symbol        | attribute                     | type | explanation                                                  |
    +===============+===============================+======+==============================================================+
    | :math:`P_{i}` | `InvestmentFlow.invest[i, o]` | V    | installed capacity of investment flow                        |
    +---------------+-------------------------------+------+--------------------------------------------------------------+
    | :math:`w_i`   | `keyword`                     | P    | weight given to investment flow named according to `keyword` |
    +---------------+-------------------------------+------+--------------------------------------------------------------+
    | :math:`limit` | `limit`                       | P    | global limit given by keyword `limit`                        |
    +---------------+-------------------------------+------+--------------------------------------------------------------+

    Parameters
    ----------
    model : oemof.solph.Model
        Model to which constraints are added.
    keyword : attribute to consider
        All flows with Investment attribute containing the keyword will be
        used.
    limit : numeric
        Global limit of keyword attribute for the energy system.

    Note
    ----
    The Investment attribute of the considered (Investment-)flows requires an
    attribute named like keyword!

    Examples
    --------
    >>> import pandas as pd
    >>> from oemof import solph
    >>> date_time_index = pd.date_range('1/1/2020', periods=5, freq='H')
    >>> es = solph.EnergySystem(timeindex=date_time_index)
    >>> bus = solph.Bus(label='bus_1')
    >>> sink = solph.Sink(label="sink", inputs={bus:
    ...     solph.Flow(nominal_value=10, fix=[10, 20, 30, 40, 50])})
    >>> src1 = solph.Source(label='source_0', outputs={bus: solph.Flow(
    ...     investment=solph.Investment(ep_costs=50, space=4))})
    >>> src2 = solph.Source(label='source_1', outputs={bus: solph.Flow(
    ...     investment=solph.Investment(ep_costs=100, space=1))})
    >>> es.add(bus, sink, src1, src2)
    >>> model = solph.Model(es)
    >>> model = solph.constraints.additional_investment_flow_limit(
    ...     model, "space", limit=1500)
    >>> a = model.solve(solver="cbc")
    >>> int(round(model.invest_limit_space()))
    1500
    """  # noqa: E501
    invest_flows = {}

    for (i, o) in model.flows:
        if hasattr(model.flows[i, o].investment, keyword):
            invest_flows[(i, o)] = model.flows[i, o].investment

    limit_name = "invest_limit_" + keyword

    setattr(
        model,
        limit_name,
        po.Expression(
            expr=sum(
                model.InvestmentFlow.invest[inflow, outflow]
                * getattr(invest_flows[inflow, outflow], keyword)
                for (inflow, outflow) in invest_flows
            )
        ),
    )

    setattr(
        model,
        limit_name + "_constraint",
        po.Constraint(expr=(getattr(model, limit_name) <= limit)),
    )

    return model
