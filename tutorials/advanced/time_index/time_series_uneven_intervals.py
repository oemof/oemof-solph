# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

import logging
import warnings
from pathlib import Path

from create_timeseries import reshape_unevenly

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from oemof.network import graph
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

warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

file_path = Path(__file__).parent

df = prepare_input_data(minutes=60)

time_index = idx = pd.date_range(
    start="2023-01-01 00:00", end="2023-12-31 23:00", freq="h"
)

df.set_index(time_index, inplace=True)

df_neu = reshape_unevenly(df)

# PV profile
h = np.arange(len(time_index))
pv_profile = df["PV (W)"]/1000

# Electricity profile
house_elec_kw = df["electricity demand (W)"]

# Heat profile
house_heat_kw = df["heat demand (W)"]

ev_charge_kW = pd.Series(0.0, index=time_index)

# COP constant value by, but will be replaced by a temperature-depending
# profile
t_supply = 55
efficiency = 0.5
cop_hp = (t_supply + 273.15 * efficiency) / (
    t_supply - df["Air Temperature (°C)"]
)

es = EnergySystem(timeindex=time_index)

bus_el = Bus(label="electricity")
bus_heat = Bus(label="heat")
es.add(bus_el, bus_heat)

pv = cmp.Source(
    label="PV",
    outputs={
        bus_el: Flow(fix=pv_profile, nominal_capacity=Investment(ep_costs=400))
    },
)
es.add(pv)

# Battery
battery = cmp.GenericStorage(
    label="Battery",
    inputs={bus_el: Flow()},
    outputs={bus_el: Flow()},
    nominal_capacity=Investment(ep_costs=500),  # kWh
    initial_storage_level=0.5,  # 50%
    min_storage_level=0.0,
    max_storage_level=1.0,
    loss_rate=0.001,  # 0.1%/h
    inflow_conversion_factor=0.95,  # Lade-Wirkungsgrad
    outflow_conversion_factor=0.95,  # Entlade-Wirkungsgrad
)
es.add(battery)

es.add(cmp.Sink(label="Excess_el", inputs={bus_el: Flow()}))
es.add(cmp.Sink(label="Excess_heat", inputs={bus_heat: Flow()}))
es.add(
    cmp.Source(label="Shortage_el", outputs={bus_el: Flow(variable_costs=99)})
)
es.add(
    cmp.Source(
        label="Shortage_heat", outputs={bus_heat: Flow(variable_costs=99)}
    )
)

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
    outputs={bus_heat: Flow(nominal_capacity=Investment(ep_costs=500))},
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

graph.create_nx_graph(
            es, filename=Path(Path.home(), "test_graph.graphml")
        )

# Create Model and solve it
logging.info("Creating Model...")
m = Model(es)
logging.info("Solving Model...")
m.solve(solver="cbc", solve_kwargs={"tee": False})

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
