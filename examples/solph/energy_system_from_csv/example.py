# -*- coding: utf-8 -*-

import logging
import pandas as pd

from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph.options import NodesFromCSV
from oemof.outputlib import to_pandas as tpd


logger.define_logging()

date_from = '2012-01-01 00:00:00'
date_to = '2012-01-31 23:00:00'

datetime_index = pd.date_range(date_from, date_to, freq='60min')

es = EnergySystem(groupings=GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows='nodes_flows.csv',
                     file_nodes_flows_sequences='nodes_flows_seq.csv',
                     delimiter=',')

om = OperationalModel(es, timeindex=datetime_index)

om.solve(solver='gurobi', solve_kwargs={'tee': True})

om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})

logging.info('Done!')

logging.info('Check the results')

# %% bugfixing of outputlib

for k, v in es.results.items():
    # results[source][target][list with flows]
    # or results[source][source][list with other information]
    print(k, v, '\n')

myresults = tpd.DataFramePlot(energy_system=es)
print(myresults)

# %% dirty slicing (to be fixed in to_pandas)

demand = myresults.slice_by(obj_label='demand1', date_from=date_from,
                            date_to=date_to)
demand.reset_index(inplace=True)
demand.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
demand.set_index('datetime', inplace=True)

solar = myresults.slice_by(obj_label='solar1', date_from=date_from,
                           date_to=date_to)
solar.reset_index(inplace=True)
solar.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
solar.set_index('datetime', inplace=True)

wind = myresults.slice_by(obj_label='wind1', date_from=date_from,
                          date_to=date_to)
wind.reset_index(inplace=True)
wind.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
wind.set_index('datetime', inplace=True)


chp_in = myresults.slice_by(obj_label='chp1', type='input',
                            bus_label='bus_el1',
                            date_from=date_from, date_to=date_to)
chp_in.reset_index(inplace=True)
chp_in.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
chp_in.set_index('datetime', inplace=True)


chp_out = myresults.slice_by(obj_label='chp1', type='output',
                             date_from=date_from, date_to=date_to)
chp_out.reset_index(inplace=True)
chp_out.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
chp_out.set_index('datetime', inplace=True)

storage_in = myresults.slice_by(obj_label='storage1', type='input',
                                date_from=date_from, date_to=date_to)
storage_in.reset_index(inplace=True)
storage_in.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
storage_in.set_index('datetime', inplace=True)

storage_out = myresults.slice_by(obj_label='storage1', type='output',
                                 date_from=date_from, date_to=date_to)
storage_out.reset_index(inplace=True)
storage_out.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
storage_out.set_index('datetime', inplace=True)

# %% dispatch plot

df = pd.concat([-demand, wind, solar, chp_in, chp_out, storage_in,
                -storage_out],
               axis=1)
df.columns = ['demand', 'wind', 'solar', 'chp_in', 'chp_out', 'storage_in',
              'storage_out']

# linear transformer and storage inputs and outputs are still confused
area_data = df[['solar', 'wind', 'chp_in', 'storage_in', 'demand',
                'storage_out']]
area = area_data.plot(kind='area', stacked=True, alpha=0.5, linewidth=0)
area.set_xlabel('Time')
area.set_ylabel('Power in MW')

# %% check energy balance arround bus

check_bus_balance = df['demand'] - df['solar'] - df['wind'] - df['chp_in'] - \
    df['storage_in'] - df['storage_out']
if sum(check_bus_balance) < 0.01:
    print('Bus is balanced')
