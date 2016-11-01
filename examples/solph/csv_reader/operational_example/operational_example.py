# -*- coding: utf-8 -*-

import os
import logging
import pandas as pd

from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import ResultsDataFrame


def run_example(config):
    # misc.
    datetime_index = pd.date_range(config['date_from'],
                                   config['date_to'],
                                   freq='60min')

    # model creation and solving
    logging.info('Starting optimization')

    es = EnergySystem(timeindex=datetime_index)

    NodesFromCSV(file_nodes_flows=os.path.join(
                             config['scenario_path'],
                             config['nodes_flows']),
                 file_nodes_flows_sequences=os.path.join(
                             config['scenario_path'],
                             config['nodes_flows_sequences']),
                 delimiter=',')

    om = OperationalModel(es)
    om.receive_duals()
    om.solve(solver=config['solver'], solve_kwargs={'tee': config['verbose']})

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


def create_result_dict(results):
    """Create a result dictionary for testing purposes."""
    tmp_dict = {
        'R2_wind': results['time_series'].loc[
            pd.IndexSlice['R2_bus_el', 'to_bus', 'R2_wind']].sum(),
        'R2_R1_powerline': results['time_series'].loc[
            pd.IndexSlice['R2_bus_el', 'from_bus', 'R2_R1_powerline']].sum(),
        'R2_storage_phs': results['time_series'].loc[pd.IndexSlice[
            'R2_bus_el', 'from_bus', 'R2_storage_phs']].sum(),
        'objective': results['objective'],
    }
    return tmp_dict


def run_operational_example():
    logger.define_logging()

    filepath = os.path.join(os.path.dirname(__file__), 'scenarios')

    # configuration
    cfg = {
        'scenario_path': os.path.join(os.path.dirname(__file__),
                                      'scenarios'),
        'date_from': '2030-01-01 00:00:00',
        'date_to': '2030-01-14 23:00:00',
        'nodes_flows': os.path.join(filepath, 'example_energy_system.csv'),
        'nodes_flows_sequences': os.path.join(
            filepath,
            'example_energy_system_seq.csv'),
        'results_path': 'results/',  # has to be created in advance!
        'solver': 'glpk',
        'verbose': True,
    }

    my_results = run_example(config=cfg)

    plotting(my_results)

    # print(create_result_dict(my_results))


if __name__ == "__main__":
    run_operational_example()


