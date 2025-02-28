# -*- coding: utf-8 -*-

"""Tests for Flows with NonConvex attribute

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt e.V.
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import pytest

from oemof import solph

from . import _run_flow_model


def test_gradient_limit():
    price_pattern = [8] + 8 * [-1] + [8]

    flow = solph.flows.Flow(
        nominal_capacity=2,
        variable_costs=price_pattern,
        positive_gradient_limit=0.4,
        negative_gradient_limit=0.25,
    )
    flow_result = list(_run_flow_model(flow)["flow"][:-1])

    assert flow_result == pytest.approx(
        [0, 0.8, 1.6, 2.0, 2.0, 2.0, 1.5, 1.0, 0.5, 0]
    )


def test_full_load_time_max():
    price_pattern = [-i for i in range(11)]

    flow = solph.flows.Flow(
        nominal_capacity=2,
        variable_costs=price_pattern,
        full_load_time_max=4.5,
    )
    flow_result = list(_run_flow_model(flow)["flow"][:-1])

    assert flow_result == pytest.approx(5 * [0] + [1] + 4 * [2])


def test_full_load_time_min():
    price_pattern = [i for i in range(11)]

    flow = solph.flows.Flow(
        nominal_capacity=2,
        variable_costs=price_pattern,
        full_load_time_min=4.5,
    )
    flow_result = list(_run_flow_model(flow)["flow"][:-1])

    assert flow_result == pytest.approx(4 * [2] + [1] + 5 * [0])


# --- BEGIN: The following code can be removed for versions >= v0.7 ---
def test_nominal_capacity_warning():
    with pytest.warns(FutureWarning, match="nominal_value"):
        _ = solph.flows.Flow(nominal_value=2)


def test_nominal_capacity_error():
    with pytest.raises(AttributeError, match="nominal_capacity"):
        _ = solph.flows.Flow(nominal_value=2, nominal_capacity=1)


# --- END ---
