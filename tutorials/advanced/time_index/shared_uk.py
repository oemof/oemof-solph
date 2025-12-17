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


def prepare_input_data(minutes):
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
    energy = (
        energy.resample(f"{minutes} min")
        .mean()
        .ffill()
        .bfill()
        .reset_index(drop=True)
    )
    temperature[temperature == np.inf] = np.nan
    temperature = (
        temperature.resample(f"{minutes} min")
        .mean()[:-1]
        .ffill()
        .bfill()
        .reset_index(drop=True)
    )
    return pd.concat([energy, temperature], axis=1)


if __name__ == "__main__":
    print(prepare_input_data(5))
