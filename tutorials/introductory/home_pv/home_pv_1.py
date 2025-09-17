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
from oemof.network.graph import create_nx_graph
import pandas as pd

from oemof import solph

# %%[input_data]

file_path = os.path.dirname(__file__)
filename = os.path.join(file_path, "pv_example_data.csv")
input_data = pd.read_csv(
    filename, index_col="timestep", parse_dates=["timestep"]
)

input_data.plot(drawstyle="steps")
plt.xlim(pd.Timestamp("2020-03-01 00:00"), pd.Timestamp("2020-03-07 00:00"))
plt.show()

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
    outputs={el_bus: solph.Flow(variable_costs=0.3)},
    balanced=False,
)

energy_system.add(grid)
# %%[graph_plotting]
plt.figure()
graph = create_nx_graph(energy_system)
nx.drawing.nx_pydot.write_dot(graph, "home_pv_graph_1.dot")
nx.draw(graph, with_labels=True, font_size=8)
plt.show()
# %%[model_optimisation]
model = solph.Model(energy_system)

model.solve(solver="cbc", solve_kwargs={"tee": True})
results = solph.processing.results(model)
meta_results = solph.processing.meta_results(model)

# %%[results]

tce = meta_results["objective"]
print(f"The total annual costs are {tce:.2f} €.")
el_costs = 0.3 * results[(grid, el_bus)]["sequences"]["flow"].sum()
print(f"The annual costs for grid electricity are {el_costs:.2f} €.")

electricity_fows = solph.views.node(results, "electricity")["sequences"]

baseline = np.zeros(len(electricity_fows))

mode = "light"
# mode = "dark"
if mode == "dark":
    plt.style.use("dark_background")

plt.fill_between(
    electricity_fows.index,
    baseline,
    electricity_fows[(("grid", "electricity"), "flow")],
    step="pre",
    label="Grid supply",
)

plt.step(
    electricity_fows.index,
    electricity_fows[(("electricity", "demand"), "flow")],
    "-",
    color="darkgrey",
    label="Electricity demand",
)
plt.legend()
plt.ylabel("Power (kW)")
plt.xlim(pd.Timestamp("2020-01-01 00:00"), pd.Timestamp("2020-01-07 00:00"))
plt.gcf().autofmt_xdate()

plt.savefig(f"home_pv_result-1_{mode}.svg")

plt.show()
