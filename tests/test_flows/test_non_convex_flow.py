# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import pandas as pd

from oemof import solph


def _run_model(flow):
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


def test_initial_status_off():
    # negative costs but turned off initially
    flow = solph.flows.Flow(
        nominal_value=10,
        nonconvex=solph.NonConvex(initial_status=0, minimum_downtime=5),
        variable_costs=-1,
    )
    flow_result = _run_model(flow)

    assert (flow_result["flow"][:-1] == 5 * [0] + 5 * [10]).all()


def test_initial_status_on():
    # positive costs but turned on initially
    flow = solph.flows.Flow(
        nominal_value=10,
        min=0.5,
        nonconvex=solph.NonConvex(initial_status=1, minimum_uptime=3),
        variable_costs=1,
    )
    flow_result = _run_model(flow)

    assert (flow_result["flow"][:-1] == 3 * [5] + 7 * [0]).all()


def test_startup_costs_start_off():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # startup costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_value=10,
        min=0.1,
        nonconvex=solph.NonConvex(startup_costs=5, initial_status=0),
        variable_costs=price_pattern,
    )
    flow_result = _run_model(flow)

    assert (flow_result["flow"][:-1] == [0, 0, 0, 10, 1, 1, 1, 10, 0, 0]).all()


def test_startup_costs_start_on():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # startup costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_value=10,
        min=0.1,
        nonconvex=solph.NonConvex(startup_costs=5, initial_status=1),
        variable_costs=price_pattern,
    )
    flow_result = _run_model(flow)

    assert (flow_result["flow"][:-1] == [1, 1, 1, 10, 1, 1, 1, 10, 0, 0]).all()


def test_shutdown_costs_start_on():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # shutdown costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_value=10,
        min=0.1,
        nonconvex=solph.NonConvex(shutdown_costs=5, initial_status=1),
        variable_costs=price_pattern,
    )
    flow_result = _run_model(flow)

    assert (flow_result["flow"][:-1] == [1, 1, 1, 10, 1, 1, 1, 10, 1, 1]).all()
