# -*- coding: utf-8 -*-

"""
General description
-------------------
This example illustrates a possible combination of solph.Investment and
solph.NonConvex. Note that both options are added to different
components of the energy system.

There are the following components:

- demand_heat: heat demand (high in winter, low in summer)
- fireplace: wood firing, has a minimum heat and will burn for a minimum time if lit
- boiler: gas firing, more flexible but with higher (flexible) cost than wood firing
- thermal_collector: solar thermal collector, size is to be optimized in this example (high gain in summer, low in winter)
- excess_heat: allow for some heat overproduction (solution would be trivial without, as the collector size would be given by the demand in summer)

Code
----
Download source code: :download:`house_without_nonconvex_investment.py </../examples/invest_nonconvex_flow_examples/house_without_nonconvex_investment.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/invest_nonconvex_flow_examples/house_without_nonconvex_investment.py
        :language: python
        :lines: 43-

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

    def solar_thermal(d):
        """
        basic model for solar thermal yield, solely based on the day of the
        year
        """
        return 0.5 - 0.5 * np.cos(2 * np.pi * d / 356)

    demand_heat = solph.components.Sink(
        label="demand_heat",
        inputs={
            b_heat: solph.flows.Flow(
                fix=[heat_demand(day) for day in range(0, periods)],
                nominal_capacity=10,
            )
        },
    )

    fireplace = solph.components.Source(
        label="fireplace",
        outputs={
            b_heat: solph.flows.Flow(
                nominal_capacity=10,
                min=0.4,
                max=1.0,
                variable_costs=0.1,
                nonconvex=solph.NonConvex(
                    minimum_uptime=2,
                    initial_status=1,
                ),
            )
        },
    )

    boiler = solph.components.Source(
        label="boiler",
        outputs={
            b_heat: solph.flows.Flow(nominal_capacity=10, variable_costs=0.2)
        },
    )

    # For one year, the equivalent periodical costs (epc) of an
    # investment are equal to the annuity.
    epc = economics.annuity(5000, 20, 0.05)

    thermal_collector = solph.components.Source(
        label="thermal_collector",
        outputs={
            b_heat: solph.flows.Flow(
                fix=[solar_thermal(day) for day in range(0, periods)],
                nominal_capacity=solph.Investment(
                    ep_costs=epc, minimum=1.0, maximum=5.0
                ),
            )
        },
    )

    excess_heat = solph.components.Sink(
        label="excess_heat",
        inputs={b_heat: solph.flows.Flow(nominal_capacity=10)},
    )

    es.add(demand_heat, fireplace, boiler, thermal_collector, excess_heat)

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
        (("thermal_collector", "b_heat"), "invest")
    ]

    print("Invested in {} solar thermal power.".format(invest))

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
