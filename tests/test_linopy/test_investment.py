# -*- coding: utf-8 -*-

"""Equivalence of the linopy and the Pyomo backend: investment flows and
storages.

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd
import pytest

from oemof import solph

pytest.importorskip("linopy")

from .equivalence import assert_backends_agree  # noqa: E402
from .equivalence import assert_frames_agree  # noqa: E402

N_STEPS = 48
RNG = np.random.default_rng(7)
PRICE = 30 + 60 * RNG.random(N_STEPS)
PV = np.clip(np.sin(np.linspace(0, 4 * np.pi, N_STEPS)), 0, None)
DEMAND = 3 + 2 * RNG.random(N_STEPS)


def _es():
    idx = pd.date_range("2025-01-01", periods=N_STEPS, freq="h")
    return solph.EnergySystem(timeindex=idx, infer_last_interval=True)


def investment_flow_system():
    es = _es()
    el = solph.Bus("el")
    es.add(el)
    es.add(
        solph.components.Source(
            "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
        ),
        # convex investment into a fixed profile, with existing capacity
        solph.components.Source(
            "pv",
            outputs={
                el: solph.Flow(
                    fix=PV,
                    nominal_capacity=solph.Investment(
                        ep_costs=15, existing=1, maximum=20
                    ),
                )
            },
        ),
        # nonconvex investment with offset and minimum
        solph.components.Source(
            "engine",
            outputs={
                el: solph.Flow(
                    variable_costs=45,
                    minimum=0.1,
                    nominal_capacity=solph.Investment(
                        ep_costs=8,
                        offset=40,
                        minimum=1,
                        maximum=10,
                        nonconvex=True,
                    ),
                )
            },
        ),
        # full-load-time limits on an investment flow
        solph.components.Source(
            "limited",
            outputs={
                el: solph.Flow(
                    variable_costs=5,
                    full_load_time_max=8,
                    full_load_time_min=2,
                    nominal_capacity=solph.Investment(ep_costs=20),
                )
            },
        ),
        solph.components.Sink(
            "demand",
            inputs={el: solph.Flow(fix=DEMAND / 5, nominal_capacity=5)},
        ),
        solph.components.Sink(
            "dump", inputs={el: solph.Flow(variable_costs=1)}
        ),
    )
    return es


def storage_system(invest=False, **storage_kwargs):
    es = _es()
    el = solph.Bus("el")
    es.add(el)
    es.add(
        solph.components.Source(
            "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
        ),
        solph.components.Sink(
            "demand",
            inputs={el: solph.Flow(fix=DEMAND / 5, nominal_capacity=5)},
        ),
    )
    if invest:
        storage = solph.components.GenericStorage(
            "battery",
            inputs={
                el: solph.Flow(nominal_capacity=solph.Investment(ep_costs=2))
            },
            outputs={
                el: solph.Flow(nominal_capacity=solph.Investment(ep_costs=1))
            },
            nominal_capacity=solph.Investment(**invest),
            **storage_kwargs,
        )
    else:
        storage = solph.components.GenericStorage(
            "battery",
            inputs={el: solph.Flow(nominal_capacity=3)},
            outputs={el: solph.Flow(nominal_capacity=3)},
            nominal_capacity=12,
            **storage_kwargs,
        )
    es.add(storage)
    return es


def test_investment_flows():
    pyomo, linopy_ = assert_backends_agree(investment_flow_system)
    for key in ("invest", "nominal_capacity", "invest_status"):
        assert_frames_agree(pyomo.get(key), linopy_.get(key))


def test_investment_flows_with_cbc():
    assert_backends_agree(investment_flow_system, solver="cbc", compare=())


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(loss_rate=0.01, balanced=True),
        dict(
            loss_rate=0.02,
            initial_storage_level=0.5,
            balanced=False,
            inflow_conversion_factor=0.95,
            outflow_conversion_factor=0.9,
            min_storage_level=0.1,
            max_storage_level=0.9,
        ),
        dict(fixed_losses_relative=0.001, fixed_losses_absolute=0.01),
        dict(storage_costs=0.5),
    ],
    ids=["balanced", "levels and efficiencies", "fixed losses", "costs"],
)
def test_storage(kwargs):
    pyomo, linopy_ = assert_backends_agree(
        lambda: storage_system(**kwargs), compare=("flow", "storage_content")
    )
    assert_frames_agree(
        pyomo.get("storage_losses"), linopy_.get("storage_losses")
    )


@pytest.mark.parametrize(
    "invest,kwargs",
    [
        (dict(ep_costs=3), dict(loss_rate=0.01)),
        (
            dict(ep_costs=3, existing=2),
            dict(
                initial_storage_level=0.5,
                invest_relation_input_capacity=1 / 4,
                invest_relation_output_capacity=1 / 4,
                min_storage_level=0.1,
            ),
        ),
        (
            dict(ep_costs=1, offset=10, minimum=2, maximum=30, nonconvex=True),
            dict(invest_relation_input_output=1, fixed_losses_relative=0.002),
        ),
    ],
    ids=["convex", "existing and relations", "nonconvex"],
)
def test_investment_storage(invest, kwargs):
    pyomo, linopy_ = assert_backends_agree(
        lambda: storage_system(invest=invest, **kwargs),
        compare=("flow", "storage_content", "invest", "storage_capacity"),
    )
    if invest.get("nonconvex"):
        assert_frames_agree(
            pyomo.get("invest_status"), linopy_.get("invest_status")
        )


def test_storage_duals():
    assert_backends_agree(
        lambda: storage_system(loss_rate=0.01),
        duals=True,
        compare=("flow", "storage_content"),
    )
