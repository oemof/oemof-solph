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
    data = {}

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

    temperature_file = Path(file_path, "temperature.csv")
    if not temperature_file.exists():
        urlretrieve(url_temperature, temperature_file)
    temperature = pd.read_csv(
        temperature_file,
        index_col="Unix Epoch",
    )
    timedelta = np.empty(len(temperature))
    timedelta[:-1] = (temperature.index[1:] - temperature.index[:-1]) / 3600
    timedelta[-1] = np.nan

    temperature.index = pd.to_datetime(
        temperature.index,
        unit="s",
        utc=True,
    )

    building_area = 120  # m² (from publication)
    specific_heat_demand = 60  #  kWh/m²/a  (educated guess)
    holidays = dict(Germany().holidays(2019))

    # We estimate the heat demand from the ambient temperature using demandlib.
    # This returns energy per time step in units of kWh.
    temperature["heat demand (kWh)"] = demandlib.bdew.HeatBuilding(
        temperature.index,
        holidays=holidays,
        temperature=temperature["Air Temperature (°C)"],
        shlp_type="EFH",
        building_class=1,
        wind_class=1,
        annual_heat_demand=building_area * specific_heat_demand,
        name="EFH",
    ).get_bdew_profile()

    temperature["heat demand (W)"] = (
        temperature["heat demand (kWh)"] * 1e3 / timedelta
    )

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
    # ToDo: Auf 1 Minuten samplen und Nan-Werte interpolieren (linear)
    #  Daten in W
    #  demand ist absolut
    #  COP einfügen
    #  Mobilitätszeitreihe, die zu den Daten passt.
    #  Zeitstempel beachten ohne Offset!

    energy = (
        energy.resample("1 min")
        .mean()
    )
    temperature[temperature == np.inf] = np.nan
    temperature = (
        temperature[10:].resample("1 min")
        .mean()
    )
    df = pd.concat([energy, temperature], axis=1)
    df = df.interpolate()

    # **************** COP calculation **********************************
    t_supply = 60
    efficiency = 0.5  # source?
    cop_max = 7  # source???

    cop_hp = (t_supply + 273.15 * efficiency) / (
        t_supply - df["Air Temperature (°C)"]
    )
    cop_hp.loc[cop_hp > cop_max] = cop_max

    df["cop"] = cop_hp

    df["PV (W/kWp)"] = df["PV (W)"].div(df["PV (W)"].sum()/60000)

    return df


if __name__ == "__main__":
    print(prepare_input_data())
