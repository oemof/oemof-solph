# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `Switch` can be used.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_generic_caes/test_generic_caes.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose.tools import eq_, ok_
import numpy as np
import pandas as pd
import oemof.solph as solph
from oemof.network import Node
from oemof.outputlib import processing
from oemof.solph.custom import SimpleSwitch


def _setup_switch(connections):
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
                           nominal_value=1, fixed=True,
                           actual_value=[1, 0, 1, 1])})
    d_ext = solph.Sink(label="d_ext",
                       inputs={b_ext: solph.Flow(
                           nominal_value=1)})

    s_int = solph.Source(label="s_int",
                         outputs={b_int: solph.Flow(
                             nominal_value=1, fixed=True,
                             actual_value=[1, 1, 1, 0])})
    s_ext = solph.Source(label="s_ext",
                         outputs={b_ext: solph.Flow(
                             maximum_value=1,
                             variable_costs=3)})

    switch = SimpleSwitch(
        label="switch",
        inputs={b_int: solph.Flow(nominal_value=10),
                b_ext: solph.Flow(nominal_value=10)},
        outputs={b_ext: solph.Flow(variable_costs=-1,
                                   nominal_value=10),
                 b_int: solph.Flow(nominal_value=10)},
        conversion_factors={(b_int, b_ext): 1,
                            (b_ext, b_int): 1},
        concurrent_connections=connections)

    # create an optimization problem and solve it
    om = solph.Model(es)

    # solve model
    om.solve(solver='cbc')

    # create result object
    return processing.results(om)[(switch, b_int)]["sequences"].values


def test_switch():
    # With one allowed connection, the example allows export
    # only for energy from the internal Source.
    # So, there will be only import when needed.
    result1 = _setup_switch(1)
    correct1 = np.ndarray(shape=(4, 1), buffer=np.array([0., 0., 0., 1.]))
    ok_(np.alltrue(result1 == correct1))

    # With two allowed connections, an import->export loop will be profitable.
    # So, all free export capacity is used by importing.
    result2 = _setup_switch(2)
    correct2 = np.ndarray(shape=(4, 1), buffer=np.array([10., 9., 10., 10.]))
    ok_(np.alltrue(result2 == correct2))


if __name__ == "__main__":
    test_switch()
