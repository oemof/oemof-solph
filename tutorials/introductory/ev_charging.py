# %%[imports]
"""
First of all, we create some input data. We use Pandas to do so and will also
import matplotlib to plot the data right away and import solph
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import oemof.solph as solph

# %%[trip_data]

time_index = pd.date_range(
    start="2025-01-01",
    end="2025-01-02",
    freq="5min",
    inclusive="both",
)

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
driving_start_evening = pd.Timestamp("2025-01-01 17:13:37")
driving_end_evening = pd.Timestamp("2025-01-01 18:47:11")
ev_demand.loc[driving_start_evening:driving_end_evening] = 9  # kW

plt.figure()
plt.plot(ev_demand)
plt.ylabel("Power (kW)")
plt.gcf().autofmt_xdate()

# %%[base_system]
"""
Now, let's create an energy system model of the electric vehicle that
follows the driving pattern. It uses the same time index defined above
and consists of a Battery (partly charged in the beginning)
and an electricity demand.
"""


def create_base_system():
    energy_system = solph.EnergySystem(
        timeindex=time_index,
        infer_last_interval=False,
    )

    b_el = solph.Bus(label="Car Electricity")

    energy_system.add(b_el)

    # As we have a demand time series which is actually in kW,
    # we use a common "hack" here: We set the nominal capacity to 1 (kW),
    # so that multiplication by the time series will just yield the correct result.
    demand_driving = solph.components.Sink(
        label="Driving Demand",
        inputs={b_el: solph.Flow(nominal_capacity=1, fix=ev_demand)},
    )

    energy_system.add(demand_driving)

    # We define a "storage revenue" (negative costs) for the last time step,
    # so that energy inside the storage in the last time step is worth
    # something.
    storage_revenue = np.zeros(len(time_index) - 1)
    storage_revenue[-1] = -0.6  # 60ct/kWh in the last time step

    car_battery = solph.components.GenericStorage(
        label="Car Battery",
        nominal_capacity=50,  # kWh
        inputs={b_el: solph.Flow()},
        outputs={b_el: solph.Flow()},
        initial_storage_level=0.75,  # 75 % full in the beginning
        loss_rate=0.001,  # 0.1 % / hr
        balanced=False,  # True: content at beginning and end need to be equal
        storage_costs=storage_revenue,  # Only has an effect on charging.
    )
    energy_system.add(car_battery)

    return energy_system


# %%[solve_and_plot]
"""
Solve the model and show results
"""


def solve_and_plot():
    model = solph.Model(es)
    model.solve(solve_kwargs={"tee": False})
    results = solph.processing.results(model)

    battery_series = solph.views.node(results, "Car Battery")["sequences"]

    plt.figure()
    plt.plot(battery_series[(("Car Battery", "None"), "storage_content")])
    plt.ylabel("Energy (kWh)")
    plt.ylim(0, 60)
    plt.twinx()
    plt.ylim(0, 12)
    energy_leaves_battery = battery_series[
        (("Car Battery", "Car Electricity"), "flow")
    ]
    plt.step(energy_leaves_battery.index, energy_leaves_battery, "r-")
    plt.grid()
    plt.ylabel("Power (kW)")
    plt.gcf().autofmt_xdate()


es = create_base_system()
solve_and_plot()
plt.show()


# %%[charging]
"""
Now, let's assume the car battery can be charged (230 V, 16 A).
This, of course, can only happen while the car is present.
"""


def add_unidirectional_loading():
    car_present = pd.Series(1, index=time_index[:-1])
    car_present.loc[driving_start_morning:driving_end_evening] = 0  # kW

    b_el = es.node["Car Electricity"]

    # To be able to load the battery a electric source e.g. electric grid is necessary.
    # We set the maximum use to 1 (so 3.68 kW are usable) if the car is present,
    # while it is 0 between the morning start and the evening arrival back home.
    charger230V = solph.components.Source(
        label="230V charger",
        outputs={b_el: solph.Flow(nominal_capacity=3.68, max=car_present)},
    )

    es.add(charger230V)


es = create_base_system()
add_unidirectional_loading()
solve_and_plot()
plt.show()
exit()

# %%
"""
Solve the model and show results
"""
model = solph.Model(es)
model.solve(solve_kwargs={"tee": False})
results = solph.processing.results(model)

battery_series = solph.views.node(results, "Car Battery")["sequences"]

plt.plot(battery_series[(("Car Battery", "None"), "storage_content")])
plt.ylabel("Energy (kWh)")
plt.ylim(0, 51)
plt.twinx()
energy_leaves_battery = battery_series[
    (("Car Electricity", "Car Battery"), "flow")
]
plt.step(energy_leaves_battery.index, energy_leaves_battery, "r-")
plt.ylabel("Power (kW)")
plt.gcf().autofmt_xdate()
plt.show()


# %%
"""
Assuming the car can be loaded at home and the car is always available to be loaded (at home), when not driven.
The car is half loaded in the beginning and should be loaded when car is at home.
"""


def create_unidirectional_loading():

    # Again setting up the energy system
    energy_system = solph.EnergySystem(
        timeindex=time_index,
        infer_last_interval=False,
    )

    b_el = solph.Bus(label="Car Electricity")
    energy_system.add(b_el)

    # To be able to load the battery a electric source e.g. electric grid is necessary
    el_grid = solph.components.Source(
        label="Electric Grid", outputs={b_el: solph.Flow()}
    )

    energy_system.add(el_grid)

    # The car is half full and has to be full when the car leaves the first time
    # In this case before 7:10, e.g. timestep 86

    timestep_loading_finished = len(ev_demand[: ev_demand.gt(0).idxmax()])

    # We need a timeseries which represents the timesteps where loading is allowed (=1)
    # In this case the first 86 timesteps

    loading_allowed = pd.Series(0, index=time_index[:-1])
    loading_allowed[:timestep_loading_finished] = 1

    # The maximal charging_capacity is assumed to be 10 kW
    charging_cap = 10

    # The car can only be loaded if at home
    loading_allowed = [
        charging_cap if demand == 0 else 0 for demand in ev_demand
    ]

    # The is now regared as loss of the car battery
    # To make sure the car battery will be loaded, gain is added to the battery

    gain = -1

    car_battery = solph.components.GenericStorage(
        label="Car Battery",
        nominal_capacity=50,  # kWh
        inputs={
            b_el: solph.Flow(
                nominal_capacity=1, max=loading_allowed, variable_costs=gain
            )
        },
        outputs={b_el: solph.Flow(nominal_capacity=0)},
        initial_storage_level=0.5,  # halffull in the beginning
        fixed_losses_absolute=ev_demand,
        loss_rate=0.001,  # 0.1 % / hr
        balanced=False,  # True: content at beginning and end need to be equal
    )
    energy_system.add(car_battery)

    return energy_system


es = create_unidirectional_loading()


# %%
"""
Solve the model and show results
"""
model = solph.Model(es)
model.solve(solve_kwargs={"tee": False})
results = solph.processing.results(model)

battery_series = solph.views.node(results, "Car Battery")["sequences"]

plt.plot(battery_series[(("Car Battery", "None"), "storage_content")])
plt.ylabel("Energy (kWh)")
plt.ylim(0, 51)
plt.twinx()
energy_leaves_battery = battery_series[
    (("Car Electricity", "Car Battery"), "flow")
]
plt.step(energy_leaves_battery.index, energy_leaves_battery, "r-")
plt.ylabel("Power (kW)")
plt.gcf().autofmt_xdate()
plt.show()
# %%
