"""
This example compares a cheap and an expensive heat pump, with the latter
adding a fixed invest cost offset to the objective function.

SPDX-FileCopyrightText: Jonas Freißmann
SPDX-FileCopyrightText: Malte Fritz

SPDX-License-Identifier: MIT
"""

import pandas as pd

from oemof.solph import EnergySystem
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import NonConvex
from oemof.solph import components
from oemof.solph import processing
from oemof.solph.buses import Bus
from oemof.solph.flows import Flow


def test_non_convex_investment_offset():
    # Energy System
    energy_system = EnergySystem(
        timeindex=pd.date_range(start="2025-01-01 12:00", freq="h", periods=2),
        infer_last_interval=False,
    )

    # Buses
    b_el = Bus("electricity bus")
    b_th = Bus("heat bus")

    energy_system.add(b_el, b_th)

    # Source & Sink
    el_source = components.Source("electricity source", outputs={b_el: Flow()})

    th_sink = components.Sink(
        "heat sink", inputs={b_th: Flow(nominal_capacity=1, fix=[1])}
    )

    energy_system.add(el_source, th_sink)

    # Converter
    hp_expensive = components.Converter(
        "heat pump expensive",
        inputs={b_el: Flow()},
        outputs={
            b_th: Flow(
                nominal_capacity=Investment(
                    ep_costs=100,
                    offset=2000,
                    maximum=1,
                    minimum=0,
                    nonconvex=True,
                ),
                variable_costs=1,
                max=1,
                min=0.1,
                nonconvex=NonConvex(),
            )
        },
        conversion_factors={b_el: [3]},
    )

    hp_cheap = components.Converter(
        "heat pump cheap",
        inputs={b_el: Flow()},
        outputs={
            b_th: Flow(
                nominal_capacity=Investment(
                    ep_costs=50, maximum=1, minimum=0, nonconvex=True
                ),
                variable_costs=1,
                max=1,
                min=0.1,
                nonconvex=NonConvex(),
            )
        },
        conversion_factors={b_el: [3]},
    )

    energy_system.add(hp_expensive, hp_cheap)

    # Model
    model = Model(energy_system)

    # Optimization
    model.solve(solver="cbc", solve_kwargs={"tee": True})

    # Check Objective
    meta_results = processing.meta_results(model)

    # Cheap heat pump should be built (50) and dispatched (1). The investment
    # offset of the expensive heat pump (2000) should be ignored.
    assert meta_results["objective"] == 51.0
