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


plot_results(results=results, plot_title="Home and work charging")
# %%[solve_and_plot_end]

# %%[DC_charging_fixed]
"""
Charging and discharging at the same time is almost always a sign that
something is not moddeled accurately in the energy system.
To avoid the energy from looping in the battery, we introduce marginal costs
to battery charging. This is a way to model cyclic aging of the battery.
As we can recharge now, we also set the "balanced" argument to the default
value and drop the (optional) incentive to recharge.
"""


def add_balanced_battery(energy_system, bus_car):
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


es, bus_car = create_base_system()
add_balanced_battery(es, bus_car)
add_domestic_socket_charging(es, bus_car)
add_11kW_charging(es, bus_car)
solve_and_plot("Home and work charging (fixed)")

# %%[AC_discharging]
"""
Now, we add an option to use the car battery bidirectionally.
The car can be charged at work and used at home to save 30 ct/kWh.
"""


def add_domestic_socket_discharging(energy_system, bus_car):
    car_at_home = pd.Series(1, index=time_index[:-1])
    car_at_home.loc[driving_start_morning:driving_end_evening] = 0

    # Same as above, but electricity is cheaper every other step.
    # Thus, battery is only charged these steps.
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

    energy_system.add(discharger230V)


es, bus_car = create_base_system()
add_balanced_battery(es, bus_car)
add_domestic_socket_charging(es, bus_car)
add_domestic_socket_discharging(es, bus_car)
add_11kW_charging(es, bus_car)
solve_and_plot("Bidirectional use (constant costs)")

# %%[AC_variable_costs]
"""
Now the energy system stays the same. But dynamic prices
are avaiable at home, so the loading and unloading if the
price is low or the gain is high."""

# assuming the prices are low in the night and early morning
# # (until 8 a.m. and after 4 p.m) and high at later morning,
# midday and afternoon (between 6 a.m. and 4 p.m.)

dynamic_price = pd.Series(0.5, index=time_index[:-1])
dynamic_price.loc[: pd.Timestamp("2025-01-01 06:00")] = 0.05
dynamic_price.loc[
    pd.Timestamp("2025-01-01 06:00") : pd.Timestamp("2025-01-01 10:00")
] = 0.5
dynamic_price.loc[pd.Timestamp("2025-01-01 16:00") :] = 0.7


def add_domestic_socket_variable_costs(energy_system, bus_car, dynamic_price):
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


es, bus_car = create_base_system()
add_balanced_battery(es, bus_car)
add_domestic_socket_variable_costs(es, bus_car, dynamic_price)
add_11kW_charging(es, bus_car)
solve_and_plot("Bidirectional use (variable costs)")

plt.show()
