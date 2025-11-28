"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

from urllib.request import urlretrieve

def download_input_data():
    url_temperature = "https://oemof.org/wp-content/uploads/2025/11/temperature.csv"
    url_energy = "https://oemof.org/wp-content/uploads/2025/11/energy.csv"

    urlretrieve(url_temperature, Path(file_path, "temperature.csv"))
    urlretrieve(url_energy, Path(file_path, "energy.csv"))
