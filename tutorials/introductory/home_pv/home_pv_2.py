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

# %%[input_data]

file_path = os.path.dirname(__file__)
filename = os.path.join(file_path, "pv_example_data.csv")
input_data = pd.read_csv(
    filename, index_col="timestep", parse_dates=["timestep"]
)

# %%[energy_system]

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

# %%[grid_feedin]

grid = solph.Bus(
    label="grid",
    outputs={el_bus: solph.Flow(variable_costs=0.3)},
    balanced=False,
)

grid.inputs[el_bus] = solph.Flow(variable_costs=-0.06)

# %%[add_grid]

energy_system.add(grid)

# %%[pv_system]

pv_size = 5  # kW
pv_specific_costs = 1500  # €/kW
pv_lifetime = 20  # years

pv_system = solph.components.Source(
    label="PV",
    outputs={
        el_bus: solph.Flow(
            nominal_capacity=pv_size,
            maximum=input_data["pv yield (kW/kW)"],
        )
    },
)

energy_system.add(pv_system)
# %%[graph_plotting]
plt.figure()
graph = energy_system.to_networkx()
nx.draw(graph, with_labels=True, font_size=8)
# %%[model_optimisation]
model = solph.Model(energy_system)

results = model.solve(solver="cbc", solve_kwargs={"tee": True})

# %%[results]

pv_annuity = pv_size * pv_specific_costs / pv_lifetime
annual_grid_supply = results["flow"][(grid, el_bus)].sum()
el_costs = 0.3 * annual_grid_supply

el_revenue = 0.1 * results["flow"][(el_bus, grid)].sum()

tce = pv_annuity + results["objective"]
# %%[result_plotting]

print(f"The annual costs for grid electricity are {el_costs:.2f} €.")
print(f"The annual revenue from feed-in is {el_revenue:.2f} €.")
print(f"The annuity for the PV system is {pv_annuity:.2f} €.")
print(f"The total annual costs are {tce:.2f} €.")

annual_demand = input_data["electricity demand (kW)"].sum()

print(
    f"Autarky is 1 - {annual_grid_supply:.2f} kWh / {annual_demand:.2f} kWh"
    + f" = {100 - 100 * annual_grid_supply / annual_demand:.2f} %."
)

flows = results["flow"]
baseline = np.zeros(len(flows))

plt.figure()

mode = "light"
# mode = "dark"
if mode == "dark":
    plt.style.use("dark_background")

plt.fill_between(
    flows.index,
    baseline,
    baseline + flows[("grid", "electricity")],
    step="pre",
    label="Grid supply",
)

baseline += flows[("grid", "electricity")]

plt.fill_between(
    flows.index,
    baseline,
    baseline + flows[("PV", "electricity")],
    step="pre",
    label="PV supply",
)

plt.step(
    flows.index,
    flows[("electricity", "demand")],
    "-",
    color="darkgrey",
    label="Electricity demand",
)

plt.step(
    flows.index,
    flows[("electricity", "demand")] + flows[("electricity", "grid")],
    ":",
    color="darkgrey",
    label="Feed-In",
)

plt.legend()
plt.ylabel("Power (kW)")
plt.xlim(pd.Timestamp("2020-02-21 00:00"), pd.Timestamp("2020-02-28 00:00"))
plt.gcf().autofmt_xdate()

plt.savefig(f"home_pv_result-2_{mode}.svg")

plt.show()
