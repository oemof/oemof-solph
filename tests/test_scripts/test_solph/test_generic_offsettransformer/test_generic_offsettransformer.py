# -*- coding: utf-8 -*-
"""
Example that shows how to use custom component `GenericOffsetTransformer`.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_scripts/test_solph/
test_generic_offsettransformer/test_generic_offsettransformer.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose.tools import eq_
import os
import pandas as pd
import oemof.solph as solph
from oemof.network import Node
from oemof.outputlib import processing, views


def test_gen_ostf():
    # read sequence data
    full_filename = os.path.join(os.path.dirname(__file__), 'ostf.csv')
    data = pd.read_csv(full_filename)

    # select periods
    periods = len(data)-1

    # create an energy system
    idx = pd.date_range('1/1/2017', periods=periods, freq='H')
    es = solph.EnergySystem(timeindex=idx)
    Node.registry = es

    # resources
    bgas = solph.Bus(label='bgas')

    solph.Source(label='rgas', outputs={bgas: solph.Flow()})

    # heat
    bth = solph.Bus(label='bth')

    solph.Source(label='source_th',
                 outputs={bth: solph.Flow(variable_costs=1000)})

    solph.Sink(label='demand_th', inputs={
        bth: solph.Flow(
            fixed=True, actual_value=data['demand_th'], nominal_value=200)})

    # power
    bel = solph.Bus(label='bel')

    solph.Source(label='source_el', outputs={
        bel: solph.Flow(variable_costs=data['price_el'])})

    # generic chp
    hp = solph.custom.OffsetTransformer(
        label='heat_pump',
        inputs={bel: solph.Flow(
            nominal_value=100,
            max=[1 for i in range(0, periods)],
            min=[0.25 for i in range(0, periods)],
            nonconvex=solph.NonConvex()
            )},
        outputs={bth: solph.Flow()},
        coefficients=[[0 for i in range(0, periods)],
                      [2 for i in range(0, periods)]])

    # create an optimization problem and solve it
    om = solph.Model(es)

    # solve model
    om.solve(solver='cbc')

    # create result object
    results = processing.results(om)

    data = views.node(results, 'bth')['sequences'].sum(axis=0).to_dict()

    test_dict = {
        (('heat_pump', 'bth'), 'flow'): 18800.0,
        (('source_th', 'bth'), 'flow'): 1200.0,
        (('bth', 'demand_th'), 'flow'): 20000.0}

    for key in test_dict.keys():
        eq_(int(round(data[key])), int(round(test_dict[key])))
