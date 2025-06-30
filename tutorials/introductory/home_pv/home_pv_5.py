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

grid = solph.Bus(
    label="grid",
    inputs={ac_bus: solph.Flow(variable_costs=-0.06)},
    outputs={ac_bus: solph.Flow(variable_costs=0.3)},
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
nx.drawing.nx_pydot.write_dot(graph, "home_pv_graph_5.dot")
nx.draw(graph, with_labels=True, font_size=8)
# %%[model_optimisation]
model = solph.Model(energy_system)

model.solve(solver="cbc", solve_kwargs={"tee": True})
results = solph.processing.results(model)
meta_results = solph.processing.meta_results(model)

# %%[results]

pv_size = results[(pv_panels, dc_bus)]["scalars"]["invest"]
pv_annuity = pv_epc * pv_size

inverter_size = results[(dc_bus, inverter)]["scalars"]["invest"]
inverter_annuity = inverter_epc * inverter_size

battery_size = results[(battery, None)]["scalars"]["invest"]
battery_annuity = battery_epc * battery_size

annual_grid_supply = results[(grid, ac_bus)]["sequences"]["flow"].sum()
el_costs = 0.3 * annual_grid_supply
el_revenue = 0.1 * results[(ac_bus, grid)]["sequences"]["flow"].sum()

tce = meta_results["objective"]

print(f"The optimal PV size is {pv_size:.2f} kW.")
print(f"The optimal inverter size is {inverter_size:.2f} kW.")
print(f"The optimal battery size is {battery_size:.2f} kWh.")

print(f"The annual costs for grid electricity are {el_costs:.2f} €.")
print(f"The annual revenue from feed-in is {el_revenue:.2f} €.")
print(f"The annuity for the PV system is {pv_annuity:.2f} €.")
print(f"The annuity for the battery is {battery_annuity:.2f} €.")
print(f"The total annual costs are {tce:.2f} €.")

annual_demand = input_data["electricity demand (kW)"].sum()

print(
    f"Autarky is 1 - {annual_grid_supply:.2f} kWh / {annual_demand:.2f} kWh"
    + f" = {100 - 100 * annual_grid_supply / annual_demand:.2f} %."
)

electricity_fows = solph.views.node(results, "electricity")["sequences"]

baseline = np.zeros(len(electricity_fows))

plt.figure()

mode = "light"
# mode = "dark"
if mode == "dark":
    plt.style.use("dark_background")

plt.fill_between(
    electricity_fows.index,
    baseline,
    baseline + electricity_fows[(("grid", "electricity"), "flow")],
    step="pre",
    label="Grid supply",
)

baseline += electricity_fows[(("grid", "electricity"), "flow")]

plt.fill_between(
    electricity_fows.index,
    baseline,
    baseline + electricity_fows[(("PV", "electricity"), "flow")],
    step="pre",
    label="PV supply",
)

baseline += electricity_fows[(("PV", "electricity"), "flow")]

plt.fill_between(
    electricity_fows.index,
    baseline,
    baseline + electricity_fows[(("Battery", "electricity"), "flow")],
    step="pre",
    label="Battery supply",
)

plt.step(
    electricity_fows.index,
    electricity_fows[(("electricity", "demand"), "flow")],
    "-",
    color="darkgrey",
    label="Electricity demand",
)

plt.step(
    electricity_fows.index,
    electricity_fows[(("electricity", "demand"), "flow")]
    + electricity_fows[(("electricity", "Battery"), "flow")],
    "--",
    color="darkgrey",
    label="Battery charging",
)

plt.step(
    electricity_fows.index,
    electricity_fows[(("electricity", "demand"), "flow")]
    + electricity_fows[(("electricity", "Battery"), "flow")]
    + electricity_fows[(("electricity", "grid"), "flow")],
    ":",
    color="darkgrey",
    label="Feed-In",
)

plt.legend()
plt.ylabel("Power (kW)")
plt.xlim(pd.Timestamp("2020-02-21 00:00"), pd.Timestamp("2020-02-28 00:00"))
plt.gcf().autofmt_xdate()

plt.savefig(f"home_pv_result-4_{mode}.svg")

plt.show()
