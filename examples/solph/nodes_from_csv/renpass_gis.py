# -*- coding: utf-8 -*-

import logging
import pandas as pd

from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import to_pandas as tp


logger.define_logging()

date_from = '2014-01-01 00:00:00'
date_to = '2014-01-28 23:00:00'

datetime_index = pd.date_range(date_from, date_to, freq='60min')

es = EnergySystem(groupings=GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows='renpass_gis_2014.csv',
                     file_nodes_flows_sequences='renpass_gis_2014_seq.csv',
                     delimiter=',')

om = OperationalModel(es, timeindex=datetime_index)

om.solve(solver='gurobi', solve_kwargs={'tee': True})

om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})

logging.info('Done!')

logging.info('Check the results')

# %% bugfixing of outputlib

for k, v in es.results.items():
    # results[source][target][list with flows]
    # or results[source][source][list with other information]
    print(k, '\n')
    print(type(v))

# %% output

myresults = tp.ResultsDataFrame(energy_system=es)

DE_inputs = myresults.slice_unstacked(bus_label="DE_bus_el", type="input",
                                      date_from=date_from, date_to=date_to,
                                      formatted=True)

DE_outputs = myresults.slice_unstacked(bus_label="DE_bus_el", type="output",
                                       date_from=date_from, date_to=date_to,
                                       formatted=True)

DE_other = myresults.slice_unstacked(bus_label="DE_bus_el", type="other",
                                     date_from=date_from, date_to=date_to,
                                     formatted=True)

DE_overall = pd.concat([DE_inputs, -DE_outputs], axis=1)
DE_overall = DE_overall[['DE_solar', 'DE_wind', 'DE_pp_gas', 'DE_storage_phs',
                         'DE_shortage', 'DE_load', 'DE_storage_phs',
                         'DE_excess', 'duals']]

area = DE_overall.plot(kind='area', stacked=True)
