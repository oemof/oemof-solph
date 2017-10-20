# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `GenericCHP` can be used.

In this case it is used to model a combined cycle extraction turbine.
"""

import matplotlib.pyplot as plt
import pandas as pd
import oemof.solph as solph
from oemof.outputlib import processing


# read sequence data
file_name = 'generic_chp.csv'
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

# dummy source at high costs that serves the residual load
source_th = solph.Source(label='source_th',
                         outputs={bth: solph.Flow(variable_costs=1000)})

demand_th = solph.Sink(label='demand_th', inputs={bth: solph.Flow(fixed=True,
                       actual_value=data['demand_th'], nominal_value=200)})

# power
bel = solph.Bus(label='bel')

demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
                       variable_costs=data['price_el'])})

# combined cycle extraction turbine
ccet = solph.components.GenericCHP(
    label='combined_cycle_extraction_turbine',
    fuel_input={bgas: solph.Flow(
        H_L_FG_share_max=[0.19 for p in range(0, periods)])},
    electrical_output={bel: solph.Flow(
        P_max_woDH=[200 for p in range(0, periods)],
        P_min_woDH=[80 for p in range(0, periods)],
        Eta_el_max_woDH=[0.53 for p in range(0, periods)],
        Eta_el_min_woDH=[0.43 for p in range(0, periods)])},
    heat_output={bth: solph.Flow(
        Q_CW_min=[30 for p in range(0, periods)])},
    Beta=[0.19 for p in range(0, periods)],
    fixed_costs=0, back_pressure=False)

# back pressure turbine with same parameters as ccet
# (for back pressure characteristics Q_CW_min=0 and back_pressure=True)
bpt = solph.components.GenericCHP(
    label='back_pressure_turbine',
    fuel_input={bgas: solph.Flow(
        H_L_FG_share_max=[0.19 for p in range(0, periods)])},
    electrical_output={bel: solph.Flow(
        P_max_woDH=[200 for p in range(0, periods)],
        P_min_woDH=[80 for p in range(0, periods)],
        Eta_el_max_woDH=[0.53 for p in range(0, periods)],
        Eta_el_min_woDH=[0.43 for p in range(0, periods)])},
    heat_output={bth: solph.Flow(
        Q_CW_min=[0 for p in range(0, periods)])},
    Beta=[0.19 for p in range(0, periods)],
    fixed_costs=0, back_pressure=True)

# motoric chp
mchp = solph.components.GenericCHP(
    label='motoric_chp',
    fuel_input={bgas: solph.Flow(
        H_L_FG_share_max=[0.18 for p in range(0, periods)],
        H_L_FG_share_min=[0.41 for p in range(0, periods)])},
    electrical_output={bel: solph.Flow(
        P_max_woDH=[200 for p in range(0, periods)],
        P_min_woDH=[100 for p in range(0, periods)],
        Eta_el_max_woDH=[0.44 for p in range(0, periods)],
        Eta_el_min_woDH=[0.40 for p in range(0, periods)])},
    heat_output={bth: solph.Flow(
        Q_CW_min=[0 for p in range(0, periods)])},
    Beta=[0 for p in range(0, periods)],
    fixed_costs=0, back_pressure=False)

# create an optimization problem and solve it
om = solph.OperationalModel(es)

# debugging
#om.write('generic_chp.lp', io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver='gurobi', solve_kwargs={'tee': True})

# create result object
results = processing.results(om)

# # store as csv
# data = results[(ccet,)]['sequences'].to_csv('results_' + file_name)
#
# # plot CCET
# data = results[(ccet,)]['sequences']
# ax = data.plot(kind='scatter', x='Q', y='P', grid=True)
# ax.set_xlabel('Q (MW)')
# ax.set_ylabel('P (MW)')
# plt.savefig('plot_ccet_' + file_name + '_PQ.pdf', format='pdf', dpi=600)
# plt.close()
#
# # plot BPT
# data = results[(bpt,)]['sequences']
# ax = data.plot(kind='scatter', x='Q', y='P', grid=True)
# ax.set_xlabel('Q (MW)')
# ax.set_ylabel('P (MW)')
# plt.savefig('plot_bpt_' + file_name + '_PQ.pdf', format='pdf', dpi=600)
# plt.close()
#
# # plot MCHP
# data = results[(mchp,)]['sequences']
# ax = data.plot(kind='scatter', x='Q', y='P', grid=True)
# ax.set_xlabel('Q (MW)')
# ax.set_ylabel('P (MW)')
# plt.savefig('plot_mchp_' + file_name + '_PQ.pdf', format='pdf', dpi=600)
# plt.close()
