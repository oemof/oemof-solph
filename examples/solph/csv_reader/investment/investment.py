# -*- coding: utf-8 -*-

import os
import logging
import matplotlib.pyplot as plt
import pandas as pd

from datetime import datetime
from oemof.outputlib import results_to_dict
from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, NodesFromCSV
from oemof.outputlib import ResultsDataFrame


def stopwatch():
    if not hasattr(stopwatch, 'now'):
        stopwatch.now = datetime.now()
        return None
    last = stopwatch.now
    stopwatch.now = datetime.now()
    return str(stopwatch.now-last)[0:-4]


def run_investment_example(solver='cbc', verbose=True, nologg=False):
    if not nologg:
        logger.define_logging()

    # %% model creation and solving
    date_from = '2050-01-01 00:00:00'
    date_to = '2050-01-01 23:00:00'

    datetime_index = pd.date_range(date_from, date_to, freq='60min')

    es = EnergySystem(timeindex=datetime_index)

    data_path = os.path.join(os.path.dirname(__file__), 'data')

    NodesFromCSV(file_nodes_flows=os.path.join(data_path, 'nodes_flows.csv'),
                 file_nodes_flows_sequences=os.path.join(data_path,
                 'nodes_flows_seq.csv'),
                 delimiter=',')

    stopwatch()

    om = OperationalModel(es)

    logging.info('OM creation time: ' + stopwatch())

    om.receive_duals()

    om.solve(solver=solver, solve_kwargs={'tee': verbose})

    logging.info('Optimization time: ' + stopwatch())

    results = ResultsDataFrame(energy_system=es)

    results_path = os.path.join(os.path.expanduser("~"), 'csv_invest')

    if not os.path.isdir(results_path):
        os.mkdir(results_path)

    results.to_csv(os.path.join(results_path, 'results.csv'))

    logging.info("The results can be found in {0}".format(results_path))
    logging.info("Read the documentation (outputlib) to learn how" +
                 " to process the results.")
    logging.info("Or search the web to learn how to handle a MultiIndex" +
                 "DataFrame with pandas.")

    logging.info('Done!')

    # create multi-indexed pandas dataframe
    results = results_to_dict(es, om)

    # flows with investment results
    ids = {'REGION1_pp_uranium': 'REGION1_bus_el',
           'REGION1_pp_lignite': 'REGION1_bus_el',
           'REGION1_pp_hard_coal': 'REGION1_bus_el',
           'REGION1_pp_lignite': 'REGION1_bus_el',
           'REGION1_pp_gas': 'REGION1_bus_el',
           'REGION1_pp_oil': 'REGION1_bus_el',
           'REGION1_pp_biomass': 'REGION1_bus_el',
           'REGION1_wind': 'REGION1_bus_el',
           'REGION1_solar': 'REGION1_bus_el',
           'REGION1_bus_el': 'REGION1_storage_phs',
           'REGION1_storage_phs': 'REGION1_bus_el'}

    # aggregation
    invest_results = pd.Series()
    for k, v in ids.items():
        tuple = (es.groups[k], es.groups[v])
        tmp = results[tuple]['scalars']
        tmp.index = [k]
        data = [invest_results, tmp]
        invest_results = pd.concat(data, ignore_index=False)

    # plot results
    invest_results.index = [str.replace(k, 'REGION1_', '') for k in ids.keys()]
    ax = invest_results.plot(kind='bar')
    ax.set_xlabel('Technology')
    ax.set_ylabel('Installed capacity in MW')
    ax.set_title('Some easy plotting')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    run_investment_example()
