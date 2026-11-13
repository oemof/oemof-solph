# -*- coding: utf-8 -*-

"""linopy builders for the storage blocks.

SPDX-License-Identifier: MIT
"""

import numpy as np

from oemof.solph._linopy._data import to_array
from oemof.solph._linopy._indexing import expression
from oemof.solph._linopy._indexing import take
from oemof.solph._linopy._registry import register_builder
from oemof.solph._plumbing import valid_sequence
from oemof.solph.components._generic_storage import (
    GenericInvestmentStorageBlock,
)
from oemof.solph.components._generic_storage import GenericStorageBlock

BLOCK = "GenericStorageBlock"


class StorageData:
    """Parameter arrays of a group of storages."""

    def __init__(self, model, group):
        n_steps = len(model.TIMESTEPS)
        self.storages = list(group)
        self.n_steps = n_steps
        self.inflow = [next(iter(n.inputs)) for n in group]
        self.outflow = [next(iter(n.outputs)) for n in group]
        self.in_pos = np.array(
            [model.flow_position(i, n) for i, n in zip(self.inflow, group)]
        )
        self.out_pos = np.array(
            [model.flow_position(n, o) for n, o in zip(group, self.outflow)]
        )

        def steps(attr, length=n_steps):
            return np.array(
                [to_array(getattr(n, attr), length, attr) for n in group]
            )

        self.steps = steps
        self.loss_rate = steps("loss_rate")
        self.fixed_losses_relative = steps("fixed_losses_relative")
        self.fixed_losses_absolute = steps("fixed_losses_absolute")
        self.inflow_conversion_factor = steps("inflow_conversion_factor")
        self.outflow_conversion_factor = steps("outflow_conversion_factor")
        self.min_storage_level = steps("min_storage_level", n_steps + 1)
        self.max_storage_level = steps("max_storage_level", n_steps + 1)


@register_builder(GenericStorageBlock)
def build_storages(model, group):
    """Storages with a fixed storage capacity."""
    data = StorageData(model, group)
    n_steps = data.n_steps
    nominal = np.array([float(n.nominal_storage_capacity) for n in group])[
        :, None
    ]

    lower = nominal * data.min_storage_level
    upper = nominal * data.max_storage_level
    for k, n in enumerate(group):
        if n.initial_storage_level is not None:
            lower[k, 0] = upper[k, 0] = n.initial_storage_level * nominal[k, 0]
    content = model.add_variables(
        f"{BLOCK}.storage_content",
        entities=group,
        entity_dim="storage",
        index="timepoint",
        lower=lower,
        upper=upper,
    )
    losses = model.add_variables(
        f"{BLOCK}.storage_losses",
        entities=group,
        entity_dim="storage",
        index="timestep",
    )
    tau = model.timeincrement_array
    content_labels = content.labels.values
    constant_losses = (
        data.fixed_losses_relative * nominal + data.fixed_losses_absolute
    ) * tau

    add_losses_and_balance(
        model, data, content_labels, losses, constant_losses
    )
    add_balanced(model, data, content_labels)
    add_power_coupled(model, data)

    soc = [k for k, n in enumerate(group) if n.constant_soc_until is not None]
    if soc:
        add_soc_charge_limit(model, data, content_labels, nominal[:, 0], soc)

    costs_k, costs = [], []
    for k, n in enumerate(group):
        if valid_sequence(n.storage_costs, n_steps):
            costs_k.append(k)
            costs.append(to_array(n.storage_costs, n_steps, "storage_costs"))
    if costs_k:
        expr = expression(
            model.linopy,
            [(content_labels[costs_k, 1:], np.asarray(costs))],
            ("storage_cost_storage", "timestep"),
        )
        model.add_objective_term(f"{BLOCK}.storage_costs", expr.sum())


