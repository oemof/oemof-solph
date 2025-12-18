# -*- coding: utf-8 -*-
import logging
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import tsam.timeseriesaggregation as tsam
from cost_data import energy_prices
from cost_data import investment_costs
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


# ---------------- some helper functions -----------------------------------------------
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


def lifetime_adjusted(lifetime, investment_period_length_in_years):
    return int(lifetime / investment_period_length_in_years)


def discount_rate_adjusted(discount_rate, investment_period_length_in_years):
    return (1 + discount_rate) ** investment_period_length_in_years - 1


def expand_energy_prices(tindex_agg_full, prices):
    years_in_index = sorted(set(tindex_agg_full.year))
    years_available = set(prices.index)

    # Strict check: all years in the index must be present in the table
    missing = [y for y in years_in_index if y not in years_available]
    if missing:
        raise KeyError(f"Missing prices for years in index: {missing}")

    # Build a year->price lookup and vectorized map
    s = pd.DataFrame()
    for col in prices.columns:
        year_prices = prices[col]
        s[col] = pd.Series(
            pd.Series(tindex_agg_full.year).map(year_prices).values,
            index=tindex_agg_full,
            name=col,
        )
    return s


# --------------------------------------------------------------------------------------
warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

# ---------- read cost data ------------------------------------------------------------

investment_costs = investment_costs()
prices = energy_prices()

# ---------- read time series data and resample-----------------------------------------

# read data
df_temperature, df_energy = prepare_input_data(plot_resampling=False)

# resample to one hour
df_temperature = df_temperature.resample("1 h").mean()
df_energy = df_energy.resample("1 h").mean()

# create data as one DataFrame
time_series_data_full = pd.concat([df_temperature, df_energy], axis=1)

# drop unnecessary columns and time steps of previous year
time_series_data_full = time_series_data_full.drop(
    columns=["Air Temperature (°C)", "heat demand (kWh)"]
).drop(time_series_data_full.index[0])

# convert untis from W to kW
time_series_data_full = time_series_data_full / 1000
time_series_data_full = time_series_data_full.rename(
    columns={
        "heat demand (W)": "heat demand (kW)",
        "electricity demand (W)": "electricity demand (kW)",
        "PV (W)": "PV (kW)",
    }
)

# -------------- Clustering of input time-series with TSAM -----------------------------
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

# create a time index for the aggregated time series
tindex_agg = pd.date_range(
    "2025-01-01", periods=typical_periods * hours_per_period, freq="h"
)

# ------------ create timeindex etc. for multiperiod -----------------------------------
# Note:
# originally the data provided is for investment periods of 5 years each
# so years = [2025, 2030, 2035, 2040, 2045]
# this was causing a bug in the mulit period calculation of the fixed_costs in the
# INVESTFLOWS, therefore years is set to [2025, 2026, 2027, 2028, 2029] in this eaxample
# this will be changed, when the bug is fixed

# list with years in which investment is possible
years = [2025, 2026, 2027, 2028, 2029]

# create a time index for the whole model
# Create a list of shifted copies of the original index, one per investment year
base_year = years[0]
shifted = [tindex_agg + pd.DateOffset(years=(y - base_year)) for y in years]

# Concatenate them into one DatetimeIndex
tindex_agg_full = shifted[0]
for s in shifted[1:]:
    tindex_agg_full = tindex_agg_full.append(s)

print("------- Time Index of Multi-Period Model --------")
print("time index: ", tindex_agg_full)
print("-------------------------------------------------")

# create the list of investent periods for the model
investment_periods = determine_periods(tindex_agg_full)

print("------- Priods of Multi-Period Model --------")
print("Investment periods: ", investment_periods)
print("---------------------------------------------")

# create parameters for time series aggregation in oemof-solph with one dict per year
tsa_parameters = [
    {
        "timesteps_per_period": aggregation.hoursPerPeriod,
        "order": aggregation.clusterOrder,
        "timeindex": aggregation.timeIndex,
    }
] * len(years)

# ------------------ calculate discount rate and lifetime ------------------------------

# the annuity has to be calculated for a period of 5 years
investment_period_length_in_years = 5

# ------------------ create energy system ----------------------------------------------
es = EnergySystem(
    timeindex=tindex_agg_full,
    periods=investment_periods,
    tsa_parameters=tsa_parameters,
    infer_last_interval=False,
)

