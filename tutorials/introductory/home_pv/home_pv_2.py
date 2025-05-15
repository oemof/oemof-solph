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
    outputs={el_bus: solph.Flow(variable_costs=0.3)},
    balanced=False,
)

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
            max=input_data["pv yield (kW/kW)"],
        )
    },
)

grid.inputs[el_bus] = solph.Flow(variable_costs=-0.06)

energy_system.add(pv_system)
# %%[graph_plotting]
plt.figure()
graph = create_nx_graph(energy_system)
nx.drawing.nx_pydot.write_dot(graph, "home_pv_graph_2.dot")
nx.draw(graph, with_labels=True, font_size=8)
# %%[model_optimisation]
model = solph.Model(energy_system)

model.solve(solver="cbc", solve_kwargs={"tee": True})
results = solph.processing.results(model)
meta_results = solph.processing.meta_results(model)

# %%[results]

pv_annuity = pv_size * pv_specific_costs / pv_lifetime
el_costs = 0.3 * results[(grid, el_bus)]["sequences"]["flow"].sum()
el_revenue = 0.1 * results[(el_bus, grid)]["sequences"]["flow"].sum()

tce = pv_annuity + meta_results["objective"]

print(
    f"The annual costs for grid electricity are {el_costs:.2f} €."
)
print(f"The annual revenue from feed-in is {el_revenue:.2f} €.")
print(f"The annuity for the PV system is {pv_annuity:.2f} €.")
print(f"The total annual costs are {tce:.2f} €.")


electricity_fows = solph.views.node(results, "electricity")["sequences"]
electricity_fows.plot(drawstyle="steps")
plt.ylabel("Power (kW)")
plt.show()
