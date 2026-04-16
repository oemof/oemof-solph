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
            nominal_capacity=10,
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
                variable_costs=-1,
                nominal_capacity=solph.Investment(ep_costs=0.1),
            )
        },
        outputs={
            bus: solph.Flow(
                variable_costs=1,
                nominal_capacity=solph.Investment(ep_costs=0.1),
            )
        },
        nominal_capacity=10,
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
                variable_costs=-1,
                nominal_capacity=solph.Investment(ep_costs=0.1),
            )
        },
        outputs={
            bus: solph.Flow(
                variable_costs=1,
                nominal_capacity=solph.Investment(ep_costs=0.1),
            )
        },
        nominal_capacity=10,
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


def test_storage_charging():
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
        inputs={bus: solph.Flow(nominal_capacity=2, variable_costs=-2)},
        outputs={bus: solph.Flow(nominal_capacity=0.1)},
        nominal_capacity=19,
        initial_storage_level=0,
        balanced=False,
    )
    es.add(storage)

    model = solph.Model(es)
    model.solve("cbc")

    result = solph.processing.results(model)
    storage_inflow = result[(bus, storage)]["sequences"]["flow"]
    assert list(storage_inflow)[:-1] == 10 * [2]

    storage_content = list(
        result[(storage, None)]["sequences"]["storage_content"]
    )
    assert storage_content == pytest.approx([i * 1.9 for i in range(0, 11)])


def test_invest_content_uncoupled():
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
        inputs={bus: solph.Flow(nominal_capacity=2, variable_costs=-2)},
        outputs={bus: solph.Flow(nominal_capacity=0.1)},
        nominal_capacity=solph.Investment(
            ep_costs=0.1,
        ),
        initial_storage_level=0,
        balanced=False,
    )
    es.add(storage)

    model = solph.Model(es)
    model.solve("cbc")

    result = solph.processing.results(model)
    storage_inflow = result[(bus, storage)]["sequences"]["flow"]
    assert list(storage_inflow)[:-1] == 10 * [2]

    invest_capacity = result[(storage, None)]["scalars"]["invest"]
    assert invest_capacity == pytest.approx(19)

    storage_content = list(
        result[(storage, None)]["sequences"]["storage_content"]
    )
    assert storage_content == pytest.approx([i * 1.9 for i in range(0, 11)])


def test_invest_content_minimum():
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
        inputs={bus: solph.Flow(nominal_capacity=2, variable_costs=-2)},
        outputs={bus: solph.Flow(nominal_capacity=0.1, variable_costs=0.1)},
        nominal_capacity=solph.Investment(
            ep_costs=0.1,
            minimum=32,
        ),
        initial_storage_level=0,
        balanced=False,
    )
    es.add(storage)

    model = solph.Model(es)
    model.solve("cbc")

    result = solph.processing.results(model)
    storage_inflow = result[(bus, storage)]["sequences"]["flow"]
    assert list(storage_inflow)[:-1] == 10 * [2]

    invest_capacity = result[(storage, None)]["scalars"]["invest"]
    assert invest_capacity == pytest.approx(32)

    storage_content = list(
        result[(storage, None)]["sequences"]["storage_content"]
    )
    assert storage_content == pytest.approx([i * 2 for i in range(0, 11)])


def test_invest_content_minimum_nonconvex():
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
        inputs={bus: solph.Flow(nominal_capacity=2, variable_costs=0.1)},
        outputs={bus: solph.Flow(nominal_capacity=0.1, variable_costs=0.1)},
        nominal_capacity=solph.Investment(
            ep_costs=0.1,
            maximum=42,
            minimum=32,
            nonconvex=True,
        ),
        balanced=False,
    )
    es.add(storage)

    model = solph.Model(es)
    model.solve("cbc")

    result = solph.processing.results(model)
    storage_inflow = result[(bus, storage)]["sequences"]["flow"]
    assert list(storage_inflow)[:-1] == 10 * [0]

    invest_capacity = result[(storage, None)]["scalars"]["invest"]
    assert invest_capacity == pytest.approx(0)

    storage_content = list(
        result[(storage, None)]["sequences"]["storage_content"]
    )
    assert storage_content == pytest.approx(11 * [0])


