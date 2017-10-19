# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `GenericCHP` can be used.

In this case it is used to model a combined cycle extraction turbine.
"""

import matplotlib.pyplot as plt
import pandas as pd
import oemof.solph as solph
from oemof.outputlib import processing, views


# read sequence data
file_name = 'ccet.csv'
data = pd.read_csv(file_name, sep=",")

# select periods
periods = len(data)-1

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
                       actual_value=data['demand_th'], nominal_value=200)})

# power
bel = solph.Bus(label='bel')

demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
                       variable_costs=data['price_el'])})

# generic chp
# (for back pressure characteristics Q_CW_min=0 and back_pressure=True)
ccet = solph.components.GenericCHP(
    label='combined_cycle_extraction_turbine',
    fuel_input={bgas: solph.Flow(
        H_L_FG_share=data['H_L_FG_share'])},
    electrical_output={bel: solph.Flow(
        P_max_woDH=data['P_max_woDH'],
        P_min_woDH=data['P_min_woDH'],
        Eta_el_max_woDH=data['Eta_el_max_woDH'],
        Eta_el_min_woDH=data['Eta_el_min_woDH'])},
    heat_output={bth: solph.Flow(
        Q_CW_min=data['Q_CW_min'])},
    Beta=data['Beta'], back_pressure=False,
    fixed_costs=0)

# create an optimization problem and solve it
om = solph.OperationalModel(es)

# debugging
#om.write('generic_chp.lp', io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver='gurobi', solve_kwargs={'tee': True})

# create result object
results = processing.results(om)

# store as csv
data = results[(ccet,)]['sequences'].to_csv('results_' + file_name)

# plot CCET (scatter)
data = results[(ccet,)]['sequences']
ax = data.plot(kind='scatter', x='Q', y='P', grid=True)
ax.set_xlabel('Q (MW)')
ax.set_ylabel('P (MW)')
plt.savefig('plot_' + file_name + '.pdf', format='pdf', dpi=600)
plt.close()
#plt.show()

# # plot CCET (line)
# data = results[(ccet,)]['sequences']
# ax = data.plot(kind='line', drawstyle='steps-post', grid=True)
# ax.set_xlabel('Time')
# ax.set_ylabel('(MW)')
# plt.show()
#
# # plot bus
# data = views.node(results, 'bel')
# ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
# ax.set_title('Dispatch')
# ax.set_xlabel('')
# ax.set_ylabel('Power (MW)')
# plt.show()
#
# # plot bus
# data = views.node(results, 'bth')
# ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
# ax.set_title('Dispatch')
# ax.set_xlabel('')
# ax.set_ylabel('Heat flow (MW)')
# plt.show()
