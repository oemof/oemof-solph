# -*- coding: utf-8 -*-

"""linopy builder for the investment flow block.

SPDX-License-Identifier: MIT
"""

import numpy as np

from oemof.solph._linopy._data import to_array
from oemof.solph._linopy._indexing import expression
from oemof.solph._linopy._indexing import take
from oemof.solph._linopy._registry import register_builder
from oemof.solph.flows._investment_flow_block import InvestmentFlowBlock

BLOCK = "InvestmentFlowBlock"


def total_capacity_terms(var_labels, invest, existing):
    """Terms of ``capacity[k, p] - sum_{rp in relevant(p)} invest[k, rp]``.

    Parameters
    ----------
    var_labels : (capacity_labels, invest_labels), both (entities, periods)
    invest : list of Investment
    existing : numpy.ndarray (entities, periods)

    Returns
    -------
    terms for :func:`expression` over (entities, periods), and the
    right-hand side (the existing capacity).
    """
    capacity_labels, invest_labels = var_labels
    n_entities, n_periods = capacity_labels.shape
    terms = [(capacity_labels, 1.0)]
    for rp in range(n_periods):
        labels = np.full((n_entities, n_periods), -1, dtype=np.int64)
        for k, inv in enumerate(invest):
            for p in range(n_periods):
                if rp in inv.relevant_periods(p):
                    labels[k, p] = invest_labels[k, rp]
        terms.append((labels, -1.0))
    return terms, existing


@register_builder(InvestmentFlowBlock)
def build_investment_flows(model, group):
    """Investment flows (convex and with a nonconvex investment)."""
    n_steps = len(model.TIMESTEPS)
    n_periods = len(model.CAPACITY_PERIODS)
    p_of_t = model.period_of_timestep
    flows = [(i, o) for i, o, _ in group]
    invest = [f.investment for _, _, f in group]
    nonconvex = np.array([inv.nonconvex is True for inv in invest])

    def per_period(attr):
        return np.array(
            [to_array(getattr(inv, attr), n_periods, attr) for inv in invest]
        )

    minimum, maximum = per_period("minimum"), per_period("maximum")
    ep_costs, offset = per_period("ep_costs"), per_period("offset")
    existing = per_period("existing")

    lower = np.where(nonconvex[:, None], 0.0, minimum)
    invest_var = model.add_variables(
        f"{BLOCK}.invest",
        entities=flows,
        entity_dim="invest_flow",
        index="capacity_period",
        lower=lower,
        upper=maximum,
    )
    capacity = model.add_variables(
        f"{BLOCK}.nominal_capacity",
        entities=flows,
        entity_dim="invest_flow",
        index="capacity_period",
        lower=0,
    )
    model.invest_flow_capacity = {
        f: capacity.labels.values[k] for k, f in enumerate(flows)
    }

    # nominal capacity = investments of relevant periods + existing
    terms, rhs = total_capacity_terms(
        (capacity.labels.values, invest_var.labels.values), invest, existing
    )
    lhs = expression(model.linopy, terms, ("invest_flow", "capacity_period"))
    model.add_constraints(
        f"{BLOCK}.total_capacity_rule", lhs, "=", _like(rhs, lhs)
    )

    flow_labels = model.flow.labels.values
    positions = np.array([model.flow_position(i, o) for i, o in flows])
    capacity_at_t = capacity.labels.values[:, p_of_t]  # (invest_flow, T)

    def flow_capacity_constraint(name, members, factor_attr, sign, dim):
        if not members:
            return
        factor = np.array(
            [
                to_array(
                    getattr(group[k][2], factor_attr), n_steps, factor_attr
                )
                for k in members
            ]
        )
        lhs = expression(
            model.linopy,
            [
                (take(flow_labels, positions[members]), 1.0),
                (capacity_at_t[members], -factor),
            ],
            (dim, "timestep"),
        )
        model.add_constraints(f"{BLOCK}.{name}", lhs, sign, 0)

    fixed = [k for k, (_, _, f) in enumerate(group) if f.fix is not None]
    not_fixed = [k for k, (_, _, f) in enumerate(group) if f.fix is None]
    with_min = [k for k, (_, _, f) in enumerate(group) if f.minimum.min() != 0]
    flow_capacity_constraint("fixed", fixed, "fix", "=", "fixed_invest_flow")
    flow_capacity_constraint(
        "max", not_fixed, "maximum", "<=", "max_invest_flow"
    )
    flow_capacity_constraint(
        "min", with_min, "minimum", ">=", "min_invest_flow"
    )

    # full load time: sum_t P(t) * tau(t) <=/>= F * sum_p capacity(p)
    for attr, sign in (
        ("full_load_time_max", "<="),
        ("full_load_time_min", ">="),
    ):
        members = [
            k
            for k, (_, _, f) in enumerate(group)
            if getattr(f, attr) is not None
        ]
        if not members:
            continue
        hours = np.array([getattr(group[k][2], attr) for k in members])
        flow_part = expression(
            model.linopy,
            [
                (
                    take(flow_labels, positions[members]),
                    model.timeincrement_array,
                )
            ],
            (f"{attr}_invest_flow", "timestep"),
        ).sum("timestep")
        capacity_part = expression(
            model.linopy,
            [(capacity.labels.values[members], -hours[:, None])],
            (f"{attr}_invest_flow", "capacity_period"),
        ).sum("capacity_period")
        model.add_constraints(
            f"{BLOCK}.{attr}", flow_part + capacity_part, sign, 0
        )

    costs = expression(
        model.linopy,
        [(invest_var.labels.values, ep_costs)],
        ("invest_flow", "capacity_period"),
    ).sum()

    nc = np.flatnonzero(nonconvex)
    if nc.size:
        nc_flows = [flows[k] for k in nc]
        status = model.add_variables(
            f"{BLOCK}.invest_status",
            entities=nc_flows,
            entity_dim="nonconvex_invest_flow",
            index="capacity_period",
            binary=True,
        )
        dims = ("nonconvex_invest_flow", "capacity_period")
        invest_nc = invest_var.labels.values[nc]
        # minimum * status <= invest, invest <= maximum * status
        model.add_constraints(
            f"{BLOCK}.minimum_rule",
            expression(
                model.linopy,
                [(status.labels.values, minimum[nc]), (invest_nc, -1.0)],
                dims,
            ),
            "<=",
            0,
        )
        model.add_constraints(
            f"{BLOCK}.maximum_rule",
            expression(
                model.linopy,
                [(invest_nc, 1.0), (status.labels.values, -maximum[nc])],
                dims,
            ),
            "<=",
            0,
        )
        costs = (
            costs
            + expression(
                model.linopy, [(status.labels.values, offset[nc])], dims
            ).sum()
        )

    model.add_expression(f"{BLOCK}.investment_costs", costs)
    model.add_objective_term(f"{BLOCK}.investment_costs", costs)


def _like(values, like):
    import xarray as xr

    dims = [d for d in like.dims if d != "_term"]
    return xr.DataArray(
        np.asarray(values, dtype=float),
        dims=dims,
        coords={d: like.coords[d] for d in dims if d in like.coords},
    )
