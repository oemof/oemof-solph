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

warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

# ---------- read cost data ------------------------------------------------------------

investment_costs = investment_costs()

# ---------- read time series data -----------------------------------------------------

file_path = Path(__file__).parent

df = pd.read_csv(
    Path(file_path, "energy.csv"),
)
df["time"] = pd.to_datetime(df["Unix Epoch"], unit="s")
# time als Index setzen
df = df.set_index("time")
df = df.drop(columns=["Unix Epoch"])
# print(df)

time_index = df.index

# Dummy pv profile
h = np.arange(len(time_index))
pv_profile = df["PV (W)"]

# Dummy electricity profile
df["house_elec_kW"] = 0.3 + 0.7 * np.random.rand(len(time_index))

# Dummy heat profile
df["house_heat_kW"] = 0.3 + 0.7 * np.random.rand(len(time_index))

# EV-Ladeprofil
df["ev_charge_kW"] = (
    0.0  # wird automatisch auf alle Zeitschritte gebroadcastet
)

# COP-Profil (konstant, später evtl. temperaturabhängig)
df["cop_hp"] = 3.5

df = df.resample("1h").mean()

# -------------- Clustering of Input time-series with TSAM -----------------------------
typical_periods = 40
hours_per_period = 24

aggregation = tsam.TimeSeriesAggregation(
    timeSeries=df.iloc[:8760],
    noTypicalPeriods=typical_periods,
    hoursPerPeriod=hours_per_period,
    clusterMethod="k_means",
    sortValues=False,
    rescaleClusterPeriods=False,
)
aggregation.createTypicalPeriods()

# pandas DatTime for the aggregated time series
tindex_agg_one_year = pd.date_range(
    "2022-01-01", periods=typical_periods * hours_per_period, freq="h"
)

# ------------ create timeindex etc. for multiperiod -----------------------------------
# list with years in which investment is possible
years = [2025, 2030, 2035, 2040, 2045]

# stretch time index to include all years (continously)
tindex_agg_full = pd.date_range(
    "2022-01-01",
    periods=typical_periods * hours_per_period * len(years),
    freq="h",
)

# list of with time index for each year
periods = [tindex_agg_one_year] * len(years)

# parameters for time series aggregation in oemof-solph with one dict per year
tsa_parameters = [
    {
        "timesteps_per_period": aggregation.hoursPerPeriod,
        "order": aggregation.clusterOrder,
        "timeindex": aggregation.timeIndex,
    }
] * len(years)

# ------------------ create energy system ----------------------------------------------
es = EnergySystem(
    timeindex=tindex_agg_full,
    # timeincrement=[1] * len(tindex_agg_full),
    periods=periods,
    tsa_parameters=tsa_parameters,
    infer_last_interval=False,
)


bus_el = Bus(label="electricity")
bus_heat = Bus(label="heat")
es.add(bus_el, bus_heat)

new_s = pd.concat(
    [aggregation.typicalPeriods["PV (W)"]] * len(years), ignore_index=True
)
print(new_s)
pv = cmp.Source(
    label="PV",
    outputs={
        bus_el: Flow(
            fix=pd.concat(
                [aggregation.typicalPeriods["PV (W)"]] * len(years),
                ignore_index=True,
            ),
            nominal_capacity=Investment(
                ep_costs=investment_costs[("pv", "specific_costs [Eur/kW]")],
                lifetime=10,
                fixed_costs=investment_costs[("pv", "fixed_costs [Eur]")],
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
        lifetime=10,
    ),  # kWh
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
                [aggregation.typicalPeriods["house_elec_kW"]] * len(years),
                ignore_index=True,
            ),
            nominal_capacity=1.0,
        )
    },
)
es.add(house_sink)

# Electric vehicle demand
wallbox_sink = cmp.Sink(
    label="Electric Vehicle",
    inputs={
        bus_el: Flow(
            fix=pd.concat(
                [aggregation.typicalPeriods["ev_charge_kW"]] * len(years),
                ignore_index=True,
            ),
            nominal_capacity=1.0,
        )
    },
)
es.add(wallbox_sink)

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
                lifetime=20,
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
                [aggregation.typicalPeriods["house_heat_kW"]] * len(years),
                ignore_index=True,
            ),
            nominal_capacity=5.0,
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
flow = results.flow
soc = results.storage_content
soc.name = "Battery SOC [kWh]"
investments = results.invest.rename(
    columns={
        c: c[0].label for c in results.invest.columns if isinstance(c, tuple)
    },
)

print("Energy Balance")
print(flow.sum())
print("")
print("Investment")
print(investments.squeeze())

investments.squeeze().plot(kind="bar")
""" 
day = 186  # day of the year
n = 2  # number of days to plot
flow = flow[day * 24 * 6 : day * 24 * 6 + n * 24 * 6]
soc = soc[day * 24 * 6 : day * 24 * 6 + 48 * 6]

supply = flow[[c for c in flow.columns if c[1].label == "electricity"]]
supply = supply.droplevel(1, axis=1)
supply.rename(columns={c: c.label for c in supply.columns}, inplace=True)
demand = flow[[c for c in flow.columns if c[0].label == "electricity"]]
demand = demand.droplevel(0, axis=1)
demand.rename(columns={c: c.label for c in demand.columns}, inplace=True)

# A plot from GPT :-)
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
# Top: Electricity bus — supply vs. demand (negative stack), net balance
sup_handles = axes[0].stackplot(
    supply.index,
    *[supply[c] for c in supply.columns],
    labels=list(supply.columns),
    alpha=0.8,
)
dem_handles = axes[0].stackplot(
    demand.index,
    *[-demand[c] for c in demand.columns],
    labels=list(demand.columns),
    alpha=0.7,
)

net = supply.sum(axis=1) - demand.sum(axis=1)
(net_line,) = axes[0].plot(
    net.index, net, color="k", linewidth=1.3, label="Net balance"
)
axes[0].axhline(0, color="gray", linestyle="--", linewidth=0.8)
axes[0].set_ylabel("Power [kW]")
axes[0].set_title("Electricity bus: supply (positive) vs demand (negative)")

# Legend combining both stacks and net line
handles = sup_handles + dem_handles + [net_line]
labels = list(supply.columns) + list(demand.columns) + ["Net balance"]
axes[0].legend(handles, labels, ncol=2, fontsize=9, loc="upper left")

# Optional: overlay SOC on right axis
if soc is not None:
    ax2 = axes[0].twinx()
    ax2.plot(
        soc.index, soc, color="tab:purple", linewidth=1.2, label="Battery SOC"
    )
    ax2.set_ylabel("Energy [kWh]")
    ax2.legend(loc="upper right")

# Bottom: Heat — HP output vs heat demand and unmet heat area
hp_heat = flow[[c for c in flow.columns if c[0].label == "heat"]].squeeze()
heat_dem = flow[[c for c in flow.columns if c[1].label == "heat"]].squeeze()

axes[1].plot(hp_heat.index, hp_heat, label="HP heat output", linewidth=2)
axes[1].plot(
    heat_dem.index, heat_dem, label="Heat demand", linewidth=2, linestyle="--"
)
axes[1].fill_between(
    heat_dem.index,
    hp_heat,
    heat_dem,
    where=(heat_dem > hp_heat),
    color="tab:red",
    alpha=0.2,
    label="Unmet heat",
)
axes[1].set_ylabel("Heat [kW]")
axes[1].set_title("Heat bus")
axes[1].legend(loc="upper left")
axes[1].set_xlabel("Time")

plt.tight_layout()
plt.show()
"""
