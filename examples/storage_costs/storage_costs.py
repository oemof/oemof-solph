# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that shows the parameter `storage_costs` of `GenericStorage`.


Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""

import pandas as pd
from matplotlib import pyplot as plt

from oemof import solph


def storage_costs_example():
    # create an energy system
    idx = pd.date_range("1/1/2023", periods=13, freq="H")
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=False)

    # power bus
    bel = solph.Bus(label="bel")
    es.add(bel)

    es.add(
        solph.components.Source(
            label="source_el",
            outputs={
                bel: solph.Flow(nominal_value=1, variable_costs=4),
            },
        )
    )

    es.add(
        solph.components.Sink(
            label="sink_el",
            inputs={
                bel: solph.Flow(nominal_value=1, variable_costs=1),
            },
        )
    )

    # Electric Storage
    battery = solph.components.GenericStorage(
        label="battery",
        nominal_storage_capacity=100,  # no effective limit
        storage_costs=-1,  # revenue for storing of 1/4 of the buying costs
        inputs={bel: solph.Flow()},
        outputs={bel: solph.Flow(variable_costs=2)},
        initial_storage_level=0,
        balanced=False,
    )
    es.add(battery)

    # create an optimization problem and solve it
    model = solph.Model(es)

    # solve model
    model.solve(solver="cbc")

    # create result object
    results = solph.processing.results(model)

    plt.plot(results[(battery, None)]["sequences"], "r--", label="content")
    plt.step(
        results[(bel, battery)]["sequences"],
        "b-",
        label="inflow",
        where="post",
    )
    plt.legend()
    plt.grid()

    plt.show()


if __name__ == "__main__":
    storage_costs_example()
