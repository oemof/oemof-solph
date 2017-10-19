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
from oemof.solph import (EnergySystem, Bus, Source, Sink, Flow, BinaryFlow,
                         OperationalModel, LinearTransformer, components)

timeindex = pd.date_range('1/1/2017', periods=168, freq='H')

energysystem = EnergySystem(timeindex=timeindex)

##########################################################################
# data
##########################################################################
# Read data file
full_filename = os.path.join(os.path.dirname(__file__),
                             "timeseries.csv")
timeseries = pd.read_csv(full_filename, sep=",")

##########################################################################
# Create oemof objects
##########################################################################

bel = Bus(label="bel")

bgas = Bus(label="bgas")

bth = Bus(label="bth")

Source(label="gas",
       outputs={bgas: Flow(variable_costs=35)})

LinearTransformer(label='boiler',
                  inputs={
                      bgas: Flow()},
                  outputs={
                      bth: Flow(nominal_value=300, min=0.2,
                                binary=BinaryFlow())},
                  conversion_factors={bth: 0.9})

Sink(label='demand_th',
     inputs={
         bth: Flow(actual_value=timeseries['demand_th'],
                   fixed=True, nominal_value=500)})

Sink(label='spot_el',
     inputs={
         bel: Flow(variable_costs=timeseries['price_el'])})


components.GenericStorage(
    label='storage_th',
    inputs={
        bth: Flow()},
    outputs={
        bth: Flow()},
    nominal_capacity=1000,
    capacity_loss=0.00,
    initial_capacity=0.5,
    nominal_input_capacity_ratio=1/61,
    nominal_output_capacity_ratio=1/61)

##########################################################################
# Create model and solve
##########################################################################

om = OperationalModel(energysystem)
# om.write(filename, io_options={'symbolic_solver_labels': True})

om.solve(solver='cbc', solve_kwargs={'tee': True})

results = processing.results(om)

graph = graph(energysystem, om, plot=True)