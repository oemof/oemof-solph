# -*- coding: utf-8 -*-
"""
Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.
"""

import matplotlib.pyplot as plt
import pandas as pd
import oemof.solph as solph
from oemof.outputlib import processing, views


# data with sequences
data = pd.read_csv('data.csv', sep=",")

# print(data['demand_el'], len(data))

# create an energy system
idx = pd.date_range('1/1/2017', periods=len(data), freq='H')
es = solph.EnergySystem(timeindex=idx)

# create busses
bgas = solph.Bus(label='bgas')
bel = solph.Bus(label='bel')

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

# create generic CHP component
ccgt = solph.custom.GenericCHP(label='pp_generic_chp',
                               inputs={bgas: solph.Flow()},
                               outputs={bel: solph.Flow()},
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

# plot results
data = views.node(results, 'bel')
data['sequences'][(('bel', 'demand'), 'flow')] = \
    data['sequences'][(('bel', 'demand'), 'flow')] * -1
ax = data['sequences'].plot(kind='line', drawstyle='steps-post')
ax.set_title('Dispatch')
ax.set_xlabel('')
ax.set_ylabel('Power in MW')
plt.show()
