# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 10:16:55 2019

@author: rad39217
"""

import oemof.solph as solph
from oemof.outputlib import processing, views

import os
import pandas as pd

import matplotlib.pyplot as plt


order = 73        

zeitindex = pd.date_range('15/3/2019', periods=order, freq='H') 

sys = solph.EnergySystem(timeindex=zeitindex)

pfad_csv = os.path.join(os.path.dirname(__file__), 'Speichertest2.csv') 
vorgaben = pd.read_csv(pfad_csv, sep=';', decimal=',')

sikosten = vorgaben['erloes']
sokosten = vorgaben['kosten']

elbus = solph.Bus(label='elbus')
sys.add(elbus)
gabus = solph.Bus(label='gabus')
sys.add(gabus)
wbus = solph.Bus(label='wbus')
sys.add(wbus)

sys.add(solph.Sink(label='eexit', inputs={elbus: solph.Flow()}))  
sys.add(solph.Sink(label='wexit', inputs={wbus: solph.Flow()})) 


sys.add(solph.Sink(label='eigenbedarf', inputs={elbus: solph.Flow(
        actual_value=vorgaben['aus'], fixed=True, nominal_value=500)}))

sys.add(solph.Source(label='Backup', outputs={elbus: solph.Flow(
    variable_costs=28)}))

sys.add(solph.Source(label='gas', outputs={gabus: solph.Flow(
    variable_costs=9)}))

sys.add(solph.Transformer(
    label='BHKW',
    inputs={gabus: solph.Flow()},
    outputs={elbus: solph.Flow(
                   investment=solph.Investment(),
                   invmax=59000000,  # invmax=60000000,
                   # invmin=64,
                   offset=10000,
                   slope=355),
             wbus: solph.Flow()},
    conversion_factors={elbus: 0.5, wbus: 0.35}))

lsg = solph.Model(sys)
lsg.solve()

sys.results['main'] = processing.results(lsg)
sys.results['meta'] = processing.meta_results(lsg)


ergebnisse1 = sys.results['main']
ele = views.node(ergebnisse1, 'elbus')
gas = views.node(ergebnisse1, 'gabus')
waerme = views.node(ergebnisse1, 'wbus')

# ergebnisse plotten

ele['sequences'].plot(kind='line', drawstyle='steps-post')
plt.show()
waerme['sequences'].plot(kind='line', drawstyle='steps-post')
plt.show()
gas['sequences'].plot(kind='line', drawstyle='steps-post')
plt.show()
