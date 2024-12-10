# -*- coding: utf-8 -*-

"""Limits for investments.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Johannes Giehl

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po

from oemof.solph._plumbing import sequence


def investment_limit(model, limit=None):
    r"""Set an absolute limit for the total investment costs of an investment
    optimization problem (over all periods in case of a multi-period model):

    .. math:: \sum_{investment\_costs} \leq limit

    Parameters
    ----------
    model : oemof.solph._models.Model
        Model to which the constraint is added
    limit : float
        Absolute limit of the investment (i.e. RHS of constraint)
    """

    def investment_rule(m):
        expr = 0

        if hasattr(m, "InvestmentFlowBlock"):
            expr += m.InvestmentFlowBlock.investment_costs

        if hasattr(m, "GenericInvestmentStorageBlock"):
            expr += m.GenericInvestmentStorageBlock.investment_costs

        if hasattr(m, "SinkDSMOemofInvestmentBlock"):
            expr += m.SinkDSMOemofInvestmentBlock.investment_costs

        if hasattr(m, "SinkDSMDIWInvestmentBlock"):
            expr += m.SinkDSMDIWInvestmentBlock.investment_costs

        if hasattr(m, "SinkDSMDLRInvestmentBlock"):
            expr += m.SinkDSMDLRInvestmentBlock.investment_costs

        return expr <= limit

    model.investment_limit = po.Constraint(rule=investment_rule)

    return model


def investment_limit_per_period(model, limit=None):
    r"""Set an absolute limit for the total investment costs of a
    investment optimization problem for each period
    of the multi-period problem.

    .. math::
        \sum_{investment\_costs(p)} \leq limit(p)
        \forall p \in \textrm{PERIODS}

    Parameters
    ----------
    model : oemof.solph.Model
        Model to which the constraint is added
    limit : sequence of float, :math:`limit(p)`
        Absolute limit of the investment for each period
        (i.e. RHS of constraint)
    """

    if model.es.periods is None:
        msg = (
            "investment_limit_per_period is only applicable "
            "for multi-period models.\nIn order to create such a model, "
            "explicitly set attribute `periods` of your energy system."
        )
        raise ValueError(msg)

    if limit is not None:
        limit = sequence(limit)
    else:
        msg = (
            "You have to provide an investment limit for each period!\n"
            "If you provide a scalar value, this will be applied as a "
            "limit for each period."
        )
        raise ValueError(msg)

    def investment_period_rule(m, p):
        expr = 0

        if hasattr(m, "InvestmentFlowBlock"):
            expr += m.InvestmentFlowBlock.period_investment_costs[p]

        if hasattr(m, "GenericInvestmentStorageBlock"):
            expr += m.GenericInvestmentStorageBlock.period_investment_costs[p]

        if hasattr(m, "SinkDSMOemofInvestmentBlock"):
            expr += m.SinkDSMOemofInvestmentBlock.period_investment_costs[p]

        if hasattr(m, "SinkDSMDIWInvestmentBlock"):
            expr += m.SinkDSMDIWInvestmentBlock.period_investment_costs[p]

        if hasattr(m, "SinkDSMDLRInvestmentBlock"):
            expr += m.SinkDSMDLRInvestmentBlock.period_investment_costs[p]

        return expr <= limit[p]

    model.investment_limit_per_period = po.Constraint(
        model.PERIODS, rule=investment_period_rule
    )

    return model


def additional_investment_flow_limit(model, keyword, limit=None):
    r"""
    Global limit for investment flows weighted by an attribute keyword.

    This constraint is only valid for Flows not for components such as an
    investment storage.

    The attribute named by keyword has to be added to every Investment
    attribute of the flow you want to take into account.
    Total value of keyword attributes after optimization can be retrieved
    calling the `oemof.solph._models.Model.invest_limit_${keyword}()`.

    .. math::
        \sum_{p \in \textrm{PERIODS}}
        \sum_{i \in IF}  P_{i}(p) \cdot w_i \leq limit

    With `IF` being the set of InvestmentFlows considered for the integral
    limit.

    The symbols used are defined as follows
    (with Variables (V) and Parameters (P)):

    +------------------+---------------------------------------+------+--------------------------------------------------------------+
    | symbol           | attribute                             | type | explanation                                                  |
    +==================+=======================================+======+==============================================================+
    | :math:`P_{i}(p)` | `InvestmentFlowBlock.invest[i, o, p]` | V    | invested capacity of investment flow in period p             |
    +------------------+---------------------------------------+------+--------------------------------------------------------------+
    | :math:`w_i`      | `keyword`                             | P    | weight given to investment flow named according to `keyword` |
    +------------------+---------------------------------------+------+--------------------------------------------------------------+
    | :math:`limit`    | `limit`                               | P    | global limit given by keyword `limit`                        |
    +------------------+---------------------------------------+------+--------------------------------------------------------------+

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
    >>> date_time_index = pd.date_range('1/1/2020', periods=6, freq='h')
    >>> es = solph.EnergySystem(
    ...     timeindex=date_time_index,
    ...     infer_last_interval=False,
    ... )
    >>> bus = solph.buses.Bus(label='bus_1')
    >>> sink = solph.components.Sink(label="sink", inputs={bus:
    ...     solph.flows.Flow(nominal_capacity=10, fix=[10, 20, 30, 40, 50])})
    >>> src1 = solph.components.Source(
    ...     label='source_0', outputs={bus: solph.flows.Flow(
    ...         nominal_capacity=solph.Investment(
    ...             ep_costs=50, custom_attributes={"space": 4},
    ...         ))
    ...     })
    >>> src2 = solph.components.Source(
    ...     label='source_1', outputs={bus: solph.flows.Flow(
    ...         nominal_capacity=solph.Investment(
    ...              ep_costs=100, custom_attributes={"space": 1},
    ...         ))
    ...     })
    >>> es.add(bus, sink, src1, src2)
    >>> model = solph.Model(es)
    >>> model = solph.constraints.additional_investment_flow_limit(
    ...     model, "space", limit=1500)
    >>> a = model.solve(solver="cbc")
    >>> int(round(model.invest_limit_space()))
    1500
    """  # noqa: E501
    invest_flows = {}

    for i, o in model.flows:
        if hasattr(model.flows[i, o].investment, keyword):
            invest_flows[(i, o)] = model.flows[i, o].investment

    limit_name = "invest_limit_" + keyword

    setattr(
        model,
        limit_name,
        po.Expression(
            expr=sum(
                model.InvestmentFlowBlock.invest[inflow, outflow, p]
                * getattr(invest_flows[inflow, outflow], keyword)
                for (inflow, outflow) in invest_flows
                for p in model.PERIODS
            )
        ),
    )

    setattr(
        model,
        limit_name + "_constraint",
        po.Constraint(expr=(getattr(model, limit_name) <= limit)),
    )

    return model
