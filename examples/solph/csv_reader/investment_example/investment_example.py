# -*- coding: utf-8 -*-

import os
import logging
import pandas as pd

from datetime import datetime
from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS, NodesFromCSV


def stopwatch():
    if not hasattr(stopwatch, 'now'):
        stopwatch.now = datetime.now()
        return None
    last = stopwatch.now
    stopwatch.now = datetime.now()
    return str(stopwatch.now-last)[0:-4]


def run_investment_example():
    logger.define_logging()

    # %% model creation and solving
    date_from = '2050-01-01 00:00:00'
    date_to = '2050-01-01 23:00:00'

    datetime_index = pd.date_range(date_from, date_to, freq='60min')

    es = EnergySystem(timeindex=datetime_index)

    data_path = os.path.join(os.path.dirname(__file__), 'data')

    nodes = NodesFromCSV(file_nodes_flows=os.path.join(data_path,
                                                       'nodes_flows.csv'),
                         file_nodes_flows_sequences=os.path.join(
                             data_path,
                             'nodes_flows_seq.csv'),
                         delimiter=',')

    stopwatch()

    om = OperationalModel(es)

    logging.info('OM creation time: ' + stopwatch())

    #om.receive_duals()

    om.solve(solver='glpk', solve_kwargs={'tee': True})

    logging.info('Optimization time: ' + stopwatch())

    logging.info('Done! \n Check the results')


if __name__ == '__main__':
    run_investment_example()

