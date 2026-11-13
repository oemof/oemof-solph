# -*- coding: utf-8 -*-

"""linopy builders for nonconvex flows (with fixed or invested capacity).

Both blocks share the status logic of :mod:`oemof.solph.flows._shared`;
they differ in what the capacity is: a parameter for
:class:`NonConvexFlowBlock`, the `invest` variable for
:class:`InvestNonConvexFlowBlock` (linearised status * invest).

SPDX-License-Identifier: MIT
"""

import numpy as np

from oemof.solph._linopy._data import to_array
from oemof.solph._linopy._indexing import expression
from oemof.solph._linopy._indexing import take
from oemof.solph._linopy._registry import register_builder
from oemof.solph._plumbing import valid_sequence
from oemof.solph.flows._invest_non_convex_flow_block import (
    InvestNonConvexFlowBlock,
)
from oemof.solph.flows._non_convex_flow_block import NonConvexFlowBlock
from oemof.solph.flows._shared import _gradient_limit


@register_builder(NonConvexFlowBlock)
def build_nonconvex_flows(model, group):
    _build(model, group, "NonConvexFlowBlock", "nonconvex_flow", invest=False)


@register_builder(InvestNonConvexFlowBlock)
def build_invest_nonconvex_flows(model, group):
    _build(
        model,
        group,
        "InvestNonConvexFlowBlock",
        "invest_nonconvex_flow",
        invest=True,
    )


class _Context:
    """Arrays shared by the parts of one nonconvex block."""

    def __init__(self, model, group, block, dim):
        self.model = model
        self.block = block
        self.dim = dim
        self.n_steps = len(model.TIMESTEPS)
        self.n_periods = len(model.CAPACITY_PERIODS)
        self.p_of_t = model.period_of_timestep
        self.flows = [(i, o) for i, o, _ in group]
        self.options = [f for _, _, f in group]
        self.nonconvex = [f.nonconvex for f in self.options]
        positions = [model.flow_position(i, o) for i, o in self.flows]
        self.flow_labels = take(model.flow.labels.values, positions)
        self.initial = np.array(
            [float(nc.initial_status) for nc in self.nonconvex]
        )
        self.weight = model.tsam_weighting

    def steps(self, seqs, name):
        return np.array([to_array(s, self.n_steps, name) for s in seqs])

    def periods(self, seqs, name):
        return np.array([to_array(s, self.n_periods, name) for s in seqs])

    def members(self, condition):
        return [k for k, nc in enumerate(self.nonconvex) if condition(k, nc)]

    def add(self, name, terms, sign, rhs, dim=None, mask=None, entities=None):
        dims = (dim or self.dim, "timestep")
        lhs = expression(self.model.linopy, terms, dims)
        name = f"{self.block}.{name}"
        if mask is not None:
            return self.model.add_masked_constraints(
                name, lhs, sign, _da(rhs, lhs), mask
            )
        return self.model.add_constraints(name, lhs, sign, _da(rhs, lhs))


