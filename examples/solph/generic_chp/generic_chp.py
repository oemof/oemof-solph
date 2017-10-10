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
periods = len(data[1:24*365])

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)

# resources
bgas = solph.Bus(label='bgas')

rgas = solph.Source(label='rgas', outputs={bgas: solph.Flow()})

# heat
bth = solph.Bus(label='bth')

source_th = solph.Sink(label='source_th',
                       outputs={bth: solph.Flow(variable_costs=1000)})

demand_th = solph.Sink(label='demand_th', inputs={bth: solph.Flow(fixed=True,
                       actual_value=data['demand_el'], nominal_value=100)})

# power
bel = solph.Bus(label='bel')

demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
                       variable_costs=data['price_el'])})

# # test sequence conversion
# ccgt = solph.custom.GenericCHP(label='pp_generic_chp',
#                                inputs={bgas: solph.Flow()},
#                                outputs={bel: solph.Flow(variable_costs=10),
#                                         bth: solph.Flow()},
#                                P_max_woDH=[187 for p in range(0, periods)],
#                                P_min_woDH=[80 for p in range(0, periods)],
#                                Eta_el_max_woDH=[0.57 for p in range(0, periods)],
#                                Eta_el_min_woDH=[0.54 for p in range(0, periods)],
#                                Q_CW_min=[28 for p in range(0, periods)],
#                                Beta=[0.12 for p in range(0, periods)],
#                                electrical_bus=bel, heat_bus=bth)

# nicer API?
ccgt = solph.custom.GenericCHP(label='pp_generic_chp',
                               fuel_bus={bgas: solph.Flow()},
                               electrical_bus={bel: solph.Flow(
                                                     P_max_woDH=[187],
                                                     P_min_woDH=[80],
                                                     Eta_el_max_woDH=[0.57],
                                                     Eta_el_min_woDH=[0.54])},
                               heat_bus={bth: solph.Flow(Q_CW_min=[28])},
                               Beta=0.12)


print(ccgt.alphas)

#print([k for k in ccgt.outputs.keys()])
# # create an optimization problem and solve it
# om = solph.OperationalModel(es)
#
# # debugging
# #om.pprint()
# om.write('my_model.lp', io_options={'symbolic_solver_labels': True})
#
# # solve model
# om.solve(solver='gurobi', solve_kwargs={'tee': True})
#
# # create result object
# results = processing.results(es, om)
#
# results[(ccgt,)]['sequences'].to_csv('CCET.csv')
#
# results[(ccgt,)]['sequences']['PQ'] = \
#     results[(ccgt,)]['sequences']['P'] / results[(ccgt,)]['sequences']['Q']
#
# print(results[(ccgt,)]['sequences'].describe())
# print(results[(ccgt,)]['sequences'].head())
#
#
# # plot CCET
# data = results[(ccgt,)]['sequences']
# ax = data.plot(kind='scatter', x='Q', y='P', grid=True)
# ax.set_xlabel('Q (MW)')
# ax.set_ylabel('P (MW)')
# plt.show()
#
#
# # # plot bus
# # data = views.node(results, 'bel')
# # ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
# # ax.set_title('Dispatch')
# # ax.set_xlabel('')
# # ax.set_ylabel('Power (MW)')
# # plt.show()
#
# # plot bus
# data = views.node(results, 'bth')
# ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
# ax.set_title('Dispatch')
# ax.set_xlabel('')
# ax.set_ylabel('Heat flow (MW)')
# plt.show()
