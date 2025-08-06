# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Daniel Niederhöfer
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""
# %%[imports]
import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from oemof import solph
from oemof.network.graph import create_nx_graph
from oemof.solph import Results

# %%[input_data]

file_path = os.path.dirname(__file__)
filename = os.path.join(file_path, "pv_example_data.csv")
input_data = pd.read_csv(
    filename, index_col="timestep", parse_dates=["timestep"]
)

# %%[energy_system]

# parse_dates does not set the freq attribute.
# However, we want to use it for the EnergySystem.
input_data.index.freq = pd.infer_freq(input_data.index)

energy_system = solph.EnergySystem(
    timeindex=input_data.index,
    infer_last_interval=True,
)

# %%[dispatch_model]

ac_bus = solph.Bus(label="electricity")

demand = solph.components.Sink(
    label="demand",
    inputs={
        ac_bus: solph.Flow(
            nominal_capacity=1,
            fix=input_data["electricity demand (kW)"],
        )
    },
)

energy_system.add(ac_bus, demand)

# %%[grid]

grid = solph.Bus(
    label="grid",
    inputs={ac_bus: solph.Flow(variable_costs=-0.06)},
    outputs={
        ac_bus: solph.Flow(
            nominal_capacity=42,
            full_load_time_max=5,
            variable_costs=0.3,
        )
    },
    balanced=False,
)

energy_system.add(grid)

# %%[pv_system]
dc_bus = solph.Bus(label="DC")

pv_specific_costs = 1200  # €/kW
pv_lifetime = 20  # years
pv_epc = pv_specific_costs / pv_lifetime

pv_panels = solph.components.Source(
    label="PV",
    outputs={
        dc_bus: solph.Flow(
            nominal_capacity=solph.Investment(ep_costs=pv_epc, maximum=10),
            max=input_data["pv yield (kW/kW)"] / 0.95,
        )
    },
)

inverter_specific_costs = 300  # €/kW
inverter_lifetime = 20  # years
inverter_epc = inverter_specific_costs / inverter_lifetime

inverter = solph.components.Converter(
    label="inverter",
    inputs={
        dc_bus: solph.Flow(
            nominal_capacity=solph.Investment(ep_costs=inverter_epc)
        )
    },
    outputs={ac_bus: solph.Flow()},
    conversion_factors={ac_bus: 0.95},
)

energy_system.add(dc_bus, pv_panels, inverter)

# %%[battery]
battery_specific_costs = 750  # €/kW
battery_lifetime = 20  # years
battery_epc = battery_specific_costs / battery_lifetime
battery_size = solph.Investment(ep_costs=battery_epc)

battery = solph.components.GenericStorage(
    label="Battery",
    nominal_capacity=battery_size,
    inputs={ac_bus: solph.Flow()},
    outputs={ac_bus: solph.Flow()},
    inflow_conversion_factor=0.9,
    loss_rate=0.01,
)

energy_system.add(battery)

# %%[graph_plotting]
plt.figure()
graph = create_nx_graph(energy_system)
nx.drawing.nx_pydot.write_dot(graph, "home_pv_graph_6.dot")
nx.draw(graph, with_labels=True, font_size=8)
# %%[model_optimisation]
model = solph.Model(energy_system)

model.solve(solver="gurobi", solve_kwargs={"tee": False})
results = solph.processing.results(model)
meta_results = solph.processing.meta_results(model)

new_results = Results(model)
# %%
keys = new_results.keys()

print("---------------------------------------------")
print("Hier findet sich die Ausgabe nach dem Solve")
print("---------------------------------------------")
print("Das sind die keys, welche man für die Results nutzen kann: ")
print(keys)

# %%

# opex = new_results.calc_opex()
# print(opex)

opex = new_results.to_df("opex")
# print(opex)
