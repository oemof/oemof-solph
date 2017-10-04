# -*- coding: utf-8 -*-
"""
Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.
"""

import matplotlib.pyplot as plt
import pandas as pd
import oemof.solph as solph
from oemof.outputlib import processing, views


# read sequence data
data = pd.read_csv('data.csv', sep=",")

# select periods
periods = len(data[1:24*31])

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)

# create busses
bgas = solph.Bus(label='bgas')
bel = solph.Bus(label='bel')
bth = solph.Bus(label='bth')

# create source object representing the natural gas commodity
rgas = solph.Source(label='rgas', outputs={bgas: solph.Flow()})

# create simple sink object representing the electrical demand
demand = solph.Sink(label='demand', inputs={bel: solph.Flow(fixed=True,
                    actual_value=data['demand_el'], nominal_value=100)})

# create simple transformer object representing a gas power plant
pp_gas = solph.LinearTransformer(label='pp_gas', inputs={bgas: solph.Flow()},
                                 outputs={bel: solph.Flow(nominal_value=300,
                                                          variable_costs=50)},
                                 conversion_factors={bel: 0.50})

# create storage object
storage = solph.custom.GenericStorage(
    label='storage',
    inputs={bel: solph.Flow(variable_costs=0)},
    outputs={bel: solph.Flow(variable_costs=0)},
    capacity_loss=0.0, nominal_capacity=50,
    nominal_input_capacity_ratio=1/6,
    nominal_output_capacity_ratio=1/6,
    inflow_conversion_factor=0.9, outflow_conversion_factor=0.9
)

# create generic CHP component
ccgt = solph.custom.GenericCHP(label='pp_generic_chp',
                               inputs={bgas: solph.Flow()},
                               outputs={bel: solph.Flow(variable_costs=40),
                                        bth: solph.Flow(variable_costs=0)},
                               P_el_max=100,
                               P_el_min=50,
                               Q_el_min=50,
                               Eta_el_max=0.56,
                               Eta_el_min=0.46,
                               Beta=0.227)

# create a optimization problem and solve it
om = solph.OperationalModel(es)
om.solve(solver='gurobi', solve_kwargs={'tee': True})

# create result object
results = processing.results(es, om)

# # plot results
# data = views.node(results, 'bel')
# data['sequences'][(('bel', 'demand'), 'flow')] = \
#     data['sequences'][(('bel', 'demand'), 'flow')] * -1
# ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
# ax.set_title('Dispatch')
# ax.set_xlabel('')
# ax.set_ylabel('Power in MW')
# plt.show()
