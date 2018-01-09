# -*- coding: utf-8 -*-

"""
General description:
---------------------

The example models the following energy system:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |


"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

from nose.tools import eq_
from oemof.tools import economics

import oemof.solph as solph
from oemof.network import Node
from oemof.outputlib import processing, views

import logging
import os
import pandas as pd


def test_optimise_storage_size(filename="storage_investment.csv", solver='cbc'):

    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2012', periods=400, freq='H')

    energysystem = solph.EnergySystem(timeindex=date_time_index)
    Node.registry = energysystem

    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data = pd.read_csv(full_filename, sep=",")

    # Buses
    bgas = solph.Bus(label="natural_gas")
    bel = solph.Bus(label="electricity")

    # Sinks
    solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})

    solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    # Sources
    solph.Source(label='rgas', outputs={bgas: solph.Flow(
        nominal_value=194397000 * 400 / 8760, summed_max=1)})

    solph.Source(label='wind', outputs={bel: solph.Flow(
        actual_value=data['wind'], nominal_value=1000000, fixed=True)})

    solph.Source(label='pv', outputs={bel: solph.Flow(
        actual_value=data['pv'], nominal_value=582000, fixed=True)})

    # Transformer
    solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
        conversion_factors={bel: 0.58})

    # Investment storage
    epc = economics.annuity(capex=1000, n=20, wacc=0.05)
    solph.components.GenericStorage(
        label='storage',
        inputs={bel: solph.Flow(variable_costs=10e10)},
        outputs={bel: solph.Flow(variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=solph.Investment(ep_costs=epc),
    )

    # Solve model
    om = solph.Model(energysystem)
    om.solve(solver=solver)
    energysystem.results['main'] = processing.results(om)
    energysystem.results['meta'] = processing.meta_results(om)

    # Check dump and restore
    energysystem.dump()
    energysystem = solph.EnergySystem()
    energysystem.restore()

    # Results
    results = energysystem.results['main']
    meta = energysystem.results['meta']

    electricity_bus = views.node(results, 'electricity')
    my_results = electricity_bus['sequences'].sum(axis=0).to_dict()
    storage = energysystem.groups['storage']
    my_results['storage_invest'] = results[(storage, None)]['scalars']['invest']

    stor_invest_dict = {
        'storage_invest': 2046851,
        (('electricity', 'demand'), 'flow'): 105867395,
        (('electricity', 'excess_bel'), 'flow'): 211771291,
        (('electricity', 'storage'), 'flow'): 2350931,
        (('pp_gas', 'electricity'), 'flow'): 5148414,
        (('pv', 'electricity'), 'flow'): 7488607,
        (('storage', 'electricity'), 'flow'): 1880745,
        (('wind', 'electricity'), 'flow'): 305471851}

    for key in stor_invest_dict.keys():
        eq_(int(round(my_results[key])), int(round(stor_invest_dict[key])))

    # Solver results
    eq_(str(meta['solver']['Termination condition']), 'optimal')
    eq_(meta['solver']['Error rc'], 0)
    eq_(str(meta['solver']['Status']), 'ok')

    # Problem results
    eq_(meta['problem']['Lower bound'], 4.2316758e+17)
    eq_(meta['problem']['Upper bound'], 4.2316758e+17)
    eq_(meta['problem']['Number of variables'], 2804)
    eq_(meta['problem']['Number of constraints'], 2805)
    eq_(meta['problem']['Number of nonzeros'], 7606)
    eq_(meta['problem']['Number of objectives'], 1)
    eq_(str(meta['problem']['Sense']), 'minimize')

    # Objective function
    eq_(round(meta['objective']), 423167578261665280)
