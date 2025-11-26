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
from matplotlib import pyplot as plt
from oemof.tools import debugging
from oemof.tools import logger

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

file_path = Path(__file__).parent


# Load CSV file and parse time column as datetime index
df = pd.read_csv(
    Path(file_path, "input_data.csv"),
    parse_dates=["time"],
    index_col="time",
)
print(df)
df = df.fillna(0)

# Initial time index from the input data
initial_index = df.index
print(f"Initial index length: {len(initial_index)}")

# Number of additional years to add
years = 2  # Example: add 2 more years

# Define original start and calculate one-year duration
original_start = initial_index[0]
one_year = pd.DateOffset(years=1)

# Build periods: each starts at same time in different years, ends one hour before next year
periods = []
for y in range(years + 1):  # include original year
    start = original_start + pd.DateOffset(years=y)
    end = start + one_year - pd.Timedelta(hours=1)
    periods.append(pd.date_range(start, end, freq="h"))

# Combine all periods into one long DatetimeIndex
long_time_index = pd.DatetimeIndex(np.concatenate(periods))

print(f"Total length: {len(long_time_index)}")
print("First period:", periods[0][:5], "...", periods[0][-5:])
print("Second period:", periods[1][:5], "...", periods[1][-5:])

# --- Stretch data to match new index ---
pv_profile_one_year = df["PV (W)"].values
original_len = len(pv_profile_one_year)
new_len = len(long_time_index)

repeat_factor = int(np.ceil(new_len / original_len))
pv_profile_stretched = np.tile(pv_profile_one_year, repeat_factor)[:new_len]

pv_profile = pd.Series(pv_profile_stretched, index=long_time_index)

# Dummy profiles
house_elec_kw = pd.Series(
    0.3 + 0.7 * np.random.rand(len(long_time_index)), index=long_time_index
)
house_heat_kw = pd.Series(
    0.3 + 0.7 * np.random.rand(len(long_time_index)), index=long_time_index
)
ev_charge_kW = pd.Series(0.0, index=long_time_index)
cop_hp = pd.Series(3.5, index=long_time_index)

print(pv_profile.head())
print(pv_profile.tail())


es = EnergySystem(timeindex=long_time_index, periods=periods)


bus_el = Bus(label="electricity")
bus_heat = Bus(label="heat")
es.add(bus_el, bus_heat)

pv = cmp.Source(
    label="PV",
    outputs={
        bus_el: Flow(
            fix=pv_profile,
            nominal_capacity=Investment(
                ep_costs=[400, 380, 350],
                lifetime=10,
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
        ep_costs=[800, 700, 600],
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
    inputs={bus_el: Flow(fix=house_elec_kw, nominal_capacity=1.0)},
)
es.add(house_sink)

# Electric vehicle demand
wallbox_sink = cmp.Sink(
    label="Electric Vehicle",
    inputs={bus_el: Flow(fix=ev_charge_kW, nominal_capacity=1.0)},
)
es.add(wallbox_sink)

# Heat Pump
hp = cmp.Converter(
    label="Heat pump",
    inputs={bus_el: Flow()},
    outputs={
        bus_heat: Flow(
            nominal_capacity=Investment(ep_costs=[500, 400, 300], lifetime=20)
        )
    },
    conversion_factors={bus_heat: cop_hp},
)
es.add(hp)

# Heat demand
heat_sink = cmp.Sink(
    label="Heat demand",
    inputs={bus_heat: Flow(fix=house_elec_kw, nominal_capacity=5.0)},
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

# debugging

# Check for NaN in input data
print("----------debugging------")
print("df: ", df.isna().sum())  # For original data
print("pv: ", pv_profile.isna().sum())  # For stretched profile
print("el: ", house_elec_kw.isna().sum())
print("heat: ", house_heat_kw.isna().sum())

# Check length consistency
print("Check length consistency")
print(
    len(long_time_index),
    len(pv_profile),
    len(house_elec_kw),
    len(house_heat_kw),
)


# Create Model and solve it
logging.info("Creating Model...")
m = Model(es)
logging.info("Solving Model...")
m.solve(solver="gurobi", solve_kwargs={"tee": True})

"""
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