def add_losses_and_balance(
    model, data, content_labels, losses, constant_losses, block=BLOCK
):
    """storage_losses == content(t) (1 - (1 - loss)^tau) + constant, and
    content(t) - losses(t) + in(t) eta_in tau - out(t) / eta_out tau ==
    content(t + 1)."""
    tau = model.timeincrement_array
    dims = ("storage", "timestep")
    content_now = content_labels[:, :-1]
    content_next = content_labels[:, 1:]
    relative = 1 - (1 - data.loss_rate) ** tau
    model.add_constraints(
        f"{block}.losses",
        expression(
            model.linopy,
            [(content_now, relative), (losses.labels.values, -1.0)],
            dims,
        ),
        "=",
        -_like(constant_losses, dims),
    )
    flow_labels = model.flow.labels.values
    model.add_constraints(
        f"{block}.balance",
        expression(
            model.linopy,
            [
                (content_now, 1.0),
                (losses.labels.values, -1.0),
                (
                    take(flow_labels, data.in_pos),
                    data.inflow_conversion_factor * tau,
                ),
                (
                    take(flow_labels, data.out_pos),
                    -tau / data.outflow_conversion_factor,
                ),
                (content_next, -1.0),
            ],
            dims,
        ),
        "=",
        0,
    )


def add_balanced(model, data, content_labels, block=BLOCK):
    """content(last timepoint) == content(first timepoint)."""
    balanced = [k for k, n in enumerate(data.storages) if n.balanced is True]
    if not balanced:
        return
    model.add_constraints(
        f"{block}.balanced_cstr",
        expression(
            model.linopy,
            [
                (content_labels[balanced, -1], 1.0),
                (content_labels[balanced, 0], -1.0),
            ],
            ("balanced_storage",),
        ),
        "=",
        0,
    )


def add_power_coupled(model, data, block=BLOCK):
    """capacity(out) * relation == capacity(in), per capacity period."""
    members = [
        k
        for k, n in enumerate(data.storages)
        if n.invest_relation_input_output is not None
    ]
    if not members:
        return
    n_periods = len(model.CAPACITY_PERIODS)
    capacities = getattr(model, "invest_flow_capacity", {})
    in_labels, out_labels, relation = [], [], []
    for k in members:
        n = data.storages[k]
        key_in, key_out = (data.inflow[k], n), (n, data.outflow[k])
        if key_in not in capacities or key_out not in capacities:
            msg = (
                f"invest_relation_input_output of storage {n.label} needs "
                "investment flows at its input and output."
            )
            raise ValueError(msg)
        in_labels.append(capacities[key_in])
        out_labels.append(capacities[key_out])
        relation.append(
            to_array(n.invest_relation_input_output, n_periods, "relation")
        )
    model.add_constraints(
        f"{block}.power_coupled",
        expression(
            model.linopy,
            [
                (np.array(out_labels), np.array(relation)),
                (np.array(in_labels), -1.0),
            ],
            ("power_coupled_storage", "capacity_period"),
        ),
        "=",
        0,
    )


def add_soc_charge_limit(model, data, content_labels, nominal, members):
    """in(t) <= a content(t + 1) + b, see GenericStorageBlock."""
    n_steps = data.n_steps
    n_periods = len(model.CAPACITY_PERIODS)
    p_of_t = model.period_of_timestep
    a = np.zeros((len(members), n_steps))
    b = np.zeros((len(members), n_steps))
    for row, k in enumerate(members):
        n = data.storages[k]
        max_charge = to_array(n.max_charge_capacity, n_periods)[p_of_t]
        limit = to_array(n.relative_charge_limit, n_steps)
        saturation = n.fraction_saturation_charging
        until = n.constant_soc_until
        a[row] = -(max_charge * limit * (1 - saturation)) / (
            nominal[k] * data.max_storage_level[k, :-1] * (1 - until)
        )
        b[row] = (
            max_charge * limit * ((1 - saturation) / (1 - until) + saturation)
        )
    flow_labels = model.flow.labels.values
    dims = ("soc_limited_storage", "timestep")
    model.add_constraints(
        "GenericStorageBlock.soc_charge_limit",
        expression(
            model.linopy,
            [
                (take(flow_labels, data.in_pos[members]), 1.0),
                (content_labels[members, 1:], -a),
            ],
            dims,
        ),
        "<=",
        _like(b, dims),
    )


def _like(values, dims):
    import xarray as xr

    values = np.asarray(values, dtype=float)
    return xr.DataArray(
        values,
        dims=dims,
        coords={d: np.arange(n) for d, n in zip(dims, values.shape)},
    )


