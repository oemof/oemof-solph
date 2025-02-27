# %%[imports_start]
"""
First of all, we create some input data. We use Pandas to do so and will also
import matplotlib to plot the data right away and import solph
Further for plotting we use a helper function from helpers.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import oemof.solph as solph

from helpers import plot_results



# %%[imports_end]

# %%[create_time_index_start]

time_index = pd.date_range(
    start="2025-01-01",
    end="2025-01-02",
    freq="5min",
    inclusive="both",
)

# %%[create_time_index_end]


# %%[trip_data_start]

# Define the trip demand series for the real trip scenario.
# As the demand is a power time series, it has N-1 entries
# when compared to the N entires of time axis for the energy.
ev_demand = pd.Series(0, index=time_index[:-1])

# Morning Driving: 07:00 to 08:00
driving_start_morning = pd.Timestamp("2025-01-01 07:10")
driving_end_morning = pd.Timestamp("2025-01-01 08:10")
ev_demand.loc[driving_start_morning:driving_end_morning] = 10  # kW

# Evening Driving: 17:00 to 18:00.
# Note that time points work even if they are not in the index.
driving_start_evening = pd.Timestamp("2025-01-01 16:13:37")
driving_end_evening = pd.Timestamp("2025-01-01 17:45:11")
ev_demand.loc[driving_start_evening:driving_end_evening] = 9  # kW

plt.figure()
plt.title("Driving pattern")
plt.plot(ev_demand)
plt.ylabel("Power (kW)")
plt.gcf().autofmt_xdate()
# %%[trip_data_end]

# %%[energysystem_and_bus_start]
"""
Now, let's create an energy system model of the electric vehicle that
follows the driving pattern. It uses the same time index defined above
and consists of a Battery (partly charged in the beginning)
and an electricity demand.
"""



energy_system = solph.EnergySystem(
    timeindex=time_index,
    infer_last_interval=False,
)

bus_car = solph.Bus(label="Car Electricity")

energy_system.add(bus_car)


# %%[energysystem_and_bus_end]

# %%[car_start]
# As we have a demand time series which is actually in kW, we use a common
# "hack" here: We set the nominal capacity to 1 (kW), so that
# multiplication by the time series will just yield the correct result.
demand_driving = solph.components.Sink(
    label="Driving Demand",
    inputs={bus_car: solph.Flow(nominal_capacity=1, fix=ev_demand)},
)

energy_system.add(demand_driving) 



# We define a "storage revenue" (negative costs) for the last time step,
# so that energy inside the storage in the last time step is worth
# something.
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
energy_system.add(car_battery)
# %%[car_end]





# %%[AC_30ct_charging_start]
"""
Now, let's assume the car battery can be charged at home. Unfortunately, there
is only a power socket available, limiting the charging process to 16 A at
230 V. This, of course, can only happen while the car is present.
"""



car_at_home = pd.Series(1, index=time_index[:-1])
car_at_home.loc[driving_start_morning:driving_end_evening] = 0

# To be able to load the battery a electric source e.g. electric grid is
# necessary. We set the maximum use to 1 if the car is present, while it
# is 0 between the morning start and the evening arrival back home.
# While the car itself can potentially charge with at a higher power,
# we just add an AC source with 16 A at 230 V.
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

energy_system.add(charger230V)

# %%[AC_30ct_charging_end]


# %%[solve_and_plot_start]
"""
Solve the model and show results
"""



model = solph.Model(energy_system)
model.solve(solve_kwargs={"tee": False})
results = solph.processing.results(model)

    
plot_results(results=results, plot_title="Domestic power socket charging")
# %%[solve_and_plot_end]

    
