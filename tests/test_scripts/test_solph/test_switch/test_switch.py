# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `Switch` can be used.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_generic_caes/test_generic_caes.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose.tools import eq_
import os
import pprint
import pandas as pd
import oemof.solph as solph
from oemof.network import Node
from oemof.outputlib import processing, views
from oemof.solph.custom import Link, Switch


def test_switch():
    # select periods
    periods = 4

    # create an energy system
    idx = pd.date_range('1/1/2017', periods=periods, freq='H')
    es = solph.EnergySystem(timeindex=idx)
    Node.registry = es

    b_int = solph.Bus(label='b_int')
    b_ext = solph.Bus(label='b_ext')

    d_int = solph.Sink(label="d_int",
                       inputs={b_int: solph.Flow(
                           nominal_value=4, fixed=True,
                           actual_value=[1, 0, 1, 0])})
    d_ext = solph.Sink(label="d_ext",
                       inputs={b_ext: solph.Flow(
                           nominal_value=1)})

    s_int = solph.Source(label="s_int",
                         outputs={b_int: solph.Flow(
                             nominal_value=1, fixed=True,
                             actual_value=[1, 1, 1, 0])})
    s_ext = solph.Source(label="s_ext",
                         outputs={b_ext: solph.Flow(
                             variable_costs=3)})

    switch = Switch(
        label="switch",
        inputs={b_int: solph.Flow(), b_ext: solph.Flow()},
        outputs={b_ext: solph.Flow(variable_costs=-1), b_int: solph.Flow()},
        conversion_factors={(b_int, b_ext): 0.5,
                            (b_ext, b_int): 1})


    # create an optimization problem and solve it
    om = solph.Model(es)

    # solve model
    om.solve(solver='cbc')

    # create result object
    results = processing.results(om)

    data = views.node(
        results, 'switch', keep_none_type=True
    )['sequences']

    pprint.pprint(data.to_dict())


if __name__ == "__main__":
    test_switch()
