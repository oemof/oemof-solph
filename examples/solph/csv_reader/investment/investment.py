# -*- coding: utf-8 -*-

import os
import logging
import matplotlib.pyplot as plt
import pandas as pd

from datetime import datetime
from oemof.outputlib import results, views
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

    results_old = ResultsDataFrame(energy_system=es)

    results_path = os.path.join(os.path.expanduser("~"), 'csv_invest')

    if not os.path.isdir(results_path):
        os.mkdir(results_path)

    results_old.to_csv(os.path.join(results_path, 'results.csv'))

    logging.info("The results can be found in {0}".format(results_path))
    logging.info("Read the documentation (outputlib) to learn how" +
                 " to process the results.")
    logging.info("Or search the web to learn how to handle a MultiIndex" +
                 "DataFrame with pandas.")

    logging.info('Done!')

    # create a dictionary with the results
    opt_results = results.create_results(es, om)

    # standard api: results for a flow
    my_id = (es.groups['REGION1_pp_oil'], es.groups['REGION1_bus_el'])
    print(opt_results[my_id]['scalars'])
    print(opt_results[my_id]['sequences'].describe())

    # standard api: results for a component
    my_id = (es.groups['REGION1_storage_phs'],)
    print(opt_results[my_id]['scalars'])
    print(opt_results[my_id]['sequences'].describe())

    # slicing functions: get all node results (bus)
    # works with node objects and string labels as argument
    region1 = views.node(opt_results, es.groups['REGION1_bus_el'])
    region1 = views.node(opt_results, 'REGION1_bus_el')
    print(region1['sequences'].max())
    print(region1['scalars'])

    # slicing functions: get all node results (component)
    # works with node objects and string labels as argument
    phs = views.node(opt_results, es.groups['REGION1_storage_phs'])
    phs = views.node(opt_results, 'REGION1_storage_phs')
    print(phs['sequences'].max())
    print(phs['scalars'])

    # example plot for sequences
    cols = [c for c in phs['sequences'].columns if 'my_sequence_var' not in c]
    phs['sequences'] = phs['sequences'][cols]
    phs['sequences'].columns = ['P-IN', 'CAP', 'P-OUT']
    ax = phs['sequences'].plot(kind='line', drawstyle='steps-post')
    ax.set_title('Dispatch results')
    ax.set_xlabel('Time')
    ax.set_ylabel('Power (MW) / Energy (MWh)')
    plt.show()

    # example plot for scalars
    idx = [i for i in phs['scalars'].index if 'my_scalar_var' not in i]
    phs['scalars'] = phs['scalars'][idx]
    phs['scalars'].index = ['P-IN', 'CAP', 'P-OUT']
    ax = phs['scalars'].plot(kind='bar')
    ax.set_title('Investment results')
    ax.set_xlabel('')
    ax.set_ylabel('Storage investment in MWh / MW')
    plt.show()



if __name__ == '__main__':
    run_investment_example()
