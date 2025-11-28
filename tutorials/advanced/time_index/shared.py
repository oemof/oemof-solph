"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

from urllib.request import urlretrieve

def download_input_data():
    url_temperature = "https://oemof.org/wp-content/uploads/2025/11/temperature.csv"
    url_energy = "https://oemof.org/wp-content/uploads/2025/11/energy.csv"

    print(
        "Data is licensed under Creative Commons Attribution 4.0 International\n"
        "from M. Schlemminger, T. Ohrdes, E. Schneider, and M. Knoop.\n"
        "It is also available at doi: 10.5281/zenodo.5642902."
    )
    
    urlretrieve(url_temperature, Path(file_path, "temperature.csv"))
    urlretrieve(url_energy, Path(file_path, "energy.csv"))
