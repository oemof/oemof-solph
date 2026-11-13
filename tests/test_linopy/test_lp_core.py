# -*- coding: utf-8 -*-

"""Equivalence of the linopy and the Pyomo backend: flows, buses,
converters, sources and sinks.

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd
import pytest

from oemof import solph

pytest.importorskip("linopy")

from oemof.solph import processing  # noqa: E402
from oemof.solph import views  # noqa: E402

from .equivalence import assert_backends_agree  # noqa: E402
from .equivalence import assert_frames_agree  # noqa: E402
from .equivalence import solve_both  # noqa: E402

N_STEPS = 48
RNG = np.random.default_rng(42)
PRICE = 40 + 40 * RNG.random(N_STEPS)
HEAT = 4 + 4 * RNG.random(N_STEPS)
POWER = 2 + 2 * RNG.random(N_STEPS)
COP = 2.5 + RNG.random(N_STEPS)


def _es(timeincrement=None):
    if timeincrement is not None:
        return solph.EnergySystem(
            timeincrement=timeincrement, infer_last_interval=False
        )
    idx = pd.date_range("2025-01-01", periods=N_STEPS, freq="h")
    return solph.EnergySystem(timeindex=idx, infer_last_interval=True)


def dispatch_system(timeincrement=None):
    """Grid, gas, CHP with two outputs, heat pump, boiler, demands."""
    es = _es(timeincrement)
    el, heat, gas = solph.Bus("el"), solph.Bus("heat"), solph.Bus("gas")
    es.add(el, heat, gas)
    es.add(
        solph.components.Source(
            "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
        ),
        solph.components.Sink(
            "export",
            inputs={
                el: solph.Flow(variable_costs=-0.9 * PRICE, nominal_capacity=3)
            },
        ),
        solph.components.Source(
            "gas supply", outputs={gas: solph.Flow(variable_costs=35)}
        ),
        solph.components.Converter(
            "chp",
            inputs={gas: solph.Flow()},
            outputs={
                el: solph.Flow(nominal_capacity=4, minimum=0.2),
                heat: solph.Flow(nominal_capacity=5),
            },
            conversion_factors={el: 0.35, heat: 0.5},
        ),
        solph.components.Converter(
            "heat pump",
            inputs={el: solph.Flow()},
            outputs={heat: solph.Flow(nominal_capacity=3)},
            conversion_factors={heat: COP},
        ),
        solph.components.Converter(
            "boiler",
            inputs={gas: solph.Flow()},
            outputs={heat: solph.Flow(nominal_capacity=10, variable_costs=1)},
            conversion_factors={heat: 0.95},
        ),
        solph.components.Sink(
            "heat demand",
            inputs={heat: solph.Flow(fix=HEAT / 8, nominal_capacity=8)},
        ),
        solph.components.Sink(
            "power demand",
            inputs={el: solph.Flow(fix=POWER / 4, nominal_capacity=4)},
        ),
    )
    return es


def limits_system():
    """Full-load-time limits and gradient limits."""
    es = dispatch_system()
    el = es.groups["el"]
    es.add(
        solph.components.Source(
            "cheap but limited",
            outputs={
                el: solph.Flow(
                    nominal_capacity=6,
                    variable_costs=5,
                    full_load_time_max=10,
                    positive_gradient_limit=0.2,
                    negative_gradient_limit=0.3,
                )
            },
        ),
        solph.components.Source(
            "must run",
            outputs={
                el: solph.Flow(
                    nominal_capacity=2,
                    variable_costs=90,
                    full_load_time_min=12,
                )
            },
        ),
    )
    return es


def integer_system():
    """A flow restricted to integer values (MILP)."""
    es = dispatch_system()
    heat = es.groups["heat"]
    es.add(
        solph.components.Source(
            "integer heat",
            outputs={
                heat: solph.Flow(
                    nominal_capacity=4, variable_costs=20, integer=True
                )
            },
        )
    )
    return es


def test_dispatch():
    assert_backends_agree(dispatch_system)


def test_dispatch_with_cbc():
    assert_backends_agree(dispatch_system, solver="cbc")


def test_non_equidistant_timeincrement():
    increments = np.where(np.arange(N_STEPS) % 3 == 0, 2.0, 0.5)
    assert_backends_agree(lambda: dispatch_system(timeincrement=increments))


def test_full_load_time_and_gradients():
    pyomo, linopy_ = assert_backends_agree(limits_system)
    for key in ("positive_gradient", "negative_gradient"):
        assert_frames_agree(pyomo.get(key), linopy_.get(key))


def test_integer_flow():
    pyomo, linopy_ = assert_backends_agree(integer_system, compare=())
    assert_frames_agree(pyomo.get("integer_flow"), linopy_.get("integer_flow"))
    values = linopy_.get("integer_flow").to_numpy()
    np.testing.assert_allclose(values, np.round(values), atol=1e-6)


def test_duals_and_reduced_costs():
    assert_backends_agree(dispatch_system, duals=True)


def test_processing_results_and_views():
    pyomo_model, _, linopy_model, _ = solve_both(dispatch_system, duals=True)
    pyomo_results = processing.results(pyomo_model)
    linopy_results = processing.results(linopy_model)

    def by_label(results):
        return {
            tuple(str(getattr(k, "label", k)) for k in key): value
            for key, value in results.items()
        }

    pyomo_results, linopy_results = by_label(pyomo_results), by_label(
        linopy_results
    )
    assert pyomo_results.keys() == linopy_results.keys()
    for key in pyomo_results:
        left = pyomo_results[key]["sequences"]
        right = linopy_results[key]["sequences"]
        assert list(left.columns) == list(right.columns), key
        np.testing.assert_allclose(
            left.to_numpy(dtype=float), right.to_numpy(dtype=float), atol=1e-6
        )

    pyomo_view = views.node(processing.results(pyomo_model), "heat")
    linopy_view = views.node(processing.results(linopy_model), "heat")
    assert pyomo_view["sequences"].shape == linopy_view["sequences"].shape
    np.testing.assert_allclose(
        pyomo_view["sequences"].to_numpy(dtype=float),
        linopy_view["sequences"].to_numpy(dtype=float),
        atol=1e-6,
    )


def test_results_keys_and_objective_call():
    _, _, linopy_model, results = solve_both(dispatch_system)
    assert "flow" in results.keys()
    assert linopy_model.objective() == pytest.approx(
        results.solver["objective"]
    )


def test_solver_options_reach_the_solver(capfd):
    """cmdline_options go to the solver by name; with tee the log shows."""
    from oemof.solph._linopy import LinopyModel

    model = LinopyModel(dispatch_system())
    model.solve(
        solver="highs",
        cmdline_options={"presolve": "off"},
        solve_kwargs={"tee": True},
    )
    assert "without presolve" in capfd.readouterr().out


def test_solve_without_constraints_with_cbc():
    """CBC rejects LP files without constraints; a dummy one is added."""
    from oemof.solph._linopy import LinopyModel

    es = _es()
    bus = solph.buses.Bus(label="bus", balanced=False)
    es.add(bus)
    bus.inputs[bus] = solph.Flow(nominal_capacity=2, variable_costs=-1)
    results = LinopyModel(es).solve(solver="cbc")
    assert results.solver["objective"] == pytest.approx(-2 * N_STEPS)
