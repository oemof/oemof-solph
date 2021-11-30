# -*- coding: utf-8 -*-

"""Constraints to limit total values that are dependent on several Flows.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Johannes Giehl

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po

from oemof.solph.plumbing import sequence


def emission_limit(om, flows=None, limit=None):
    r"""
    Short handle for generic_integral_limit() with keyword="emission_factor".

    Note
    ----
    Flow objects required an attribute "emission_factor"!

    """
    generic_integral_limit(
        om, keyword="emission_factor", flows=flows, limit=limit
    )


def emission_limit_per_period(om, flows=None, limit=None):
    r"""
    Short handle for generic_periodical_integral_limit()
    with keyword="emission_factor". Only applicable for multi-period models.

    Note
    ----
    Flow objects required an attribute "emission_factor"!

    """
    generic_periodical_integral_limit(
        om, keyword="emission_factor", flows=flows, limit=limit
    )


def generic_integral_limit(om, keyword, flows=None, limit=None):
    r"""Set a global limit for flows weighted by attribute called keyword.
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
    keyword : string
        attribute to consider
    limit : numeric
        Absolute limit of keyword attribute for the energy system.

    Note
    ----
    Flow objects required an attribute named like keyword!

    **Constraint:**

    * Standard model:
        .. math:: \sum_{i \in F_I} \sum_{t \in T} P_i(t) \cdot w_i(t)
                   \cdot \tau(t) \leq L
    * Model:
        .. math:: \sum_{i \in F_I} \sum_{p, t \in \textrm{TIMEINDEX}}
                    P_i(p, t) \cdot w_i(t) \cdot \tau(t) \leq L


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
    ================ ==== =====================================================

    Examples
    --------
    >>> import pandas as pd
    >>> from oemof import solph
    >>> date_time_index = pd.date_range('1/1/2012', periods=5, freq='H')
    >>> energysystem = solph.EnergySystem(timeindex=date_time_index)
    >>> bel = solph.Bus(label='electricityBus')
    >>> flow1 = solph.Flow(nominal_value=100, my_factor=0.8)
    >>> flow2 = solph.Flow(nominal_value=50)
    >>> src1 = solph.Source(label='source1', outputs={bel: flow1})
    >>> src2 = solph.Source(label='source2', outputs={bel: flow2})
    >>> energysystem.add(bel, src1, src2)
    >>> model = solph.Model(energysystem)
    >>> flow_with_keyword = {(src1, bel): flow1, }
    >>> model = solph.constraints.generic_integral_limit(
    ...     model, "my_factor", flow_with_keyword, limit=777)
    """
    flows = _check_and_set_flows(om, flows, keyword)
    limit_name = "integral_limit_" + keyword

    setattr(
        om,
        limit_name,
        po.Expression(
            expr=sum(
                om.flow[inflow, outflow, p, t]
                * om.timeincrement[t]
                * sequence(getattr(flows[inflow, outflow], keyword))[t]
                for (inflow, outflow) in flows
                for p, t in om.TIMEINDEX
            )
        ),
    )

    setattr(
        om,
        limit_name + "_constraint",
        po.Constraint(expr=(getattr(om, limit_name) <= limit)),
    )

    return om


def generic_periodical_integral_limit(om, keyword, flows=None, limit=None):
    r"""Set a global limit for flows for each period of a multi-period model
    which is weighted by attribute called keyword.
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
    keyword : string
        attribute to consider
    limit : sequence of float
        Absolute limit of keyword attribute for the energy system.

    Note
    ----
    Flow objects required an attribute named like keyword!

    **Constraint:**

    .. math:: \sum_{i \in F_I} \sum_{t \in T} P_i(t) \cdot w_i(t)
               \cdot \tau(t) \leq L(p) \forall p in \textrm{PERIODS}


    For the parameter and variable explanation, please refer to the docs
    of generic_integral_limit.

    """
    flows = _check_and_set_flows(om, flows, keyword)
    limit_name = "integral_limit_" + keyword

    if not om.es.multi_period:
        msg = ("generic_periodical_integral_limit is only applicable\n"
               "for multi-period models.\nFor standard models, use "
               "generic_integral_limit instead.")
        raise ValueError(msg)

    if limit is not None:
        limit = sequence(limit)
    else:
        msg = ("You have to provide a limit for each period!\n"
               "If you provide a scalar value, this will be applied as a "
               "limit for each period.")
        raise ValueError(msg)

    def _periodical_integral_limit_rule(m, p):
        expr = sum(
            om.flow[inflow, outflow, p, t]
            * om.timeincrement[t]
            * sequence(getattr(flows[inflow, outflow], keyword))[t]
            for (inflow, outflow) in flows
            for t in m.TIMESTEPS_IN_PERIOD[p]
        )

        return expr <= limit[p]

    om.periodical_integral_limit = po.Constraint(
        om.PERIODS,
        rule=_periodical_integral_limit_rule,
        name=limit_name + "_constraint"
    )

    return om


def _check_and_set_flows(om, flows, keyword):
    """Checks and sets flows if needed

    Parameters
    ----------
    om : oemof.solph.Model
        Model to which constraints are added.

    flows : dict
        Dictionary holding the flows that should be considered in constraint.
        Keys are (source, target) objects of the Flow. If no dictionary is
        given all flows containing the keyword attribute will be
        used.

    keyword : string
        attribute to consider

    Returns
    -------
    flows : dict
        the flows to be considered
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
                    (
                        "Flow with source: {0} and target: {1} "
                        "has no attribute {2}."
                    ).format(i.label, o.label, keyword)
                )