def _build(model, group, block, dim, invest):
    c = _Context(model, group, block, dim)
    n_steps, p_of_t = c.n_steps, c.p_of_t
    flows = c.flows

    # --- status ---------------------------------------------------------
    lower = np.zeros((len(flows), n_steps))
    upper = np.ones((len(flows), n_steps))
    if not invest:
        # NonConvexFlowBlock fixes the status before the first flexible
        # timestep (InvestNonConvexFlowBlock does not)
        for k, nc in enumerate(c.nonconvex):
            if nc.initial_status is not None:
                first = int(nc.first_flexible_timestep)
                lower[k, :first] = upper[k, :first] = nc.initial_status
    status = model.add_variables(
        f"{block}.status",
        entities=flows,
        entity_dim=dim,
        index="timestep",
        lower=lower,
        upper=upper,
        binary=True,
    )
    status_labels = status.labels.values
    status_nominal = model.add_variables(
        f"{block}.status_nominal",
        entities=flows,
        entity_dim=dim,
        index="timestep",
        lower=0,
    )
    sn_labels = status_nominal.labels.values
    # status and status * capacity per flow, for components that use them
    # (e.g. OffsetConverter)
    model.nonconvex_status = getattr(model, "nonconvex_status", {})
    model.nonconvex_status_nominal = getattr(
        model, "nonconvex_status_nominal", {}
    )
    for k, f in enumerate(flows):
        model.nonconvex_status[f] = status_labels[k]
        model.nonconvex_status_nominal[f] = sn_labels[k]

    costs = []
    if invest:
        invest_labels, invest_costs = _investment(c, status_labels, sn_labels)
        capacity_at_t = invest_labels[:, p_of_t]
        costs.append(invest_costs)
    else:
        nominal = np.array(
            [
                to_array(f.nominal_capacity, c.n_periods, "nominal_capacity")
                for f in c.options
            ]
        )[:, p_of_t]
        # status_nominal == status * nominal capacity
        c.add(
            "status_nominal_constraint",
            [(sn_labels, 1.0), (status_labels, -nominal)],
            "=",
            0,
        )

    # --- flow limits relative to the status -----------------------------
    minimum = c.steps([f.minimum for f in c.options], "minimum")
    maximum = c.steps([f.maximum for f in c.options], "maximum")
    c.add("min", [(sn_labels, minimum), (c.flow_labels, -1.0)], "<=", 0)
    c.add("max", [(sn_labels, maximum), (c.flow_labels, -1.0)], ">=", 0)

    # --- start-ups, shut-downs, up- and downtimes -----------------------
    previous = np.roll(status_labels, 1, axis=1)
    previous[:, 0] = -1
    costs += _startup_shutdown(c, status_labels, previous)
    _uptime_downtime(c, status_labels, previous)

    # --- gradients --------------------------------------------------------
    if invest:
        capacity = (capacity_at_t, None)
    else:
        capacity = (None, nominal)
    _gradients(c, status_labels, sn_labels, capacity, minimum)

    # --- activity costs ---------------------------------------------------
    for attr, sign in (("activity_costs", 1.0), ("inactivity_costs", -1.0)):
        members = c.members(
            lambda k, nc, a=attr: valid_sequence(getattr(nc, a), n_steps)
        )
        if not members:
            continue
        cost = c.steps([getattr(c.nonconvex[k], attr) for k in members], attr)
        cost = cost * c.weight
        const = cost.sum() if sign < 0 else None
        expr = expression(
            model.linopy,
            [(status_labels[members], sign * cost)],
            (f"{attr}_flow", "timestep"),
        ).sum()
        if const is not None:
            expr = expr + const  # (1 - status) * cost
        costs.append(expr)

    if costs:
        total = costs[0]
        for term in costs[1:]:
            total = total + term
        model.add_objective_term(f"{block}.costs", total)


def _investment(c, status_labels, sn_labels):
    """Investment variables of InvestNonConvexFlowBlock: invest is the
    capacity; status_nominal linearises status * invest."""
    model, block = c.model, c.block
    invest = [f.investment for f in c.options]
    offset_flows = np.array([inv.nonconvex is True for inv in invest])
    minimum = c.periods([inv.minimum for inv in invest], "minimum")
    maximum = c.periods([inv.maximum for inv in invest], "maximum")
    ep_costs = c.periods([inv.ep_costs for inv in invest], "ep_costs")
    offset = c.periods([inv.offset for inv in invest], "offset")
    invest_var = model.add_variables(
        f"{block}.invest",
        entities=c.flows,
        entity_dim=c.dim,
        index="capacity_period",
        lower=np.where(offset_flows[:, None], 0.0, minimum),
        upper=maximum,
    )
    invest_labels = invest_var.labels.values
    p_of_t = c.p_of_t
    max_at_t = maximum[:, p_of_t]
    invest_at_t = invest_labels[:, p_of_t]
    # (1) status_nominal <= status * max, (2) status_nominal <= invest,
    # (3) status_nominal >= invest - (1 - status) * max
    c.add(
        "invest_nc_one",
        [(status_labels, max_at_t), (sn_labels, -1.0)],
        ">=",
        0,
    )
    c.add("invest_nc_two", [(invest_at_t, 1.0), (sn_labels, -1.0)], ">=", 0)
    c.add(
        "invest_nc_three",
        [(invest_at_t, 1.0), (status_labels, max_at_t), (sn_labels, -1.0)],
        "<=",
        max_at_t,
    )

    costs = expression(
        model.linopy,
        [(invest_labels, ep_costs)],
        (c.dim, "capacity_period"),
    ).sum()
    nc = np.flatnonzero(offset_flows)
    if nc.size:
        invest_status = model.add_variables(
            f"{block}.invest_status",
            entities=[c.flows[k] for k in nc],
            entity_dim=f"offset_{c.dim}",
            index="capacity_period",
            binary=True,
        )
        dims = (f"offset_{c.dim}", "capacity_period")
        st = invest_status.labels.values
        model.add_constraints(
            f"{block}.minimum_investment",
            expression(
                model.linopy,
                [(st, minimum[nc]), (invest_labels[nc], -1.0)],
                dims,
            ),
            "<=",
            0,
        )
        model.add_constraints(
            f"{block}.maximum_investment",
            expression(
                model.linopy,
                [(invest_labels[nc], 1.0), (st, -maximum[nc])],
                dims,
            ),
            "<=",
            0,
        )
        costs = (
            costs + expression(model.linopy, [(st, offset[nc])], dims).sum()
        )
    return invest_labels, costs


