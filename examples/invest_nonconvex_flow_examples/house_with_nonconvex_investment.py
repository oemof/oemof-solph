# -*- coding: utf-8 -*-

"""
General description
-------------------
This example illustrates a possible combination of solph.Investment and
solph.NonConvex. Note that both options are added to the same
component of the energy system.

There are the following components:

- demand_heat: heat demand (high in winter, low in summer)
- fireplace: wood firing, has a minimum heat and will burn for a minimum time if lit.
- boiler: gas firing, more flexible but still with minimal load and also with higher cost than wood firing

Code
----
Download source code: :download:`house_with_nonconvex_investment.py </../examples/invest_nonconvex_flow_examples/house_with_nonconvex_investment.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/invest_nonconvex_flow_examples/house_with_nonconvex_investment.py
        :language: python
        :lines: 37-

Installation requirements
-------------------------
This example requires the version v0.5.x of oemof.solph. Install by:

.. code:: bash

    pip install 'oemof.solph>=0.5,<0.6'

"""

__copyright__ = "oemof developer group"
__license__ = "MIT"

import numpy as np
import pandas as pd
from oemof.tools import economics

from oemof import solph

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def main(optimize=True):
    ##########################################################################
    # Initialize the energy system and calculate necessary parameters
    ##########################################################################

    periods = 365
    time = pd.date_range("1/1/2018", periods=periods, freq="D")

    es = solph.EnergySystem(timeindex=time)

    b_heat = solph.buses.Bus(label="b_heat")

    es.add(b_heat)

    def heat_demand(d):
        """basic model for heat demand, solely based on the day of the year"""
        return 0.6 + 0.4 * np.cos(2 * np.pi * d / 356)

    demand_heat = solph.components.Sink(
        label="demand_heat",
        inputs={
            b_heat: solph.flows.Flow(
                fix=[heat_demand(day) for day in range(0, periods)],
                nominal_capacity=10,
            )
        },
    )

    # For one year, the equivalent periodical costs (epc) of an
    # investment are equal to the annuity.
    epc = economics.annuity(5000, 20, 0.05)

    fireplace = solph.components.Source(
        label="fireplace",
        outputs={
            b_heat: solph.flows.Flow(
                max=1.0,
                min=0.9,
                variable_costs=0.1,
                nonconvex=solph.NonConvex(
                    minimum_uptime=5,
                    initial_status=1,
                ),
                nominal_capacity=solph.Investment(
                    ep_costs=epc,
                    minimum=1.0,
                    maximum=10.0,
                ),
            )
        },
    )

    boiler = solph.components.Source(
        label="boiler",
        outputs={
            b_heat: solph.flows.Flow(
                nominal_capacity=10, min=0.3, variable_costs=0.2
            )
        },
    )

    excess_heat = solph.components.Sink(
        label="excess_heat",
        inputs={b_heat: solph.flows.Flow(nominal_capacity=10)},
    )

    es.add(demand_heat, fireplace, boiler, excess_heat)

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

    invest = solph.views.node(results, "b_heat")["scalars"][
        (("fireplace", "b_heat"), "invest")
    ]

    print("Invested in {} solar fireplace power.".format(invest))

    # plot data
    if plt is not None:
        # plot heat bus
        data = solph.views.node(results, "b_heat")["sequences"]
        exclude = ["excess_heat", "status"]
        columns = [
            c
            for c in data.columns
            if not any(s in c[0] or s in c[1] for s in exclude)
        ]
        data = data[columns]
        ax = data.plot(kind="line", drawstyle="steps-post", grid=True, rot=0)
        ax.set_xlabel("Date")
        ax.set_ylabel("Heat (arb. units)")
        plt.show()


if __name__ == "__main__":
    main()
