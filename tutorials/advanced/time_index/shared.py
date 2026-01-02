"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

from pathlib import Path

import demandlib
import pandas as pd
import numpy as np
from urllib.request import urlretrieve
from workalendar.europe import Germany


def prepare_input_data():
    # ToDo: Mobilitätszeitreihe, die zu den Daten passt.

    url_temperature = (
        "https://oemof.org/wp-content/uploads/2025/12/temperature.csv"
    )
    url_energy = "https://oemof.org/wp-content/uploads/2025/12/energy.csv"

    print(
        "Data is licensed from M. Schlemminger, T. Ohrdes, E. Schneider,"
        " and M. Knoop. Under Creative Commons Attribution 4.0 International"
        " License. It is also available at doi: 10.5281/zenodo.5642902."
        " (We use single family home 26 plus the south-facing PV"
        " from that dataset.)"
    )

    file_path = Path(__file__).parent

    def _temperature_dataframe():
        temperature_file = Path(file_path, "temperature.csv")
        if not temperature_file.exists():
            urlretrieve(url_temperature, temperature_file)
        temperature = pd.read_csv(
            temperature_file,
            index_col="Unix Epoch",
        )

        temperature.index = pd.to_datetime(
            temperature.index,
            unit="s",
            utc=True,
        )

        temperature[temperature == np.inf] = np.nan
        temperature = temperature[10:].resample("1 min").mean()
        return temperature

    def _energy_dataframe():
        energy_file = Path(file_path, "energy.csv")
        if not energy_file.exists():
            urlretrieve(url_energy, energy_file)

        energy = pd.read_csv(
            energy_file,
            index_col=0,
        )
        energy.index = pd.to_datetime(
            energy.index,
            unit="s",
            utc=True,
        )

        energy[energy == np.inf] = np.nan

        energy = (
            energy.resample("1 min")
            .mean()
        )
        return energy

    df = pd.concat([_energy_dataframe(), _temperature_dataframe()], axis=1)

    df = df.interpolate()

    building_area = 120  # m² (from publication)
    specific_heat_demand = 60  #  kWh/m²/a  (educated guess)
    holidays = dict(Germany().holidays(2019))

    # We estimate the heat demand from the ambient temperature using demandlib.
    # This returns energy per time step in units of kWh, but we want kW.
    df["heat demand (kW)"] = demandlib.bdew.HeatBuilding(
        df.index,
        holidays=holidays,
        temperature=df["Air Temperature (°C)"],
        shlp_type="EFH",
        building_class=1,
        wind_class=1,
        annual_heat_demand=building_area * specific_heat_demand,
        name="EFH",
    ).get_bdew_profile() * 60

    # **************** COP calculation **********************************
    t_supply = 60
    efficiency = 0.5  # source?
    cop_max = 7  # source???

    cop_hp = (t_supply + 273.15 * efficiency) / (
        t_supply - df["Air Temperature (°C)"]
    )
    cop_hp.loc[cop_hp > cop_max] = cop_max

    df["cop"] = cop_hp

    df["PV (kW/kWp)"] = df["PV (W)"] / 14.5e3  # Wp from publication

    df["electricity demand (W)"] /= 1000
    df.rename(
        columns={"electricity demand (W)": "electricity demand (kW)"},
        inplace=True,
    )

    # drop colums that are no longer useful
    df.drop(columns=["PV (W)"], inplace=True)

    return df


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    df =prepare_input_data()

    p_pv = {}
    resolutions = [
        "1 min",
        "5 min",
        "10 min",
        "15 min",
        "30 min",
        "1 h",
        "2 h",
        "3 h",
        "6 h",
    ]

    for resolution in resolutions:
        p_pv[resolution] = df["PV (kW/kWp)"].resample(resolution).mean()
        plt.plot(
            np.linspace(0, 8760, len(p_pv[resolution])),
            sorted(p_pv[resolution])[::-1],
            label=resolution,
        )

    # plt.xlim(-10, 510)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.show()
