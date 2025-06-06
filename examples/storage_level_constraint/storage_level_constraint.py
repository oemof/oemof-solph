# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that shows the `storage_level_constraint`.

Code
----
Download source code: :download:`storage_level_constraint.py </../examples/storage_level_constraint/storage_level_constraint.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/storage_level_constraint/storage_level_constraint.py
        :language: python
        :lines: 33-

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x) and matplotlib, install by:

.. code:: bash

    pip install oemof.solph[examples] matplotlib


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""


import matplotlib.pyplot as plt
import pandas as pd

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph.components import GenericStorage
from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.constraints import storage_level_constraint
from oemof.solph.processing import results


def storage_level_constraint_example():
    es = EnergySystem(
        timeindex=pd.date_range("2022-01-01", freq="1H", periods=24),
        infer_last_interval=True,
    )

    multiplexer = Bus(
        label="multiplexer",
    )

    storage = GenericStorage(
        label="storage",
        nominal_capacity=3,
        initial_storage_level=1,
        balanced=True,
        loss_rate=0.05,
        inputs={multiplexer: Flow()},
        outputs={multiplexer: Flow()},
    )

    es.add(multiplexer, storage)

    in_0 = Source(
        label="in_0",
        outputs={multiplexer: Flow(nominal_capacity=0.5, variable_costs=0.15)},
    )
    es.add(in_0)

    in_1 = Source(
        label="in_1", outputs={multiplexer: Flow(nominal_capacity=0.1)}
    )
    es.add(in_1)

    out_0 = Sink(
        label="out_0",
        inputs={multiplexer: Flow(nominal_capacity=0.25, variable_costs=-0.1)},
    )
    es.add(out_0)

    out_1 = Sink(
        label="out_1",
        inputs={multiplexer: Flow(nominal_capacity=0.15, variable_costs=-0.1)},
    )
    es.add(out_1)

    model = Model(es)

    storage_level_constraint(
        model=model,
        name="multiplexer",
        storage_component=storage,
        multiplexer_bus=multiplexer,
        input_levels={in_1: 1 / 3},  # in_0 is always active
        output_levels={out_0: 1 / 6, out_1: 1 / 2},
    )
    model.solve()

    my_results = results(model)

    df = pd.DataFrame(my_results[(storage, None)]["sequences"])
    df["in1_status"] = my_results[(in_1, None)]["sequences"]
    df["out1_status"] = my_results[(out_1, None)]["sequences"]
    df["out0_status"] = my_results[(out_0, None)]["sequences"]

    df["in1"] = my_results[(in_1, multiplexer)]["sequences"]
    df["in0"] = my_results[(in_0, multiplexer)]["sequences"]
    df["out0"] = my_results[(multiplexer, out_0)]["sequences"]
    df["out1"] = my_results[(multiplexer, out_1)]["sequences"]

    plt.step(df.index, df["in0"], where="post", label="inflow (<= 1)")
    plt.step(df.index, df["in1"], where="post", label="inflow (< 1/3)")
    plt.step(df.index, df["out0"], where="post", label="outflow (> 1/6)")
    plt.step(df.index, df["out1"], where="post", label="outflow (> 1/2)")

    plt.grid()
    plt.legend()
    plt.ylabel("Flow Power (arb. units)")
    plt.ylim(0, 0.5)

    plt.twinx()

    plt.plot(df.index, df["storage_content"], "k--", label="storage content")
    plt.ylim(0, 3)
    plt.legend(loc="center right")
    plt.ylabel("Stored Energy (arb. units)")

    print(df)

    plt.show()


if __name__ == "__main__":
    storage_level_constraint_example()
