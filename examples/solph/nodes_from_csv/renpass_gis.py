# -*- coding: utf-8 -*-

import logging
import pandas as pd

from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import to_pandas as tp


logger.define_logging()

date_from = '2014-01-01 00:00:00'
date_to = '2014-02-28 23:00:00'

datetime_index = pd.date_range(date_from, date_to, freq='60min')

es = EnergySystem(groupings=GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows='renpass_gis_2014.csv',
                     file_nodes_flows_sequences='renpass_gis_2014_seq.csv',
                     delimiter=',')

om = OperationalModel(es, timeindex=datetime_index)

om.solve(solver='gurobi', solve_kwargs={'tee': True})

om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})

logging.info('Done!')

logging.info('Check the results')

## %% bugfixing of outputlib
##
##for k, v in es.results.items():
##    # results[source][target][list with flows]
##    # or results[source][source][list with other information]
##    print(k, v, '\n')
#
myresults = tp.DataFramePlot(energy_system=es)
#print(myresults)

# %% dirty slicing (to be fixed in to_pandas)

DE_load = myresults.slice_by(obj_label='DE_load', date_from=date_from,
                             date_to=date_to)
DE_load.reset_index(inplace=True)
DE_load.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
DE_load.set_index('datetime', inplace=True)

DE_solar = myresults.slice_by(obj_label='DE_solar', date_from=date_from,
                              date_to=date_to)
DE_solar.reset_index(inplace=True)
DE_solar.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
DE_solar.set_index('datetime', inplace=True)

DE_wind = myresults.slice_by(obj_label='DE_wind', date_from=date_from,
                             date_to=date_to)
DE_wind.reset_index(inplace=True)
DE_wind.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
DE_wind.set_index('datetime', inplace=True)


DE_pp_gas_in = myresults.slice_by(obj_label='DE_pp_gas', type='input',
                                  date_from=date_from, date_to=date_to)
DE_pp_gas_in.reset_index(inplace=True)
DE_pp_gas_in.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
DE_pp_gas_in.set_index('datetime', inplace=True)


DE_pp_gas_out = myresults.slice_by(obj_label='DE_pp_gas', type='output',
                                   date_from=date_from, date_to=date_to)
DE_pp_gas_out.reset_index(inplace=True)
DE_pp_gas_out.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
DE_pp_gas_out.set_index('datetime', inplace=True)

DE_storage_phs_in = myresults.slice_by(obj_label='DE_storage_phs',
                                       type='input',
                                       date_from=date_from, date_to=date_to)
DE_storage_phs_in.reset_index(inplace=True)
DE_storage_phs_in.drop(['bus_label', 'type', 'obj_label'], axis=1,
                       inplace=True)
DE_storage_phs_in.set_index('datetime', inplace=True)

DE_storage_phs_out = myresults.slice_by(obj_label='DE_storage_phs',
                                        type='output',
                                        date_from=date_from, date_to=date_to)
DE_storage_phs_out.reset_index(inplace=True)
DE_storage_phs_out.drop(['bus_label', 'type', 'obj_label'], axis=1,
                        inplace=True)
DE_storage_phs_out.set_index('datetime', inplace=True)

# %% dispatch plot

df = pd.concat([-DE_load, DE_wind, DE_solar, DE_pp_gas_in, DE_pp_gas_in,
                DE_storage_phs_in, -DE_storage_phs_in],
               axis=1)
df.columns = ['DE_load', 'DE_wind', 'DE_solar', 'DE_pp_gas_in',
              'DE_pp_gas_out', 'DE_storage_phs_in', 'DE_storage_phs_out']

# linear transformer and storage inputs and outputs are still confused
area_data = df[['DE_solar', 'DE_wind', 'DE_pp_gas_out', 'DE_storage_phs_in',
                'DE_load', 'DE_storage_phs_out']]
area = area_data.plot(kind='area', stacked=True, alpha=0.5, linewidth=0)
area.set_xlabel('Time')
area.set_ylabel('Power in MW')

# %% check energy balance arround bus

check_bus_balance = df['DE_load'] - df['DE_solar'] - df['DE_wind'] -\
                    df['DE_pp_gas_out'] - df['DE_storage_phs_in'] -\
                    df['DE_storage_phs_in']
if sum(check_bus_balance) < 0.01:
    print('Bus is balanced')
