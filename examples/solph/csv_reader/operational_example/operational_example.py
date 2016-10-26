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

date_from = '2030-01-01 00:00:00'
date_to = '2030-01-14 23:00:00'

nodes_flows = 'example_energy_system.csv'
nodes_flows_sequences = 'example_energy_system_seq.csv'


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

es = EnergySystem(groupings=GROUPINGS, timeindex=datetime_index)

nodes = NodesFromCSV(file_nodes_flows=os.path.join(
                         scenario_path, nodes_flows),
                     file_nodes_flows_sequences=os.path.join(
                         scenario_path, nodes_flows_sequences),
                     delimiter=',')

stopwatch()

om = OperationalModel(es)

logging.info('OM creation time: ' + stopwatch())

om.receive_duals()

om.solve(solver='glpk', solve_kwargs={'tee': True})

logging.info('Optimization time: ' + stopwatch())

logging.info('Done! \n Check the results')


# %% output: create pandas dataframe with results

results = ResultsDataFrame(energy_system=es)


# %% postprocessing: write complete result dataframe to file system

# this folder has to be created in advance if it doesn't exist
results_path = 'results/'

date = str(datetime.now())

file_name = 'scenario_' + nodes_flows.replace('.csv', '_') + date + '_' + \
            'results_complete.csv'

results.to_csv(os.path.join(results_path, file_name))


# %% postprocessing: write dispatch and prices for all regions to file system

# region codes
region_codes = ['R1', 'R2']

for rc in region_codes:

    # build single dataframe for electric busses
    inputs = results.slice_unstacked(bus_label=rc + '_bus_el', type='to_bus',
                                     date_from=date_from, date_to=date_to,
                                     formatted=True)

    outputs = results.slice_unstacked(bus_label=rc + '_bus_el',
                                      type='from_bus',
                                      date_from=date_from, date_to=date_to,
                                      formatted=True)

    other = results.slice_unstacked(bus_label=rc + '_bus_el', type='other',
                                    date_from=date_from, date_to=date_to,
                                    formatted=True)

    inputs.rename(columns={rc + '_storage_phs': rc + '_storage_phs_out'},
                  inplace=True)
    outputs.rename(columns={rc + '_storage_phs': rc + '_storage_phs_in'},
                   inplace=True)
    other.rename(columns={rc + '_storage_phs': rc + '_storage_phs_level'},
                 inplace=True)

    # data from model in MWh
    region_data = pd.concat([inputs, outputs, other], axis=1)

    # sort columns and save as csv file
    file_name = 'scenario_' + nodes_flows.replace('.csv', '_') + date + '_' + \
                rc + '.csv'
    region_data.sort_index(axis=1, inplace=True)
    region_data.to_csv(os.path.join(results_path, file_name))

# %% plotting (exemplary)

# thesis:
# since R2 has more installed renewable energy capacities than R1, we assume
# that energy is likely to be transmitted from R2 to R1 in times with a
# low residual load

# create a dataframe with all inputs/outputs in region2
r2 = pd.concat(
    [results.slice_unstacked(bus_label='R2_bus_el', type='to_bus',
                             date_from=date_from, date_to=date_to,
                             formatted=True),
     results.slice_unstacked(bus_label=rc + '_bus_el', type='from_bus',
                             date_from=date_from, date_to=date_to,
                             formatted=True)], axis=1)

# calculation of normed residual load
r2['residual_load'] = (r2['R2_load'] - r2['R2_wind'] - r2['R2_solar'])
r2['residual_load'] = r2['residual_load']/r2['residual_load'].max()

# scatterplot: can our thesis can be confirmed?
r2.plot(kind='scatter', x='residual_load', y='R2_R1_powerline')
