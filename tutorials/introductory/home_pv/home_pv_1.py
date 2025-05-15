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

# %%[plot_results]

electricity_fows = solph.views.node(results, "electricity")["sequences"]

electricity_fows.plot(drawstyle="steps")
plt.ylabel("Power (kW)")
plt.show()
