# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that shows how to add an emission constraint in a model.

Code
----
Download source code: :download:`emission_constraint.py </../examples/emission_constraint/emission_constraint.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/emission_constraint/emission_constraint.py
        :language: python
        :lines: 32-129

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

from oemof import solph
from oemof.solph import constraints


def main(optimize=True):
    # create energy system
    energysystem = solph.EnergySystem(
        timeindex=pd.date_range("1/1/2012", periods=3, freq="h")
    )

    # create gas bus
    bgas = solph.Bus(label="gas")

    # create electricity bus
    bel = solph.Bus(label="electricity")

    # adding the buses to the energy system
    energysystem.add(bel, bgas)

    # create fixed source object representing biomass plants
    energysystem.add(
        solph.components.Source(
            label="biomass",
            outputs={
                bel: solph.Flow(
                    nominal_capacity=100,
                    variable_costs=10,
                    fix=[0.1, 0.2, 0.3],
                    custom_attributes={"emission_factor": 0.01},
                )
            },
        )
    )

    # create source object representing the gas commodity
    energysystem.add(
        solph.components.Source(
            label="gas-source",
            outputs={
                bgas: solph.Flow(
                    variable_costs=10,
                    custom_attributes={"emission_factor": 0.2},
                )
            },
        )
    )

    energysystem.add(
        solph.components.Sink(
            label="demand",
            inputs={
                bel: solph.Flow(
                    nominal_capacity=200,
                    variable_costs=10,
                    fix=[0.1, 0.2, 0.3],
                )
            },
        )
    )

    # create simple converter object representing a gas power plant
    energysystem.add(
        solph.components.Converter(
            label="pp_gas",
            inputs={bgas: solph.Flow()},
            outputs={bel: solph.Flow(nominal_capacity=200)},
            conversion_factors={bel: 0.58},
        )
    )

    if optimize is False:
        return energysystem

    # initialise the operational model
    model = solph.Model(energysystem)

    # add the emission constraint
    constraints.emission_limit(model, limit=100)

    # print out the emission constraint
    model.integral_limit_emission_factor_upper_limit.pprint()
    model.integral_limit_emission_factor.pprint()

    # solve the model
    model.solve()

    # print out the amount of emissions from the emission constraint
    print(model.integral_limit_emission_factor())

    results = solph.processing.results(model)

    data = solph.views.node(results, "electricity")["sequences"]
    ax = data.plot(kind="line", grid=True)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("P (MW)")
    plt.show()


if __name__ == "__main__":
    main()
