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
def check_equal_timesteps_after_aggregation(hours_per_period : int,
                                            hours_of_input_time_series: int,
                                            periods_total_occurrence: list):

    if not sum(periods_total_occurrence) * hours_per_period == 8760:
        #todo: prints can be deleted in future
        print("aggregated timeseries has: " + str(int(sum(periods_total_occurrence) * hours_per_period)) + " timesteps")
        print("unaggregated timeseries has: " + str(hours_of_input_time_series) + " timesteps")
        print("therefore the occurrence of the typical periods for the objective weighting will be customized")
        customize_factor = hours_of_input_time_series / int(sum(periods_total_occurrence) * hours_per_period)
        result_list = [float(occurrence) * customize_factor for occurrence in periods_total_occurrence]
        periods_total_occurrence = result_list
        return periods_total_occurrence
    else:
        return periods_total_occurrence

def set_aggregated_timeseries_and_objective_weighting(segmentation,
                                                      periods_total_occurrence,
                                                      aggregated_period_dict,
                                                      first_time_stamp):
    previous_period = 0
    objective_weighting = []
    aggregated_time_series = []
    current_timestamp=first_time_stamp
    if segmentation:
        for period, timestep, segmented_timestep in aggregated_period_dict.index:
            if previous_period == period:
                aggregated_time_series.append(current_timestamp)
            else:
                aggregated_time_series.append(current_timestamp)
                previous_period = period
            objective_weighting.append(periods_total_occurrence[period] * segmented_timestep)
            current_timestamp += pd.Timedelta(minutes=60 * segmented_timestep)
    else:
        for period, timestep in aggregated_period_dict.index:
            if previous_period == period:
                aggregated_time_series.append(current_timestamp)
            else:
                aggregated_time_series.append(current_timestamp)
                previous_period = period
            objective_weighting.append(periods_total_occurrence[period])
            current_timestamp += pd.Timedelta(minutes=60)
    aggregated_time_series = pd.DatetimeIndex(aggregated_time_series)
    return aggregated_time_series, objective_weighting

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

    ##########################################################################
    # Initialize the energy system and read/calculate necessary parameters
    ##########################################################################

    logger.define_logging()
    logging.info("Initialize the energy system")

    t1 = pd.date_range("2022-01-01", periods=8760, freq="H")
    t2 = pd.date_range("2033-01-01", periods=8760, freq="H")
    tindex = t1.append(t2)

    data.index = tindex
    del data["timestep"]

    typical_periods = 40
    hours_per_period = 24
    segmentation = False
    if segmentation:
        print("segmentation hasn't been added so far")


    else:
        aggregation1 = tsam.TimeSeriesAggregation(
            timeSeries=data.iloc[:8760],
            noTypicalPeriods=typical_periods,
            hoursPerPeriod=hours_per_period,
            clusterMethod="k_means",
            sortValues=False,
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
            sortValues=False,
            rescaleClusterPeriods=False,
            extremePeriodMethod="replace_cluster_center",
            addPeakMin=["wind", "pv"],
            representationMethod="durationRepresentation",
        )

    aggregation1.createTypicalPeriods()
    aggregation2.createTypicalPeriods()

    periods_total_occurrence1 = [
        (aggregation1.clusterOrder == typical_period_name).sum() for typical_period_name in
        aggregation1.clusterPeriodIdx]
    periods_total_occurrence2 = [
        (aggregation2.clusterOrder == typical_period_name).sum() for typical_period_name in
        aggregation2.clusterPeriodIdx]
    periods_total_occurrence1 = check_equal_timesteps_after_aggregation(hours_per_period=hours_per_period,
                                            hours_of_input_time_series=t1.__len__(),
                                            periods_total_occurrence=periods_total_occurrence1
                                                                        )
    periods_total_occurrence2 = check_equal_timesteps_after_aggregation(hours_per_period = hours_per_period,
                                            hours_of_input_time_series = t2.__len__(),
                                            periods_total_occurrence=periods_total_occurrence2
                                                                        )
    #before timeseries generation was based on freq="H" (hourly), now you have to set the number of minutes of one timestep
    t1_agg, objective_weighting1 = set_aggregated_timeseries_and_objective_weighting(segmentation=segmentation,
                                                      periods_total_occurrence = periods_total_occurrence1,
                                                      aggregated_period_dict=pd.DataFrame.from_dict(aggregation1.clusterPeriodDict),
                                                      first_time_stamp=pd.to_datetime(t1[0])
                                                                                     )
    t2_agg, objective_weighting2 = set_aggregated_timeseries_and_objective_weighting(segmentation=segmentation,
                                                      periods_total_occurrence = periods_total_occurrence2,
                                                      aggregated_period_dict=pd.DataFrame.from_dict(aggregation2.clusterPeriodDict),
                                                      first_time_stamp=pd.to_datetime(t2[0])
                                                                                     )
    objective_weighting = objective_weighting1 + objective_weighting2

    t2_agg = t2_agg.append(pd.DatetimeIndex([t2_agg[-1] + pd.DateOffset(hours=1)]))
    tindex_agg = t1_agg.append(t2_agg)

    energysystem = solph.EnergySystem(
        timeindex=tindex_agg,
        periods=[t1_agg, t2_agg],
        tsa_parameters=[
            {
                "timesteps_per_period": aggregation1.hoursPerPeriod,
                "order": aggregation1.clusterOrder,
                "occurrences": aggregation1.clusterPeriodNoOccur,
                "timeindex": aggregation1.timeIndex,
            },
            {
                "timesteps_per_period": aggregation2.hoursPerPeriod,
                "order": aggregation2.clusterOrder,
                "occurrences": aggregation2.clusterPeriodNoOccur,
                "timeindex": aggregation2.timeIndex,
            },
        ],
        infer_last_interval=False,
    )

    price_gas = 5

    # If the period is one year the equivalent periodical costs (epc) of an
    # investment are equal to the annuity. Use oemof's economic tools.
    epc_wind = economics.annuity(capex=1000, n=20, wacc=0.05)
    epc_pv = economics.annuity(capex=1000, n=20, wacc=0.05)
    epc_storage = economics.annuity(capex=1000, n=20, wacc=0.05)

    ##########################################################################
    # Create oemof objects
    ##########################################################################

    logging.info("Create oemof objects")
    # create natural gas bus
    bgas = solph.Bus(label="natural_gas")

    # create electricity bus
    bel = solph.Bus(label="electricity")

    energysystem.add(bgas, bel)

    # create excess component for the electricity bus to allow overproduction
    excess = solph.components.Sink(
        label="excess_bel", inputs={bel: solph.Flow()}
    )

    # create source object representing the gas commodity (annual limit)
    gas_resource = solph.components.Source(
        label="rgas", outputs={bgas: solph.Flow(variable_costs=price_gas)}
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
                investment=solph.Investment(ep_costs=epc_wind, lifetime=10),
            )
        },
    )

    pv_profile = pd.concat(
        [aggregation1.typicalPeriods["pv"], aggregation2.typicalPeriods["pv"]],
        ignore_index=True,
    )
    pv_profile.iloc[-24:] = 0

    # create fixed source object representing pv power plants
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
                investment=solph.Investment(ep_costs=epc_pv, lifetime=10),
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
                nominal_value=1,
            )
        },
    )

    # create simple Converter object representing a gas power plant
    pp_gas = solph.components.Converter(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=0)},
        conversion_factors={bel: 0.58},
    )

    # create storage object representing a battery
    storage = solph.components.GenericStorage(
        label="storage",
        nominal_storage_capacity=5000,
        inputs={bel: solph.Flow(variable_costs=0.0001)},
        outputs={bel: solph.Flow()},
        loss_rate=0.01,
        lifetime_inflow=10,
        lifetime_outflow=10,
        invest_relation_input_capacity=1 / 6,
        invest_relation_output_capacity=1 / 6,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )

    energysystem.add(excess, gas_resource, wind, pv, demand, pp_gas, storage)

    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    logging.info("Optimise the energy system")

    # initialise the operational model
    om = solph.Model(energysystem,
                     objective_weighting= objective_weighting
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

    my_results = electricity_bus["period_scalars"]

    # installed capacity of storage in GWh
    my_results["storage_invest_GWh"] = (
        results[(storage, None)]["period_scalars"]["invest"] / 1e6
    )

    # installed capacity of wind power plant in MW
    my_results["wind_invest_MW"] = (
        results[(wind, bel)]["period_scalars"]["invest"] / 1e3
    )

    # resulting renewable energy share
    print(
        "res_share:",
        (
            1
            - results[(pp_gas, bel)]["sequences"].sum()
            / results[(bel, demand)]["sequences"].sum()
        ),
    )

    pp.pprint(my_results)


if __name__ == "__main__":
    main()
