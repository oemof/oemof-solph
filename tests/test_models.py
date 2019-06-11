# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import pandas as pd
from oemof import solph
from oemof import outputlib
from nose.tools import eq_, raises
from nose import tools


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


def test_optimal_solution():
    es = solph.EnergySystem(timeindex=[1])
    bel = solph.Bus(label='bus')
    es.add(bel)
    es.add(solph.Sink(inputs={bel: solph.Flow(nominal_value=5, actual_value=[1], fixed=True)}))
    es.add(solph.Source(outputs={bel: solph.Flow(variable_costs=5)}))
    m = solph.models.Model(es, timeincrement=1)
    m.solve('cbc')
    m.results()
    outputlib.processing.meta_results(m)


def test_infeasable_model():
    with tools.assert_raises_regexp(ValueError, ''):
        es = solph.EnergySystem(timeindex=[1])
        bel = solph.Bus(label='bus')
        es.add(bel)
        es.add(solph.Sink(inputs={bel: solph.Flow(nominal_value=5, actual_value=[1], fixed=True)}))
        es.add(solph.Source(outputs={bel: solph.Flow(nominal_value=4, variable_costs=5)}))
        m = solph.models.Model(es, timeincrement=1)
        m.solve(solver='glpk')
        outputlib.processing.meta_results(m)
