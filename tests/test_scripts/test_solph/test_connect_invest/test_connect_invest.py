# -*- coding: utf-8 -*-

"""Connecting different investment variables.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_connect_invest/test_connect_invest.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose.tools import eq_
import oemof.solph as solph
from oemof.outputlib import processing, views

import logging
import os
import pandas as pd
from oemof.network import Node


def test_connect_invest():
    date_time_index = pd.date_range('1/1/2012', periods=24 * 7, freq='H')

    energysystem = solph.EnergySystem(timeindex=date_time_index)
    Node.registry = energysystem
    
    # Read data file
    full_filename = os.path.join(os.path.dirname(__file__),
                                 'connect_invest.csv')
    data = pd.read_csv(full_filename, sep=",")

    logging.info('Create oemof objects')

    # create electricity bus
    bel1 = solph.Bus(label="electricity1")
    bel2 = solph.Bus(label="electricity2")

    # create excess component for the electricity bus to allow overproduction
    solph.Sink(label='excess_bel', inputs={bel2: solph.Flow()})
    solph.Source(label='shortage', outputs={bel2: solph.Flow(
        variable_costs=50000)})

    # create fixed source object representing wind power plants
    solph.Source(label='wind', outputs={bel1: solph.Flow(
        actual_value=data['wind'], nominal_value=1000000, fixed=True)})

    # create simple sink object representing the electrical demand
    solph.Sink(label='demand', inputs={bel1: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    storage = solph.components.GenericStorage(
        label='storage',
        inputs={bel1: solph.Flow(variable_costs=10e10)},
        outputs={bel1: solph.Flow(variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        invest_relation_input_capacity=1/6,
        invest_relation_output_capacity=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=solph.Investment(ep_costs=0.2),
    )

    line12 = solph.Transformer(
        label="line12",
        inputs={bel1: solph.Flow()},
        outputs={bel2: solph.Flow(investment=solph.Investment(ep_costs=20))})

    line21 = solph.Transformer(
        label="line21",
        inputs={bel2: solph.Flow()},
        outputs={bel1: solph.Flow(investment=solph.Investment(ep_costs=20))})

    om = solph.Model(energysystem)

    solph.constraints.equate_variables(
        om, om.InvestmentFlow.invest[line12, bel2],
        om.InvestmentFlow.invest[line21, bel1], 2)
    solph.constraints.equate_variables(
        om, om.InvestmentFlow.invest[line12, bel2],
        om.GenericInvestmentStorageBlock.invest[storage])

    # if tee_switch is true solver messages will be displayed
    logging.info('Solve the optimization problem')
    om.solve(solver='cbc')

    # check if the new result object is working for custom components
    results = processing.results(om)

    my_results = dict()
    my_results['line12'] = float(views.node(results, 'line12')['scalars'])
    my_results['line21'] = float(views.node(results, 'line21')['scalars'])
    stor_res = views.node(results, 'storage')['scalars']
    my_results['storage_in'] = stor_res.iloc[0]  # ('electricity1', 'storage')
    my_results['storage'] = stor_res.iloc[1]     # ('storage', 'None')
    my_results['storage_out'] = stor_res.iloc[2] # ('storage', 'electricity1')

    connect_invest_dict = {
        'line12': 814705,
        'line21': 1629410,
        'storage': 814705,
        'storage_in': 135784,
        'storage_out': 135784}

    for key in connect_invest_dict.keys():
        eq_(int(round(my_results[key])), int(round(connect_invest_dict[key])))
