# -*- coding: utf-8 -*-
import logging
import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import tsam.timeseriesaggregation as tsam
from cost_data import energy_prices
from cost_data import investment_costs
from oemof.tools import debugging
from oemof.tools import logger
from shared import prepare_input_data

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import Results
from oemof.solph import components as cmp

from time_series_un_even import populate_and_solve_energy_system


# ---------------- some helper functions --------------------------------------
def lifetime_adjusted(lifetime, investment_period_length_in_years):
    return int(lifetime / investment_period_length_in_years)


def discount_rate_adjusted(discount_rate, investment_period_length_in_years):
    return (1 + discount_rate) ** investment_period_length_in_years - 1


def expand_energy_prices(tidx_agg_full, e_prices):
    years_in_index = sorted(set(tidx_agg_full.year))
    years_available = set(e_prices.index)

    # Strict check: all years in the index must be present in the table
    missing = [y for y in years_in_index if y not in years_available]
    if missing:
        raise KeyError(f"Missing prices for years in index: {missing}")

    # Build a year->price lookup and vectorized map
    df = pd.DataFrame()
    for col in e_prices.columns:
        year_prices = e_prices[col]
        df[col] = pd.Series(
            pd.Series(tidx_agg_full.year).map(year_prices).values,
            index=tidx_agg_full,
            name=col,
        )
    return df


# -----------------------------------------------------------------------------
warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

# ---------- read cost data ---------------------------------------------------

investment_costs = investment_costs()
prices = energy_prices()

# Note:
# originally the data provided is for investment periods of 5 years each
# so years = [2025, 2030, 2035, 2040, 2045]
# this was causing a bug in the mulit period calculation of the fixed_costs in
# the INVESTFLOWS, therefore years is set to [2025, 2026, 2027, 2028, 2029] in
# this example this will be changed, when the bug is fixed

# list with years in which investment is possible
years = [2025, 2026, 2027, 2028, 2029]

investment_costs_new = investment_costs.loc[[2025, 2030, 2035, 2040, 2045]]
investment_costs_new.index = years
investment_costs = investment_costs_new

prices_new = prices.loc[[2025, 2030, 2035, 2040, 2045]]
prices_new.index = years
prices = prices_new

# ---------- read time series data and resample--------------------------------

data = prepare_input_data()

data = data.resample("1 h").mean()
print(data)

# -------------- Clustering of input time-series with TSAM --------------------
typical_periods = 100
hours_per_period = 24

start = datetime.now()

aggregation = tsam.TimeSeriesAggregation(
    timeSeries=data.iloc[:8760],
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

# ------------ create timeindex etc. for multiperiod --------------------------


# create a time index for the whole model
# Create a list of shifted copies of the original index,
# one per investment year
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
investment_periods = [
    tindex_agg + pd.DateOffset(years=i) for i in range(len(years))
]


print("------- Priods of Multi-Period Model --------")
print("Investment periods: ", investment_periods)
print("---------------------------------------------")

# create parameters for time series aggregation in oemof-solph
# with one dict per year
tsa_parameters = [
    {
        "timesteps_per_period": aggregation.hoursPerPeriod,
        "order": aggregation.clusterOrder,
        "timeindex": tindex_agg + pd.DateOffset(years=i),
    }
    for i in range(len(years))
]

timeincrement = [1] * (len(tindex_agg_full))

time_series = {
    "cop": pd.concat(
        [aggregation.typicalPeriods["cop"]] * len(years),
        ignore_index=True,
    ),
    "electricity demand (kW)": pd.concat(
        [aggregation.typicalPeriods["electricity demand (kW)"]] * len(years),
        ignore_index=True,
    ),
    "heat demand (kW)": pd.concat(
        [aggregation.typicalPeriods["heat demand (kW)"]] * len(years),
        ignore_index=True,
    ),
    "PV (kW/kWp)": pd.concat(
        [aggregation.typicalPeriods["PV (kW/kWp)"]] * len(years),
        ignore_index=True,
    ),
    "Electricity for Car Charging_HH1": pd.concat(
        [aggregation.typicalPeriods["Electricity for Car Charging_HH1"]]
        * len(years),
        ignore_index=True,
    ),
}

investments = {
    "pv": Investment(
        ep_costs=investment_costs[("pv", "specific_costs [Eur/kW]")] / 5,
        lifetime=4,
        nonconvex=True,
        offset=investment_costs[("pv", "fixed_costs [Eur]")] / 5,
        maximum=10,
        overall_maximum=10,
    ),
    "battery": Investment(
        ep_costs=investment_costs[("battery", "specific_costs [Eur/kWh]")] / 5,
        lifetime=2,
    ),
    "heat pump": Investment(
        ep_costs=investment_costs[("heat pump", "specific_costs [Eur/kW]")]
        / 5,
        lifetime=4,
        nonconvex=True,
        offset=investment_costs[("heat pump", "fixed_costs [Eur]")] / 5,
        maximum=10,
        overall_maximum=10,
    ),
    "gas boiler": Investment(
        ep_costs=investment_costs[("gas boiler", "specific_costs [Eur/kW]")]
        / 5,
        lifetime=4,
        fixed_costs=investment_costs[("gas boiler", "fixed_costs [Eur]")] / 5,
        existing=3.5,  # existing cannot be combined with nonconvex
        age=2,
    ),
}

# ------------------ create energy system -------------------------------------
es = EnergySystem(
    timeindex=tindex_agg_full,
    timeincrement=timeincrement,
    periods=investment_periods,
    tsa_parameters=tsa_parameters,
    infer_last_interval=False,
    use_remaining_value=True,
)

populate_and_solve_energy_system(
    es=es,
    time_series=time_series,
    investments=investments,
    variable_costs=expand_energy_prices(tindex_agg_full, prices),
    discount_rate=discount_rate_adjusted(0.05, 5),
)

# ----------------- Post Processing -------------------------------------------

# Create Results
results = Results(m)

# invest and total installed capacity
invest = results["invest"]
total = results["total"]
print(datetime.now() - start)

years = [2025, 2030, 2035, 2040, 2045]
invest.index = years
total.index = years

fig, ax1 = plt.subplots(
    1, 1, figsize=(8, 2.5), sharex=True, constrained_layout=True
)

total.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Total installed capacity")
ax1.grid(True, linewidth=0.3, alpha=0.6)
ax1.legend(["heat pump", "gas boiler", "PV", "battery"], loc="best")

plt.show()

# Note: if you want to extract values for the flow, you have to change
# to_df() in the class Results() in this way:
#
#     # overwrite known indexes
#     index_type = tuple(dataset.index_set().subsets())[-1].name
#     match index_type:
#         case "TIMEPOINTS":
#             df.index = self.timeindex
#         case "TIMESTEPS":
#             # df.index = self.timeindex[:-1]
#             df.index = self.timeindex
#         case _:
#             df.index = df.index.get_level_values(-1)
#
# otherwise including the storage leads to Length mismatch Value Error
# why: no clue, something with TIMESTEPS and TIMEPOINTS for storage
#
# if you changed this you can use
# flows = results["flow"]
# to look at the time series
