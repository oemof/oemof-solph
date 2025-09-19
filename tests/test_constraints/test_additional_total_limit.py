# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Maximilian Hillen

SPDX-License-Identifier: MIT
"""

import pandas as pd
import pytest

from oemof import solph


def test_additional_total_limit():
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=True,
    )

    a = solph.buses.Bus(label="a", balanced=False)
    b = solph.buses.Bus(label="b", balanced=True)

    # Converter a
    conv_linear = 4
    conv_offset = 5
    conv_flow = 1
    converter = solph.components.Converter(
        label="trafo_a",
        inputs={a: solph.Flow()},
        outputs={
            b: solph.Flow(
                nominal_capacity=solph.Investment(
                    ep_costs=1,
                    offset=1,
                    custom_attributes={
                        "emission": {
                            "linear": conv_linear,
                            "offset": conv_offset,
                        }
                    },
                    nonconvex=True,
                    maximum=5,
                ),
                custom_attributes={"emission": conv_flow},
            )
        },
        conversion_factors={a: 1},
    )
    energysystem.add(converter)
    s = solph.components.Sink(
        label="s",
        inputs={b: solph.Flow(nominal_capacity=1, fix=[1, 1, 1])},
    )

    energysystem.add(converter, a, b, s)

    model = solph.Model(energysystem)

    model = solph.constraints.additional_total_limit(
        model, "emission", limit=100
    )

    model.solve(solver="gurobi")

    results = solph.processing.results(model)

    emission_used = model.total_limit_emission()
    print(emission_used)
    assert (1 * 3 + 4 + 5) == emission_used
