# -*- coding: utf-8 -*-

"""
Test example for soc-dependent charging.

Licence
-------
`MIT licence <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_

"""

import logging
from oemof.tools import logger
from oemof.network.graph import create_nx_graph
from oemof import solph


def main():
    demand = [0] * (24 * 2) + [70] * (24 * 2)
    volatile = [70] * (24 * 2) + [0] * (24 * 2)
    number_timesteps = len(demand)

    logger.define_logging()
    logging.info("Initialize the energy system")
    date_time_index = solph.create_time_index(2012, number=number_timesteps)

    energysystem = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=False
    )

    logging.info("Create oemof objects")

    # create electricity bus
    bel = solph.Bus(label="electricity")

    energysystem.add(bel)

    excess = solph.components.Sink(
        label="excess_bel", inputs={bel: solph.Flow(variable_costs=4)}
    )

    volatile = solph.components.Source(
        label="volatile",
        outputs={bel: solph.Flow(fix=volatile, nominal_capacity=1)},
    )

    shortage = solph.components.Source(
        label="shortage",
        outputs={bel: solph.Flow(variable_costs=999)},
    )

    # create simple sink object representing the electrical demand
    demand = solph.components.Sink(
        label="demand",
        inputs={bel: solph.Flow(fix=demand, nominal_capacity=1)},
    )

    # create storage object representing a battery
    storage = solph.components.GenericStorage(
        label="storage",
        inputs={bel: solph.Flow(35)},
        outputs={bel: solph.Flow(40)},
        nominal_capacity=1000,
        initial_storage_level=0,
        balanced=True,
        constant_soc_until=0.4,
        fraction_saturation_charging=0.2,
    )

    energysystem.add(excess, shortage, volatile, demand, storage)
    # create_nx_graph(energysystem, filename="test.graphml")
    logging.info("Optimise the energy system")

    om = solph.Model(energysystem)

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    om.solve(solver="cbc", solve_kwargs={"tee": True})

    results = solph.Results(om)
    from matplotlib import pyplot as plt

    print(results["flow"].sum())
    ax = results["flow"][
        [c for c in results["flow"].columns if "storage" in str(c)]
    ].plot()
    results["storage_content"].div(10).plot(ax=ax)
    plt.show()


if __name__ == "__main__":
    main()
