# -*- coding: utf-8 -*-

"""A constraint to have one common limit for several components.

SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

from pyomo import environ as po


def shared_limit(
    model,
    quantity,
    limit_name,
    components,
    weights,
    lower_limit=0,
    upper_limit=None,
):
    r"""
    Adds a constraint to the given model that restricts
    the weighted sum of variables to a corridor.

    **The following constraints are build:**

      .. math::
        l_\mathrm{low} \le \sum v_i(t) \times w_i(t) \le l_\mathrm{up}
        \forall t

    Parameters
    ----------
    model : oemof.solph.Model
        Model to which the constraint is added.
    limit_name : string
        Name of the constraint to create
    quantity : pyomo.core.base.var.IndexedVar
        Shared Pyomo variable for all components of a type.
        (:math:`v_i(t)`)
    components : list of components
        list of components of the same type
    weights : list of numeric values
        has to have the same length as the list of components
        (:math:`w_i(t)`)
    lower_limit : numeric
        the lower limit (:math:`l_\mathrm{low}`)
    upper_limit : numeric
        the upper limit (:math:`l_\mathrm{up}`)

    Examples
    --------
    The constraint can e.g. be used to define a common storage
    that is shared between parties but that do not exchange
    energy on balance sheet.
    Thus, every party has their own bus and storage, respectively,
    to model the energy flow. However, as the physical storage is shared,
    it has a common limit.

    >>> import pandas as pd
    >>> from oemof import solph
    >>> date_time_index = pd.date_range('1/1/2012', periods=6, freq='h')
    >>> energysystem = solph.EnergySystem(
    ...     timeindex=date_time_index,
    ...     infer_last_interval=False,
    ... )
    >>> b1 = solph.buses.Bus(label="Party1Bus")
    >>> b2 = solph.buses.Bus(label="Party2Bus")
    >>> storage1 = solph.components.GenericStorage(
    ...     label="Party1Storage",
    ...     nominal_capacity=5,
    ...     inputs={b1: solph.flows.Flow()},
    ...     outputs={b1: solph.flows.Flow()}
    ... )
    >>> storage2 = solph.components.GenericStorage(
    ...     label="Party2Storage",
    ...     nominal_capacity=5,
    ...     inputs={b1: solph.flows.Flow()},
    ...     outputs={b1: solph.flows.Flow()}
    ... )
    >>> energysystem.add(b1, b2, storage1, storage2)
    >>> components = [storage1, storage2]
    >>> model = solph.Model(energysystem)
    >>> solph.constraints.shared_limit(
    ...    model,
    ...    model.GenericStorageBlock.storage_content,
    ...    "limit_storage", components,
    ...    [1, 1], upper_limit=5
    ... )
    """

    setattr(model, limit_name, po.Var(model.TIMESTEPS))

    for t in model.TIMESTEPS:
        getattr(model, limit_name)[t].setlb(lower_limit)
        getattr(model, limit_name)[t].setub(upper_limit)

    weighted_sum_constraint = limit_name + "_constraint"

    def _weighted_sum_rule(m):
        for ts in m.TIMESTEPS:
            lhs = sum(quantity[c, ts] * w for c, w in zip(components, weights))
            rhs = getattr(model, limit_name)[ts]
            expr = lhs == rhs
            getattr(m, weighted_sum_constraint).add(ts, expr)

    setattr(
        model,
        weighted_sum_constraint,
        po.Constraint(model.TIMESTEPS, noruleinit=True),
    )
    setattr(
        model,
        weighted_sum_constraint + "_build",
        po.BuildAction(rule=_weighted_sum_rule),
    )
