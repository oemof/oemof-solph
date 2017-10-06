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
periods = len(data[1:24])

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)

# resources
bgas = solph.Bus(label='bgas')

rgas = solph.Source(label='rgas', outputs={bgas: solph.Flow()})

# heat
bth = solph.Bus(label='bth')

source_th = solph.Source(label='source_th', outputs={bth: solph.Flow(
                         variable_costs=1000)})

demand_th = solph.Sink(label='demand_th', inputs={bth: solph.Flow(fixed=True,
                       actual_value=data['demand_el'], nominal_value=100)})

# power
bel = solph.Bus(label='bel')

source_el = solph.Source(label='source_el', outputs={bel: solph.Flow(
                         variable_costs=1000)})

demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(fixed=True,
                       actual_value=data['demand_el'], nominal_value=187)})

ccgt = solph.custom.GenericCHP(label='pp_generic_chp',
                               inputs={bgas: solph.Flow()},
                               outputs={bel: solph.Flow(nominal_value=187,
                                                        variable_costs=300),
                                        bth: solph.Flow()},
                               P_max_woDH=187, P_min_woDH=80,
                               Eta_el_max_woDH=0.49, Eta_el_min_woDH=0.41,
                               Q_CW_min=28,
                               electrical_bus=bel,
                               heat_bus=bth,
                               Beta=0.21)

# create a optimization problem and solve it
om = solph.OperationalModel(es)

# debugging
#om.pprint()
om.write('my_model.lp', io_options={'symbolic_solver_labels': True})

# solve model
#om.solve(solver='gurobi', solve_kwargs={'tee': True})

# create result object
results = processing.results(es, om)

results[(ccgt,)]['sequences']['PQ'] = \
    results[(ccgt,)]['sequences']['P'] / results[(ccgt,)]['sequences']['Q']

print(results[(ccgt,)]['sequences'].describe())
print(results[(ccgt,)]['sequences'].head())

# results[(ccgt,)]['sequences'].plot(kind='line', drawstyle='steps-post')
# plt.show()

# # plot results
# data = views.node(results, 'bel')
# data['sequences'][(('bel', 'demand'), 'flow')] = \
#     data['sequences'][(('bel', 'demand'), 'flow')] * -1
# ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
# ax.set_title('Dispatch')
# ax.set_xlabel('')
# ax.set_ylabel('Power in MW')
# plt.show()
