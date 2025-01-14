# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

from oemof import solph

from . import _run_flow_model


def test_initial_status_off():
    # negative costs but turned off initially
    flow = solph.flows.Flow(
        nominal_capacity=10,
        nonconvex=solph.NonConvex(initial_status=0, minimum_downtime=5),
        variable_costs=-1,
    )
    flow_result = _run_flow_model(flow)

    assert (flow_result["flow"][:-1] == 5 * [0] + 5 * [10]).all()


def test_maximum_shutdowns():
    flow = solph.flows.Flow(
        nominal_capacity=10,
        min=0.5,
        nonconvex=solph.NonConvex(maximum_shutdowns=1),
        variable_costs=[1, -2, 1, 1, 1, -5, 1, 1, 1, -2],
    )
    flow_result = _run_flow_model(flow)

    assert list(flow_result["status"][:-1]) == [0, 1, 1, 1, 1, 1, 0, 0, 0, 1]


def test_maximum_startups():
    flow = solph.flows.Flow(
        nominal_capacity=10,
        min=0.5,
        nonconvex=solph.NonConvex(maximum_startups=1),
        variable_costs=[1, -4, 1, 1, 1, -5, 1, 1, 5, -3],
    )
    flow_result = _run_flow_model(flow)

    assert list(flow_result["status"][:-1]) == [0, 1, 1, 1, 1, 1, 0, 0, 0, 0]


def test_initial_status_on():
    # positive costs but turned on initially
    flow = solph.flows.Flow(
        nominal_capacity=10,
        min=0.5,
        nonconvex=solph.NonConvex(initial_status=1, minimum_uptime=3),
        variable_costs=1,
    )
    flow_result = _run_flow_model(flow)

    assert (flow_result["flow"][:-1] == 3 * [5] + 7 * [0]).all()


def test_activity_costs():
    # activity costs higher then revenue for first time steps
    flow = solph.flows.Flow(
        nominal_capacity=10,
        min=0.1,
        max=[0.1] + [i * 0.1 for i in range(1, 10)],
        nonconvex=solph.NonConvex(activity_costs=9 * [1] + [10]),
        variable_costs=-0.45,
    )
    flow_result = _run_flow_model(flow)["flow"][:-1]

    assert (flow_result == [0, 0, 0, 3, 4, 5, 6, 7, 8, 0]).all()


def test_inactivity_costs():
    # inactivity costs lower then running costs for middle time steps
    flow = solph.flows.Flow(
        nominal_capacity=10,
        min=[i * 0.1 for i in range(10)],
        nonconvex=solph.NonConvex(inactivity_costs=9 * [1] + [10]),
        variable_costs=0.45,
    )
    flow_result = _run_flow_model(flow)["flow"][:-1]

    assert (flow_result == [0, 1, 2, 0, 0, 0, 0, 0, 0, 9]).all()


def test_startup_costs_start_off():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # startup costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_capacity=10,
        min=0.1,
        nonconvex=solph.NonConvex(startup_costs=5, initial_status=0),
        variable_costs=price_pattern,
    )
    flow_result = _run_flow_model(flow)

    assert (flow_result["flow"][:-1] == [0, 0, 0, 10, 1, 1, 1, 10, 0, 0]).all()


def test_startup_costs_start_on():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # startup costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_capacity=10,
        min=0.1,
        nonconvex=solph.NonConvex(startup_costs=5, initial_status=1),
        variable_costs=price_pattern,
    )
    flow_result = _run_flow_model(flow)

    assert (flow_result["flow"][:-1] == [1, 1, 1, 10, 1, 1, 1, 10, 0, 0]).all()


def test_shutdown_costs_start_on():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # shutdown costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_capacity=10,
        min=0.1,
        nonconvex=solph.NonConvex(shutdown_costs=5, initial_status=1),
        variable_costs=price_pattern,
    )
    flow_result = _run_flow_model(flow)

    assert (flow_result["flow"][:-1] == [1, 1, 1, 10, 1, 1, 1, 10, 1, 1]).all()
