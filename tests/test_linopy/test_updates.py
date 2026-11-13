# -*- coding: utf-8 -*-

"""Parameter updates with in-place re-solves, and the solver paths of the
linopy backend.

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd
import pytest

from oemof import solph

linopy = pytest.importorskip("linopy")

from linopy.solvers import RebuildRequiredError  # noqa: E402

from oemof.solph._linopy import LinopyModel  # noqa: E402

N_STEPS = 48
RNG = np.random.default_rng(13)
PRICE = 30 + 60 * RNG.random(N_STEPS)
DEMAND = 3 + 2 * RNG.random(N_STEPS)
COP = 2.5 + RNG.random(N_STEPS)


def system():
    idx = pd.date_range("2025-01-01", periods=N_STEPS, freq="h")
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=True)
    el, heat = solph.Bus("el"), solph.Bus("heat")
    es.add(el, heat)
    es.add(
        solph.components.Source(
            "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
        ),
        solph.components.Converter(
            "heat pump",
            inputs={el: solph.Flow()},
            outputs={
                heat: solph.Flow(
                    nominal_capacity=solph.Investment(ep_costs=20, maximum=10)
                )
            },
            conversion_factors={heat: COP},
        ),
        solph.components.Source(
            "boiler", outputs={heat: solph.Flow(variable_costs=90)}
        ),
        solph.components.Sink(
            "demand",
            inputs={heat: solph.Flow(fix=DEMAND / 5, nominal_capacity=5)},
        ),
        solph.components.GenericStorage(
            "tank",
            inputs={heat: solph.Flow(nominal_capacity=3)},
            outputs={heat: solph.Flow(nominal_capacity=3)},
            nominal_capacity=10,
            loss_rate=0.01,
        ),
    )
    return es


def _nodes(es):
    g = es.groups
    return g["grid"], g["el"], g["heat pump"], g["heat"], g["demand"]


def _apply(es, change):
    """The same change, applied to an energy system directly."""
    grid, el, hp, heat, demand = _nodes(es)
    flows, nodes = change(grid, el, hp, heat, demand, es.groups["tank"])
    for key, attrs in flows.items():
        for name, value in attrs.items():
            *path, attr = name.split(".")
            target = es.flows()[key]
            for part in path:
                target = getattr(target, part)
            setattr(target, attr, value)
    for node, attrs in nodes.items():
        for name, value in attrs.items():
            current = getattr(node, name)
            if isinstance(value, dict):
                current = dict(current)
                current.update(value)
                value = current
            setattr(node, name, value)


CHANGES = {
    "variable costs": lambda grid, el, hp, heat, demand, tank: (
        {(grid, el): {"variable_costs": 1.2 * PRICE}},
        {},
    ),
    "fixed demand": lambda grid, el, hp, heat, demand, tank: (
        {(heat, demand): {"fix": 1.1 * DEMAND / 5}},
        {},
    ),
    "flow bound": lambda grid, el, hp, heat, demand, tank: (
        {(tank, heat): {"maximum": 0.5}},
        {},
    ),
    "nominal capacity": lambda grid, el, hp, heat, demand, tank: (
        {(heat, tank): {"nominal_capacity": 1.5}},
        {},
    ),
    "conversion factor": lambda grid, el, hp, heat, demand, tank: (
        {},
        {hp: {"conversion_factors": {heat: COP * 0.9}}},
    ),
    "investment costs": lambda grid, el, hp, heat, demand, tank: (
        {(hp, heat): {"investment.ep_costs": 35}},
        {},
    ),
    "storage losses": lambda grid, el, hp, heat, demand, tank: (
        {},
        {tank: {"loss_rate": 0.05}},
    ),
}


@pytest.mark.parametrize("name", list(CHANGES))
def test_update_resolves_in_place_like_a_fresh_model(name):
    model = LinopyModel(system())
    model.solve(solver="highs", persistent=True)
    flows, nodes = CHANGES[name](*_nodes(model.es), model.es.groups["tank"])
    model.update(flows=flows, nodes=nodes)
    updated = model.resolve(require_in_place=True)

    es = system()
    _apply(es, CHANGES[name])
    fresh = LinopyModel(es).solve(solver="highs")
    assert updated.solver["objective"] == pytest.approx(
        fresh.solver["objective"], rel=1e-7
    )


def test_structural_change_needs_a_rebuild():
    model = LinopyModel(system())
    model.solve(solver="highs", persistent=True)
    grid, el, *_ = _nodes(model.es)
    model.add_custom_constraints(
        lambda m: m.linopy.add_constraints(
            m.flow_var(grid, el) <= 2, name="grid_limit"
        )
    )
    with pytest.raises(RebuildRequiredError):
        model.resolve(require_in_place=True)
    limited = model.resolve()
    assert limited.get("flow")[(grid, el)].max() <= 2 + 1e-6


def test_custom_constraints_survive_updates():
    model = LinopyModel(system())
    grid, el, *_ = _nodes(model.es)
    model.add_custom_constraints(
        lambda m: m.linopy.add_constraints(
            m.flow_var(grid, el) <= 3, name="grid_limit"
        )
    )
    model.solve(solver="highs", persistent=True)
    model.update(flows={(grid, el): {"variable_costs": 0.5 * PRICE}})
    results = model.resolve(require_in_place=True)
    assert results.get("flow")[(grid, el)].max() <= 3 + 1e-6


def test_resolve_needs_a_persistent_solve():
    model = LinopyModel(system())
    model.solve(solver="highs")
    with pytest.raises(RuntimeError, match="persistent=True"):
        model.resolve()


def test_solve_kwargs_are_translated():
    with pytest.warns(UserWarning, match="no equivalent"):
        LinopyModel(system()).solve(
            solver="highs", solve_kwargs={"mip_rel_gap": 0.01}
        )
    results = LinopyModel(system()).solve(
        solver="highs",
        solve_kwargs={"timelimit": 60, "symbolic_solver_labels": True},
    )
    assert results.solver["optimal"]
