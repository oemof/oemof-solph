# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that shows the parameter `balanced` of `GenericStorage`.

Code
----
Download source code: :download:`storage.py </../examples/storage_balanced_unbalanced/storage.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/storage_balanced_unbalanced/storage.py
        :language: python
        :lines: 32-

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""

import pandas as pd
from matplotlib import pyplot as plt

from oemof import solph

DATA = [
    {
        "name": "unbalanced (20% filled)",
        "initial_storage_level": 0.2,
        "balanced": False,
    },
    {
        "name": "unbalanced (None)",
        "initial_storage_level": None,
        "balanced": False,
    },
    {
        "name": "balanced (20% filled)",
        "initial_storage_level": 0.2,
        "balanced": True,
    },
    {
        "name": "balanced (None)",
        "initial_storage_level": None,
        "balanced": True,
    },
]

PARAMETER = {"el_price": 10, "ex_price": 5, "nominal_storage_capacity": 7}


def main(optimize=True):
    timeseries = pd.DataFrame(
        {"demand_el": [7, 6, 6, 7], "pv_el": [3, 5, 3, 12]}
    )

    # create an energy system
    idx = pd.date_range("1/1/2017", periods=len(timeseries), freq="h")
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=True)

    for data_set in DATA:
        name = data_set["name"]

        # power bus
        bel = solph.Bus(label="bel_{0}".format(name))
        es.add(bel)

        es.add(
            solph.components.Source(
                label="source_el_{0}".format(name),
                outputs={
                    bel: solph.Flow(variable_costs=PARAMETER["el_price"])
                },
            )
        )

        es.add(
            solph.components.Source(
                label="pv_el_{0}".format(name),
                outputs={
                    bel: solph.Flow(
                        fix=timeseries["pv_el"], nominal_capacity=1
                    )
                },
            )
        )

        es.add(
            solph.components.Sink(
                label="demand_el_{0}".format(name),
                inputs={
                    bel: solph.Flow(
                        fix=timeseries["demand_el"], nominal_capacity=1
                    )
                },
            )
        )

        es.add(
            solph.components.Sink(
                label="excess_{0}".format(name),
                inputs={bel: solph.Flow()},
            )
        )

        # Electric Storage
        es.add(
            solph.components.GenericStorage(
                label="storage_elec_{0}".format(name),
                nominal_capacity=PARAMETER["nominal_storage_capacity"],
                inputs={bel: solph.Flow()},
                outputs={bel: solph.Flow()},
                initial_storage_level=data_set["initial_storage_level"],
                balanced=data_set["balanced"],
            )
        )

    if optimize is False:
        return es

    # create an optimization problem and solve it
    om = solph.Model(es)

    # solve model
    om.solve(solver="cbc")

    # create result object
    results = solph.processing.results(om)

    components = [x for x in results if x[1] is None]

    storage_cap = pd.DataFrame()
    balance = pd.Series(dtype=float)

    storages = [x[0] for x in components if "storage" in x[0].label]

    for s in storages:
        name = s.label
        storage_cap[name] = results[s, None]["sequences"]["storage_content"]
        balance[name] = storage_cap.iloc[0][name] - storage_cap.iloc[-1][name]

    storage_cap.plot(
        drawstyle="steps-mid",
        subplots=False,
        sharey=True,
        title="Storage content",
    )
    storage_cap.plot(
        drawstyle="steps-mid",
        subplots=True,
        sharey=True,
        title="Storage content",
    )

    balance.plot(
        kind="bar",
        linewidth=1,
        edgecolor="#000000",
        rot=0,
        ax=plt.subplots()[1],
        title="Gained energy from storage",
    )
    plt.show()


if __name__ == "__main__":
    main()
