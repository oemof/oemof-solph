# -*- coding: utf-8 -*-

"""linopy versions of the functions in :mod:`oemof.solph.constraints`.

Each function is registered under the name of its Pyomo counterpart and
takes the same arguments;
:func:`oemof.solph.constraints._backend.backend_dispatch` calls it when
the model is a :class:`~oemof.solph.LinopyModel`. Where the Pyomo
version takes Pyomo variables (``shared_limit``, ``equate_variables``),
this one takes the linopy equivalents: ``model.flow``, block variables
as ``model.<Block>.<variable>`` or their elements
``model.<Block>.<variable>[keys]``.

SPDX-License-Identifier: MIT
"""

import warnings

import numpy as np
import xarray as xr

from oemof.solph._linopy._data import to_array
from oemof.solph._linopy._indexing import expression
from oemof.solph._linopy._indexing import take

_CONSTRAINTS = {}


def register_constraint(name):
    """Register `function` as the linopy version of constraint `name`."""

    def decorator(function):
        _CONSTRAINTS[name] = function
        return function

    return decorator


def get_constraint(name):
    """The linopy version of constraint function `name`, or None."""
    return _CONSTRAINTS.get(name)


def _timesteps(model):
    return len(model.TIMESTEPS)


def _bounds_variable(model, name, lower, upper):
    """A variable over the timesteps, bounded by lower and upper."""
    return model.add_variables(
        name,
        index="timestep",
        lower=-np.inf if lower is None else lower,
        upper=np.inf if upper is None else upper,
    )


def _row(model, terms, n_steps):
    """A single row of terms over the timesteps, as an expression with a
    leading dimension of length 1."""
    if not terms:
        return None
    return expression(
        model.linopy,
        [(np.asarray(lab)[None, :], np.asarray(c)) for lab, c in terms],
        ("_row", "timestep"),
    ).isel(_row=0)


@register_constraint("equate_flows")
def equate_flows(model, flows1, flows2, factor1=1, name="equate_flows"):
    n_steps = _timesteps(model)
    labels = model.flow.labels.values
    terms = [(labels[model.flow_position(i, o)], factor1) for i, o in flows1]
    terms += [(labels[model.flow_position(i, o)], -1.0) for i, o in flows2]
    lhs = _row(model, terms, n_steps)
    if lhs is not None:
        model.add_constraints(name, lhs, "=", 0)
    return model


@register_constraint("equate_flows_by_keyword")
def equate_flows_by_keyword(
    model, keyword1, keyword2, factor1=1, name="equate_flows"
):
    flows = {}
    for n, keyword in enumerate([keyword1, keyword2]):
        flows[n] = [
            (i, o)
            for i, o in model.flows
            if keyword in model.flows[i, o].custom_properties
        ]
    return equate_flows(model, flows[0], flows[1], factor1=factor1, name=name)


@register_constraint("equate_variables")
def equate_variables(model, var1, var2, factor1=1, name=None):
    """var1 * factor1 == var2 for two linopy variable elements, e.g.
    ``model.InvestmentFlowBlock.invest[source, target, 0]``."""
    if name is None:
        model._equate_count = getattr(model, "_equate_count", 0) + 1
        name = f"equate_variables_{model._equate_count}"
    model.linopy.add_constraints(factor1 * var1 - var2 == 0, name=name)
    return model


@register_constraint("shared_limit")
def shared_limit(
    model,
    quantity,
    limit_name,
    components,
    weights,
    lower_limit=0,
    upper_limit=None,
):
    """lower <= sum_i quantity[i, t] * w_i <= upper for every timestep.

    `quantity` is ``model.flow`` or a block variable such as
    ``model.GenericStorageBlock.storage_content`` (only its first
    len(TIMESTEPS) values are used, as in the Pyomo version).
    """
    n_steps = _timesteps(model)
    limit = _bounds_variable(model, limit_name, lower_limit, upper_limit)
    terms = [
        (model.entity_labels(quantity, c)[:n_steps], float(w))
        for c, w in zip(components, weights)
    ]
    terms.append((limit.labels.values, -1.0))
    model.add_constraints(
        limit_name + "_constraint", _row(model, terms, n_steps), "=", 0
    )
    return model


def _check_and_set_flows(model, flows, keyword):
    from oemof.solph.constraints.integral_limit import (
        _check_and_set_flows as check,
    )

    return check(model, flows, keyword)


@register_constraint("generic_integral_limit")
def generic_integral_limit(
    om,
    keyword,
    flows=None,
    upper_limit=None,
    lower_limit=None,
    limit=None,
    limit_name=None,
):
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
    n_steps = _timesteps(om)
    keys = list(flows)
    labels = take(om.flow.labels.values, [om.flow_position(*k) for k in keys])
    factors = np.array(
        [
            to_array(flows[k].custom_properties[keyword], n_steps, keyword)
            for k in keys
        ]
    ).reshape(len(keys), n_steps)
    total = expression(
        om.linopy,
        [(labels, factors * om.timeincrement_array)],
        ("integral_limit_flow", "timestep"),
    ).sum()
    om.add_expression(limit_name, total)
    if upper_limit is not None:
        om.linopy.add_constraints(
            total <= upper_limit, name=limit_name + "_upper_limit"
        )
    if lower_limit is not None:
        om.linopy.add_constraints(
            total >= lower_limit, name=limit_name + "_lower_limit"
        )
    return om


@register_constraint("emission_limit")
def emission_limit(om, flows=None, limit=None):
    return generic_integral_limit(
        om, keyword="emission_factor", flows=flows, upper_limit=limit
    )


