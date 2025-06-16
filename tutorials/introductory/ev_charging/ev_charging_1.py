# %%[imports_start]

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from oemof.network.graph import create_nx_graph
import pandas as pd
from helpers import plot_results

# %%[imports_end]
# %%[create_time_index_set_up_energysystem_start]
import oemof.solph as solph

time_index = pd.date_range(
    start="2025-01-01",
    end="2025-01-02",
    freq="5min",
    inclusive="both",
)

ev_energy_system = solph.EnergySystem(
    timeindex=time_index,
    infer_last_interval=False,
)
# %%[create_time_index_set_up_energysystem_end]
# %%[trip_data_start]
ev_demand = pd.Series(0, index=time_index[:-1])

driving_start_morning = pd.Timestamp("2025-01-01 07:10")
driving_end_morning = pd.Timestamp("2025-01-01 08:10")
ev_demand.loc[driving_start_morning:driving_end_morning] = 10  # kW


driving_start_evening = pd.Timestamp("2025-01-01 16:13:37")
driving_end_evening = pd.Timestamp("2025-01-01 17:45:11")
ev_demand.loc[driving_start_evening:driving_end_evening] = 9  # kW
# %%[trip_data_end]
## %%[plot_trip_data_start]
plt.figure()
# plt.style.use("dark_background")
plt.title("Driving pattern")
plt.plot(ev_demand)
plt.ylabel("Power (kW)")
plt.gcf().autofmt_xdate()
## %%[plot_trip_data_end]
# %%[energysystem_and_bus_start]
bus_car = solph.Bus(label="Car Electricity")

ev_energy_system.add(bus_car)
# %%[energysystem_and_bus_end]
# %%[car_start]
demand_driving = solph.components.Sink(
    label="Driving Demand",
    inputs={bus_car: solph.Flow(nominal_capacity=1, fix=ev_demand)},
)

ev_energy_system.add(demand_driving)

storage_revenue = np.zeros(len(time_index) - 1)
storage_revenue[-1] = -0.6  # 60 ct/kWh in the last time step

car_battery = solph.components.GenericStorage(
    label="Car Battery",
    nominal_capacity=50,  # kWh
    inputs={bus_car: solph.Flow()},
    outputs={bus_car: solph.Flow()},
    initial_storage_level=1,  # full in the beginning
    loss_rate=0.001,  # 0.1 % / hr
    inflow_conversion_factor=0.9,  # 90 % charging efficiency
    balanced=False,  # True: content at beginning and end need to be equal
    storage_costs=storage_revenue,  # Only has an effect on charging.
)

ev_energy_system.add(car_battery)
# %%[car_end]
# %%[graph_start]
plt.figure()
graph = create_nx_graph(ev_energy_system)
nx.drawing.nx_pydot.write_dot(graph, "ev_carging_graph_1.dot")
nx.draw(graph, with_labels=True, font_size=8)

# %%[graph_end]
# %%[solve_start]
model = solph.Model(ev_energy_system)
model.solve(solver="cbc", solve_kwargs={"tee": True})
results = solph.processing.results(model)
# %%[solve_end]
# %%[plot_results_start]
plot_results(
    results=results, plot_title="Driving demand only", dark_mode=False
)
plt.show()
# %%[plot_results_end]
