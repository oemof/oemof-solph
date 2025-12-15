# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

import logging
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import tsam.timeseriesaggregation as tsam
from cost_data import investment_costs
from matplotlib import pyplot as plt
from oemof.tools import debugging
from oemof.tools import logger
from shared import prepare_input_data

from oemof import solph
from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import Results
from oemof.solph import components as cmp


def determine_periods(datetimeindex):
    """Explicitly define and return periods of the energy system

    Leap years have 8784 hourly time steps, regular years 8760.

    Parameters
    ----------
    datetimeindex : pd.date_range
        DatetimeIndex of the model comprising all time steps

    Returns
    -------
    periods : list
        periods for the optimization run
    """
    years = sorted(list(set(getattr(datetimeindex, "year"))))
    periods = []
    filter_series = datetimeindex.to_series()
    for number, year in enumerate(years):
        start = filter_series.loc[filter_series.index.year == year].min()
        end = filter_series.loc[filter_series.index.year == year].max()
        periods.append(pd.date_range(start, end, freq=datetimeindex.freq))

    return periods


warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

# ---------- read cost data ------------------------------------------------------------

investment_costs = investment_costs()

# ---------- read time series data and resample-----------------------------------------
df_temperature, df_energy = prepare_input_data(plot_resampling=False)

df_temperature = df_temperature.resample("1 h").mean()
df_energy = df_energy.resample("1 h").mean()

time_series_data_full = pd.concat([df_temperature, df_energy], axis=1)

time_series_data_full = time_series_data_full.drop(
    columns=["Air Temperature (°C)", "heat demand (kWh)"]
).drop(time_series_data_full.index[0])

time_index = time_series_data_full.index

# -------------- Clustering of Input time-series with TSAM -----------------------------
typical_periods = 40
hours_per_period = 24

aggregation = tsam.TimeSeriesAggregation(
    timeSeries=time_series_data_full.iloc[:8760],
    noTypicalPeriods=typical_periods,
    hoursPerPeriod=hours_per_period,
    clusterMethod="k_means",
    sortValues=False,
    rescaleClusterPeriods=False,
)
aggregation.createTypicalPeriods()

# pandas DatTime for the aggregated time series
tindex_agg = pd.date_range(
    "2025-01-01", periods=typical_periods * hours_per_period, freq="h"
)

# ------------ create timeindex etc. for multiperiod -----------------------------------
# list with years in which investment is possible
years = [2025, 2030, 2035, 2040, 2045]
# base_year = tindex_agg[0].year

# # Create a list of shifted copies of the original index, one per investment year
# shifted = [tindex_agg + pd.DateOffset(years=(y - base_year)) for y in years]

# # Concatenate them into one DatetimeIndex
# tindex_agg_full = shifted[0]
# for s in shifted[1:]:
#     tindex_agg_full = tindex_agg_full.append(s)

tindex_agg_full = pd.date_range(
    "2025-01-01",
    periods=typical_periods * hours_per_period * len(years),
    freq="h",
)

# list of with time index for each year
# periods = determine_periods(tindex_agg_full)
periods = [tindex_agg] * len(years)

# parameters for time series aggregation in oemof-solph with one dict per year
tsa_parameters = [
    {
        "timesteps_per_period": aggregation.hoursPerPeriod,
        "order": aggregation.clusterOrder,
        "timeindex": aggregation.timeIndex,
    }
] * len(years)

# # ---------- read time series data -----------------------------------------------------

# file_path = Path(__file__).parent

# df = pd.read_csv(
#     Path(file_path, "energy.csv"),
# )
# df["time"] = pd.to_datetime(df["Unix Epoch"], unit="s")
# # time als Index setzen
# df = df.set_index("time")
# df = df.drop(columns=["Unix Epoch"])
# # print(df)

# time_index = df.index

# # Dummy pv profile
# h = np.arange(len(time_index))
# pv_profile = df["PV (W)"]

# # Dummy electricity profile
# df["house_elec_kW"] = 0.3 + 0.7 * np.random.rand(len(time_index))

# # Dummy heat profile
# df["house_heat_kW"] = 0.3 + 0.7 * np.random.rand(len(time_index))

# # EV-Ladeprofil
# df["ev_charge_kW"] = (
#     0.0  # wird automatisch auf alle Zeitschritte gebroadcastet
# )

# # COP-Profil (konstant, später evtl. temperaturabhängig)
# df["cop_hp"] = 3.5

# df = df.resample("1h").mean()

# # -------------- Clustering of Input time-series with TSAM -----------------------------
# typical_periods = 40
# hours_per_period = 24

# aggregation = tsam.TimeSeriesAggregation(
#     timeSeries=df.iloc[:8760],
#     noTypicalPeriods=typical_periods,
#     hoursPerPeriod=hours_per_period,
#     clusterMethod="k_means",
#     sortValues=False,
#     rescaleClusterPeriods=False,
# )
# aggregation.createTypicalPeriods()

# # pandas DatTime for the aggregated time series
# tindex_agg_one_year = pd.date_range(
#     "2022-01-01", periods=typical_periods * hours_per_period, freq="h"
# )

# # ------------ create timeindex etc. for multiperiod -----------------------------------
# # list with years in which investment is possible
# years = [2025, 2030, 2035, 2040, 2045]

