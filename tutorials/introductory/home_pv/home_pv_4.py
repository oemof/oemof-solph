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
from oemof.network.graph import create_nx_graph
import pandas as pd

from oemof import solph

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

el_bus = solph.Bus(label="electricity")

demand = solph.components.Sink(
    label="demand",
    inputs={
        el_bus: solph.Flow(
            nominal_capacity=1,
            fix=input_data["electricity demand (kW)"],
        )
    },
)

energy_system.add(el_bus, demand)

grid = solph.Bus(
    label="grid",
    inputs={el_bus: solph.Flow(variable_costs=-0.06)},
    outputs={el_bus: solph.Flow(variable_costs=0.3)},
    balanced=False,
)

energy_system.add(grid)

pv_specific_costs = 1500  # €/kW
pv_lifetime = 20  # years
pv_epc = pv_specific_costs / pv_lifetime

pv_system = solph.components.Source(
    label="PV",
    outputs={
        el_bus: solph.Flow(
            nominal_capacity=solph.Investment(ep_costs=pv_epc, maximum=10),
            max=input_data["pv yield (kW/kW)"],
        )
    },
)

energy_system.add(pv_system)

# %%[battery]

battery_specific_costs = 1000  # €/kW
battery_lifetime = 10  # years
battery_epc = battery_specific_costs / battery_lifetime
battery_size = 2  # kWh

battery = solph.components.GenericStorage(
    label="Battery",
    nominal_capacity=battery_size,
    inputs={el_bus: solph.Flow()},
    outputs={el_bus: solph.Flow()},
    inflow_conversion_factor=0.9,
    loss_rate=0.01,
)

energy_system.add(battery)

# %%[graph_plotting]
plt.figure()
graph = create_nx_graph(energy_system)
nx.drawing.nx_pydot.write_dot(graph, "home_pv_graph_4.dot")
nx.draw(graph, with_labels=True, font_size=8)
# %%[model_optimisation]
model = solph.Model(energy_system)

model.solve(solver="cbc", solve_kwargs={"tee": True})
results = solph.processing.results(model)
meta_results = solph.processing.meta_results(model)

# %%[results]

pv_size = results[(pv_system, el_bus)]["scalars"]["invest"]

battery_annuity = battery_epc * battery_size
pv_annuity = pv_epc * results[(pv_system, el_bus)]["scalars"]["invest"]
el_costs = 0.3 * results[(grid, el_bus)]["sequences"]["flow"].sum()
el_revenue = 0.1 * results[(el_bus, grid)]["sequences"]["flow"].sum()

tce = meta_results["objective"] + battery_annuity

print(f"The optimal PV size is {pv_size:.2f} kW.")

print(f"The annual costs for grid electricity are {el_costs:.2f} €.")
print(f"The annual revenue from feed-in is {el_revenue:.2f} €.")
print(f"The annuity for the PV system is {pv_annuity:.2f} €.")
print(f"The annuity for the battery is {battery_annuity:.2f} €.")
print(f"The total annual costs are {tce:.2f} €.")


electricity_fows = solph.views.node(results, "electricity")["sequences"]
electricity_fows.plot(drawstyle="steps")
plt.ylabel("Power (kW)")
plt.show()
