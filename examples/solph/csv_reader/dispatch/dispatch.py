# -*- coding: utf-8 -*-
"""
Dispatch optimisation using oemof's csv-reader.
"""

import os
import pandas as pd

from oemof.solph import OperationalModel, EnergySystem
from oemof.solph import nodes_from_csv
from oemof.outputlib import processing, views
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# configuration
cfg = {
    'scenario_path': os.path.join(os.path.dirname(__file__), 'scenarios'),
    'date_from': '2030-01-01 00:00:00',
    'date_to': '2030-01-14 23:00:00',
    'nodes_flows': 'example_energy_system.csv',
    'nodes_flows_sequences': 'example_energy_system_seq.csv',
    'results_path': os.path.join(os.path.expanduser("~"), 'csv_dispatch'),
    'solver': 'cbc',
    'verbose': False,  # Set to True to see solver outputs
}


def run_csv_reader_dispatch_example(config=cfg):

    # creation of an hourly datetime_index
    datetime_index = pd.date_range(config['date_from'],
                                   config['date_to'],
                                   freq='60min')

    # initialisation of the energy system
    es = EnergySystem(timeindex=datetime_index)

    # adding all nodes and flows to the energy system
    # (data taken from csv-file)
    nodes_from_csv(file_nodes_flows=os.path.join(
                             config['scenario_path'],
                             config['nodes_flows']),
                   file_nodes_flows_sequences=os.path.join(
                             config['scenario_path'],
                             config['nodes_flows_sequences']),
                   delimiter=',')

    # creation of a least cost model from the energy system
    om = OperationalModel(es)
    om.receive_duals()

    # solving the linear problem using the given solver
    om.solve(solver=config['solver'], solve_kwargs={'tee': config['verbose']})

    # create results path if it does not exist
    if not os.path.isdir(cfg['results_path']):
        os.mkdir(cfg['results_path'])

    # generic result object
    results = processing.results(es=es, om=om)

    data = views.node(results, 'R1_bus_el')

    print('Optimization successful. Printing some results:',
          data['sequences'].info())

    # plot data if matplotlib is installed
    # see: https://pandas.pydata.org/pandas-docs/stable/visualization.html
    if plt is not None:
        ax = data['sequences'].sum(axis=0).plot(kind='barh')
        ax.set_title('Sums for optimization period')
        ax.set_xlabel('Energy (MWh)')
        ax.set_ylabel('Flow')
        plt.tight_layout()
        plt.show()

    # generate results to be evaluated in tests
    rdict = data['sequences'].sum(axis=0).to_dict()

    return rdict


if __name__ == "__main__":
    run_csv_reader_dispatch_example()
