# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import pandas as pd

from oemof import solph


def _run_flow_model(flow):
    date_time_index = pd.date_range("1/1/2012", periods=10, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=True,
    )
    bus = solph.buses.Bus(label="bus", balanced=False)
    energysystem.add(bus)

    bus.inputs[bus] = flow

    model = solph.Model(energysystem)
    model.solve()

    return solph.processing.results(model)[(bus, bus)]["sequences"]
