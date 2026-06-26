# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import pandas as pd

from oemof import solph


def _run_flow_model(flow, multi_period=False):
    date_time_index = pd.date_range("1/1/2012", periods=11, freq="h")

    if multi_period:
        investment_times = (
            date_time_index[0],
            date_time_index[5],
            date_time_index[-1],
        )
    else:
        investment_times = None
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        investment_times=investment_times,
        infer_last_interval=False,
    )
    bus = solph.buses.Bus(label="bus", balanced=False)
    energysystem.add(bus)

    bus.inputs[bus] = flow

    model = solph.Model(energysystem)
    results = model.solve()

    return list(results["flow"][(bus, bus)])
