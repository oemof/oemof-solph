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

date_from = '2014-01-01 00:00:00'
date_to = '2014-12-31 23:00:00'
nodes_flows = 'nep_2014.csv'

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

nodes = NodesFromCSV(file_nodes_flows=nodes_flows,
                     file_nodes_flows_sequences=nodes_flows_sequences,
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

    # add price volatility that's lacking in duals by adding a regression for
    # the EEX day-ahead prices of 2014 (used in project 'DLSK-SH')
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

        # residual load in bidding area
        residual_load = country_data['DE_load'] + country_data['AT_load'] + \
            country_data['LU_load'] - country_data['DE_wind'] - \
            country_data['AT_wind'] - country_data['LU_wind'] - \
            country_data['DE_solar'] - country_data['AT_solar'] - \
            country_data['LU_solar']

        # polynomial regression for 2014
        def spot_price(x):
            coeff = [3.39995259e-13, -6.22068602e-08,
                     4.48623593e-03, -8.55571083e+01]
            y = coeff[0] * x ** 3 + \
                coeff[1] * x ** 2 + \
                coeff[2] * x ** 1 + \
                coeff[3]
            return y

        # assign data to dataframe
        country_data['price_volatility'] = residual_load.apply(spot_price)

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
