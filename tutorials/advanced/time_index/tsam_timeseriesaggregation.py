# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

import logging
import warnings
from pathlib import Path
import tsam.timeseriesaggregation as tsam

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
from oemof import solph

warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

file_path = Path(__file__).parent

df = pd.read_csv(
    Path(file_path, "energy.csv"),
)
df["time"] = pd.to_datetime(df["Unix Epoch"], unit="s")
# time als Index setzen
df = df.set_index("time")
df = df.drop(columns=["Unix Epoch"])
print(df)

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
# Clustering of Input time-series with TSAM
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
tindex_agg = pd.date_range(
    "2022-01-01", periods=typical_periods * hours_per_period, freq="H"
)
es = EnergySystem(
    timeindex=tindex_agg,
    timeincrement=[1] * len(tindex_agg),
    periods=[tindex_agg],
    tsa_parameters=[
        {
            "timesteps_per_period": aggregation.hoursPerPeriod,
            "order": aggregation.clusterOrder,
            "timeindex": aggregation.timeIndex,
        }
    ],
    infer_last_interval=False,
)

bus_el = Bus(label="electricity")
bus_heat = Bus(label="heat")
es.add(bus_el, bus_heat)

pv = cmp.Source(
    label="PV",
    outputs={
        bus_el: Flow(
            fix=pv_profile,
            nominal_capacity=Investment(ep_costs=400, lifetime=20, maximum=10),
        )
    },
)
es.add(pv)

# Battery
battery = cmp.GenericStorage(
    label="Battery",
    inputs={bus_el: Flow()},
    outputs={bus_el: Flow()},
    nominal_capacity=Investment(ep_costs=500, lifetime=20),  # kWh
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
            fix=aggregation.typicalPeriods["house_elec_kW"],
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
            fix=aggregation.typicalPeriods["ev_charge_kW"],
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
        bus_heat: Flow(nominal_capacity=Investment(ep_costs=500, lifetime=20))
    },
    conversion_factors={bus_heat: aggregation.typicalPeriods["cop_hp"]},
)
es.add(hp)

# Heat demand
heat_sink = cmp.Sink(
    label="Heat demand",
    inputs={
        bus_heat: Flow(
            fix=aggregation.typicalPeriods["house_heat_kW"],
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
m.solve(solver="cbc", solve_kwargs={"tee": False})

# Create Results
results = solph.processing.results(m)

results_bus_el = solph.views.node(results, bus_el)
results_bus_heat = solph.views.node(results, bus_heat)

my_results = results_bus_el["period_scalars"]

# installed capacity of pv-system in kW
pv_invest_kW = results[(pv, bus_el)]["period_scalars"]["invest"]

# installed capacity of storage in kWh
storage_invest_kWh = results[(battery, None)]["period_scalars"]["invest"]


# installed capacity of hp in kW
hp_invest_kW = results[(hp, bus_heat)]["period_scalars"]["invest"]

investments = pd.Series(
    {
        "PV (kW)": pv_invest_kW.iloc[0],
        "Battery (kWh)": storage_invest_kWh.iloc[0],
        "HP (kW_th)": hp_invest_kW.iloc[0],
    }
)
investments.squeeze().plot(kind="bar")

day = 186  # day of the year
n = 2

# Concatenate flows:
flows = pd.concat([flow["sequences"] for flow in results.values()], axis=1)
flows.columns = list(results.keys())

soc = flows[battery, None]
flows = flows.drop(columns=[(battery, None)])

supply = flows[
    [c for c in flows.columns if getattr(c[1], "label", None) == "electricity"]
].copy()
supply.columns = [c[0].label for c in supply.columns]


demand = flows[
    [c for c in flows.columns if getattr(c[0], "label", None) == "electricity"]
].copy()
demand.columns = [c[1].label for c in demand.columns]

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


hp_heat = flows[
    [c for c in flows.columns if getattr(c[1], "label", None) == "heat"]
].copy()
hp_heat.columns = [c[0].label for c in hp_heat.columns]

heat_dem = flows[
    [c for c in flows.columns if getattr(c[0], "label", None) == "heat"]
].copy()
heat_dem.columns = [c[1].label for c in heat_dem.columns]

axes[1].plot(hp_heat.index, hp_heat, label="HP heat output", linewidth=2)
axes[1].plot(
    heat_dem.index, heat_dem, label="Heat demand", linewidth=2, linestyle="--"
)
axes[1].fill_between(
    heat_dem.index,
    hp_heat.squeeze(),
    heat_dem.squeeze(),
    where=(heat_dem.squeeze() > hp_heat.squeeze()),
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
