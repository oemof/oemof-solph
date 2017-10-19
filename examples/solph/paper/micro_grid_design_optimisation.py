# -*- coding: utf-8 -*-
"""
Example from the SDEWES conference paper:

Simon Hilpert, Cord Kaldemeyer, Uwe Krien, Stephan Günther (2017).
'Solph - An Open Multi Purpose Optimisation Library for Flexible
         Energy System Analysis'. Paper presented at SDEWES Conference,
         Dubrovnik.

"""
import os
import pandas as pd

from oemof.outputlib.graph_tools import graph
from oemof.outputlib import processing, views
from oemof.solph import (EnergySystem, Bus, Source, Sink, Flow,
                         OperationalModel, Investment, components)
from oemof.tools import economics

timeindex = pd.date_range('1/1/2017', periods=168, freq='H')

energysystem = EnergySystem(timeindex=timeindex)

#################################################################
# data
#################################################################
# Read data file
full_filename = os.path.join(os.path.dirname(__file__),
                             'timeseries.csv')
timeseries = pd.read_csv(full_filename, sep=',')

costs = {'pp_wind': {
                'fix': 25,
                'epc': economics.annuity(capex=1000, n=20, wacc=0.05)},
         'pp_pv': {
             'fix': 20,
             'epc': economics.annuity(capex=750, n=20, wacc=0.05)},
         'pp_diesel': {
             'fix': 10,
             'epc': economics.annuity(capex=300, n=10, wacc=0.05),
             'var': 30},
         'pp_bio': {
             'fix': 10,
             'epc': economics.annuity(capex=1000, n=10, wacc=0.05),
             'var': 50},
         'storage': {
             'fix': 8,
             'epc': economics.annuity(capex=1500, n=10, wacc=0.05),
             'var': 0}}
#################################################################
# Create oemof object
#################################################################

bel = Bus(label='micro_grid')

Sink(label='excess',
     inputs={bel: Flow()})

Source(label='pp_wind',
       outputs={
           bel: Flow(nominal_value=None, fixed=True,
                     actual_value=timeseries['wind'],
                     fixed_costs=costs['pp_wind']['fix'],
                     investment=Investment(ep_costs=costs['pp_wind']['epc']))})

Source(label='pp_pv',
       outputs={
           bel: Flow(nominal_value=None, fixed=True,
                     actual_value=timeseries['pv'],
                     fixed_costs=costs['pp_pv']['fix'],
                     investment=Investment(ep_costs=costs['pp_wind']['epc']))})

Source(label='pp_diesel',
       outputs={
           bel: Flow(nominal_value=None,
                     fixed_costs=costs['pp_diesel']['fix'],
                     variable_costs=costs['pp_diesel']['var'],
                     investment=Investment(ep_costs=costs['pp_diesel']['epc']))})

Source(label='pp_bio',
       outputs={
           bel: Flow(nominal_value=None,
                     fixed_costs=costs['pp_bio']['fix'],
                     variable_costs=costs['pp_bio']['var'],
                     summed_max=300e3,
                     investment=Investment(ep_costs=costs['pp_bio']['epc']))})

Sink(label='demand_el',
     inputs={
         bel: Flow(actual_value=timeseries['demand_el'],
                   fixed=True, nominal_value=500)})

components.GenericStorage(
    label='storage',
    inputs={
        bel: Flow()},
    outputs={
        bel: Flow()},
    capacity_loss=0.00,
    initial_capacity=0.5,
    nominal_input_capacity_ratio=1/6,
    nominal_output_capacity_ratio=1/6,
    inflow_conversion_factor=0.95,
    outflow_conversion_factor=0.95,
    fixed_costs=costs['storage']['fix'],
    investment=Investment(ep_costs=costs['storage']['epc']))

#################################################################
# Create model and solve
#################################################################

om = OperationalModel(energysystem)
# om.write(filename, io_options={'symbolic_solver_labels': True})

om.solve(solver='cbc', solve_kwargs={'tee': True})

results = processing.results(om)

views.node(results, 'storage')

graph = graph(energysystem, om, plot=True, layout='neato', node_size=3000,
              node_color={'micro_grid': '#7EC0EE'})

