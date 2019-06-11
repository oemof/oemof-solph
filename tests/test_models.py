# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import pandas as pd
from oemof import solph
from nose.tools import eq_, raises


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
