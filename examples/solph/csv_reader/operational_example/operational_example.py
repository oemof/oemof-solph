# -*- coding: utf-8 -*-

import os
import logging
import pandas as pd

from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import ResultsDataFrame


def run_example(cfg):

    # misc.
    datetime_index = pd.date_range(cfg['date_from'],
                                   cfg['date_to'],
                                   freq='60min')

    logger.define_logging()

    # model creation and solving
    logging.info('Starting optimization')

    es = EnergySystem(groupings=GROUPINGS, timeindex=datetime_index)

    nodes = NodesFromCSV(file_nodes_flows=os.path.join(
                             cfg['scenario_path'],
                             cfg['nodes_flows']),
                         file_nodes_flows_sequences=os.path.join(
                             cfg['scenario_path'],
                             cfg['nodes_flows_sequences']),
                         delimiter=',')

    om = OperationalModel(es)
    om.receive_duals()
    om.solve(solver=cfg['solver'], solve_kwargs={'tee': True})

    logging.info('Done! \n Check the results')

    # create pandas dataframe with results
    results = ResultsDataFrame(energy_system=es)

    rdict = {
        'objective': es.results.objective,
        'time_series': results
    }

    return rdict


def plotting(results):

    # plotting (exemplary)
    # thesis:
    # since R2 has more installed renewable energy capacities than R1, we
    # assume that energy is likely to be transmitted from R2 to R1 in times
    # with a low residual load

    results = results['time_series']

    # create a dataframe with all inputs/outputs in region2
    r2_inputs = results.slice_unstacked(bus_label='R2_bus_el',
                                        type='to_bus',
                                        formatted=True)
    r2_outputs = results.slice_unstacked(bus_label='R2_bus_el',
                                         type='from_bus',
                                         formatted=True)
    r2 = pd.concat([r2_inputs, r2_outputs], axis=1)

    # calculation of normed residual load
    r2['residual_load'] = (r2['R2_load'] - r2['R2_wind'] - r2['R2_solar'])
    r2['residual_load'] = r2['residual_load']/r2['residual_load'].max()

    # scatterplot: can our thesis can be confirmed?
    r2.plot(kind='scatter', x='residual_load', y='R2_R1_powerline')


if __name__ == "__main__":

    # configuration
    cfg = {
        'scenario_path': 'scenarios/',
        'date_from': '2030-01-01 00:00:00',
        'date_to': '2030-01-14 23:00:00',
        'nodes_flows': 'example_energy_system.csv',
        'nodes_flows_sequences': 'example_energy_system_seq.csv',
        'results_path': 'results/',  # has to be created in advance!
        'solver': 'glpk'
    }

    results = run_example(cfg=cfg)  # results['objective'] can be added to test

    # plotting(results)
