"""Tests of the _energy_system module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import pandas as pd
import pytest

from oemof.solph import EnergySystem


@pytest.mark.filterwarnings(
    "ignore:Ensure that your timeindex and timeincrement are"
    " consistent.:UserWarning"
)
@pytest.mark.filterwarnings(
    "ignore:CAUTION! You specified the 'periods' attribute:UserWarning"
)
def test_add_periods():
    """test method _add_periods of energy system"""
    timeindex = pd.date_range(start="2012-01-01", periods=10000, freq="h")
    periods = [
        pd.date_range(start="2012-01-01", periods=8784, freq="h"),
        pd.date_range(start="2013-01-01", periods=1217, freq="h"),
    ]
    es = EnergySystem(
        timeindex=timeindex, investment_times=periods, infer_last_interval=True
    )
    assert len(es.investment_times) == 2
    assert es.investment_times[0].equals(
        pd.date_range(start="2012-01-01", periods=8784, freq="h")
    )
    assert es.investment_times[1].equals(
        pd.date_range(start="2013-01-01", periods=1217, freq="h")
    )
