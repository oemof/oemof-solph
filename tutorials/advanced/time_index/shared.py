"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

from pathlib import Path
from urllib.request import urlretrieve

import demandlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from workalendar.europe import Germany


def prepare_input_data(plot_resampling=False):
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
    df_temperature = pd.read_csv(
        temperature_file,
        index_col="Unix Epoch",
    )

    df_temperature.index = pd.to_datetime(
        df_temperature.index,
        unit="s",
        utc=True,
    )

    # ----- clean up data --------------------------------------------------------------
    # 1) Duplikate durch Mittelwert ersetzen
    df_temperature = df_temperature.groupby(df_temperature.index).mean()

    # 2) Regulären 5-Minuten-Index erzeugen (Zeitzone erhalten)
    tz = df_temperature.index.tz
    full_idx = pd.date_range(
        start=df_temperature.index.min(),
        end=df_temperature.index.max(),
        freq="5min",
        tz=tz,
    )

    # 3) Auf 5-Minuten-Raster reindizieren -> Lücken werden NaN
    df_regular = df_temperature.reindex(full_idx)

    # 4) Zeitbasierte Interpolation nur für numerische Spalten
    num_cols = df_regular.select_dtypes(include="number").columns

    # Interpolation (zeitbasiert: berücksichtigt die Zeitabstände im Index)
    df_regular[num_cols] = df_regular[num_cols].interpolate(method="time")

    # 5) Ränder ohne beidseitige Nachbarn per ffill/bfill schließen
    df_regular[num_cols] = df_regular[num_cols].ffill().bfill()

    df_temperature = df_regular

    # -------------------------------------------

    building_area = 120  # m² (from publication)
    specific_heat_demand = 60  #  kWh/m²/a  (educated guess)
    holidays = dict(Germany().holidays(2019))

    # We estimate the heat demand from the ambient temperature using demandlib.
    # This returns energy per time step in units of kWh.
    df_temperature["heat demand (kWh)"] = demandlib.bdew.HeatBuilding(
        df_temperature.index,
        holidays=holidays,
        temperature=df_temperature["Air Temperature (°C)"],
        shlp_type="EFH",
        building_class=1,
        wind_class=1,
        annual_heat_demand=building_area * specific_heat_demand,
        name="EFH",
    ).get_bdew_profile()

    df_temperature["heat demand (W)"] = (
        df_temperature["heat demand (kWh)"] * 1e3 / (5 / 60)
    )

    energy_file = Path(file_path, "energy.csv")
    if not energy_file.exists():
        urlretrieve(url_energy, energy_file)
    df_energy = pd.read_csv(
        energy_file,
        index_col=0,
    )
    df_energy.index = pd.to_datetime(
        df_energy.index,
        unit="s",
        utc=True,
    )

    if plot_resampling:
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
            p_pv[resolution] = df_energy["PV (W)"].resample(resolution).mean()
            plt.plot(
                np.linspace(0, 8760, len(p_pv[resolution])),
                sorted(p_pv[resolution] / 1e3)[::-1],
                label=resolution,
            )

        plt.xlim(-10, 510)
        plt.ylim(7, 16)
        plt.legend()
        plt.show()

    return df_temperature, df_energy


if __name__ == "__main__":
    prepare_input_data(plot_resampling=True)
