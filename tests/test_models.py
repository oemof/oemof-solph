# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: MIT
"""

import warnings

import pandas as pd
import pytest

from oemof import solph


def test_optimal_solution():
    es = solph.EnergySystem(timeincrement=[1])
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={bel: solph.flows.Flow(nominal_value=5, fix=[1])},
        )
    )
    es.add(
        solph.components.Source(
            label="source",
            outputs={bel: solph.flows.Flow(variable_costs=5)},
        )
    )
    m = solph.Model(es)
    m.solve("cbc")
    m.results()
    solph.processing.meta_results(m)


def test_infeasible_model():
    # FutureWarning is i.e. emitted by network Entity registry
    warnings.simplefilter(action="ignore", category=FutureWarning)

    with pytest.raises(ValueError, match=""):
        with warnings.catch_warnings(record=True) as w:
            es = solph.EnergySystem(timeincrement=[1])
            bel = solph.buses.Bus(label="bus")
            es.add(bel)
            es.add(
                solph.components.Sink(
                    inputs={bel: solph.flows.Flow(nominal_value=5, fix=[1])}
                )
            )
            es.add(
                solph.components.Source(
                    outputs={
                        bel: solph.flows.Flow(
                            nominal_value=4, variable_costs=5
                        )
                    }
                )
            )
            m = solph.Model(es)
            m.solve(solver="cbc")
            assert "Optimization ended with status" in str(w[0].message)
            solph.processing.meta_results(m)


def test_multi_period_default_discount_rate():
    """Test error being thrown for default multi-period discount rate"""
    warnings.filterwarnings("ignore", category=FutureWarning)
    timeindex = pd.date_range(start="2017-01-01", periods=100, freq="D")
    es = solph.EnergySystem(
        timeindex=timeindex,
        timeincrement=[1] * len(timeindex),
        periods=[timeindex],
        infer_last_interval=False,
    )
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=5, fix=[1] * len(timeindex)
                )
            },
        )
    )
    es.add(
        solph.components.Source(
            label="source",
            outputs={bel: solph.flows.Flow(nominal_value=4, variable_costs=5)},
        )
    )
    msg = (
        "By default, a discount_rate of 0.02 is used for a multi-period model."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.Model(es)
        assert msg in str(w[0].message)


def test_cellular_structure_detection():
    """Test flag creation if list is passed as energysystem to model"""
    timeindex = pd.date_range(start="2020-01-01", periods=1, freq="H")
    es = solph.EnergySystem(
        label="es", timeindex=timeindex, infer_last_interval=True
    )
    ec_1 = solph.EnergySystem(
        label="ec_1", timeindex=timeindex, infer_last_interval=True
    )
    ec_2 = solph.EnergySystem(
        label="ec_2", timeindex=timeindex, infer_last_interval=True
    )
    m = solph.Model(energysystem=[es, ec_1, ec_2])
    assert m.is_cellular


def test_sub_cell_node_consideration():
    """
    Test if the nodes of sub-cells are considered for cellular
    energysystems.
    """
    timeindex = pd.date_range(start="2020-01-01", periods=1, freq="H")
    es = solph.EnergySystem(
        label="es", timeindex=timeindex, infer_last_interval=True
    )
    ec_1 = solph.EnergySystem(
        label="ec_1", timeindex=timeindex, infer_last_interval=True
    )
    bus_es = solph.buses.Bus(label="bus_es")
    bus_ec_1 = solph.buses.Bus(label="bus_ec_1")
    es.add(bus_es)
    ec_1.add(bus_ec_1)
    m = solph.Model(energysystem=[es, ec_1])
    assert bus_ec_1 in m.nodes.values()


def test_sub_cell_flow_consideration():
    """
    Test if the flows of sub-cells are considered for cellular
    energysystems.
    """
    timeindex = pd.date_range(start="2020-01-01", periods=1, freq="H")
    es = solph.EnergySystem(
        label="es", timeindex=timeindex, infer_last_interval=True
    )
    ec_1 = solph.EnergySystem(
        label="ec_1", timeindex=timeindex, infer_last_interval=True
    )
    bus_es = solph.buses.Bus(label="bus_es")
    bus_ec_1 = solph.buses.Bus(label="bus_ec_1")
    es.add(bus_es)
    ec_1.add(bus_ec_1)

    connector_ec_1 = solph.buses.Bus(
        label="connector_ec_1",
        inputs={
            bus_es: solph.flows.Flow(),
            bus_ec_1: solph.flows.Flow(),
        },
        outputs={
            bus_es: solph.flows.Flow(),
            bus_ec_1: solph.flows.Flow(),
        },
    )
    es.add(connector_ec_1)

    test_flow = [io for io in ec_1.flows().keys()][0]

    m = solph.Model(energysystem=[es, ec_1])
    assert test_flow in m.FLOWS
