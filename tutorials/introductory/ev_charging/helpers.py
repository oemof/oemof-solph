import matplotlib.pyplot as plt

import oemof.solph as solph


def plot_results(results, plot_title, dark_mode=False):

    plt.figure()
    if dark_mode:
        plt.style.use("dark_background")
    plt.title(plot_title)
    (line1,) = plt.plot(
        results["storage_content"]["Car Battery"],
        label="Battery SOC",
    )

    plt.ylabel("Energy (kWh)")
    plt.ylim(0, 55)
    plt.twinx()
    plt.ylim(0, 12)
    energy_enters_battery = results["flow"][("Car Electricity", "Car Battery")]
    energy_leaves_battery = results["flow"][("Car Battery", "Car Electricity")]
    (line2,) = plt.step(
        energy_leaves_battery.index,
        energy_leaves_battery,
        "r--",
        label="Discharge",
    )
    (line3,) = plt.step(
        energy_enters_battery.index,
        energy_enters_battery,
        "g-",
        label="Charge",
    )
    plt.grid()
    plt.ylabel("Power (kW)")
    plt.legend(handles=[line1, line2, line3])
    plt.gcf().autofmt_xdate()