def _startup_shutdown(c, status_labels, previous):
    model, block, n_steps = c.model, c.block, c.n_steps
    costs = []
    for kind, cost_attr, max_attr in (
        ("startup", "startup_costs", "maximum_startups"),
        ("shutdown", "shutdown_costs", "maximum_shutdowns"),
    ):
        members = c.members(
            lambda k, nc, a=cost_attr, b=max_attr: getattr(nc, a) is not None
            or getattr(nc, b) is not None
        )
        if not members:
            continue
        dim = f"{kind}_{c.dim}"
        var = model.add_variables(
            f"{block}.{kind}",
            entities=[c.flows[k] for k in members],
            entity_dim=dim,
            index="timestep",
            binary=True,
        )
        labels = var.labels.values
        rhs = np.zeros((len(members), n_steps))
        if kind == "startup":
            # startup(t) >= status(t) - status(t-1)
            terms = [
                (labels, 1.0),
                (status_labels[members], -1.0),
                (previous[members], 1.0),
            ]
            rhs[:, 0] = -c.initial[members]
        else:
            # shutdown(t) >= status(t-1) - status(t)
            terms = [
                (labels, 1.0),
                (previous[members], -1.0),
                (status_labels[members], 1.0),
            ]
            rhs[:, 0] = c.initial[members]
        c.add(f"{kind}_constr", terms, ">=", rhs, dim=dim)

        limited = [
            row
            for row, k in enumerate(members)
            if getattr(c.nonconvex[k], max_attr) is not None
        ]
        if limited:
            limit = np.array(
                [getattr(c.nonconvex[members[r]], max_attr) for r in limited],
                dtype=float,
            )
            lhs = expression(
                model.linopy,
                [(labels[limited], 1.0)],
                (f"max_{kind}_{c.dim}", "timestep"),
            ).sum("timestep")
            model.add_constraints(
                f"{block}.max_{kind}_constr", lhs, "<=", _da(limit, lhs)
            )

        priced = [
            row
            for row, k in enumerate(members)
            if valid_sequence(getattr(c.nonconvex[k], cost_attr), n_steps)
        ]
        if priced:
            cost = c.steps(
                [getattr(c.nonconvex[members[r]], cost_attr) for r in priced],
                cost_attr,
            )
            if kind == "shutdown":
                # only the shut-down costs are weighted in the Pyomo block
                cost = cost * c.weight
            costs.append(
                expression(
                    model.linopy,
                    [(labels[priced], cost)],
                    (f"{cost_attr}_flow", "timestep"),
                ).sum()
            )
    return costs


