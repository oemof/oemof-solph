import oemof.solph as solph

import matplotlib.pyplot as plt


def plot_results(results, plot_title, dark_mode=False):

    battery_series = solph.views.node(results, "Car Battery")["sequences"]

    plt.figure()
    if dark_mode:
        plt.style.use("dark_background")
    plt.title(plot_title)
    plt.plot(battery_series[(("Car Battery", "None"), "storage_content")])
    plt.ylabel("Energy (kWh)")
    plt.ylim(0, 55)
    plt.twinx()
    plt.ylim(0, 12)
    energy_enters_battery = battery_series[
        (("Car Electricity", "Car Battery"), "flow")
    ]
    energy_leaves_battery = battery_series[
        (("Car Battery", "Car Electricity"), "flow")
    ]
    plt.step(energy_leaves_battery.index, energy_leaves_battery, "r--")
    plt.step(energy_enters_battery.index, energy_enters_battery, "r-")
    plt.grid()
    plt.ylabel("Power (kW)")
    plt.gcf().autofmt_xdate()
