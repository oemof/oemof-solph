# %%[imports_start]
"""
First of all, we create some input data. We use Pandas to do so and will also
import matplotlib to plot the data right away and import solph
Further for plotting we use a helper function from helpers.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from helpers import plot_results

import oemof.solph as solph

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


"""
Charging and discharging at the same time is almost always a sign that
something is not moddeled accurately in the energy system.
To avoid the energy from looping in the battery, we introduce marginal costs
to battery charging. This is a way to model cyclic aging of the battery.
As we can recharge now, we also set the "balanced" argument to the default
value and drop the (optional) incentive to recharge.
"""
# We define a "storage revenue" (negative costs) for the last time step,
# so that energy inside the storage in the last time step is worth
# something.
storage_revenue = np.zeros(len(time_index) - 1)
storage_revenue[-1] = -0.6  # 60 ct/kWh in the last time step

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

energy_system.add(car_battery)
# %%[car_end]


# %%[AC_dynamic_price_charging_discharging_start]
"""
Now the energy system stays the same. But dynamic prices
are avaiable at home, so the loading and unloading if the
price is low or the gain is high."""


car_at_home = pd.Series(1, index=time_index[:-1])
car_at_home.loc[driving_start_morning:driving_end_evening] = 0

# assuming the prices are low in the night and early morning
# # (until 8 a.m. and after 4 p.m) and high at later morning,
# midday and afternoon (between 6 a.m. and 4 p.m.)

dynamic_price = pd.Series(0.5, index=time_index[:-1])
dynamic_price.loc[: pd.Timestamp("2025-01-01 06:00")] = 0.05
dynamic_price.loc[
    pd.Timestamp("2025-01-01 06:00") : pd.Timestamp("2025-01-01 10:00")
] = 0.5
dynamic_price.loc[pd.Timestamp("2025-01-01 16:00") :] = 0.7


car_at_home = pd.Series(1, index=time_index[:-1])
car_at_home.loc[driving_start_morning:driving_end_evening] = 0

# use the configuration as before but use the dynamic prices
charger230V = solph.components.Source(
    label="230V AC",
    outputs={
        bus_car: solph.Flow(
            nominal_capacity=3.68,  # 230 V * 16 A = 3.68 kW
            variable_costs=dynamic_price,
            max=car_at_home,
        )
    },
)

# use the configuration as before but use the dynamic prices
# as gain
discharger230V = solph.components.Sink(
    label="230V AC discharge",
    inputs={
        bus_car: solph.Flow(
            nominal_capacity=3.68,  # 230 V * 16 A = 3.68 kW
            variable_costs=-dynamic_price,
            max=car_at_home,
        )
    },
)

energy_system.add(charger230V, discharger230V)


# %%[AC_dynamic_price_charging_discharging_end]


# %%[DC_charging_start]
"""
Now, we add an 11 kW charger (free of charge) which is available at work.
This, of course, can only happen while the car is present at work.
"""


car_at_work = pd.Series(0, index=time_index[:-1])
car_at_work.loc[driving_end_morning:driving_start_evening] = 1

# variable_costs in the Flow default to 0, so it's free
charger11kW = solph.components.Source(
    label="11kW",
    outputs={
        bus_car: solph.Flow(
            nominal_capacity=11,  # 11 kW
            max=car_at_work,
        )
    },
)

energy_system.add(charger11kW)

# %%[DC_charging_end]


# %%[solve_and_plot_start]
"""
Solve the model and show results
"""

model = solph.Model(energy_system)
model.solve(solve_kwargs={"tee": False})
results = solph.processing.results(model)


plot_results(results=results, plot_title="Bidirectional use (variable costs)")
# %%[solve_and_plot_end]