bus_el = Bus(label="electricity")
bus_heat = Bus(label="heat")
bus_gas = Bus(label="gas")
es.add(bus_el, bus_heat, bus_gas)

# test_pv = pd.concat(
#     [aggregation.typicalPeriods["PV (kW)"]] * len(years),
#     ignore_index=True,
# )
# test_pv.plot()

pv = cmp.Source(
    label="PV",
    outputs={
        bus_el: Flow(
            fix=pd.concat(
                [aggregation.typicalPeriods["PV (kW)"]] * len(years),
                ignore_index=True,
            ),
            nominal_capacity=Investment(
                ep_costs=investment_costs[("pv", "specific_costs [Eur/kW]")],
                lifetime=lifetime_adjusted(
                    20, investment_period_length_in_years
                ),
                fixed_costs=investment_costs[("pv", "fixed_costs [Eur]")]
                / lifetime_adjusted(20, investment_period_length_in_years),
                overall_maximum=10,
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
        ep_costs=investment_costs[("battery", "specific_costs [Eur/kWh]")],
        lifetime=lifetime_adjusted(10, investment_period_length_in_years),
    ),
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
                [aggregation.typicalPeriods["electricity demand (kW)"]]
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
                    ("heat pump", "specific_costs [Eur/kW]")
                ],
                lifetime=lifetime_adjusted(
                    20, investment_period_length_in_years
                ),
                fixed_costs=investment_costs[
                    ("heat pump", "fixed_costs [Eur]")
                ]
                / lifetime_adjusted(20, investment_period_length_in_years),
            )
        )
    },
    conversion_factors={bus_heat: 3.5},
)
es.add(hp)

# Gas Boiler
gas_boiler = cmp.Converter(
    label="Gas boiler",
    inputs={bus_gas: Flow()},
    outputs={
        bus_heat: Flow(
            nominal_capacity=Investment(
                ep_costs=investment_costs[
                    ("gas boiler", "specific_costs [Eur/kW]")
                ],
                lifetime=lifetime_adjusted(
                    20, investment_period_length_in_years
                ),
                fixed_costs=investment_costs[
                    ("gas boiler", "fixed_costs [Eur]")
                ]
                / lifetime_adjusted(20, investment_period_length_in_years),
                existing=3.5,
                age=2,
            )
        )
    },
    conversion_factors={bus_heat: 0.9},
)
es.add(gas_boiler)

# Heat demand
heat_sink = cmp.Sink(
    label="Heat demand",
    inputs={
        bus_heat: Flow(
            fix=pd.concat(
                [aggregation.typicalPeriods["heat demand (kW)"]] * len(years),
                ignore_index=True,
            ),
            nominal_capacity=1.0,
        )
    },
)
es.add(heat_sink)

# calculate prices for each time step
p = expand_energy_prices(tindex_agg_full, prices)

grid_import = cmp.Source(
    label="Grid import",
    outputs={bus_el: Flow(variable_costs=p["electricity_prices [Eur/kWh]"])},
)
es.add(grid_import)

# Grid feed-in
feed_in = cmp.Sink(
    label="Grid Feed-in",
    inputs={bus_el: Flow(variable_costs=p["pv_feed_in [Eur/kWh]"])},
)
es.add(feed_in)

# Gas grid
gas_grid = cmp.Source(
    label="Gas grid",
    outputs={bus_gas: Flow(variable_costs=p["gas_prices [Eur/kWh]"])},
)
es.add(gas_grid)

# Create Model and solve it
logging.info("Creating Model...")
m = Model(es)
logging.info("Solving Model...")
m.solve(
    solver="gurobi",
    solve_kwargs={
        "tee": True,
        "keepfiles": True,
        "symbolic_solver_labels": True,
    },
)

# ----------------- Post Processing ----------------------------------------------------

# Create Results
# results = Results(m)
# print(results.keys())
# total = results.total
# print(results.total)
# print(results.invest)
# print(results.flow)
# results.flow.iloc[:, 6].plot()
# total.plot(kind="bar")
# plt.show()
# print(results.invest)
# print(results.old)
# print(results.old_exo)
# print(results.old_end)

results = solph.processing.results(m)

results_bus_el = solph.views.node(results, bus_el)
results_bus_heat = solph.views.node(results, bus_heat)

my_results = results_bus_el["period_scalars"]

# installed capacity of pv-system in kW
pv_invest_kW = results[(pv, bus_el)]["period_scalars"]["invest"]
print(pv_invest_kW)
