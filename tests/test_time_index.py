# -*- coding: utf-8 -

"""Test the definition of the time index of the model.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Stephan Günther

SPDX-License-Identifier: MIT
"""

import pandas as pd
import pytest
from oemof.tools import debugging

from oemof import solph


def test_energysystem_with_datetimeindex_infer_last_interval():
    """Test EnergySystem with DatetimeIndex (equidistant)"""
    datetimeindex = pd.date_range("1/1/2012", periods=24, freq="h")
    es = solph.EnergySystem(timeindex=datetimeindex, infer_last_interval=True)
    assert es.timeincrement[1] == 1.0
    assert es.timeincrement.sum() == 24


def test_energysystem_with_datetimeindex():
    datetimeindex = pd.date_range("1/1/2012", periods=24, freq="h")
    es = solph.EnergySystem(timeindex=datetimeindex, infer_last_interval=False)
    assert es.timeincrement[1] == 1.0
    assert es.timeincrement.sum() == 23


def test_energysystem_interval_inference_warning():
    datetimeindex = pd.date_range("1/1/2012", periods=24, freq="h")
    with pytest.warns(FutureWarning):
        _ = solph.EnergySystem(timeindex=datetimeindex)


def test_energysystem_with_datetimeindex_non_equidistant_infer_last_interval():
    """Test EnergySystem with DatetimeIndex (non-equidistant)"""
    dtindex1 = pd.date_range("1/1/2012", periods=24, freq="h")
    dtindex2 = pd.date_range("1/2/2012", periods=49, freq="30min")
    dtindex = dtindex1.union(dtindex2)
    msg = (
        "You cannot infer the last interval if the 'freq' attribute of your "
        "DatetimeIndex is None."
    )
    with pytest.raises(AttributeError, match=msg):
        solph.EnergySystem(timeindex=dtindex, infer_last_interval=True)


def test_energysystem_with_datetimeindex_non_equidistant():
    """Test EnergySystem with DatetimeIndex (non-equidistant)"""
    dtindex1 = pd.date_range("1/1/2012", periods=24, freq="h")
    dtindex2 = pd.date_range("1/2/2012", periods=49, freq="30min")
    dtindex = dtindex1.union(dtindex2)
    es = solph.EnergySystem(timeindex=dtindex, infer_last_interval=False)
    assert es.timeincrement.sum() == 48.0
    assert es.timeincrement[0] == 1
    assert es.timeincrement[25] == 0.5


def test_energysystem_with_numeric_index_infer_last_interval():
    """Test EnergySystem with numeric index (equidistant)"""
    time_increments = [1, 1, 1, 1, 1]
    es = solph.EnergySystem(timeincrement=time_increments)
    assert es.timeincrement[1] == 1.0
    assert pd.Series(es.timeincrement).sum() == 5


def test_energysystem_with_numeric_index():
    """Test EnergySystem with numeric index (equidistant)"""
    time_increments = [1, 1, 1, 1, 1]
    es = solph.EnergySystem(
        timeincrement=time_increments, infer_last_interval=False
    )
    assert es.timeincrement[1] == 1.0
    assert pd.Series(es.timeincrement).sum() == 5


def test_energysystem_with_numeric_index_non_equidistant_infer_last_interval():
    """
    Test EnergySystem with DatetimeIndex (non-equidistant)
    'infer_last_interval=True/False' does not have any effect.
    """
    time_increments = [1, 1, 1, 1, 1, 0.5, 0.5, 0.25, 0.25, 0.5]

    es = solph.EnergySystem(
        timeincrement=time_increments, infer_last_interval=True
    )
    assert pd.Series(es.timeincrement).sum() == 7.0
    assert es.timeincrement[0] == 1
    assert es.timeincrement[6] == 0.5


def test_energysystem_with_numeric_index_non_equidistant():
    """
    Test EnergySystem with DatetimeIndex (non-equidistant)
    'infer_last_interval=True/False' does not have any effect.
    """
    time_increments = [1, 1, 1, 1, 1, 0.5, 0.5, 0.25, 0.25, 0.5]
    es = solph.EnergySystem(
        timeincrement=time_increments, infer_last_interval=False
    )
    assert pd.Series(es.timeincrement).sum() == 7.0
    assert es.timeincrement[0] == 1
    assert es.timeincrement[8] == 0.25


def test_model_timeincrement_with_valid_timeindex():
    datetimeindex = pd.date_range("1/1/2012", periods=5, freq="h")
    es = solph.EnergySystem(timeindex=datetimeindex, infer_last_interval=True)
    m = solph._models.Model(es)
    assert es.timeincrement.sum() == 5
    assert m.timeincrement.sum() == 5
    assert m.timeincrement[2] == 1


def test_timeincrement_with_non_valid_timeindex():
    with pytest.raises(
        TypeError, match="Parameter 'timeindex' has to be of type"
    ):
        solph.EnergySystem(timeindex=4)


def test_conflicting_time_index():
    msg = (
        "Specifying the timeincrement and the timeindex parameter at the same "
        "time is not allowed"
    )
    with pytest.raises(AttributeError, match=msg):
        solph.EnergySystem(
            timeindex=pd.date_range("1/1/2012", periods=2, freq="h"),
            timeincrement=[1, 2, 3, 4],
            infer_last_interval=False,
        )


def test_missing_timeincrement():
    msg = (
        "The EnergySystem needs to have a valid 'timeincrement' attribute to "
        "build a model."
    )
    es = solph.EnergySystem()
    with pytest.raises(AttributeError, match=msg):
        solph.Model(es)


def test_overwrite_timeincrement():
    es = solph.EnergySystem(
        timeindex=pd.date_range("1/1/2012", periods=2, freq="h"),
        infer_last_interval=True,
    )
    assert es.timeincrement[0] == 1
    with pytest.warns(debugging.SuspiciousUsageWarning):
        m = solph._models.Model(es, timeincrement=[3])
    assert m.timeincrement[0] == 3


def test_model_timeincrement_list():
    es = solph.EnergySystem(timeincrement=[0.1, 1, 2, 3])
    m = solph._models.Model(es)
    assert m.timeincrement[3] == 3


def test_nonequ_inconsistent_timeindex():
    # with pytest.raises(IndexError):
    timeindex_one = pd.date_range("1/1/2019", periods=1, freq="h")
    timeindex_hourly = pd.date_range("1/1/2019", periods=3, freq="h")
    timeindex_45mins = pd.date_range("1/1/2019", periods=2, freq="45min")
    timeindex1 = timeindex_one.append(timeindex_hourly)
    timeindex2 = timeindex_hourly.append([timeindex_45mins])
    with pytest.raises(TypeError):
        solph.EnergySystem(timeindex=timeindex1, infer_last_interval=False)
    with pytest.raises(TypeError):
        solph.EnergySystem(timeindex=timeindex2, infer_last_interval=False)
