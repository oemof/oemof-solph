# -*- coding: utf-8 -*-

import logging
import pandas as pd

from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import to_pandas as tp


logger.define_logging()

date_from = '2014-01-01 00:00:00'
date_to = '2014-03-28 23:00:00'

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
myresults = tp.ResultsDataFrame(energy_system=es)
#print(myresults)

# %% dirty slicing (to be fixed in to_pandas)

DE_inputs = myresults.slice_unstacked(bus_label="DE_bus_el", type="input",
                                      date_from=date_from, date_to=date_to)
DE_inputs.reset_index(level=[1], drop=True, inplace=True)

DE_outputs = myresults.slice_unstacked(bus_label="DE_bus_el", type="output",
                                       date_from=date_from, date_to=date_to)
DE_outputs.reset_index(level=[1], drop=True, inplace=True)

DE_bus_el = pd.concat([DE_inputs, DE_outputs], axis=1, ignore_index=False)

# %% dispatch plot

## linear transformer and storage inputs and outputs are still confused
#area_data = df[['DE_solar', 'DE_wind', 'DE_pp_gas_out', 'DE_storage_phs_in',
#                'DE_load', 'DE_storage_phs_out']]
#area = area_data.plot(kind='area', stacked=True, alpha=0.5, linewidth=0)
#area.set_xlabel('Time')
#area.set_ylabel('Power in MW')

# %% check energy balance arround bus

check_bus_balance = df['DE_load'] - df['DE_solar'] - df['DE_wind'] -\
                    df['DE_pp_gas_out'] - df['DE_storage_phs_in'] -\
                    df['DE_storage_phs_in']
if sum(check_bus_balance) < 0.01:
    print('Bus is balanced')