# # stretch time index to include all years (continously)
# tindex_agg_full = pd.date_range(
#     "2022-01-01",
#     periods=typical_periods * hours_per_period * len(years),
#     freq="h",
# )

# # list of with time index for each year
# periods = [tindex_agg_one_year] * len(years)

# # parameters for time series aggregation in oemof-solph with one dict per year
# tsa_parameters = [
#     {
#         "timesteps_per_period": aggregation.hoursPerPeriod,
#         "order": aggregation.clusterOrder,
#         "timeindex": aggregation.timeIndex,
#     }
# ] * len(years)

# ------------------ calculate discount rate and lifetime ------------------------------

# the annuity has to be calculated for a period of 5 years
investment_period_length_in_years = 5


def lifetime_adjusted(lifetime, investment_period_length_in_years):
    return lifetime / investment_period_length_in_years


def discount_rate_adjusted(discount_rate, investment_period_length_in_years):
    return (1 + discount_rate) ** investment_period_length_in_years - 1


# ------------------ create energy system ----------------------------------------------
es = EnergySystem(
    timeindex=tindex_agg_full,
    timeincrement=[1] * len(tindex_agg_full),
    periods=periods,
    tsa_parameters=tsa_parameters,
    infer_last_interval=False,
)


bus_el = Bus(label="electricity")
bus_heat = Bus(label="heat")
es.add(bus_el, bus_heat)

# new_s = pd.concat(
#     [aggregation.typicalPeriods["PV (W)"]] * len(years), ignore_index=True
# )
# print(new_s)
pv = cmp.Source(
    label="PV",
    outputs={
        bus_el: Flow(
            fix=pd.concat(
                [aggregation.typicalPeriods["PV (W)"]] * len(years),
                ignore_index=True,
            ),
            nominal_capacity=Investment(
                ep_costs=investment_costs[("pv", "specific_costs [Eur/W]")],
                lifetime=lifetime_adjusted(
                    50, investment_period_length_in_years
                ),
                fixed_costs=investment_costs[("pv", "fixed_costs [Eur]")],
                maximum=500,
            ),
        )
    },
)
es.add(pv)

# Battery
battery = cmp.GenericStorage(
    label="Battery",
    inputs={bus_el: Flow()},
    outputs={bus_el: Flow()},
    nominal_capacity=Investment(
        ep_costs=investment_costs[("battery", "specific_costs [Eur/Wh]")],
        lifetime=lifetime_adjusted(50, investment_period_length_in_years),
    ),
    # kWh
    # initial_storage_level=0.5,  # 50%
    min_storage_level=0.0,
    max_storage_level=1.0,
    loss_rate=0.001,  # 0.1%/h
    inflow_conversion_factor=0.95,  # Lade-Wirkungsgrad
    outflow_conversion_factor=0.95,  # Entlade-Wirkungsgrad
)
es.add(battery)

# Electricity demand
house_sink = cmp.Sink(
    label="Electricity demand",
    inputs={
        bus_el: Flow(
            fix=pd.concat(
                [aggregation.typicalPeriods["electricity demand (W)"]]
                * len(years),
                ignore_index=True,
            ),
            nominal_capacity=1.0,
        )
    },
)
es.add(house_sink)

# Electric vehicle demand
# wallbox_sink = cmp.Sink(
#     label="Electric Vehicle",
#     inputs={
#         bus_el: Flow(
#             fix=pd.concat(
#                 [aggregation.typicalPeriods["ev_charge_kW"]] * len(years),
#                 ignore_index=True,
#             ),
#             nominal_capacity=1.0,
#         )
#     },
# )
# es.add(wallbox_sink)

# Heat Pump
hp = cmp.Converter(
    label="Heat pump",
    inputs={bus_el: Flow()},
    outputs={
        bus_heat: Flow(
            nominal_capacity=Investment(
                ep_costs=investment_costs[
                    ("heat pump", "specific_costs [Eur/W]")
                ],
                lifetime=lifetime_adjusted(
                    50, investment_period_length_in_years
                ),
                fixed_costs=investment_costs[
                    ("heat pump", "fixed_costs [Eur]")
                ],
            )
        )
    },
    conversion_factors={bus_heat: 3.5},
)
es.add(hp)

# Heat demand
heat_sink = cmp.Sink(
    label="Heat demand",
    inputs={
        bus_heat: Flow(
            fix=pd.concat(
                [aggregation.typicalPeriods["heat demand (W)"]] * len(years),
                ignore_index=True,
            ),
            nominal_capacity=1.0,
        )
    },
)
es.add(heat_sink)

grid_import = cmp.Source(
    label="Grid import", outputs={bus_el: Flow(variable_costs=0.30)}
)
es.add(grid_import)

# Grid feed-in
feed_in = cmp.Sink(
    label="Grid Feed-in", inputs={bus_el: Flow(variable_costs=-0.08)}
)
es.add(feed_in)

# Create Model and solve it
logging.info("Creating Model...")
m = Model(es)
logging.info("Solving Model...")
m.solve(solver="gurobi", solve_kwargs={"tee": True})


# Create Results
results = Results(m)
print(results.keys())
total = results.total
print(total)
