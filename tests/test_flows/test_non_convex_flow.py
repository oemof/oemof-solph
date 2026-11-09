# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Dylan Pulver
SPDX-FileCopyrightText: Syed Inayatullah

SPDX-License-Identifier: MIT
"""

import pytest

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

    assert flow_result == 5 * [0] + 5 * [10]


def test_maximum_shutdowns():
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.5,
        nonconvex=solph.NonConvex(maximum_shutdowns=1),
        variable_costs=[1, -2, 1, 1, 1, -5, 1, 1, 1, -2],
    )
    flow_result = [round(f, 10) for f in _run_flow_model(flow)]

    assert flow_result == [0.0, 10.0, 5.0, 5.0, 5.0, 10.0, 0.0, 0.0, 0.0, 10.0]


def test_maximum_startups():
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.5,
        nonconvex=solph.NonConvex(maximum_startups=1),
        variable_costs=[1, -4, 1, 1, 1, -5, 1, 1, 5, -3],
    )
    flow_result = [round(f, 10) for f in _run_flow_model(flow)]

    assert flow_result == [0, 10, 5, 5, 5, 10, 0, 0, 0, 0]


def test_initial_status_on():
    # positive costs but turned on initially
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.5,
        nonconvex=solph.NonConvex(initial_status=1, minimum_uptime=3),
        variable_costs=1,
    )
    flow_result = [round(f, 10) for f in _run_flow_model(flow)]

    assert flow_result == 3 * [5] + 7 * [0]


def test_activity_costs():
    # activity costs higher then revenue for first time steps
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.1,
        maximum=[0.1] + [i * 0.1 for i in range(1, 10)],
        nonconvex=solph.NonConvex(activity_costs=9 * [1] + [10]),
        variable_costs=-0.45,
    )
    flow_result = [round(f, 10) for f in _run_flow_model(flow)]

    assert flow_result == [0, 0, 0, 3, 4, 5, 6, 7, 8, 0]


def test_inactivity_costs():
    # inactivity costs lower then running costs for middle time steps
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=[i * 0.1 for i in range(10)],
        nonconvex=solph.NonConvex(inactivity_costs=9 * [1] + [10]),
        variable_costs=0.45,
    )
    flow_result = _run_flow_model(flow)

    assert flow_result == [0, 1, 2, 0, 0, 0, 0, 0, 0, 9]


def test_startup_costs_start_off():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # startup costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.1,
        nonconvex=solph.NonConvex(startup_costs=5, initial_status=0),
        variable_costs=price_pattern,
    )
    flow_result = _run_flow_model(flow)

    assert flow_result == [0, 0, 0, 10, 1, 1, 1, 10, 0, 0]


def test_startup_costs_start_on():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # startup costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.1,
        nonconvex=solph.NonConvex(startup_costs=5, initial_status=1),
        variable_costs=price_pattern,
    )
    flow_result = _run_flow_model(flow)

    assert flow_result == [1, 1, 1, 10, 1, 1, 1, 10, 0, 0]


def test_shutdown_costs_start_on():
    price_pattern = [1, 1, 1, -4, 1, 1, 1, -4, 1, 1]

    # shutdown costs higher then effect of shutting down
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.1,
        nonconvex=solph.NonConvex(shutdown_costs=5, initial_status=1),
        variable_costs=price_pattern,
    )
    flow_result = _run_flow_model(flow)

    assert flow_result == [1, 1, 1, 10, 1, 1, 1, 10, 1, 1]


def test_positive_gradient_limit_startup_to_minimum():
    # The gradient limit (1 per step) is below the minimum load (5).
    # A start-up still reaches the minimum load, then the flow ramps up.
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.5,
        nonconvex=solph.NonConvex(positive_gradient_limit=0.1),
        variable_costs=[4] + 9 * [-1],
    )
    flow_result = _run_flow_model(flow)

    assert flow_result == pytest.approx([0, 5, 6, 7, 8, 9, 10, 10, 10, 10])


def test_positive_gradient_limit_without_minimum():
    flow = solph.flows.Flow(
        nominal_capacity=10,
        nonconvex=solph.NonConvex(positive_gradient_limit=0.3),
        variable_costs=[4] + 9 * [-1],
    )
    flow_result = _run_flow_model(flow)

    assert flow_result == pytest.approx([0, 3, 6, 9, 10, 10, 10, 10, 10, 10])


def test_negative_gradient_limit_shutdown_from_minimum():
    # The flow ramps down by 2.5 per step and shuts down from the
    # minimum load (5).
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.5,
        nonconvex=solph.NonConvex(negative_gradient_limit=0.25),
        variable_costs=5 * [-1] + 5 * [3],
    )
    flow_result = _run_flow_model(flow)

    assert flow_result == pytest.approx([10, 10, 10, 7.5, 5, 0, 0, 0, 0, 0])


def test_positive_gradient_limit_changing_capacity():
    # The nominal capacity doubles at the second investment time (step 5).
    # The gradient limit refers to the capacity of the current step.
    flow = solph.flows.Flow(
        nominal_capacity=[10, 20],
        minimum=0.5,
        nonconvex=solph.NonConvex(positive_gradient_limit=0.1),
        variable_costs=[4] + 9 * [-1],
    )
    flow_result = _run_flow_model(flow, multi_period=True)

    assert flow_result == pytest.approx([0, 5, 6, 7, 8, 10, 12, 14, 16, 18])


def test_positive_gradient_limit_invest_non_convex():
    flow = solph.flows.Flow(
        nominal_capacity=solph.Investment(maximum=10, ep_costs=0.1),
        minimum=0.5,
        nonconvex=solph.NonConvex(positive_gradient_limit=0.1),
        variable_costs=[4] + 9 * [-1],
    )
    flow_result = _run_flow_model(flow)

    assert flow_result == pytest.approx([0, 5, 6, 7, 8, 9, 10, 10, 10, 10])


def test_minimum_uptime_near_horizon_end():
    # Running costs 5 per step before step 8 and earns 3 per step in the
    # last two steps. A start-up in step 8 pays off only if the flow may
    # run until the end of the horizon, which is shorter than the
    # minimum uptime.
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.5,
        nonconvex=solph.NonConvex(minimum_uptime=4),
        variable_costs=8 * [1] + 2 * [-0.3],
    )
    flow_result = [round(f, 10) for f in _run_flow_model(flow)]

    assert flow_result == 8 * [0] + 2 * [10]


def test_minimum_uptime_still_enforced():
    # A start-up for the single paid step 4 would need three more steps
    # at the minimum load, which costs more (15) than the step earns (10).
    flow = solph.flows.Flow(
        nominal_capacity=10,
        minimum=0.5,
        nonconvex=solph.NonConvex(minimum_uptime=4),
        variable_costs=4 * [1] + [-1] + 5 * [1],
    )
    flow_result = [round(f, 10) for f in _run_flow_model(flow)]

    assert flow_result == 10 * [0]
