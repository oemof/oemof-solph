# -*- coding: utf-8 -*-

"""
General description
-------------------
This example shows how to perform a capacity optimization for
an energy system with storage. The following energy system is modeled:

.. code-block:: text

                    input/output  bgas     bel
                         |          |        |
                         |          |        |
     wind(FixedSource)   |------------------>|
                         |          |        |
     pv(FixedSource)     |------------------>|
                         |          |        |
     gas_resource        |--------->|        |
     (Commodity)         |          |        |
                         |          |        |
     demand(Sink)        |<------------------|
                         |          |        |
                         |          |        |
     pp_gas(Converter)   |<---------|        |
                         |------------------>|
                         |          |        |
     storage(Storage)    |<------------------|
                         |------------------>|

The example exists in four variations. The following parameters describe
the main setting for the optimization variation 1:

- optimize wind, pv, gas_resource and storage
- set investment cost for wind, pv and storage
- set gas price for kWh

Results show an installation of wind and the use of the gas resource.
A renewable energy share of 51% is achieved.

.. tip::

    Have a look at different parameter settings. There are four variations
    of this example in the same folder.

Code
----
Download source code: :download:`v1_invest_optimize_all_technologies.py </../examples/storage_investment/v1_invest_optimize_all_technologies.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/storage_investment/v1_invest_optimize_all_technologies.py
        :language: python
        :lines: 80-

Data
----
Download data: :download:`storage_investment.csv </../examples/storage_investment/storage_investment.csv>`


Installation requirements
-------------------------

This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_

"""

###############################################################################
# Imports
###############################################################################

import logging
import os
import pprint as pp
import warnings
import tsam.timeseriesaggregation as tsam
import matplotlib.pyplot as plt

import pandas as pd
from oemof.tools import economics
from oemof.tools import logger
from oemof.solph import views

from oemof import solph


