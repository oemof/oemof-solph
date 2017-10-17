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
periods = len(data[0:24])

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)

# resources
bgas = solph.Bus(label='bgas')

rgas = solph.Source(label='rgas', outputs={bgas: solph.Flow()})

# heat
bth = solph.Bus(label='bth')

source_th = solph.Source(label='source_th',
                         outputs={bth: solph.Flow(variable_costs=1000)})

demand_th = solph.Sink(label='demand_th', inputs={bth: solph.Flow(fixed=True,
                       actual_value=data['demand_el'], nominal_value=100)})

# power
bel = solph.Bus(label='bel')

demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
                       variable_costs=data['price_el'])})

pp_gas = solph.LinearTransformer(label='pp_gas',
                                 inputs={bgas: solph.Flow()},
                                 outputs={bel: solph.Flow(nominal_value=41,
                                                          variable_costs=40)},
                                 conversion_factors={bel: 0.50})

# generic chp
ccgt = solph.custom.GenericCHP(label='pp_generic_chp',
                               fuel_input={bgas: solph.Flow()},
                               electrical_output={bel: solph.Flow(
                                                     P_max_woDH=[217.35 for p in range(0, periods)],
                                                     P_min_woDH=[89.10 for p in range(0, periods)],
                                                     Eta_el_max_woDH=[0.57 for p in range(0, periods)],
                                                     Eta_el_min_woDH=[0.47 for p in range(0, periods)])},
                               heat_output={bth: solph.Flow(Q_CW_min=[27.85 for p in range(0, periods)], variable_costs=1)},
                               Beta=[0.12 for p in range(0, periods)],
                               fixed_costs=300)

# create an optimization problem and solve it
om = solph.OperationalModel(es)

# debugging
#om.pprint()
#om.write('my_model.lp', io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver='cbc', solve_kwargs={'tee': True})

# create result object
results = processing.results(om)

# store as csv
data = results[(ccgt,)]['sequences'].to_csv('CCET.csv')

# plot CCET (line)
data = results[(ccgt,)]['sequences']
ax = data.plot(kind='line', drawstyle='steps-post', grid=True)
ax.set_xlabel('Time')
ax.set_ylabel('(MW)')
plt.show()

# plot CCET (scatter)
data = results[(ccgt,)]['sequences']
ax = data.plot(kind='scatter', x='Q', y='P', grid=True)
ax.set_xlabel('Q (MW)')
ax.set_ylabel('P (MW)')
plt.show()

# # plot bus
# data = views.node(results, 'bel')
# ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
# ax.set_title('Dispatch')
# ax.set_xlabel('')
# ax.set_ylabel('Power (MW)')
# plt.show()

# # plot bus
# data = views.node(results, 'bth')
# ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
# ax.set_title('Dispatch')
# ax.set_xlabel('')
# ax.set_ylabel('Heat flow (MW)')
# plt.show()
