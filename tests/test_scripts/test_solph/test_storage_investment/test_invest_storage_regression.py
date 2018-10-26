# -*- coding: utf-8 -*-

"""
This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_scripts/test_solph/
test_storage_investment/test_storage_investment.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import oemof.solph as solph
from oemof.network import Node
from oemof.outputlib import processing, views

import logging
import pandas as pd


def test_regression_investment_storage(solver='cbc'):
    """The problem was infeasible if the existing capacity and the maximum was
    defined in the Flow.
    """

    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2012', periods=4, freq='H')

    energysystem = solph.EnergySystem(timeindex=date_time_index)
    Node.registry = energysystem

    # Buses
    bgas = solph.Bus(label=('natural', 'gas'))
    bel = solph.Bus(label='electricity')

    solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=[209643, 207497, 200108, 191892], fixed=True,
        nominal_value=1)})

    # Sources
    solph.Source(label='rgas', outputs={bgas: solph.Flow()})

    # Transformer
    solph.Transformer(
        label='pp_gas',
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=300000)},
        conversion_factors={bel: 0.58})

    # Investment storage
    solph.components.GenericStorage(
        label='storage',
        inputs={bel: solph.Flow(investment=solph.Investment(
            existing=625046/6, maximum=0))},
        outputs={bel: solph.Flow(investment=solph.Investment(
            existing=104174.33, maximum=1))},
        capacity_loss=0.00, initial_capacity=0,
        invest_relation_input_capacity=1/6,
        invest_relation_output_capacity=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=solph.Investment(ep_costs=50, existing=625046),
    )

    # Solve model
    om = solph.Model(energysystem)
    om.solve(solver=solver)

    # Results
    results = processing.results(om)

    electricity_bus = views.node(results, 'electricity')
    my_results = electricity_bus['sequences'].sum(axis=0).to_dict()
    storage = energysystem.groups['storage']
    my_results['storage_invest'] = results[(storage, None)]['scalars'][
        'invest']