def main():
    # Read data file
    filename = os.path.join(os.getcwd(), "storage_investment.csv")
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError:
        msg = "Data file not found: {0}. Only one value used!"
        warnings.warn(msg.format(filename), UserWarning)
        data = pd.DataFrame(
            {"pv": [0.3, 0.5], "wind": [0.6, 0.8], "demand_el": [500, 600]}
        )

    data = pd.concat([data, data], ignore_index=True)
    data["wind"].iloc[8760 - 24 : 8760] = 0
    data["wind"].iloc[8760 * 2 - 24 : 8760] = 0
    data["pv"].iloc[8760 - 24 : 8760] = 0
    data["pv"].iloc[8760 * 2 - 24 : 8760] = 0

    # add a season without electricity production to simulate the possible advantage using a seasonal storages
    # for the first perido
    data["wind"].iloc[2920: 2 * 2920 + 1] = 0
    data["pv"].iloc[2920:2 * 2920 + 1] = 0

    ##########################################################################
    # Initialize the energy system and read/calculate necessary parameters
    ##########################################################################

    logger.define_logging()
    logging.info("Initialize the energy system")
    #todo: right now, tsam only determines the timeincrement right, when you pick the
    #first periods last timestamp next to the second periods first timestep
    #2022-31-12-23:00 --> 2023-01-01-00:00 , than timeincrement in between is equal to 1
    #todo add initial storage level in new periods is equal to zero?
    t1 = pd.date_range("2022-01-01", periods=8760, freq="H")
    t2 = pd.date_range("2023-01-01", periods=8760, freq="H")
    tindex = t1.append(t2)

    data.index = tindex
    del data["timestep"]

    typical_periods = 10
    hours_per_period = 24
    segmentation = False
    if segmentation:
        print("segmentation hasn't been added so far")


    else:
        aggregation1 = tsam.TimeSeriesAggregation(
            timeSeries=data.iloc[:8760],
            noTypicalPeriods=typical_periods,
            hoursPerPeriod=hours_per_period,
            clusterMethod="hierarchical",
            sortValues=True,
            segmentation=False,
            rescaleClusterPeriods=False,
            extremePeriodMethod="replace_cluster_center",
            addPeakMin=["wind", "pv"],
            representationMethod="durationRepresentation",
        )

        aggregation2 = tsam.TimeSeriesAggregation(
            timeSeries=data.iloc[8760:],
            noTypicalPeriods=typical_periods,
            hoursPerPeriod=hours_per_period,
            clusterMethod="hierarchical",
            sortValues=True,
            segmentation=False,
            rescaleClusterPeriods=False,
            extremePeriodMethod="replace_cluster_center",
            addPeakMin=["wind", "pv"],
            representationMethod="durationRepresentation",
        )

    energysystem = solph.EnergySystem(
        tsam_aggregations=[aggregation1, aggregation2],
        infer_last_interval=False,
    )

    electricity_price = 100

    ##########################################################################
    # Create oemof objects
    ##########################################################################

    logging.info("Create oemof objects")


    # create electricity bus
    bel = solph.Bus(label="electricity")

    energysystem.add( bel)

    # create excess component for the electricity bus to allow overproduction
    excess = solph.components.Sink(
        label="excess_bel", inputs={bel: solph.Flow()}
    )

    # create source object representing the gas commodity (annual limit)
    elect_resource = solph.components.Source(
        label="electricity_source", outputs={bel: solph.Flow(variable_costs=electricity_price)}
    )

    wind_profile = pd.concat(
        [
            aggregation1.typicalPeriods["wind"],
            aggregation2.typicalPeriods["wind"],
        ],
        ignore_index=True,
    )
    wind_profile.iloc[-24:] = 0

    # create fixed source object representing wind power plants
    wind = solph.components.Source(
        label="wind",
        outputs={
            bel: solph.Flow(
                fix=wind_profile,
                nominal_value=1500000
            )
        },
    )

    pv_profile = pd.concat(
        [aggregation1.typicalPeriods["pv"],
         aggregation2.typicalPeriods["pv"]
         ],
        ignore_index=True,
    )
    pv_profile.iloc[-24:] = 0

    # create fixed source object representing pv power plants
    if False:
        pv = solph.components.Source(
            label="pv",
            outputs={
                bel: solph.Flow(
                    fix=pd.concat(
                        [
                            aggregation1.typicalPeriods["pv"],
                            aggregation2.typicalPeriods["pv"],
                        ],
                        ignore_index=True,
                    ),
                    nominal_value=900000
                )
            },
        )

    # create simple sink object representing the electrical demand
    demand = solph.components.Sink(
        label="demand",
        inputs={
            bel: solph.Flow(
                fix=pd.concat(
                    [
                        aggregation1.typicalPeriods["demand_el"],
                        aggregation2.typicalPeriods["demand_el"],
                    ],
                    ignore_index=True,
                ),
                nominal_value=0.05,
            )
        },
    )

    # create storage object representing a battery
    storage = solph.components.GenericStorage(
        label="storage",
        nominal_storage_capacity=3000000,
        initial_storage_level=0,
        inputs={bel: solph.Flow(variable_costs=0.0, nominal_value=2000)},
        outputs={bel: solph.Flow(nominal_value=2000)},
        loss_rate=0.001,
        inflow_conversion_factor=1,
        outflow_conversion_factor=1,
    )
    if False:
        energysystem.add(excess, elect_resource, wind, pv, demand, storage)
    else:
        energysystem.add(excess, elect_resource, wind, demand, storage)

    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    logging.info("Optimise the energy system")

    # initialise the operational model
    om = solph.Model(energysystem
                     )

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    om.solve(solver="cbc", solve_kwargs={"tee": True})

    ##########################################################################
    # Check and plot the results
    ##########################################################################

    # check if the new result object is working for custom components
    results = solph.processing.results(om)
    print(results)

    # Concatenate flows:
    flows = pd.concat([flow["sequences"] for flow in results.values()], axis=1)
    flows.columns = [
        f"{oemof_tuple[0]}-{oemof_tuple[1]}" for oemof_tuple in results.keys()
    ]
    print(flows)

    electricity_bus = solph.views.node(results, "electricity")

    meta_results = solph.processing.meta_results(om)
    pp.pprint(meta_results)

    fig, ax = plt.subplots(figsize=(10, 5))
    storage_results = results[(storage, None)]["sequences"] / storage.nominal_storage_capacity
    storage_results .plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 5))
    storage_results = results[(wind, bel)]["sequences"]
    storage_results .plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    ax.set_title("Elect. from Wind")
    plt.show()
    if False:
        fig, ax = plt.subplots(figsize=(10, 5))
        storage_results = results[(pv, bel)]["sequences"]
        storage_results .plot(
            ax=ax, kind="line", drawstyle="steps-post"
        )
        ax.set_title("Elect. from PV")
        plt.show()

    fig, ax = plt.subplots(figsize=(10, 5))
    storage_results = results[(bel, demand)]["sequences"]
    storage_results .plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    ax.set_title("Demand")
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 5))
    storage_results = results[(elect_resource, bel)]["sequences"]
    storage_results .plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    ax.set_title("Elect. from Grid")
    plt.show()
    my_results = electricity_bus["period_scalars"]


    pp.pprint(my_results)


if __name__ == "__main__":
    main()
