# -*- coding: utf-8 -*-

"""Equivalence of the linopy and the Pyomo backend: nonconvex flows,
nonconvex investment flows and offset converters (MILP).

MILPs can have alternative optima; the tests compare the objective and,
where the optimum is unique by construction, the flows.

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd
import pytest

from oemof import solph

pytest.importorskip("linopy")

from .equivalence import assert_backends_agree  # noqa: E402
from .equivalence import solve_both  # noqa: E402

N_STEPS = 24
RNG = np.random.default_rng(3)
PRICE = np.round(20 + 80 * RNG.random(N_STEPS))
DEMAND = np.round(4 + 6 * RNG.random(N_STEPS), 1)


def _es():
    idx = pd.date_range("2025-01-01", periods=N_STEPS, freq="h")
    return solph.EnergySystem(timeindex=idx, infer_last_interval=True)


def unit_commitment(**nonconvex):
    """A gas engine with a nonconvex flow next to an expensive grid."""

    def build():
        es = _es()
        el, gas = solph.Bus("el"), solph.Bus("gas")
        es.add(el, gas)
        es.add(
            solph.components.Source(
                "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
            ),
            solph.components.Source(
                "gas supply", outputs={gas: solph.Flow(variable_costs=20)}
            ),
            solph.components.Converter(
                "engine",
                inputs={gas: solph.Flow()},
                outputs={
                    el: solph.Flow(
                        nominal_capacity=8,
                        minimum=0.4,
                        nonconvex=solph.NonConvex(**nonconvex),
                    )
                },
                conversion_factors={el: 0.4},
            ),
            solph.components.Sink(
                "demand",
                inputs={el: solph.Flow(fix=DEMAND / 10, nominal_capacity=10)},
            ),
        )
        return es

    return build


@pytest.mark.parametrize(
    "nonconvex",
    [
        dict(),
        dict(startup_costs=30, shutdown_costs=10),
        dict(startup_costs=30, maximum_startups=2, maximum_shutdowns=2),
        dict(minimum_uptime=4, minimum_downtime=3, startup_costs=5),
        dict(minimum_uptime=3, initial_status=1, minimum_downtime=2),
        dict(activity_costs=12, inactivity_costs=4),
        dict(positive_gradient_limit=0.3, negative_gradient_limit=0.5),
        dict(
            positive_gradient_limit=[0.2] * 12 + [0.6] * 12,
            startup_costs=20,
            initial_status=1,
        ),
    ],
    ids=[
        "status",
        "start and stop costs",
        "start and stop limits",
        "up and down times",
        "initial status on",
        "activity costs",
        "gradients",
        "gradient sequence",
    ],
)
def test_nonconvex_flow(nonconvex):
    assert_backends_agree(unit_commitment(**nonconvex), compare=())


def test_nonconvex_flow_with_cbc():
    assert_backends_agree(
        unit_commitment(startup_costs=30, minimum_uptime=3),
        solver="cbc",
        compare=(),
    )


def invest_nonconvex(**investment):
    def build():
        es = _es()
        el = solph.Bus("el")
        es.add(el)
        es.add(
            solph.components.Source(
                "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
            ),
            solph.components.Source(
                "engine",
                outputs={
                    el: solph.Flow(
                        variable_costs=40,
                        minimum=0.3,
                        nominal_capacity=solph.Investment(**investment),
                        nonconvex=solph.NonConvex(
                            startup_costs=15, positive_gradient_limit=0.5
                        ),
                    )
                },
            ),
            solph.components.Sink(
                "demand",
                inputs={el: solph.Flow(fix=DEMAND / 10, nominal_capacity=10)},
            ),
        )
        return es

    return build


@pytest.mark.parametrize(
    "investment",
    [
        dict(ep_costs=50, maximum=12),
        dict(ep_costs=40, offset=200, minimum=2, maximum=12, nonconvex=True),
    ],
    ids=["linear", "offset"],
)
def test_invest_nonconvex_flow(investment):
    assert_backends_agree(invest_nonconvex(**investment), compare=("invest",))


def offset_converter_system():
    es = _es()
    el, gas, heat = solph.Bus("el"), solph.Bus("gas"), solph.Bus("heat")
    es.add(el, gas, heat)
    slope, offset = solph.components.slope_offset_from_nonconvex_output(
        1, 0.5, 0.4, 0.3
    )
    es.add(
        solph.components.Source(
            "gas supply", outputs={gas: solph.Flow(variable_costs=20)}
        ),
        solph.components.Source(
            "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
        ),
        solph.components.OffsetConverter(
            label="chp",
            inputs={gas: solph.Flow()},
            outputs={
                el: solph.Flow(
                    nominal_capacity=6,
                    minimum=0.5,
                    nonconvex=solph.NonConvex(),
                ),
            },
            conversion_factors={gas: slope},
            normed_offsets={gas: offset},
        ),
        solph.components.Sink(
            "demand",
            inputs={el: solph.Flow(fix=DEMAND / 10, nominal_capacity=10)},
        ),
        solph.components.Sink("heat sink", inputs={heat: solph.Flow()}),
    )
    return es


def test_offset_converter():
    assert_backends_agree(offset_converter_system, compare=())


def test_relaxed_milp_matches():
    """relax_problem() gives the same LP relaxation on both backends."""
    from oemof.solph._linopy import LinopyModel
    from oemof.solph._models import Model as PyomoModel

    build = unit_commitment(startup_costs=30, minimum_uptime=3)
    pyomo = PyomoModel(build()).relax_problem().solve(solver="highs")
    linopy_ = LinopyModel(build()).relax_problem().solve(solver="highs")
    assert linopy_.solver["objective"] == pytest.approx(
        pyomo.solver["objective"], rel=1e-6
    )


def test_status_results():
    _, pyomo, _, linopy_ = solve_both(unit_commitment(startup_costs=30))
    assert "status" in linopy_.keys()
    assert (
        linopy_.get("status").shape
        == pyomo.get("status").dropna(axis=1, how="all").shape
    )
