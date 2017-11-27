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
from oemof.solph import (EnergySystem, Bus, Source, Sink, Flow, NonConvex,
                         OperationalModel, LinearTransformer, components)
from oemof.solph.overarching_constraints import emission_limit

timeindex = pd.date_range('1/1/2017', periods=5, freq='H')

energysystem = EnergySystem(timeindex=timeindex)

##########################################################################
# data
##########################################################################
# Read data file
full_filename = os.path.join(os.path.dirname(__file__),
                             'timeseries.csv')
timeseries = pd.read_csv(full_filename, sep=',')


##########################################################################
# Create oemof object
##########################################################################

bel = Bus(label='bel')

Sink(label='demand_el',
     inputs={
         bel: Flow(actual_value=timeseries['demand_el'],
                   fixed=True, nominal_value=100)})

Source(label='pp_wind',
       outputs={
           bel: Flow(nominal_value=15, fixed=True,
                     actual_value=timeseries['wind'])})

Source(label='pp_pv',
       outputs={
           bel: Flow(nominal_value=10, fixed=True,
                     actual_value=timeseries['pv'])})

Source(label='pp_gas',
       outputs={
           bel: Flow(nominal_value=30, nonconvex=NonConvex(),
                     variable_costs=60,
                     negative_gradient=0.05,
                     positive_gradient=0.05)})

Source(label='pp_bio',
       outputs={
           bel: Flow(nominal_value=7,
                     variable_costs=100)})

components.GenericStorage(
    label='storage_el',
    inputs={
        bel: Flow()},
    outputs={
        bel: Flow()},
    nominal_capacity=10,
    nominal_input_capacity_ratio=1/10,
    nominal_output_capacity_ratio=1/10,
)

# heat componentes
bth = Bus(label='bth')

bgas = Bus(label='bgas')

Source(label='gas',
       outputs={
           bgas: Flow()})


Sink(label='demand_th',
     inputs={
         bel: Flow(actual_value=timeseries['demand_th'],
                   fixed=True, nominal_value=100)})

LinearTransformer(label='pth',
                  inputs={
                      bel: Flow()},
                  outputs={
                      bth: Flow()},
                  conversion_factors={bth: 0.99})

LinearTransformer(label='chp',
                  inputs={
                      bgas: Flow(variable_costs=20)},
                  outputs={
                      bel: Flow(nominal_value=40),
                      bth: Flow()},
                  conversion_factors={bel: 0.35,
                                      bth: 0.4})

Source(label='boiler_bio',
       outputs={bel: Flow(nominal_value=100, variable_costs=60)})

components.GenericStorage(
    label='storage_th',
    inputs={
        bth: Flow()},
    outputs={
        bth: Flow()},
    nominal_capacity=30,
    nominal_input_capacity_ratio=1/8,
    nominal_output_capacity_ratio=1/8,
)

##########################################################################
# Create model and solve
##########################################################################

om = OperationalModel(energysystem)
emission_limit(om, flows=om.flows, limit=954341)

om.write('test_nc.lp', io_options={'symbolic_solver_labels': True})

om.solve(solver='cbc', solve_kwargs={'tee': True})

results = processing.results(om)


graph = graph(energysystem, om, plot=True, layout='neato', node_size=3000,
              node_color={'bel': '#7EC0EE', 'bgas': '#eeac7e', 'bth': '#cd3333'})