def _uptime_downtime(c, status_labels, previous):
    n_steps = c.n_steps
    steps = np.arange(n_steps)
    for kind in ("uptime", "downtime"):
        attr = f"minimum_{kind}"
        members = c.members(lambda k, nc, a=attr: getattr(nc, a).max() > 0)
        if not members:
            continue
        duration = c.steps(
            [getattr(c.nonconvex[k], attr) for k in members], attr
        ).astype(int)
        window = np.minimum(steps + duration, n_steps) - steps  # L(t)
        width = int(window.max()) if window.size else 0
        status = status_labels[members]
        initial = c.initial[members][:, None]
        first = (steps == 0)[None, :]
        window_terms = []
        for d in range(width):
            shifted = np.full_like(status, -1)
            shifted[:, : n_steps - d] = status[:, d:]
            window_terms.append(np.where(d < window, shifted, -1))
        if kind == "uptime":
            # (status(t) - status(t-1)) L(t) - sum_window status <= 0
            terms = [(status, window), (previous[members], -window)]
            terms += [(lab, -1.0) for lab in window_terms]
            # status(-1) is the initial status, a constant:
            # status(0) L - initial L - ... <= 0  ->  ... <= initial L
            rhs = np.where(first, initial * window, 0.0)
            mask = window > 0
        else:
            # (status(t-1) - status(t)) D - D + sum_window status <= 0
            terms = [(previous[members], duration), (status, -duration)]
            terms += [(lab, 1.0) for lab in window_terms]
            rhs = duration - np.where(first, initial * duration, 0.0)
            mask = duration > 0
        c.add(
            f"min_{kind}_constr",
            terms,
            "<=",
            rhs,
            dim=f"min_{kind}_{c.dim}",
            mask=mask,
        )


def _gradients(c, status_labels, sn_labels, capacity, minimum):
    """Gradient limits of nonconvex flows, see
    oemof.solph.flows._shared.shared_constraints_for_non_convex_flows."""
    n_steps, p_of_t = c.n_steps, c.p_of_t
    capacity_labels, nominal = capacity
    for direction in ("positive", "negative"):
        members = [
            k
            for k, f in enumerate(c.options)
            if _gradient_limit(f, direction) is not None
        ]
        if not members:
            continue
        limit = c.steps(
            [_gradient_limit(c.options[k], direction) for k in members],
            f"{direction}_gradient_limit",
        )
        m_now = minimum[members]
        m_prev = np.roll(m_now, 1, axis=1)
        mask = np.ones((len(members), n_steps), dtype=bool)
        mask[:, 0] = False
        flow_now = c.flow_labels[members]
        flow_prev = np.roll(flow_now, 1, axis=1)
        if nominal is not None:
            cap = nominal[members]
            cap_prev = np.roll(cap, 1, axis=1)
            mask &= cap != 0
            with np.errstate(divide="ignore", invalid="ignore"):
                ratio = np.where(cap != 0, cap_prev / cap, 1.0)
            st_now = status_labels[members]
            st_prev = np.roll(st_now, 1, axis=1)
        else:
            mask[:, 1:] &= p_of_t[1:] == p_of_t[:-1]
            ratio = np.ones_like(limit)
            st_now = sn_labels[members]  # status * capacity
            st_prev = np.roll(st_now, 1, axis=1)
            cap = np.ones_like(limit)
        if direction == "positive":
            start = np.maximum(limit, m_now)
            off = np.minimum(start, limit + m_prev * ratio)
            # P(t) - P(t-1) - (G - S) on(t-1) - off on(t) - (S - off) cap
            terms = [
                (flow_now, 1.0),
                (flow_prev, -1.0),
                (
                    st_prev,
                    -(limit - start) * (cap if nominal is not None else 1),
                ),
                (st_now, -off * (cap if nominal is not None else 1)),
            ]
            constant = (start - off) * cap
        else:
            stop = np.maximum(limit, m_prev * ratio)
            off = np.minimum(stop, limit + m_now)
            # P(t-1) - P(t) - (G - S) on(t) - off on(t-1) - (S - off) cap
            terms = [
                (flow_prev, 1.0),
                (flow_now, -1.0),
                (
                    st_now,
                    -(limit - stop) * (cap if nominal is not None else 1),
                ),
                (st_prev, -off * (cap if nominal is not None else 1)),
            ]
            constant = (stop - off) * cap
        if nominal is None:
            # the capacity is the invest variable
            terms.append((capacity_labels[members], -constant))
            rhs = np.zeros_like(constant)
        else:
            rhs = constant
        c.add(
            f"{direction}_gradient_constr",
            terms,
            "<=",
            np.where(mask, rhs, 0.0),
            dim=f"{direction}_gradient_{c.dim}",
            mask=mask,
        )


def _da(values, like):
    import xarray as xr

    dims = [d for d in like.dims if d != "_term"]
    values = np.broadcast_to(
        np.asarray(values, dtype=float),
        tuple(like.sizes[d] for d in dims),
    )
    return xr.DataArray(
        values,
        dims=dims,
        coords={d: like.coords[d] for d in dims if d in like.coords},
    )
