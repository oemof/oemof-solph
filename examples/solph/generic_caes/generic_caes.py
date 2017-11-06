# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `GenericCAES` can be used.

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import oemof.solph as solph
import time
from oemof.outputlib import processing


# read sequence data
file_name = 'generic_caes.csv'
input_data = pd.read_csv(file_name, sep=",")

# select periods
periods = len(input_data)-1

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)

# resources
bgas = solph.Bus(label='bgas')

rgas = solph.Source(label='rgas',
                    outputs={bgas: solph.Flow(variable_costs=20)})

# power
bel = solph.Bus(label='bel')

source_el = solph.Source(label='source_el',
                         outputs={bel: solph.Flow(
                            variable_costs=input_data['price_el_source'])})

# demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
#                        variable_costs=data['price_el'])})
demand_el = solph.Sink(label='demand_el',
                       inputs={bel: solph.Flow(
                            variable_costs=input_data['price_el_demand'])})

# dictionary with parameters for a specific CAES plant
# based on thermal modelling and linearization techniques
concept = {
    'cav_e_in_b': 0,
    'cav_e_in_m': 0.6457267578,
    'cav_e_out_b': 0,
    'cav_e_out_m': 0.3739636077,
    'cav_eta_temp': 1.0,
    'cav_level_max': 211.11,  # 211.11
    'cmp_p_max_b': 86.0918959849,
    'cmp_p_max_m': 0.0679999932,
    'cmp_p_min': 1,
    'cmp_q_out_b': -19.3996965679,
    'cmp_q_out_m': 1.1066036114,
    'cmp_q_tes_share': 0,
    'exp_p_max_b': 46.1294016678,
    'exp_p_max_m': 0.2528340303,
    'exp_p_min': 1,
    'exp_q_in_b': -2.2073411014,
    'exp_q_in_m': 1.129249765,
    'exp_q_tes_share': 0,
    'tau': 0.25,
    'tes_eta_temp': 1.0,
    'tes_level_max': 0.0
}

# generic caes plant
caes = solph.custom.GenericCAES(
    label='compressed_air_energy_storage',
    electrical_input={bel: solph.Flow()},
    fuel_input={bgas: solph.Flow()},
    electrical_output={bel: solph.Flow()},
    params=concept, fixed_costs=0)

# create an optimization problem and solve it
om = solph.OperationalModel(es)

# debugging
#om.write('generic_caes.lp', io_options={'symbolic_solver_labels': True})

print('Start: ', time.strftime('%Y-%m-%d %H:%M:%S'))
# solve model
om.solve(solver='gurobi', solve_kwargs={'tee': False})
print('End: ', time.strftime('%Y-%m-%d %H:%M:%S'))

# create result object
results = processing.results(om)

# create dataframe with CAES results
data = results[(caes,)]['sequences']

# add prices
other = pd.DataFrame()
other['eex'] = input_data[0:len(data)]['price_el_source']
other.index = data.index
data = pd.concat([data, other], axis=1)

# print(data.columns)
data.to_csv('cav_level.csv')

# # plot dispatch
# columns = ['cav_level', 'cmp_p', 'exp_p', 'eex']
# ax = data[columns].plot(kind='line', drawstyle='steps-post',
#                         grid=True, subplots=True)
# plt.show()
