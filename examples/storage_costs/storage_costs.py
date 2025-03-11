# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that shows the parameter `storage_costs` of `GenericStorage`.
A battery is used to make profit from fluctuating electricity prices.
For a battery without storage costs, it is beneficial to be empty
the end of the time horizon of the optimisation. For a battery that
assumes the average revenue, energy is kept at the end.

Code
----
Download source code: :download:`storage_costs.py </../examples/storage_costs/storage_costs.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/storage_costs/storage_costs.py
        :language: python
        :lines: 36-

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x) and matplotlib, install by:

.. code:: bash

    pip install oemof.solph[examples] matplotlib


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from oemof import solph


def main(optimize=True):
    # create an energy system
    idx = pd.date_range("1/1/2023", periods=13, freq="h")
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=False)

    # power bus
    bel = solph.Bus(label="bel")
    es.add(bel)

    es.add(
        solph.components.Source(
            label="source_el",
            outputs={bel: solph.Flow()},
        )
    )

    es.add(
        solph.components.Sink(
            label="sink_el",
            inputs={bel: solph.Flow()},
        )
    )

    electricity_price = np.array(
        [
            0.38,
            0.31,
            0.32,
            0.33,
            0.37,
            0.32,
            0.33,
            0.34,
            0.39,
            0.38,
            0.37,
            0.35,
            0.35,
        ]
    )

    # Electric Storage 1
    # Costs are designed in a way that storing energy is benificial until the
    # last four time steps but emptying it is not a good option.
    battery1 = solph.components.GenericStorage(
        label="battery 1",
        nominal_capacity=10,
        inputs={
            bel: solph.Flow(
                nominal_capacity=1,
                variable_costs=electricity_price,
            )
        },
        outputs={
            bel: solph.Flow(
                nominal_capacity=1,
                variable_costs=-electricity_price,
            )
        },
        initial_storage_level=0.5,
        balanced=False,
    )
    es.add(battery1)

    # storages that balance our fluctuating costs
    # Electric Storage 2
    battery2 = solph.components.GenericStorage(
        label="battery 2",
        nominal_capacity=10,
        inputs={
            bel: solph.Flow(
                nominal_capacity=1,
                variable_costs=electricity_price,
            )
        },
        outputs={
            bel: solph.Flow(
                nominal_capacity=1,
                variable_costs=-electricity_price,
            )
        },
        storage_costs=12 * [0] + [-np.mean(electricity_price)],
        initial_storage_level=0.5,
        balanced=False,
    )
    es.add(battery2)

    if optimize is False:
        return es

    # create an optimization problem and solve it
    model = solph.Model(es)

    # solve model
    model.solve(solver="cbc")

    # create result object
    results = solph.processing.results(model)

    plt.plot(
        results[(battery1, None)]["sequences"],
        label="content w/o storage costs",
    )
    plt.plot(
        results[(battery2, None)]["sequences"],
        label="content w/ storage revenue",
    )
    plt.legend()
    plt.grid()

    plt.show()


if __name__ == "__main__":
    storage_costs_example()
