# -*- coding: utf-8 -*-

import os
import logging
import pandas as pd

from datetime import datetime
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


if __name__ == '__main__':
    run_investment_example()
