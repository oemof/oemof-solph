# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 08:53:42 2018

@author: rad39217

Beispiel fuer den Speicher - OffsetInvestor mit
"""

import oemof.solph as solph
from oemof.outputlib import processing, views

import os
import pandas as pd

import matplotlib.pyplot as plt


order = 66        

zeitindex = pd.date_range('15/3/2019', periods=order, freq='H') 

storesys = solph.EnergySystem(timeindex=zeitindex)

pfad_csv = os.path.join(os.path.dirname(__file__), 'Speichertest_inv.csv') 

vorgaben = pd.read_csv(pfad_csv, sep=';', decimal=',')

sikosten = 3
sokosten = vorgaben['kosten']

elbus = solph.custom.ElectricalBus(label='elbus')
storesys.add(elbus)

storesys.add(solph.Sink(label='exit', inputs={elbus: solph.Flow(
        variable_costs=sikosten)}))

storesys.add(solph.Sink(label='eigenbedarf', inputs={elbus: solph.Flow(
        actual_value=vorgaben['aus'], fixed=True, nominal_value=500)}))

storesys.add(solph.Source(label='Backup', outputs={elbus: solph.Flow(
        variable_costs=sokosten)}))

storesys.add(solph.Source(label='pv', outputs={elbus: solph.Flow(
        actual_value=vorgaben['ein'], fixed=True, nominal_value=350)}))

# Speicher und investment Speicher unterschiedlich erzeugen
# Speicher fuer oemof
# V3 normal einfacher speicher mit vordefinierter Groeße
'''
speicher = solph.components.GenericStorage(
        nominal_storage_capacity=1095,
        label='speicher',
        
        inputs={elbus: solph.Flow(nominal_value=333)},
        outputs={elbus: solph.Flow(nominal_value=333, variable_costs=0.05)},
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=vorgaben['eta'],
        outflow_conversion_factor=(vorgaben['eta']),
        )
'''
# investment speicher Version original oemof
'''
speicher = solph.components.GenericStorage(
        
        label='speicher',
        investment = solph.Investment(ep_costs = 29),
        inputs={elbus: solph.Flow()},
        outputs={elbus: solph.Flow()},
        invest_relation_input_capacity=1/3,
        invest_relation_output_capacity=1/3,
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=vorgaben['eta'],
        outflow_conversion_factor=(vorgaben['eta']),
        )

'''
# v3 offset investment speicher mit korrelation zwischen Leistungen und Energie
'''
speicher = solph.components.GenericStorage(
        label='speicher',
        investment = solph.Investment(),
        minimum = 1,
        potenzial = 50000000,
        offset = 50,
        slope = 22,
        inputs={elbus: solph.Flow()},
        outputs={elbus: solph.Flow()},
        invest_relation_input_capacity=1/3,
        invest_relation_output_capacity=1/3,
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=vorgaben['eta'],
        outflow_conversion_factor=(vorgaben['eta']),
        )
'''
# offset investment speicher ohne korrelation zwischen leistungen und energie

speicher = solph.components.GenericStorage(
        label='speicher',
        investment=solph.Investment(),
        minimum=1,
        
        # es wird investiert (15 nullen)
        potenzial=5000000000000000,
        offset=30,
        slope=20,
        
        # es wird nicht investiert (17 nullen)
        # potenzial = 500000000000000000,
        # offset = 30,
        # slope = 20,
        
        # es wird investiert (19 nullen)
        # potenzial = 50000000000000000000,
        # offset = 30,
        # slope = 25,
        inputs={elbus: solph.Flow(
                investment=solph.Investment(),
                offset=20,
                slope=5,
                invmax=2000000)},
        outputs={elbus: solph.Flow(
                investment=solph.Investment(),
                offset=20,
                slope=10,
                invmax=1000)},
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=vorgaben['eta'],
        outflow_conversion_factor=(vorgaben['eta']),
        )

storesys.add(speicher)

lsg = solph.Model(storesys)

lsg.solve()

storesys.results['main'] = processing.results(lsg)
storesys.results['meta'] = processing.meta_results(lsg)

storesys.dump(dpath=os.path.dirname(__file__), filename='storetest.oemof')

storesys2 = solph.EnergySystem()

storesys2.restore(dpath=os.path.dirname(__file__), filename='storetest.oemof')

ergebnisse = storesys2.results['main']

speicherergebnisse = views.node(ergebnisse, 'speicher')

stromergebnisse = views.node(ergebnisse, 'elbus')

# ergebnisse plotten

speicherergebnisse['sequences'].plot()
plt.show()
stromergebnisse['sequences'].plot(kind='line', drawstyle='steps-post')
plt.show()
