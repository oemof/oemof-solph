# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that shows the how to implement a `GenericStorage`
that charges at reduced rates for high storage contents.

Code
----
Download source code: :download:`saturating_storage.py </../examples/flexible_modelling/saturating_storage.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/flexible_modelling/saturating_storage.py
        :language: python
        :lines: 34-140


Installation requirements
-------------------------
This example requires oemof.solph (v0.6.x), install by:

.. code:: bash

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""

import pandas as pd
from matplotlib import pyplot as plt
from pyomo import environ as po

from oemof import solph


def main(optimize=True):
    # create an energy system
    idx = pd.date_range("1/1/2023", periods=100, freq="h")
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=False)

    # power bus
    bel = solph.Bus(label="bel")
    es.add(bel)

    es.add(
        solph.components.Source(
            label="source_el",
            outputs={bel: solph.Flow(nominal_capacity=1, fix=1)},
        )
    )

    es.add(
        solph.components.Sink(
            label="sink_el",
            inputs={
                bel: solph.Flow(
                    nominal_capacity=1,
                    variable_costs=1,
                )
            },
        )
    )

    # Electric Storage

    inflow_capacity = 0.5
    full_charging_limit = 0.4
    storage_capacity = 10
    battery = solph.components.GenericStorage(
        label="battery",
        nominal_capacity=storage_capacity,
        inputs={bel: solph.Flow(nominal_capacity=inflow_capacity)},
        outputs={bel: solph.Flow(variable_costs=2)},
        initial_storage_level=0,
        balanced=False,
        loss_rate=0.0001,
    )
    es.add(battery)

    if optimize is False:
        return es

    # create an optimization problem and solve it
    model = solph.Model(es)

    def soc_limit_rule(m):
        for ts in m.TIMESTEPS:
            soc = (
                m.GenericStorageBlock.storage_content[battery, ts + 1]
                / storage_capacity
            )
            expr = (1 - soc) / (1 - full_charging_limit) >= m.flow[
                bel, battery, ts
            ] / inflow_capacity
            getattr(m, "soc_limit").add(ts, expr)

    setattr(
        model,
        "soc_limit",
        po.Constraint(
            model.TIMESTEPS,
            noruleinit=True,
        ),
    )
    setattr(
        model,
        "soc_limit_build",
        po.BuildAction(rule=soc_limit_rule),
    )

    # solve model
    model.solve(solver="cbc")

    # create result object
    results = solph.processing.results(model)

    plt.plot(
        results[(battery, None)]["sequences"]["storage_content"],
        "r--",
        label="content",
    )
    plt.step(
        20 * results[(bel, battery)]["sequences"]["flow"],
        "b-",
        label="20*inflow",
    )
    plt.legend()
    plt.grid()

    plt.figure()
    plt.plot(
        results[(battery, None)]["sequences"]["storage_content"][1:],
        results[(bel, battery)]["sequences"]["flow"][:-1],
        "b-",
    )
    plt.grid()
    plt.xlabel("Storage content")
    plt.ylabel("Charging power")

    plt.show()


if __name__ == "__main__":
    main()
