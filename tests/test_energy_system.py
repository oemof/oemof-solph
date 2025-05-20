"""Tests of the _energy_system module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd
import pytest

from oemof.solph import EnergySystem


def test_default_invest_times():
    start_time = pd.Timestamp("2012-01-01 00:00")
    timeindex = pd.date_range(start=start_time, periods=8760, freq="h")
    es = EnergySystem(
        timeindex=timeindex,
        infer_last_interval=True,
    )
    assert len(es.investment_times) == 1
    assert es.investment_times[0] == start_time
    assert (es.investment_index == np.array([0])).all()


def test_custom_invest_times():
    start_time = pd.Timestamp("2012-01-01 00:00")
    time2 = pd.Timestamp("2012-01-11 00:00")

    timeindex = pd.date_range(start=start_time, periods=8760, freq="h")

    investment_times = [start_time, time2]
    es = EnergySystem(
        timeindex=timeindex,
        investment_times=investment_times,
        infer_last_interval=True,
    )
    assert len(es.investment_times) == 2
    assert es.investment_times[0] == start_time
    assert es.investment_times[1] == time2

    # start time is added automatically
    es = EnergySystem(
        timeindex=timeindex,
        investment_times=[time2],
        infer_last_interval=True,
    )
    assert len(es.investment_times) == 2
    assert es.investment_times[0] == start_time
    assert es.investment_times[1] == time2

    # invest times are sorted automatically
    investment_times = [time2, start_time]
    es = EnergySystem(
        timeindex=timeindex,
        investment_times=investment_times,
        infer_last_interval=True,
    )
    assert len(es.investment_times) == 2
    assert es.investment_times[0] == start_time
    assert es.investment_times[1] == time2


def test_invelid_invest_time():
    start_time = pd.Timestamp("2012-01-01 00:00")
    time3 = pd.Timestamp("2012-01-11 00:15")

    timeindex = pd.date_range(start=start_time, periods=8760, freq="h")
    investment_times = [start_time, time3]
    with pytest.raises(KeyError, match="2012-01-11 00:15"):
        _ = EnergySystem(
            timeindex=timeindex,
            investment_times=investment_times,
            infer_last_interval=True,
        )
