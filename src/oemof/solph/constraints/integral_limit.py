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
import warnings

from pyomo import environ as po

from oemof.solph._plumbing import sequence


def emission_limit(om, flows=None, limit=None):
    r"""
    Short handle for generic_integral_limit() with keyword="emission_factor".
    Can be used to impose an emissions budget limit in a multi-period model.

    Note
    ----
    Flow objects require an attribute "emission_factor"!

    """
    generic_integral_limit(
        om, keyword="emission_factor", flows=flows, upper_limit=limit
    )


def emission_limit_per_period(om, flows=None, limit=None):
    r"""
    Short handle for generic_periodical_integral_limit()
    with keyword="emission_factor". Only applicable for multi-period models.
    Puts a limit on each period's emissions.

    Note
    ----
    Flow objects required an attribute "emission_factor"!

    """
    generic_periodical_integral_limit(
        om, keyword="emission_factor", flows=flows, limit=limit
    )


def generic_integral_limit(
    om,
    keyword,
    flows=None,
    upper_limit=None,
    lower_limit=None,
    limit=None,
    limit_name=None,
):
    r"""Set a global limit for flows weighted by attribute named keyword.
    The attribute named keyword has to be added
    to every flow you want to take into account.

    Total value of keyword attributes after optimization can be retrieved
    calling the
    `om.oemof.solph._models.Model.integral_limit_${keyword}()`.

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
    limit_name : string
        Unique name for the constraint,
        Defaults to "integral_limit_{keyword}".
    upper_limit : numeric
        Absolute upper limit of keyword attribute for the energy system.
    lower_limit : numeric
        Absolute lower limit of keyword attribute for the energy system.

    Note
    ----
    Flow objects require an attribute named like keyword!


    **Constraint:**

    .. math:: \sum_{i \in F_E} \sum_{t \in T} P_i(p, t) \cdot w_i(t)
               \cdot \tau(t) \leq UB

    .. math:: \sum_{i \in F_E} \sum_{t \in T} P_i(p, t) \cdot w_i(t)
               \cdot \tau(t) \geq LB


    With `F_I` being the set of flows considered for the integral limit and
    `T` being the set of time steps.

    The symbols used are defined as follows
    (with Variables (V) and Parameters (P)):

    ================= ==== ====================================================
    math. symbol      type explanation
    ================= ==== ====================================================
    :math:`P_n(p, t)` V    power flow :math:`n` at time index :math:`p, t`
    :math:`w_N(t)`    P    weight given to Flow named according to `keyword`
    :math:`\tau(t)`   P    width of time step :math:`t`
    :math:`UB`        P    global limit given by keyword `upper_limit`
    :math:`LB`        P    global limit given by keyword `lower_limit`
    ================= ==== ====================================================

    Examples
    --------
    >>> import pandas as pd
    >>> from oemof import solph
    >>> date_time_index = pd.date_range('1/1/2012', periods=6, freq='h')
    >>> energysystem = solph.EnergySystem(
    ...     timeindex=date_time_index,
    ...     infer_last_interval=False,
    ... )
    >>> bel = solph.buses.Bus(label='electricityBus')
    >>> flow1 = solph.flows.Flow(
    ...     nominal_capacity=100,
    ...     custom_attributes={"my_factor": 0.8},
    ... )
    >>> flow2 = solph.flows.Flow(nominal_capacity=50)
    >>> src1 = solph.components.Source(label='source1', outputs={bel: flow1})
    >>> src2 = solph.components.Source(label='source2', outputs={bel: flow2})
    >>> energysystem.add(bel, src1, src2)
    >>> model = solph.Model(energysystem)
    >>> flow_with_keyword = {(src1, bel): flow1, }
    >>> model = solph.constraints.generic_integral_limit(
    ...     model, "my_factor", flow_with_keyword, upper_limit=777)
    """
    flows = _check_and_set_flows(om, flows, keyword)
    if limit_name is None:
        limit_name = "integral_limit_" + keyword

    if limit is not None:
        msg = (
            "The keyword argument 'limit' to generic_integral_limit has been"
            "renamed to 'upper_limit'. The transitional wrapper will be"
            "deleted in a future version."
        )
        warnings.warn(msg, FutureWarning)
        upper_limit = limit

    if upper_limit is None and lower_limit is None:
        raise ValueError(
            "At least one of upper_limit and lower_limit needs to be defined."
        )

    setattr(
        om,
        limit_name,
        po.Expression(
            expr=sum(
                om.flow[inflow, outflow, t]
                * om.timeincrement[t]
                * sequence(getattr(flows[inflow, outflow], keyword))[t]
                for (inflow, outflow) in flows
                for t in om.TIMESTEPS
            )
        ),
    )

    if upper_limit is not None:
        setattr(
            om,
            limit_name + "_upper_limit",
            po.Constraint(expr=(getattr(om, limit_name) <= upper_limit)),
        )
    if lower_limit is not None:
        setattr(
            om,
            limit_name + "_lower_limit",
            po.Constraint(expr=(getattr(om, limit_name) >= lower_limit)),
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
               \cdot \tau(t) \leq L(p) \forall p \in \textrm{PERIODS}


    For the parameter and variable explanation, please refer to the docs
    of generic_integral_limit.

    """
    flows = _check_and_set_flows(om, flows, keyword)
    limit_name = "integral_limit_" + keyword

    if om.es.periods is None:
        msg = (
            "generic_periodical_integral_limit is only applicable\n"
            "for multi-period models.\nFor standard models, use "
            "generic_integral_limit instead."
        )
        raise ValueError(msg)

    if limit is not None:
        limit = sequence(limit)
    else:
        msg = (
            "You have to provide a limit for each period!\n"
            "If you provide a scalar value, this will be applied as a "
            "limit for each period."
        )
        raise ValueError(msg)

    def _periodical_integral_limit_rule(m, p):
        expr = sum(
            om.flow[inflow, outflow, t]
            * om.timeincrement[t]
            * sequence(getattr(flows[inflow, outflow], keyword))[t]
            for (inflow, outflow) in flows
            for t in m.TIMESTEPS_IN_PERIOD[p]
        )

        return expr <= limit[p]

    om.periodical_integral_limit = po.Constraint(
        om.PERIODS,
        rule=_periodical_integral_limit_rule,
        name=limit_name + "_constraint",
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
        for i, o in om.flows:
            if hasattr(om.flows[i, o], keyword):
                flows[(i, o)] = om.flows[i, o]

    else:
        for i, o in flows:
            if not hasattr(flows[i, o], keyword):
                raise AttributeError(
                    (
                        "Flow with source: {0} and target: {1} "
                        "has no attribute {2}."
                    ).format(i.label, o.label, keyword)
                )

    return flows