def test_invest_content_maximum():
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
                nominal_capacity=2,
                variable_costs=[-2 + i * 0.01 for i in range(0, 10)],
            )
        },
        outputs={bus: solph.Flow(nominal_capacity=0.1, variable_costs=0.1)},
        nominal_capacity=solph.Investment(
            ep_costs=0.1,
            maximum=10,
        ),
        initial_storage_level=0,
        balanced=False,
    )
    es.add(storage)

    model = solph.Model(es)
    model.solve("cbc")

    result = solph.processing.results(model)

    invest_capacity = result[(storage, None)]["scalars"]["invest"]
    assert invest_capacity == pytest.approx(10)

    storage_content = list(
        result[(storage, None)]["sequences"]["storage_content"]
    )
    assert storage_content == pytest.approx(
        [min(i * 1.9, 10) for i in range(0, 11)]
    )


# --- BEGIN: The following code can be removed for versions >= v0.7 ---
def test_capacity_keyword_wrapper_warning():
    with pytest.warns(FutureWarning, match="nominal_storage_capacity"):
        bus = solph.Bus()
        _ = solph.components.GenericStorage(
            nominal_storage_capacity=5,
            inputs={bus: solph.Flow()},
            outputs={bus: solph.Flow()},
        )


def test_capacity_keyword_wrapper_error():
    with pytest.raises(AttributeError, match="nominal_storage_capacity"):
        bus = solph.Bus()
        _ = solph.components.GenericStorage(
            nominal_storage_capacity=5,
            nominal_capacity=5,
            inputs={bus: solph.Flow()},
            outputs={bus: solph.Flow()},
        )


def test_soc_dependent_charging_with_investment():
    with pytest.raises(
        NotImplementedError, match="has to be fixed not variable"
    ):
        bus = solph.Bus()
        _ = solph.components.GenericStorage(
            label="storage",
            inputs={bus: solph.Flow()},
            outputs={bus: solph.Flow()},
            nominal_capacity=solph.Investment(),
            constant_soc_until=0.4,
            fraction_saturation_charging=0.2,
        )


def test_soc_dependent_charging_without_inputs():
    with pytest.raises(
        NotImplementedError, match="adding Flows later"
    ):
        bus = solph.Bus()
        _ = solph.components.GenericStorage(
            label="storage",
            inputs={bus: "This is not a Flow"},
            outputs={bus: solph.Flow()},
            nominal_capacity=1,
            constant_soc_until=0.4,
            fraction_saturation_charging=0.2,
        )


def test_soc_dependent_charging():
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
        label="Constant",
        inputs={bus: solph.Flow(10, variable_costs=-1)},
        outputs={bus: solph.Flow(10, variable_costs=2)},
        nominal_capacity=100,
        balanced=False,
    )
    storage_new = solph.components.GenericStorage(
        label="SOC-dependent",
        inputs={bus: solph.Flow(10, variable_costs=-1)},
        outputs={bus: solph.Flow(10, variable_costs=2)},
        nominal_capacity=100,
        balanced=False,
        constant_soc_until=0.2,
        fraction_saturation_charging=0.3,
    )
    es.add(storage, storage_new)

    model = solph.Model(es)
    model.solve("cbc")
    results = solph.Results(model)
    cols = sorted([c for c in results["flow"].columns if bus == c[0]])
    assert results["flow"][cols].iloc[0].to_list() == [10.0, 10.0]
    assert results["flow"][cols].iloc[-1].round(2).to_list() == [10.0, 5.11]

    storage_content = results["storage_content"].sort_index(axis=1)
    assert storage_content.iloc[0].to_list() == [0.0, 0.0]
    assert storage_content.iloc[-1].round(2).to_list() == [100.0, 75.87]
