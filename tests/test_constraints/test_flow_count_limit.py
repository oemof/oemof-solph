# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import pandas as pd
import pytest

from oemof import solph


def test_flow_count_limit():
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=False,
    )

    b1 = solph.buses.Bus(label="b1", balanced=False)
    s0 = solph.components.Sink(
        label="s0",
        inputs={
            b1: solph.Flow(
                variable_costs=[-0.5, 0.5],
                nominal_capacity=4,
                minimum=0.5,
                nonconvex=solph.NonConvex(),
                custom_properties={"keyword1": "group 1"},
            )
        },
    )
    s1 = solph.components.Sink(
        label="s1",
        inputs={
            b1: solph.Flow(
                variable_costs=[-0.2, 0.2],
                nominal_capacity=2,
                minimum=0.5,
                nonconvex=solph.NonConvex(),
                custom_properties={"keyword1": "also group 1"},
            )
        },
    )
    s2 = solph.components.Sink(
        label="s2",
        inputs={
            b1: solph.Flow(
                variable_costs=[-0.1, 0.1],
                nominal_capacity=3,
                minimum=0.5,
                nonconvex=solph.NonConvex(),
                custom_properties={"keyword1": "still group 1"},
            )
        },
    )
    s3 = solph.components.Sink(
        label="s3",
        inputs={
            b1: solph.Flow(
                variable_costs=[-0.1, 0.2],
                nominal_capacity=3,
                minimum=0.5,
                nonconvex=solph.NonConvex(),
                custom_properties={"keyword2": "not in group 1"},
            )
        },
    )
    energysystem.add(b1, s0, s1, s2, s3)

    model = solph.Model(energysystem)

    solph.constraints.limit_active_flow_count_by_keyword(
        model,
        "keyword1",
        lower_limit=1,
        upper_limit=2,
    )

    results = model.solve()

    flow = {s: list(results["flow"][(b1, s)]) for s in [s0, s1, s2, s3]}

    assert flow[s0] == pytest.approx([4, 0])
    assert flow[s1] == pytest.approx([2, 0])
    assert flow[s2] == pytest.approx([0, 1.5])
    assert flow[s3] == pytest.approx([3, 0])


def test_flow_count_limit_investment():
    """The count limit must also cover investment nonconvex flows."""
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=False,
    )

    b1 = solph.buses.Bus(label="b1", balanced=False)
    # Three investment + nonconvex sinks. Running is profitable, so each would
    # be active without the limit; the distinct variable_costs make the two
    # cheapest run at full capacity and the most expensive one stay off.
    sinks = [
        solph.components.Sink(
            label=f"s{i}",
            inputs={
                b1: solph.Flow(
                    variable_costs=vc,
                    nominal_capacity=solph.Investment(
                        maximum=4, ep_costs=0.01
                    ),
                    minimum=0.5,
                    nonconvex=solph.NonConvex(),
                    custom_properties={"keyword1": "group 1"},
                )
            },
        )
        for i, vc in enumerate([-3, -2, -1])
    ]
    energysystem.add(b1, *sinks)

    model = solph.Model(energysystem)

    solph.constraints.limit_active_flow_count_by_keyword(
        model,
        "keyword1",
        lower_limit=0,
        upper_limit=2,
    )

    model.solve()
    results = solph.processing.results(model)

    flow = [
        list(results[(b1, s)]["sequences"]["flow"][:-1]) for s in sinks
    ]

    # Only two of the three investment nonconvex flows may be active at once.
    assert flow[0] == pytest.approx([4, 4])
    assert flow[1] == pytest.approx([4, 4])
    assert flow[2] == pytest.approx([0, 0])


def test_flow_count_limit_mixed():
    """The count limit must count plain and investment nonconvex flows
    together within a single constraint."""
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=False,
    )

    b1 = solph.buses.Bus(label="b1", balanced=False)
    # One plain and one investment nonconvex sink are cheapest and run; the
    # other plain and investment sinks are blocked by the shared count limit.
    plain_sinks = [
        solph.components.Sink(
            label=f"plain{i}",
            inputs={
                b1: solph.Flow(
                    variable_costs=vc,
                    nominal_capacity=4,
                    minimum=0.5,
                    nonconvex=solph.NonConvex(),
                    custom_properties={"keyword1": "group 1"},
                )
            },
        )
        for i, vc in enumerate([-4, -2])
    ]
    invest_sinks = [
        solph.components.Sink(
            label=f"invest{i}",
            inputs={
                b1: solph.Flow(
                    variable_costs=vc,
                    nominal_capacity=solph.Investment(
                        maximum=4, ep_costs=0.01
                    ),
                    minimum=0.5,
                    nonconvex=solph.NonConvex(),
                    custom_properties={"keyword1": "group 1"},
                )
            },
        )
        for i, vc in enumerate([-3, -1])
    ]
    sinks = plain_sinks + invest_sinks
    energysystem.add(b1, *sinks)

    model = solph.Model(energysystem)

    solph.constraints.limit_active_flow_count_by_keyword(
        model,
        "keyword1",
        lower_limit=0,
        upper_limit=2,
    )

    model.solve()
    results = solph.processing.results(model)

    flow = [
        list(results[(b1, s)]["sequences"]["flow"][:-1]) for s in sinks
    ]

    # The limit is shared across both blocks: the cheapest plain sink and the
    # cheapest investment sink run, the two more expensive ones are blocked.
    assert flow[0] == pytest.approx([4, 4])  # plain, vc=-4
    assert flow[1] == pytest.approx([0, 0])  # plain, vc=-2
    assert flow[2] == pytest.approx([4, 4])  # invest, vc=-3
    assert flow[3] == pytest.approx([0, 0])  # invest, vc=-1
