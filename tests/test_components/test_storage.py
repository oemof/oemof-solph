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
