"""
General description
-------------------
The gradient constraint can restrict a component to change the output within
one time step. In this example a storage will buffer this restriction, so the
more flexible the power plant can be run the less the storage will be used.

Change the GRADIENT variable in the example to see the effect on the usage of
the storage.

Code
----
Download source code: :download:`gradient_example.py </../examples/gradient_example/gradient_example.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/gradient_example/gradient_example.py
        :language: python
        :lines: 35-211

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""

import matplotlib.pyplot as plt
import pandas as pd

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import flows
from oemof.solph import processing


def main(optimize=True):
    # The gradient for the output of the natural gas power plant.
    # Change the gradient between 0.1 and 0.0001 and check the results. The
    # more flexible the power plant can be run the less the storage will be
    # used.
    gradient = 0.01

    date_time_index = pd.date_range("1/1/2012", periods=48, freq="h")
    print(date_time_index)
    energysystem = EnergySystem(
        timeindex=date_time_index, infer_last_interval=True
    )

    demand = [
        209643,
        207497,
        200108,
        191892,
        185717,
        180672,
        172683,
        170048,
        171132,
        179532,
        189155,
        201026,
        208466,
        207718,
        205443,
        206255,
        217240,
        232798,
        237321,
        232387,
        224306,
        219280,
        223701,
        213926,
        201834,
        192215,
        187152,
        184355,
        184438,
        182786,
        180105,
        191509,
        207104,
        222501,
        231127,
        238410,
        241184,
        237413,
        234469,
        235193,
        242730,
        264196,
        265950,
        260283,
        245578,
        238849,
        241553,
        231372,
    ]

    # create natural gas bus
    bgas = buses.Bus(label="natural_gas")

    # create electricity bus
    bel = buses.Bus(label="electricity")

    # adding the buses to the energy system
    energysystem.add(bgas, bel)

    # create excess component for the electricity bus to allow overproduction
    energysystem.add(cmp.Sink(label="excess_bel", inputs={bel: flows.Flow()}))

    # create source object representing the gas commodity (annual limit)
    energysystem.add(
        cmp.Source(
            label="rgas",
            outputs={bgas: flows.Flow(variable_costs=5)},
        )
    )

    # create simple sink object representing the electrical demand
    energysystem.add(
        cmp.Sink(
            label="demand",
            inputs={bel: flows.Flow(fix=demand, nominal_capacity=1)},
        )
    )

    # create simple Converter object representing a gas power plant
    energysystem.add(
        cmp.Converter(
            label="pp_gas",
            inputs={bgas: flows.Flow()},
            outputs={
                bel: flows.Flow(
                    nominal_capacity=10e5,
                    negative_gradient_limit=gradient,
                    positive_gradient_limit=gradient,
                )
            },
            conversion_factors={bel: 0.58},
        )
    )

    # create storage object representing a battery
    storage = cmp.GenericStorage(
        nominal_capacity=999999999,
        label="storage",
        inputs={bel: flows.Flow()},
        outputs={bel: flows.Flow()},
        loss_rate=0.0,
        initial_storage_level=None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )

    energysystem.add(storage)

    if optimize is False:
        return energysystem

    # initialise the operational model
    model = Model(energysystem)

    # solve
    model.solve(solver="cbc")

    # processing the results
    results = processing.results(model)

    # *** Create a table with all sequences and store it into a file (csv/xlsx)
    flows_to_bus = pd.DataFrame(
        {
            str(k[0].label): v["sequences"]["flow"]
            for k, v in results.items()
            if k[1] is not None and k[1] == bel
        }
    )
    flows_from_bus = pd.DataFrame(
        {
            str(k[1].label): v["sequences"]["flow"]
            for k, v in results.items()
            if k[1] is not None and k[0] == bel
        }
    )

    storage = pd.DataFrame(
        {
            str(k[0].label): v["sequences"]["storage_content"]
            for k, v in results.items()
            if k[1] is None and k[0] == storage
        }
    )

    my_flows = pd.concat(
        [flows_to_bus, flows_from_bus, storage],
        keys=["to_bus", "from_bus", "content", "duals"],
        axis=1,
    )

    my_flows.plot()
    plt.show()


if __name__ == "__main__":
    main()
