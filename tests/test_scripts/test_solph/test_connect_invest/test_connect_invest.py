# -*- coding: utf-8 -*-

"""Connecting different investment variables.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_connect_invest/test_connect_invest.py

SPDX-License-Identifier: MIT
"""

import logging
import os

import pandas as pd
from nose.tools import eq_
from oemof.network import network
from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import Sink
from oemof.solph import Source
from oemof.solph import Transformer
from oemof.solph import components
from oemof.solph import constraints
from oemof.solph import processing
from oemof.solph import views


def test_connect_invest():
    date_time_index = pd.date_range('1/1/2012', periods=24 * 7, freq='H')

    energysystem = EnergySystem(timeindex=date_time_index)
    network.Node.registry = energysystem

    # Read data file
    full_filename = os.path.join(os.path.dirname(__file__),
                                 'connect_invest.csv')
    data = pd.read_csv(full_filename, sep=",")

    logging.info('Create oemof objects')

    # create electricity bus
    bel1 = Bus(label="electricity1")
    bel2 = Bus(label="electricity2")

    # create excess component for the electricity bus to allow overproduction
    Sink(label='excess_bel', inputs={bel2: Flow()})
    Source(label='shortage', outputs={bel2: Flow(
        variable_costs=50000)})

    # create fixed source object representing wind power plants
    Source(label='wind', outputs={bel1: Flow(
        fix=data['wind'], nominal_value=1000000)})

    # create simple sink object representing the electrical demand
    Sink(label='demand', inputs={bel1: Flow(
        fix=data['demand_el'], nominal_value=1)})

    storage = components.GenericStorage(
        label='storage',
        inputs={bel1: Flow(variable_costs=10e10)},
        outputs={bel1: Flow(variable_costs=10e10)},
        loss_rate=0.00, initial_storage_level=0,
        invest_relation_input_capacity=1/6,
        invest_relation_output_capacity=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=Investment(ep_costs=0.2),
    )

    line12 = Transformer(
        label="line12",
        inputs={bel1: Flow()},
        outputs={bel2: Flow(investment=Investment(ep_costs=20))})

    line21 = Transformer(
        label="line21",
        inputs={bel2: Flow()},
        outputs={bel1: Flow(investment=Investment(ep_costs=20))})

    om = Model(energysystem)

    constraints.equate_variables(
        om, om.InvestmentFlow.invest[line12, bel2],
        om.InvestmentFlow.invest[line21, bel1], 2)
    constraints.equate_variables(
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
    my_results['storage_in'] = stor_res[
        (('electricity1', 'storage'), 'invest')]
    my_results['storage'] = stor_res[(('storage', 'None'), 'invest')]
    my_results['storage_out'] = stor_res[
        (('storage', 'electricity1'), 'invest')]

    connect_invest_dict = {
        'line12': 814705,
        'line21': 1629410,
        'storage': 814705,
        'storage_in': 135784,
        'storage_out': 135784}

    for key in connect_invest_dict.keys():
        eq_(int(round(my_results[key])), int(round(connect_invest_dict[key])))
