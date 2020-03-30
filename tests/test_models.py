# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: MIT
"""

import warnings

import pandas as pd
from nose import tools
from nose.tools import eq_
from nose.tools import raises
from oemof import solph
from oemof.solph.helpers import calculate_timeincrement


def test_timeincrement_with_valid_timeindex():
    datetimeindex = pd.date_range('1/1/2012', periods=1, freq='H')
    es = solph.EnergySystem(timeindex=datetimeindex)
    m = solph.models.BaseModel(es)
    eq_(m.timeincrement[0], 1)
    eq_(es.timeindex.freq.nanos / 3.6e12, 1)


@raises(AttributeError)
def test_timeincrement_with_non_valid_timeindex():
    es = solph.EnergySystem(timeindex=4)
    solph.models.BaseModel(es)


def test_timeincrement_value():
    es = solph.EnergySystem(timeindex=4)
    m = solph.models.BaseModel(es, timeincrement=3)
    eq_(m.timeincrement[0], 3)


def test_timeincrement_list():
    es = solph.EnergySystem(timeindex=4)
    m = solph.models.BaseModel(es, timeincrement=[0, 1, 2, 3])
    eq_(m.timeincrement[3], 3)


def test_nonequ_timeincrement():
    timeindex_hourly = pd.date_range('1/1/2019', periods=2, freq='H')
    timeindex_30mins = pd.date_range(
        '1/1/2019 03:00:00', periods=2, freq='30min')
    timeindex_2h = pd.date_range('1/1/2019 04:00:00', periods=2, freq='2H')
    timeindex = timeindex_hourly.append([timeindex_30mins, timeindex_2h])
    timeincrement = calculate_timeincrement(timeindex=timeindex)
    eq_(timeincrement, solph.sequence([1.0, 1.0, 2.0, 0.5, 0.5, 2.0]))


def test_nonequ_timeincrement_fill():
    timeindex_hourly = pd.date_range('1/1/2019', periods=2, freq='H')
    timeindex_30mins = pd.date_range(
        '1/1/2019 03:00:00', periods=2, freq='30min')
    timeindex_2h = pd.date_range('1/1/2019 04:00:00', periods=2, freq='2H')
    timeindex = timeindex_hourly.append([timeindex_30mins, timeindex_2h])
    fvalue = pd.Timedelta(hours=9)
    timeincrement = calculate_timeincrement(timeindex=timeindex,
                                            fill_value=fvalue)
    eq_(timeincrement, solph.sequence([9.0, 1.0, 2.0, 0.5, 0.5, 2.0]))


@raises(IndexError)
def test_nonequ_duplicate_timeindex():
    timeindex_hourly = pd.date_range('1/1/2019', periods=2, freq='H')
    timeindex_45mins = pd.date_range('1/1/2019', periods=2, freq='45min')
    timeindex = timeindex_hourly.append([timeindex_45mins])
    calculate_timeincrement(timeindex=timeindex)


@raises(AttributeError)
def test_nonequ_with_non_valid_timeindex():
    timeindex = 5
    calculate_timeincrement(timeindex=timeindex)


@raises(AttributeError)
def test_nonequ_with_non_valid_fill():
    timeindex = pd.date_range('1/1/2019', periods=2, freq='H')
    fill_value = 2
    calculate_timeincrement(timeindex=timeindex, fill_value=fill_value)


def test_optimal_solution():
    es = solph.EnergySystem(timeindex=[1])
    bel = solph.Bus(label='bus')
    es.add(bel)
    es.add(solph.Sink(inputs={bel: solph.Flow(
        nominal_value=5, actual_value=[1], fixed=True)}))
    es.add(solph.Source(outputs={bel: solph.Flow(variable_costs=5)}))
    m = solph.models.Model(es, timeincrement=1)
    m.solve('cbc')
    m.results()
    solph.processing.meta_results(m)


def test_infeasible_model():
    with tools.assert_raises_regexp(ValueError, ''):
        with warnings.catch_warnings(record=True) as w:
            es = solph.EnergySystem(timeindex=[1])
            bel = solph.Bus(label='bus')
            es.add(bel)
            es.add(solph.Sink(inputs={bel: solph.Flow(
                nominal_value=5, actual_value=[1], fixed=True)}))
            es.add(solph.Source(outputs={bel: solph.Flow(
                nominal_value=4, variable_costs=5)}))
            m = solph.models.Model(es, timeincrement=1)
            m.solve(solver='cbc')
            assert "Optimization ended with status" in str(w[0].message)
            solph.processing.meta_results(m)
