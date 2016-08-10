# -*- coding: utf-8 -*-

import os
import logging
import pandas as pd

from datetime import datetime
from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import ResultsDataFrame


# %% configuration

scenario_path = 'scenarios/'

date_from = '2035-01-01 00:00:00'
date_to = '2035-12-31 23:00:00'

nodes_flows = 'nep_2035_ee_minus_25.csv'
nodes_flows_sequences = 'nep_2014_seq.csv'


# %% misc.

datetime_index = pd.date_range(date_from, date_to, freq='60min')


def stopwatch():
    if not hasattr(stopwatch, 'now'):
        stopwatch.now = datetime.now()
        return None
    last = stopwatch.now
    stopwatch.now = datetime.now()
    return str(stopwatch.now-last)[0:-4]

logger.define_logging()


# %% model creation and solving

es = EnergySystem(groupings=GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows=os.path.join(
                         scenario_path, nodes_flows),
                     file_nodes_flows_sequences=os.path.join(
                         scenario_path, nodes_flows_sequences),
                     delimiter=',')

stopwatch()

om = OperationalModel(es)

print('OM creation time: ' + stopwatch())

om.receive_duals()

om.solve(solver='gurobi', solve_kwargs={'tee': True})

print('Optimization time: ' + stopwatch())

logging.info('Done!')

logging.info('Check the results')


# %% output: create pandas dataframe with results

results = ResultsDataFrame(energy_system=es)


# %% postprocessing: write complete result dataframe to file system

results_path = 'results/'

date = str(datetime.now())

file_name = 'scenario_' + nodes_flows.replace('.csv', '_') + date + '_' + \
            'results_complete.csv'

results.to_csv(os.path.join(results_path, file_name))


# %% postprocessing: write dispatch and prices for all regions to file system

# country codes
country_codes = ['AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'FR', 'LU', 'NL', 'NO',
                 'PL', 'SE']

for cc in country_codes:

    # build single dataframe for electric busses
    inputs = results.slice_unstacked(bus_label=cc + '_bus_el', type='input',
                                     date_from=date_from, date_to=date_to,
                                     formatted=True)

    outputs = results.slice_unstacked(bus_label=cc + '_bus_el', type='output',
                                      date_from=date_from, date_to=date_to,
                                      formatted=True)

    other = results.slice_unstacked(bus_label=cc + '_bus_el', type='other',
                                    date_from=date_from, date_to=date_to,
                                    formatted=True)

    # AT, DE and LU are treated as one bidding area
    if cc == 'DE':

        for c in ['DE', 'AT', 'LU']:

            # rename redundant columns
            inputs.rename(columns={c + '_storage_phs':
                                   c + '_storage_phs_out'},
                          inplace=True)

            outputs.rename(columns={c + '_storage_phs':
                                    c + '_storage_phs_in'},
                           inplace=True)

            other.rename(columns={c + '_storage_phs':
                                  c + '_storage_phs_level'},
                         inplace=True)

            # data from model in MWh
            country_data = pd.concat([inputs, outputs, other], axis=1)

    else:

        # rename redundant columns
        inputs.rename(columns={cc + '_storage_phs': cc + '_storage_phs_out'},
                      inplace=True)

        outputs.rename(columns={cc + '_storage_phs': cc + '_storage_phs_in'},
                       inplace=True)

        other.rename(columns={cc + '_storage_phs': cc + '_storage_phs_level'},
                     inplace=True)

        # data from model in MWh
        country_data = pd.concat([inputs, outputs, other], axis=1)

    # sort columns and save as csv file
    file_name = 'scenario_' + nodes_flows.replace('.csv', '_') + date + '_' + \
                cc + '.csv'
    country_data.sort_index(axis=1, inplace=True)
    country_data.to_csv(os.path.join(results_path, file_name))
