# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import pandas as pd
import pytest

from oemof import solph


def test_equate_flows():
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
                variable_costs=-0.5,
                max=[0.5, 1],
                nominal_capacity=4,
                custom_attributes={"keyword1": "group 1"},
            )
        },
    )
    s1 = solph.components.Sink(
        label="s2",
        inputs={
            b1: solph.Flow(
                variable_costs=0.1,
                nominal_capacity=2,
                custom_attributes={"keyword2": "group 2"},
            )
        },
    )
    s2 = solph.components.Sink(
        label="s3",
        inputs={
            b1: solph.Flow(
                variable_costs=0.2,
                nominal_capacity=3,
                custom_attributes={"keyword2": "group 2"},
            )
        },
    )
    s3 = solph.components.Sink(
        label="s4",
        inputs={
            b1: solph.Flow(
                variable_costs=0.2,
                nominal_capacity=3,
                custom_attributes={"keyword3": "no group"},
            )
        },
    )
    energysystem.add(b1, s0, s1, s2, s3)

    model = solph.Model(energysystem)

    solph.constraints.equate_flows_by_keyword(
        model, "keyword1", "keyword2", 0.75
    )

    model.solve()

    results = solph.processing.results(model)

    flow = [
        list(results[(b1, s)]["sequences"]["flow"][:-1])
        for s in [s0, s1, s2, s3]
    ]

    assert flow[0] == pytest.approx([2, 4])
    assert flow[1] == pytest.approx([1.5, 2])
    assert flow[2] == pytest.approx([0, 1])
    assert flow[3] == pytest.approx([0, 0])
