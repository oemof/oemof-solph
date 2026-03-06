# -*- coding: utf-8 -*-

"""
General description
-------------------
This script implements the method to cosider offering storage capacity
at a flexibility market that is described in https://elib.dlr.de/212741/.


SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-License-Identifier: MIT
"""

import numpy as np
from pyomo import environ as po

from oemof import solph

BATTERY_CAPACITY = 50

def create_model():
    es = solph.EnergySystem(timeindex=solph.create_time_index(2026, 1, 24))

    driving_pattern = np.array(
        6 * [0] + 2 * [1.] + 8 * [0] + 2 * [1.] + 6 * [0]
    )
    presence_pattern = np.ones(24) - driving_pattern

    b_plan = solph.Bus("electricity")
    b_flex = solph.Bus("flexibility")
    es.add(b_plan, b_flex)

    s_plan = solph.components.Source(
        "source plan",
        outputs={
            b_plan: solph.Flow(
                nominal_capacity=11,
                nonconvex=solph.NonConvex(),
                variable_costs=0.3,
                maximum=presence_pattern,
                custom_properties={"charger": True},
            ),
        },
    )

    s_flex = solph.components.Source(
        "source flex",
        outputs={
            b_flex: solph.Flow(
                nominal_capacity=11,
                nonconvex=solph.NonConvex(),
                variable_costs=-0.01,
                maximum=presence_pattern,
                custom_properties={"charger": True},
            ),
        },
    )
    es.add(s_plan, s_flex)

    storage_plan = solph.components.GenericStorage(
        "storage plan",
        nominal_capacity=BATTERY_CAPACITY,
        inputs={b_plan: solph.Flow()},
        outputs={b_plan: solph.Flow()},
    )
    storage_flex = solph.components.GenericStorage(
        "storage flex",
        nominal_capacity=BATTERY_CAPACITY,
        inputs={b_flex: solph.Flow()},
        outputs={b_flex: solph.Flow()},
    )
    es.add(storage_plan, storage_flex)

    sink_plan = solph.components.Sink(
        "sink plan",
        inputs={b_plan: solph.Flow(
            nominal_capacity=18,
            fix=driving_pattern,
        )},
    )
    sink_flex = solph.components.Sink(
        "sink flex",
        inputs={b_flex: solph.Flow()},
    )
    es.add(sink_plan, sink_flex)

    model = solph.Model(es)

    solph.constraints.limit_active_flow_count_by_keyword(
        model, "charger", upper_limit=1,
    )

    solph.constraints.shared_limit(
        model,
        model.GenericStorageBlock.storage_content,
        "limit_storage",
        [storage_plan, storage_flex],
        [1, 1],
        upper_limit=BATTERY_CAPACITY,
    )

    def _limit_flow_rule(m):
        for ts in m.TIMESTEPS:
            getattr(m, "discharge_limit").add(
                ts,
                m.flow[b_flex, sink_flex, ts] <= m.flow[b_plan, sink_plan, ts]
            )

    setattr(
        model,
        "discharge_limit",
        po.Constraint(model.TIMESTEPS, noruleinit=True),
    )
    setattr(
        model,
        "discharge_limit_build",
        po.BuildAction(rule=_limit_flow_rule),
    )

    return model

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    model = create_model()
    model.solve()

    results = solph.Results(model)

    results["flow"].plot(drawstyle="steps-post")
    results["storage_content"].plot.area()

    plt.show()
