"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

from pathlib import Path

from urllib.request import urlretrieve


def download_input_data():
    url_temperature = (
        "https://oemof.org/wp-content/uploads/2025/12/temperature.csv"
    )
    url_energy = "https://oemof.org/wp-content/uploads/2025/12/energy.csv"

    print(
        "Data is licensed from M. Schlemminger, T. Ohrdes, E. Schneider,"
        " and M. Knoop. Under Creative Commons Attribution 4.0 International"
        " License It is also available at doi: 10.5281/zenodo.5642902."
    )

    file_path = Path(__file__).parent

    temperature_file = Path(file_path, "temperature.csv")
    if not temperature_file.exists():
        urlretrieve(url_temperature, temperature_file)

    energy_file = Path(file_path, "energy.csv")
    if not energy_file.exists():
        urlretrieve(url_energy, energy_file)


if __name__ == "__main__":
    download_input_data()
