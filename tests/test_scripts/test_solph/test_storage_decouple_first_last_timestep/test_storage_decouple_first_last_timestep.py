# -*- coding: utf-8 -*-
"""
Unit test for parameter `balanced` of `GenericStorage`.

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


def test_storage_decouple():
    # read sequence data
    full_filename = os.path.join(os.path.dirname(__file__), 'gsdtf.csv')
    data = pd.read_csv(full_filename)
    
    # select periods
    periods = 3
    
    # create an energy system
    idx = pd.date_range('1/1/2017', periods=periods, freq='H')
    es = solph.EnergySystem(timeindex=idx)
    #Node.registry = es
    
    # power bus
    bel = solph.Bus(label='bel')
    
    source_el = solph.Source(label='source_el',
                             outputs={bel: solph.Flow(variable_costs=data['price_el'])})
    
    pv_el = solph.Source(label='pv_el',
                         outputs={bel: solph.Flow(actual_value=data['pv_el'],
                                                  nominal_value=1,
                                                  fixed=True)})
    
    demand_el = solph.Sink(label='demand_el',
                           inputs={bel: solph.Flow(actual_value=data['demand_el'],
                                                   nominal_value=1,
                                                   fixed=True)})
    
    shunt_el = solph.Sink(label='shunt_el',
                          inputs={bel: solph.Flow()})
    
    # Electric Storage
    storage_elec = solph.components.GenericStorage(label='storage_elec',
                                                   nominal_storage_capacity = 10,
                                                   inputs={bel: solph.Flow(nominal_value = 10)},
                                                   outputs={bel: solph.Flow(nominal_value = 10)},
                                                   loss_rate = 0.00,
                                                   initial_storage_level = 0.2,
                                                   balanced = False,
                                                   inflow_conversion_factor = 1,
                                                   outflow_conversion_factor = 1)
    
    es.add(bel, source_el, pv_el, demand_el, shunt_el, storage_elec)
    
    # create an optimization problem and solve it
    om = solph.Model(es)
    
    # solve model
    om.solve(solver='cbc')
    
    # create result object
    results = processing.results(om)
    
    data = views.node(results, 'bel')['sequences'].sum(axis=0).to_dict()
    
    test_dict = {
        (('bel', 'demand_el'), 'flow'): 15.0,
        (('bel', 'shunt_el'), 'flow'): 0.0,
        (('bel', 'storage_elec'), 'flow'): 3.0,
        (('pv_el', 'bel'), 'flow'): 8.0,
        (('source_el', 'bel'), 'flow'): 5.0,
        (('storage_elec', 'bel'), 'flow'): 5.0}
    
    for key in test_dict.keys():
            eq_(int(round(data[key])), int(round(test_dict[key])))



def test_storage_couple():
    # read sequence data
    full_filename = os.path.join(os.path.dirname(__file__), 'gsdtf.csv')
    data = pd.read_csv(full_filename)
    
    # select periods
    periods = 3
    
    # create an energy system
    idx = pd.date_range('1/1/2017', periods=periods, freq='H')
    es = solph.EnergySystem(timeindex=idx)
    #Node.registry = es
    
    # power bus
    bel = solph.Bus(label='bel')
    
    source_el = solph.Source(label='source_el',
                             outputs={bel: solph.Flow(variable_costs=data['price_el'])})
    
    pv_el = solph.Source(label='pv_el',
                         outputs={bel: solph.Flow(actual_value=data['pv_el'],
                                                  nominal_value=1,
                                                  fixed=True)})
    
    demand_el = solph.Sink(label='demand_el',
                           inputs={bel: solph.Flow(actual_value=data['demand_el'],
                                                   nominal_value=1,
                                                   fixed=True)})
    
    shunt_el = solph.Sink(label='shunt_el',
                          inputs={bel: solph.Flow()})
    
    # Electric Storage
    storage_elec = solph.components.GenericStorage(label='storage_elec',
                                                   nominal_storage_capacity = 10,
                                                   inputs={bel: solph.Flow(nominal_value = 10)},
                                                   outputs={bel: solph.Flow(nominal_value = 10)},
                                                   loss_rate = 0.00,
                                                   initial_storage_level = 0.2,
                                                   balanced = True,
                                                   inflow_conversion_factor = 1,
                                                   outflow_conversion_factor = 1)
    
    es.add(bel, source_el, pv_el, demand_el, shunt_el, storage_elec)
    
    # create an optimization problem and solve it
    om = solph.Model(es)
    
    # solve model
    om.solve(solver='cbc')
    
    # create result object
    results = processing.results(om)
    
    data = views.node(results, 'bel')['sequences'].sum(axis=0).to_dict()
    
    test_dict = {
        (('bel', 'demand_el'), 'flow'): 15.0,
        (('bel', 'shunt_el'), 'flow'): 0.0,
        (('bel', 'storage_elec'), 'flow'): 3.0,
        (('pv_el', 'bel'), 'flow'): 8.0,
        (('source_el', 'bel'), 'flow'): 7.0,
        (('storage_elec', 'bel'), 'flow'): 3.0}
    
    for key in test_dict.keys():
            eq_(int(round(data[key])), int(round(test_dict[key])))