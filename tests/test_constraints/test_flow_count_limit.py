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
        label="s1",
        inputs={
            b1: solph.Flow(
                variable_costs=[-0.5, 0.5],
                nominal_capacity=4,
                min=0.5,
                nonconvex=solph.NonConvex(),
                custom_attributes={"keyword1": "group 1"},
            )
        },
    )
    s1 = solph.components.Sink(
        label="s2",
        inputs={
            b1: solph.Flow(
                variable_costs=[-0.2, 0.2],
                nominal_capacity=2,
                min=0.5,
                nonconvex=solph.NonConvex(),
                custom_attributes={"keyword1": "also group 1"},
            )
        },
    )
    s2 = solph.components.Sink(
        label="s3",
        inputs={
            b1: solph.Flow(
                variable_costs=[-0.1, 0.1],
                nominal_capacity=3,
                min=0.5,
                nonconvex=solph.NonConvex(),
                custom_attributes={"keyword1": "still group 1"},
            )
        },
    )
    s3 = solph.components.Sink(
        label="s4",
        inputs={
            b1: solph.Flow(
                variable_costs=[-0.1, 0.2],
                nominal_capacity=3,
                min=0.5,
                nonconvex=solph.NonConvex(),
                custom_attributes={"keyword2": "not in group 1"},
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

    model.solve()

    results = solph.processing.results(model)

    flow = [
        list(results[(b1, s)]["sequences"]["flow"][:-1])
        for s in [s0, s1, s2, s3]
    ]

    assert flow[0] == pytest.approx([4, 0])
    assert flow[1] == pytest.approx([2, 0])
    assert flow[2] == pytest.approx([0, 1.5])
    assert flow[3] == pytest.approx([3, 0])
