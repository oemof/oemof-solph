# %%[imports_start]

import matplotlib.pyplot as plt
import networkx as nx
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
# %%[car_end]
# %%[car_battery_start]
car_battery = solph.components.GenericStorage(
    label="Car Battery",
    nominal_capacity=50,
    inputs={bus_car: solph.Flow(variable_costs=0.1)},
    outputs={bus_car: solph.Flow()},
    loss_rate=0.001,
    inflow_conversion_factor=0.9,
    balanced=True,  # this is the default: SOC(T=0) = SOC(T=T_max)
    min_storage_level=0.1,  # 10 % as reserve
)

ev_energy_system.add(car_battery)
# %%[car_battery_end]


# %%[AC_30ct_charging_start]
car_at_home = pd.Series(1, index=time_index[:-1])
car_at_home.loc[driving_start_morning:driving_end_evening] = 0

charger230V = solph.components.Source(
    label="230V AC",
    outputs={
        bus_car: solph.Flow(
            nominal_capacity=3.68,  # 230 V * 16 A = 3.68 kW
            variable_costs=0.3,  # 30 ct/kWh
            max=car_at_home,
        )
    },
)

ev_energy_system.add(charger230V)
# %%[AC_30ct_charging_end]


# %%[DC_charging_start]
car_at_work = pd.Series(0, index=time_index[:-1])
car_at_work.loc[driving_end_morning:driving_start_evening] = 1

charger11kW = solph.components.Source(
    label="11kW",
    outputs={
        bus_car: solph.Flow(
            nominal_capacity=11,  # 11 kW
            max=car_at_work,
        )
    },
)

ev_energy_system.add(charger11kW)
# %%[DC_charging_end]


# %%[AC_discharging_start]
discharger230V = solph.components.Sink(
    label="230V AC discharge",
    inputs={
        bus_car: solph.Flow(
            nominal_capacity=3.68,  # 230 V * 16 A = 3.68 kW
            variable_costs=-0.3,
            max=car_at_home,
        )
    },
)

ev_energy_system.add(discharger230V)
# %%[AC_discharging_end]
# %%[graph_start]
plt.figure()
graph = create_nx_graph(ev_energy_system)
nx.drawing.nx_pydot.write_dot(graph, "ev_carging_graph_4.dot")
nx.draw(graph, with_labels=True, font_size=8)
# %%[graph_end]
# %%[solve_start]
# %%[solve_and_plot_start]
model = solph.Model(ev_energy_system)
model.solve(solver="cbc", solve_kwargs={"tee": False})
results = solph.processing.results(model)


plot_results(results=results, plot_title="Bidirectional use constant costs")
plt.show()
# %%[solve_and_plot_end]
