"""Tests of the _energy_system module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import pandas as pd
import pytest
from oemof.tools.debugging import ExperimentalFeatureWarning

from oemof import solph


@pytest.mark.filterwarnings(
    "ignore:Ensure that your timeindex and timeincrement are"
    " consistent.:UserWarning"
)
@pytest.mark.filterwarnings(
    "ignore:CAUTION! You specified the 'investment_times':UserWarning"
)
def test_add_periods():
    """test method _add_periods of energy system"""
    timeindex = pd.date_range(start="2012-01-01", periods=10000, freq="h")
    periods = [
        timeindex[:8784],
        timeindex[8784:-1],
    ]
    es = solph.EnergySystem(
        timeindex=timeindex,
        investment_times=[timeindex[0], timeindex[8784], timeindex[-1]],
        infer_last_interval=False,
    )
    assert len(es.capacity_periods) == 2
    assert (es.capacity_periods[0] == periods[0]).all()
    assert (es.capacity_periods[1] == periods[1]).all()


def test_infer_last_interval_known_freq():
    timeindex = pd.date_range(start="2025-01-01", periods=25, freq="h")
    es = solph.EnergySystem(
        timeindex=timeindex[:24],
        infer_last_interval=True,
    )
    assert len(es.timeindex) == 25
    assert es.timeindex[-1] == timeindex[-1]


def test_infer_last_interval_infer_freq():
    timeindex = pd.date_range(start="2025-01-01", periods=25, freq="h")
    timeindex.freq = None

    es = solph.EnergySystem(
        timeindex=timeindex[:-1],
        infer_last_interval=True,
    )
    assert len(es.timeindex) == 25
    assert es.timeindex[-1] == timeindex[-1]


def test_infer_last_interval_no_freq():
    timeindex1 = pd.date_range(start="2025-01-01", periods=24, freq="h")
    timeindex2 = pd.date_range(start="2025-01-02", periods=48, freq="30min")
    timeindex = timeindex1.append(timeindex2)

    msg = "interval_last_interval requires that the timeindex"

    with pytest.raises(AttributeError, match=msg):
        solph.EnergySystem(
            timeindex=timeindex,
            infer_last_interval=True,
        )
    with pytest.raises(AttributeError, match=msg):
        solph.EnergySystem(
            timeindex=[1, 2, 3],
            infer_last_interval=True,
        )


def test_capacity_period_of_timestep_numeric():
    timeindex = list(range(0, 13))

    with pytest.warns(ExperimentalFeatureWarning, match="investment_times"):
        es = solph.EnergySystem(
            timeindex=timeindex,
            infer_last_interval=False,
            investment_times=[0, 5, 6, 10, 15],
        )
    assert len(es.capacity_periods) == 4

    assert es.capacity_period_of_timestep(0) == 0
    assert es.capacity_period_of_timestep(1) == 0
    assert es.capacity_period_of_timestep(2) == 0
    assert es.capacity_period_of_timestep(3) == 0
    assert es.capacity_period_of_timestep(4) == 0
    assert es.capacity_period_of_timestep(5) == 1
    assert es.capacity_period_of_timestep(6) == 2
    assert es.capacity_period_of_timestep(7) == 2
    assert es.capacity_period_of_timestep(8) == 2
    assert es.capacity_period_of_timestep(9) == 2
    assert es.capacity_period_of_timestep(10) == 3
    assert es.capacity_period_of_timestep(11) == 3

    with pytest.raises(ValueError, match="12 not in capacity range."):
        es.capacity_period_of_timestep(12)


def test_capacity_period_of_timestep_datetime():
    timeindex = solph.create_time_index(2025, 1, 12)

    with pytest.warns(ExperimentalFeatureWarning, match="investment_times"):
        es = solph.EnergySystem(
            timeindex=timeindex,
            infer_last_interval=False,
            investment_times=[
                timeindex[0],
                timeindex[5],
                timeindex[6],
                timeindex[10],
                timeindex[-1],
            ],
        )
    assert es.capacity_period_of_timestep(0) == 0
    assert es.capacity_period_of_timestep(1) == 0
    assert es.capacity_period_of_timestep(2) == 0
    assert es.capacity_period_of_timestep(3) == 0
    assert es.capacity_period_of_timestep(4) == 0
    assert es.capacity_period_of_timestep(5) == 1
    assert es.capacity_period_of_timestep(6) == 2
    assert es.capacity_period_of_timestep(7) == 2
    assert es.capacity_period_of_timestep(8) == 2
    assert es.capacity_period_of_timestep(9) == 2
    assert es.capacity_period_of_timestep(10) == 3
    assert es.capacity_period_of_timestep(11) == 3
    with pytest.raises(ValueError, match="12 not in capacity range."):
        es.capacity_period_of_timestep(12)


@pytest.mark.filterwarnings(
    "ignore:Ensure that your timeindex and timeincrement are"
    " consistent.:UserWarning"
)
@pytest.mark.filterwarnings(
    "ignore:CAUTION! You specified the 'investment_times':UserWarning"
)
def test_extract_period_years():
    """test method _extract_period_years of energy system"""
    t_idx_1 = pd.date_range("1/1/2020", periods=3, freq="h").to_series()
    t_idx_2 = pd.date_range("1/1/2041", periods=3, freq="h").to_series()
    t_idx_3 = pd.date_range("1/1/2050", periods=4, freq="h").to_series()
    timeindex = pd.concat([t_idx_1, t_idx_2, t_idx_3]).index
    periods = [
        t_idx_1.iloc[0],
        t_idx_2.iloc[0],
        t_idx_3.iloc[0],
        t_idx_3.iloc[-1],
    ]
    es = solph.EnergySystem(
        timeindex=timeindex,
        timeincrement=[1] * len(timeindex),
        infer_last_interval=False,
        investment_times=periods,
    )
    period_years = [0, 21, 30]
    assert es.capacity_period_years == period_years
