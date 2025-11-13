# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

import os

import pandas as pd

file_path = os.path.dirname(__file__)

df = pd.read_csv(
    os.path.join(file_path, "input_data.csv"),
    parse_dates=["time"],
    index_col="time",
)
print(df)
