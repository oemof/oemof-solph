# -*- coding: utf-8 -*-

"""
General description
-------------------

This example illustrates the effect of activity_costs.

There are the following components:

- demand_heat: heat demand (constant, for the sake of simplicity)
- fireplace: wood firing, burns "for free" if somebody is around
- boiler: gas firing, consumes (paid) gas

Notice that activity_costs is an attribute to NonConvex.
This is because it relies on the activity status of a component
which is only available for nonconvex flows.

Code
----
Download source code: :download:`activity_costs.py </../examples/activity_costs/activity_costs.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/activity_costs/activity_costs.py
        :language: python
        :lines: 43-118

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
import numpy as np
import pandas as pd

from oemof import solph


def main(optimize=True):
    ##########################################################################
    # Calculate parameters and initialize the energy system and
    ##########################################################################
    periods = 24
    time = pd.date_range("1/1/2018", periods=periods, freq="h")

    demand_heat = np.full(periods, 5)
    demand_heat[:4] = 0
    demand_heat[4:18] = 4

    activity_costs = np.full(periods, 5)
    activity_costs[18:] = 0

    es = solph.EnergySystem(timeindex=time)

    b_heat = solph.Bus(label="b_heat")

    es.add(b_heat)

    sink_heat = solph.components.Sink(
        label="demand",
        inputs={b_heat: solph.Flow(fix=demand_heat, nominal_capacity=1)},
    )

    fireplace = solph.components.Source(
        label="fireplace",
        outputs={
            b_heat: solph.Flow(
                nominal_capacity=3,
                variable_costs=0,
                nonconvex=solph.NonConvex(activity_costs=activity_costs),
            )
        },
    )

    boiler = solph.components.Source(
        label="boiler",
        outputs={b_heat: solph.Flow(nominal_capacity=10, variable_costs=1)},
    )

    es.add(sink_heat, fireplace, boiler)

    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    if optimize is False:
        return es
    # create an optimization problem and solve it
    om = solph.Model(es)

    # solve model
    om.solve(solver="cbc", solve_kwargs={"tee": True})

    ##########################################################################
    # Check and plot the results
    ##########################################################################

    results = solph.processing.results(om)

    # plot data
    data = solph.views.node(results, "b_heat")["sequences"]
    ax = data.plot(kind="line", drawstyle="steps-post", grid=True, rot=0)
    ax.set_xlabel("Time")
    ax.set_ylabel("Heat (arb. units)")
    plt.show()


if __name__ == "__main__":
    main()
