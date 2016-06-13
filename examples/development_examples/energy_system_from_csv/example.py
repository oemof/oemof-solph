# -*- coding: utf-8 -*-

import logging
import pandas as pd

from oemof.tools import logger
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import OperationalModel
from oemof.solph.options import NodesFromCSV
from oemof.outputlib import to_pandas as tpd
from collections import Iterable


logger.define_logging()

date_from = '2012-01-01 00:00:00'

date_to = '2012-12-31 23:00:00'

timesteps_max = 8760

datetime_index = pd.date_range(date_from, periods=timesteps_max, freq='60min')

es = core_es.EnergySystem(groupings=solph.GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows='nodes_flows.csv',
                     file_nodes_flows_sequences='nodes_flows_seq.csv',
                     delimiter=',')

## print out nodes
#for k, v in nodes.items():
#    attrs = dir(v)
#    print('\n OBJ:', k, type(v))
#    print('--------------------')
#    for i in attrs:
#        if '_' not in i:
#            # dirty hack to print weakref dicts by converting to list
#            o = getattr(v, str(i))
#            if isinstance(o, Iterable) and not isinstance(o, str):
#                o = list(o)
#            print(i, ':', o)

om = OperationalModel(es, timeindex=datetime_index)

om.solve(solver='gurobi', solve_kwargs={'tee': True})

om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})

logging.info('Done!')

logging.info('Check the results')

myresults = tpd.DataFramePlot(energy_system=es)

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
print(check_bus_balance)
