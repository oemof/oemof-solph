# -*- coding: utf-8 -*-
"""
Example that shows the parameter `balanced` of `GenericStorage`.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_scripts/test_solph/
test_generic_offsettransformer/test_generic_offsettransformer.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import os
import pandas as pd
import oemof.solph as solph
from oemof.outputlib import processing
try:
    from matplotlib import pyplot as plt
except ImportError:
    print("Install matplotlib to see the plots.")
    plt = None


DATA = [
    {'name': 'unbalanced', 'initial_storage_level': 0.2, 'balanced': False},
    {'name': 'unbalanced_None', 'initial_storage_level': None,
     'balanced': False},
    {'name': 'balanced', 'initial_storage_level': 0.2, 'balanced': True},
    {'name': 'balanced_None', 'initial_storage_level': None, 'balanced': True}]

PARAMETER = {
    'el_price': 10,
    'sh_price': 5,
    'nominal_storage_capacity': 7
}


def storage_example():
    # read time series
    timeseries = pd.read_csv(
        os.path.join(os.path.dirname(__file__), 'storage_data.csv'))
    # create an energy system
    idx = pd.date_range('1/1/2017', periods=len(timeseries), freq='H')
    es = solph.EnergySystem(timeindex=idx)

    for data_set in DATA:
        name = data_set['name']

        # power bus
        bel = solph.Bus(label='bel_{0}'.format(name))
        es.add(bel)

        es.add(solph.Source(
            label='source_el_{0}'.format(name),
            outputs={bel: solph.Flow(variable_costs=PARAMETER['el_price'])}))

        es.add(solph.Source(
            label='pv_el_{0}'.format(name), outputs={bel: solph.Flow(
                actual_value=timeseries['pv_el'],
                nominal_value=1, fixed=True)}))

        es.add(solph.Sink(
            label='demand_el_{0}'.format(name),
            inputs={bel: solph.Flow(
                actual_value=timeseries['demand_el'],
                nominal_value=1, fixed=True)}))

        es.add(solph.Sink(label='shunt_el_{0}'.format(name),
                          inputs={bel: solph.Flow(
                              variable_costs=PARAMETER['sh_price'])}))

        # Electric Storage
        es.add(solph.components.GenericStorage(
            label='storage_elec_{0}'.format(name),
            nominal_storage_capacity=PARAMETER['nominal_storage_capacity'],
            inputs={bel: solph.Flow()},
            outputs={bel: solph.Flow()},
            initial_storage_level=data_set['initial_storage_level'],
            balanced=data_set['balanced']))
    
    # create an optimization problem and solve it
    om = solph.Model(es)
    
    # solve model
    om.solve(solver='cbc')
    
    # create result object
    results = processing.results(om)

    flows = [x for x in results if x[1] is not None]
    components = [x for x in results if x[1] is None]

    storage_cap = pd.DataFrame()
    costs = pd.Series()
    balance = pd.Series()

    for flow in [x for x in flows if 'source_el' in x[0].label]:
        name = '_'.join(flow[0].label.split('_')[2:])
        print(name, float(results[flow]['sequences'].sum()))
        costs[name] = float(results[flow]['sequences'].sum() *
                            PARAMETER['el_price'])

    for flow in [x for x in flows if 'shunt_el' in x[1].label]:
        name = '_'.join(flow[1].label.split('_')[2:])
        costs[name] += float(results[flow]['sequences'].sum() *
                             PARAMETER['sh_price'])

    storages = [x[0] for x in components if 'storage' in x[0].label]
    idx = results[storages[0], None]['sequences']['capacity'].index
    last = idx[-1]
    prev = idx[0] - 1
    for s in storages:
        name = s.label
        storage_cap[name] = results[s, None]['sequences']['capacity']
        storage_cap.loc[prev, name] = results[s, None]['scalars']['init_cap']
        balance[name] = (storage_cap.loc[last][name] -
                         storage_cap.loc[prev][name])

    if plt is not None:
        storage_cap.plot(drawstyle="steps-mid", subplots=False, sharey=True)
        storage_cap.plot(drawstyle="steps-mid", subplots=True, sharey=True)
        costs.plot(kind='bar', ax=plt.subplots()[1])
        balance.plot(kind='bar', linewidth=1, edgecolor='#000000',
                     ax=plt.subplots()[1])
        plt.show()

    print(storage_cap)
    print(costs)
    print(balance)