INVEST_BLOCK = "GenericInvestmentStorageBlock"


@register_builder(GenericInvestmentStorageBlock)
def build_investment_storages(model, group):
    """Storages whose capacity (or flows) are invested in."""
    data = StorageData(model, group)
    n_steps = data.n_steps
    n_periods = len(model.CAPACITY_PERIODS)
    p_of_t = model.period_of_timestep
    # timepoint t belongs to the period of timestep t; the last one to the
    # last period, as EnergySystem.capacity_period_of_timepoint
    p_of_tp = np.append(p_of_t, p_of_t[-1] if n_steps else 0)
    invest = [n.investment for n in group]
    nonconvex = np.array([inv.nonconvex is True for inv in invest])

    def per_period(attr):
        return np.array(
            [to_array(getattr(inv, attr), n_periods, attr) for inv in invest]
        )

    minimum, maximum = per_period("minimum"), per_period("maximum")
    ep_costs, offset = per_period("ep_costs"), per_period("offset")
    existing = per_period("existing")
    dims_p = ("storage", "capacity_period")

    content = model.add_variables(
        f"{INVEST_BLOCK}.storage_content",
        entities=group,
        entity_dim="storage",
        index="timepoint",
        lower=0,
    )
    invest_var = model.add_variables(
        f"{INVEST_BLOCK}.invest",
        entities=group,
        entity_dim="storage",
        index="capacity_period",
        lower=np.where(nonconvex[:, None], 0.0, minimum),
        upper=maximum,
    )
    capacity = model.add_variables(
        f"{INVEST_BLOCK}.storage_capacity",
        entities=group,
        entity_dim="storage",
        index="capacity_period",
        lower=0,
    )
    content_labels = content.labels.values
    capacity_labels = capacity.labels.values
    invest_labels = invest_var.labels.values

    # storage capacity = invest + existing
    model.add_constraints(
        f"{INVEST_BLOCK}.total_storage_rule",
        expression(
            model.linopy,
            [(capacity_labels, 1.0), (invest_labels, -1.0)],
            dims_p,
        ),
        "=",
        _like(existing, dims_p),
    )

    # initial content: limited by, or fixed relative to, the capacity of
    # the first period
    no_init = [
        k for k, n in enumerate(group) if n.initial_storage_level is None
    ]
    with_init = [
        k for k, n in enumerate(group) if n.initial_storage_level is not None
    ]
    if no_init:
        model.add_constraints(
            f"{INVEST_BLOCK}.init_content_limit",
            expression(
                model.linopy,
                [
                    (content_labels[no_init, 0], 1.0),
                    (invest_labels[no_init, 0], -1.0),
                ],
                ("no_init_storage",),
            ),
            "<=",
            _like(existing[no_init, 0], ("no_init_storage",)),
        )
    if with_init:
        level = np.array([group[k].initial_storage_level for k in with_init])
        model.add_constraints(
            f"{INVEST_BLOCK}.init_content_fix",
            expression(
                model.linopy,
                [
                    (content_labels[with_init, 0], 1.0),
                    (invest_labels[with_init, 0], -level),
                ],
                ("init_storage",),
            ),
            "=",
            _like(level * existing[with_init, 0], ("init_storage",)),
        )

    # balance: content(t+1) - content(t) (1 - loss)^tau
    #          + fixed_rel capacity(p) tau + fixed_abs tau
    #          - in eta_in tau + out / eta_out tau == 0
    tau = model.timeincrement_array
    flow_labels = model.flow.labels.values
    dims_t = ("storage", "timestep")
    model.add_constraints(
        f"{INVEST_BLOCK}.balance",
        expression(
            model.linopy,
            [
                (content_labels[:, 1:], 1.0),
                (content_labels[:, :-1], -((1 - data.loss_rate) ** tau)),
                (capacity_labels[:, p_of_t], data.fixed_losses_relative * tau),
                (
                    take(flow_labels, data.in_pos),
                    -data.inflow_conversion_factor * tau,
                ),
                (
                    take(flow_labels, data.out_pos),
                    tau / data.outflow_conversion_factor,
                ),
            ],
            dims_t,
        ),
        "=",
        -_like(data.fixed_losses_absolute * tau, dims_t),
    )
    add_balanced(model, data, content_labels, block=INVEST_BLOCK)
    add_power_coupled(model, data, block=INVEST_BLOCK)

    # flow capacities proportional to the storage capacity
    capacities = getattr(model, "invest_flow_capacity", {})
    for attr, side, name in (
        ("invest_relation_input_capacity", "in", "storage_capacity_inflow"),
        ("invest_relation_output_capacity", "out", "storage_capacity_outflow"),
    ):
        members = [
            k for k, n in enumerate(group) if getattr(n, attr) is not None
        ]
        if not members:
            continue
        flow_cap, ratio = [], []
        for k in members:
            n = group[k]
            key = (data.inflow[k], n) if side == "in" else (n, data.outflow[k])
            if key not in capacities:
                msg = f"{attr} of storage {n.label} needs an investment flow."
                raise ValueError(msg)
            flow_cap.append(capacities[key])
            ratio.append(to_array(getattr(n, attr), n_periods, attr))
        model.add_constraints(
            f"{INVEST_BLOCK}.{name}",
            expression(
                model.linopy,
                [
                    (np.array(flow_cap), 1.0),
                    (capacity_labels[members], -np.array(ratio)),
                ],
                (f"{name}_storage", "capacity_period"),
            ),
            "=",
            0,
        )

    # content limits relative to the capacity of the timepoint's period
    dims_tp = ("storage", "timepoint")
    model.add_constraints(
        f"{INVEST_BLOCK}.max_storage_content",
        expression(
            model.linopy,
            [
                (content_labels, 1.0),
                (capacity_labels[:, p_of_tp], -data.max_storage_level),
            ],
            dims_tp,
        ),
        "<=",
        0,
    )
    with_min = [
        k
        for k in range(len(group))
        if data.min_storage_level[k, :n_steps].sum() > 0
    ]
    if with_min:
        model.add_constraints(
            f"{INVEST_BLOCK}.min_storage_content",
            expression(
                model.linopy,
                [
                    (content_labels[with_min], 1.0),
                    (
                        capacity_labels[with_min][:, p_of_tp],
                        -data.min_storage_level[with_min],
                    ),
                ],
                ("min_storage", "timepoint"),
            ),
            ">=",
            0,
        )

    costs = expression(model.linopy, [(invest_labels, ep_costs)], dims_p).sum()
    nc = np.flatnonzero(nonconvex)
    if nc.size:
        status = model.add_variables(
            f"{INVEST_BLOCK}.invest_status",
            entities=[group[k] for k in nc],
            entity_dim="nonconvex_storage",
            index="capacity_period",
            binary=True,
        )
        dims_nc = ("nonconvex_storage", "capacity_period")
        model.add_constraints(
            f"{INVEST_BLOCK}.limit_max",
            expression(
                model.linopy,
                [
                    (status.labels.values, maximum[nc]),
                    (invest_labels[nc], -1.0),
                ],
                dims_nc,
            ),
            ">=",
            0,
        )
        model.add_constraints(
            f"{INVEST_BLOCK}.limit_min",
            expression(
                model.linopy,
                [
                    (invest_labels[nc], 1.0),
                    (status.labels.values, -minimum[nc]),
                ],
                dims_nc,
            ),
            ">=",
            0,
        )
        costs = (
            costs
            + expression(
                model.linopy, [(status.labels.values, offset[nc])], dims_nc
            ).sum()
        )

    # investment_limit sums the investment costs without storage costs
    model.add_expression(f"{INVEST_BLOCK}.investment_costs", costs)
    costs_k, storage_costs = [], []
    for k, n in enumerate(group):
        if valid_sequence(n.storage_costs, n_steps):
            costs_k.append(k)
            storage_costs.append(
                to_array(n.storage_costs, n_steps, "storage_costs")
            )
    if costs_k:
        costs = (
            costs
            + expression(
                model.linopy,
                [(content_labels[costs_k, 1:], np.asarray(storage_costs))],
                ("storage_cost_storage", "timestep"),
            ).sum()
        )
    model.add_objective_term(f"{INVEST_BLOCK}.costs", costs)
