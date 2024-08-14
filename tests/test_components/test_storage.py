# -*- coding: utf-8 -*-

import numpy as np
import pytest

from oemof import solph


def test_relative_losses():
    cases = [
        {"number": 500, "interval": 2},
        {"number": 1000, "interval": 1},
        {"number": 2000, "interval": 0.5},
    ]

    for case in cases:
        es = solph.EnergySystem(
            timeindex=solph.create_time_index(
                year=2023, number=case["number"], interval=case["interval"]
            ),
            infer_last_interval=True,
        )

        bus = solph.Bus("slack_bus", balanced=False)
        es.add(bus)

        storage = solph.components.GenericStorage(
            "storage",
            inputs={bus: solph.Flow(variable_costs=1)},
            outputs={bus: solph.Flow(variable_costs=1)},
            nominal_storage_capacity=10,
            initial_storage_level=1,
            loss_rate=0.004125876075,  # half life of one week
        )
        es.add(storage)

        model = solph.Model(es)
        model.solve("cbc")

        result = solph.processing.results(model)[(storage, None)]["sequences"][
            "storage_content"
        ]
        case["result"] = np.array(result)

    for i in range(500):
        assert (
            cases[0]["result"][i]
            == pytest.approx(cases[1]["result"][2 * i])
            == pytest.approx(cases[2]["result"][4 * i])
        )


def test_invest_power_uncoupled():
    es = solph.EnergySystem(
        timeindex=solph.create_time_index(
            year=2023,
            number=10,
        ),
        infer_last_interval=False,
    )

    bus = solph.Bus("slack_bus", balanced=False)
    es.add(bus)

    storage = solph.components.GenericStorage(
        "storage",
        inputs={
            bus: solph.Flow(
                variable_costs=-1, nominal_value=solph.Investment(ep_costs=0.1)
            )
        },
        outputs={
            bus: solph.Flow(
                variable_costs=1, nominal_value=solph.Investment(ep_costs=0.1)
            )
        },
        nominal_storage_capacity=10,
        initial_storage_level=0,
        balanced=False,
    )
    es.add(storage)

    model = solph.Model(es)
    model.solve("cbc")

    result = solph.processing.results(model)
    storage_content = result[(storage, None)]["sequences"]["storage_content"]
    assert (storage_content == np.arange(0, 10.5, 1)).all()

    invest_inflow = result[(bus, storage)]["scalars"]["invest"]
    assert invest_inflow == pytest.approx(1)

    invest_outflow = result[(storage, bus)]["scalars"]["invest"]
    assert invest_outflow == pytest.approx(0)

    print(result)


def test_invest_power_coupled():
    es = solph.EnergySystem(
        timeindex=solph.create_time_index(
            year=2023,
            number=10,
        ),
        infer_last_interval=False,
    )

    bus = solph.Bus("slack_bus", balanced=False)
    es.add(bus)

    storage = solph.components.GenericStorage(
        "storage",
        inputs={
            bus: solph.Flow(
                variable_costs=-1, nominal_value=solph.Investment(ep_costs=0.1)
            )
        },
        outputs={
            bus: solph.Flow(
                variable_costs=1, nominal_value=solph.Investment(ep_costs=0.1)
            )
        },
        nominal_storage_capacity=10,
        invest_relation_input_output=0.5,
        initial_storage_level=0,
        balanced=False,
    )
    es.add(storage)

    model = solph.Model(es)
    model.solve("cbc")

    result = solph.processing.results(model)
    storage_content = result[(storage, None)]["sequences"]["storage_content"]
    assert (storage_content == np.arange(0, 10.5, 1)).all()

    invest_inflow = result[(bus, storage)]["scalars"]["invest"]
    assert invest_inflow == pytest.approx(1)

    invest_outflow = result[(storage, bus)]["scalars"]["invest"]
    assert invest_outflow == pytest.approx(2)

    print(result)
