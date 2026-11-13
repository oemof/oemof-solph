# -*- coding: utf-8 -*-

"""linopy builders for the flow blocks.

SPDX-License-Identifier: MIT
"""

import numpy as np

from oemof.solph._linopy._data import to_array
from oemof.solph._linopy._indexing import expression
from oemof.solph._linopy._indexing import take
from oemof.solph._linopy._registry import register_builder
from oemof.solph._plumbing import valid_sequence
from oemof.solph.flows._simple_flow_block import SimpleFlowBlock

BLOCK = "SimpleFlowBlock"


def time_weight(model):
    """timeincrement * tsam_weighting per timestep."""
    return model.timeincrement_array * model.tsam_weighting


@register_builder(SimpleFlowBlock)
def build_simple_flows(model, group):
    """Constraints and costs of :class:`SimpleFlowBlock` (all flows)."""
    _variable_costs(model)
    _full_load_time(model, group)
    _gradients(model, group)
    _integer_flows(model, group)


def _variable_costs(model):
    """Variable costs of all flows, as `SimpleFlowBlock._objective_expression`
    (it sums over all flows of the model, not only the group)."""
    n_steps = len(model.TIMESTEPS)
    positions, costs = [], []
    for k, (i, o) in enumerate(model.FLOWS):
        variable_costs = model.flows[i, o].variable_costs
        if valid_sequence(variable_costs, n_steps):
            positions.append(k)
            costs.append(to_array(variable_costs, n_steps, "variable_costs"))
    if not positions:
        return
    labels = take(model.flow.labels.values, positions)
    coeffs = np.asarray(costs) * time_weight(model)
    expr = expression(
        model.linopy, [(labels, coeffs)], ("cost_flow", "timestep")
    )
    model.add_objective_term(f"{BLOCK}.variable_costs", expr.sum())


def _full_load_time(model, group):
    weight = time_weight(model)
    labels = model.flow.labels.values
    for attr, sign in (
        ("full_load_time_max", "<="),
        ("full_load_time_min", ">="),
    ):
        members = [
            (i, o, f)
            for i, o, f in group
            if getattr(f, attr) is not None and f.nominal_capacity is not None
        ]
        if not members:
            continue
        positions = [model.flow_position(i, o) for i, o, _ in members]
        # FIXME in the Pyomo block as well: hardcoded single period
        rhs = np.array(
            [getattr(f, attr) * f.nominal_capacity[0] for _, _, f in members]
        )
        lhs = expression(
            model.linopy,
            [(take(labels, positions), weight)],
            ("full_load_time_flow", "timestep"),
        ).sum("timestep")
        model.add_constraints(
            f"{BLOCK}.{attr}_constr", lhs, sign, _array(rhs, lhs)
        )


def _gradients(model, group):
    n_steps = len(model.TIMESTEPS)
    p_of_t = model.period_of_timestep
    n_periods = len(model.CAPACITY_PERIODS)
    flow_labels = model.flow.labels.values
    for direction in ("positive", "negative"):
        attr = f"{direction}_gradient_limit"
        members = [
            (i, o, f)
            for i, o, f in group
            if getattr(f, attr) is not None and f.nonconvex is None
        ]
        if not members:
            continue
        upper = np.full((len(members), n_steps), np.inf)
        for k, (i, o, f) in enumerate(members):
            if valid_sequence(getattr(f, attr), n_steps):
                if f.nominal_capacity is None:
                    msg = (
                        f"The {attr} of flow {i.label} -> {o.label} needs a "
                        "nominal_capacity."
                    )
                    raise ValueError(msg)
                nominal = to_array(f.nominal_capacity, n_periods)[p_of_t]
                upper[k] = to_array(getattr(f, attr), n_steps, attr) * nominal
        dim = f"{direction}_gradient_flow"
        var = model.add_variables(
            f"{BLOCK}.{direction}_gradient",
            entities=[(i, o) for i, o, _ in members],
            entity_dim=dim,
            index="timestep",
            lower=0,
            upper=upper,
        )
        positions = [model.flow_position(i, o) for i, o, _ in members]
        current = take(flow_labels, positions)
        previous = np.roll(current, 1, axis=1)
        current[:, 0] = -1
        previous[:, 0] = -1
        # positive: P(t) - P(t-1) <= ve_p(t)
        # negative: P(t-1) - P(t) <= ve_n(t)
        # first timestep: ve(0) == 0
        sign_flow = 1.0 if direction == "positive" else -1.0
        gradient_coeff = np.full((len(members), n_steps), -1.0)
        gradient_coeff[:, 0] = 1.0
        lhs = expression(
            model.linopy,
            [
                (current, sign_flow),
                (previous, -sign_flow),
                (var.labels.values, gradient_coeff),
            ],
            (dim, "timestep"),
        )
        signs = np.full((len(members), n_steps), "<=", dtype=object)
        signs[:, 0] = "="
        model.add_constraints(
            f"{BLOCK}.{direction}_gradient_constr",
            lhs,
            _array(signs, lhs),
            0,
        )


def _integer_flows(model, group):
    members = [(i, o) for i, o, f in group if f.integer]
    if not members:
        return
    var = model.add_variables(
        f"{BLOCK}.integer_flow",
        entities=members,
        entity_dim="integer_flow",
        index="timestep",
        integer=True,
    )
    positions = [model.flow_position(i, o) for i, o in members]
    lhs = expression(
        model.linopy,
        [
            (var.labels.values, 1.0),
            (take(model.flow.labels.values, positions), -1.0),
        ],
        ("integer_flow", "timestep"),
    )
    model.add_constraints(f"{BLOCK}.integer_flow_constr", lhs, "=", 0)


def _array(values, like):
    """values as a DataArray on the dims and coords of expression `like`."""
    import xarray as xr

    dims = [d for d in like.dims if d != "_term"]
    return xr.DataArray(
        np.asarray(values),
        dims=dims,
        coords={d: like.coords[d] for d in dims if d in like.coords},
    )
