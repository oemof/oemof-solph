# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

import logging
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from create_timeseries import reshape_unevenly
from matplotlib import pyplot as plt
from oemof.network import graph
from oemof.tools import debugging
from oemof.tools import logger
from shared_uk import prepare_input_data

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

minutes = 10
year = 2023

df = prepare_input_data(minutes=minutes)

time_index = pd.date_range(
    start=f"{year}-01-01 00:00",
    end=f"{year}-12-31 23:59",
    freq=f"{minutes}min",
)
start_time = datetime.strptime(f"{year}-01-01 00:00", "%Y-%m-%d %H:%M")

df.set_index(time_index, inplace=True)

df_neu = reshape_unevenly(df)
intervals = pd.Series(df.index.diff().seconds / 3600, index=df.index)
intervals.iloc[0] = (start_time - intervals.index[-1]).seconds / 3600

intervals_neu = pd.Series(df_neu.index.diff().seconds / 3600, index=df_neu.index)
intervals_neu.iloc[0] = (start_time - intervals_neu.index[-1]).seconds / 3600

print((df_neu.mul(intervals_neu, axis=0).sum()))
print((df.mul(intervals, axis=0).sum()))

# PV profile
h = np.arange(len(time_index))
pv_profile = df["PV (W)"] / 1000

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

es = EnergySystem(timeindex=df.index)

# Buses
bus_el = Bus(label="electricity")
bus_heat = Bus(label="heat")
es.add(bus_el, bus_heat)

# Sources
es.add(
    cmp.Source(
        label="PV",
        outputs={bus_el: Flow(fix=pv_profile, nominal_capacity=400)},
    )
)
es.add(
    cmp.Source(label="Shortage_el", outputs={bus_el: Flow(variable_costs=9)})
)
es.add(
    cmp.Source(
        label="Shortage_heat", outputs={bus_heat: Flow(variable_costs=9)}
    )
)
es.add(
    cmp.Source(
        label="Grid import", outputs={bus_el: Flow(variable_costs=0.30)}
    )
)


# Battery
es.add(
    cmp.GenericStorage(
        label="Battery",
        inputs={bus_el: Flow()},
        outputs={bus_el: Flow()},
        nominal_capacity=50000,  # kWh
        initial_storage_level=0.5,  # 50%
        min_storage_level=0.0,
        max_storage_level=1.0,
        loss_rate=0.001,  # 0.1%/h
        inflow_conversion_factor=0.95,  # Lade-Wirkungsgrad
        outflow_conversion_factor=0.95,  # Entlade-Wirkungsgrad
    )
)

# Sinks
es.add(cmp.Sink(label="Excess_el", inputs={bus_el: Flow()}))
es.add(cmp.Sink(label="Excess_heat", inputs={bus_heat: Flow()}))
es.add(
    cmp.Sink(
        label="Heat demand",
        inputs={bus_heat: Flow(fix=house_elec_kw, nominal_capacity=5.0)},
    )
)
es.add(
    cmp.Sink(
        label="Electricity demand",
        inputs={bus_el: Flow(fix=house_elec_kw, nominal_capacity=1.0)},
    )
)
es.add(
    cmp.Sink(
        label="Electric Vehicle",
        inputs={bus_el: Flow(fix=ev_charge_kW, nominal_capacity=1.0)},
    )
)
es.add(
    cmp.Sink(label="Grid Feed-in", inputs={bus_el: Flow(variable_costs=-0.08)})
)

# Heat Pump
es.add(
    cmp.Converter(
        label="Heat pump",
        inputs={bus_el: Flow()},
        outputs={bus_heat: Flow(nominal_capacity=Investment(ep_costs=500))},
        conversion_factors={bus_heat: cop_hp},
    )
)

graph.create_nx_graph(es, filename=Path(Path.home(), "test_graph.graphml"))

# Create Model and solve it
logging.info("Creating Model...")
m = Model(es)
logging.info("Solving Model...")
m.solve(solver="cbc", solve_kwargs={"tee": False})

# Create Results
results = Results(m)

flow = results["flow"]
intervals = pd.Series(flow.index.diff().seconds / 3600, index=flow.index)
intervals.iloc[0] = (start_time - intervals.index[-1]).seconds / 3600

print(flow.mul(intervals, axis=0).sum())