@register_constraint("investment_limit")
def investment_limit(model, limit=None):
    """Sum of the investment costs of InvestmentFlowBlock and
    GenericInvestmentStorageBlock <= limit (as the Pyomo version, which
    also leaves out InvestNonConvexFlowBlock)."""
    total = None
    for name in (
        "InvestmentFlowBlock.investment_costs",
        "GenericInvestmentStorageBlock.investment_costs",
    ):
        if name in model._expressions:
            expr = model.expression(name)
            total = expr if total is None else total + expr
    if total is not None:
        model.linopy.add_constraints(total <= limit, name="investment_limit")
    return model


@register_constraint("additional_investment_flow_limit")
def additional_investment_flow_limit(model, keyword, limit=None):
    invest = model.InvestmentFlowBlock.invest
    terms = []
    for i, o in model.flows:
        option = model.flows[i, o].investment
        if option is not None and keyword in option.custom_properties:
            terms.append(
                (
                    model.entity_labels(invest, (i, o)),
                    float(option.custom_properties[keyword]),
                )
            )
    limit_name = "invest_limit_" + keyword
    total = expression(
        model.linopy,
        [(np.asarray(lab)[None, :], c) for lab, c in terms],
        ("_row", "capacity_period"),
    ).sum()
    model.add_expression(limit_name, total)
    model.linopy.add_constraints(
        total <= limit, name=limit_name + "_constraint"
    )
    return model


@register_constraint("limit_active_flow_count")
def limit_active_flow_count(
    model, constraint_name, flows, lower_limit=0, upper_limit=None
):
    """lower <= number of active nonconvex flows <= upper per timestep."""
    n_steps = _timesteps(model)
    count = _bounds_variable(model, constraint_name, lower_limit, upper_limit)
    status = getattr(model, "nonconvex_status", {})
    terms = [(status[f], 1.0) for f in flows if f in status]
    terms.append((count.labels.values, -1.0))
    model.add_constraints(
        constraint_name + "_constraint", _row(model, terms, n_steps), "=", 0
    )
    return model


@register_constraint("limit_active_flow_count_by_keyword")
def limit_active_flow_count_by_keyword(
    model, keyword, lower_limit=0, upper_limit=None
):
    flows = [
        f
        for f in getattr(model, "nonconvex_status", {})
        if keyword in model.flows[f].custom_properties
    ]
    return limit_active_flow_count(
        model,
        keyword,
        flows=flows,
        lower_limit=lower_limit,
        upper_limit=upper_limit,
    )


@register_constraint("storage_level_constraint")
def storage_level_constraint(
    model,
    name,
    storage_component,
    multiplexer_bus,
    input_levels,
    output_levels,
):
    """Inputs and outputs of a multiplexer bus allowed depending on the
    storage level, see the Pyomo version."""
    if model.TSAM_MODE:
        msg = (
            "solph.constraints.storage_level_constraint in tsam mode is not "
            "supported by the linopy backend yet."
        )
        raise NotImplementedError(msg)
    n_periods = len(model.CAPACITY_PERIODS)
    p_of_t = model.period_of_timestep
    content = model.entity_labels(
        model.GenericStorageBlock.storage_content, storage_component
    )
    nominal = float(storage_component.nominal_storage_capacity)
    labels = model.flow.labels.values

    def per_step_capacity(i, o):
        return to_array(model.flows[i, o].nominal_capacity, n_periods)[p_of_t]

    def binary(suffix, entities):
        return model.add_variables(
            f"{name}_{suffix}",
            entities=list(entities),
            entity_dim=f"{name}_{suffix}",
            index="timestep",
            binary=True,
        ).labels.values

    def add(constraint, terms, sign, rhs, dim):
        lhs = expression(model.linopy, terms, (dim, "timestep"))
        rhs = xr.DataArray(
            np.broadcast_to(np.asarray(rhs, dtype=float), lhs.shape[:2]),
            dims=(dim, "timestep"),
            coords={d: lhs.coords[d] for d in (dim, "timestep")},
        )
        model.add_constraints(constraint, lhs, sign, rhs)

    outputs = list(output_levels)
    if outputs:
        dim = f"{name}_active_output"
        active = binary("active_output", outputs)
        levels = np.array([output_levels[o] for o in outputs])[:, None]
        # E(t + 1) / E_nom >= y(t) * level
        add(
            f"{name}_output_active_constraint",
            [
                (np.broadcast_to(content[1:], active.shape), 1 / nominal),
                (active, -levels),
            ],
            ">=",
            0,
            dim,
        )
        # P(t) / P_nom <= y(t)
        flow = take(
            labels, [model.flow_position(multiplexer_bus, o) for o in outputs]
        )
        capacity = np.array(
            [per_step_capacity(multiplexer_bus, o) for o in outputs]
        )
        add(
            f"{name}_output_constraint",
            [(flow, 1 / capacity), (active, -1.0)],
            "<=",
            0,
            dim,
        )

    inputs = list(input_levels)
    if inputs:
        dim = f"{name}_active_input"
        inactive = binary("active_input", inputs)
        levels = np.array([input_levels[i] for i in inputs])[:, None]
        # E(t) / E_nom - level <= y_hat(t)
        add(
            f"{name}_input_active_constraint",
            [
                (np.broadcast_to(content[:-1], inactive.shape), 1 / nominal),
                (inactive, -1.0),
            ],
            "<=",
            levels,
            dim,
        )
        # P(t) / P_nom <= 1 - y_hat(t)
        flow = take(
            labels, [model.flow_position(i, multiplexer_bus) for i in inputs]
        )
        capacity = np.array(
            [per_step_capacity(i, multiplexer_bus) for i in inputs]
        )
        add(
            f"{name}_input_constraint",
            [(flow, 1 / capacity), (inactive, 1.0)],
            "<=",
            1,
            dim,
        )
    return model
