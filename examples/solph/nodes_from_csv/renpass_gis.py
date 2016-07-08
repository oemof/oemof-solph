# -*- coding: utf-8 -*-

import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime

from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import ResultsDataFrame

def stopwatch():
    if not hasattr(stopwatch, "now"):
        stopwatch.now = datetime.now()
        return None
    last = stopwatch.now
    stopwatch.now = datetime.now()
    return str(stopwatch.now-last)[0:-4]

logger.define_logging()

# %% configuration

date_from = '2014-01-01 00:00:00'
date_to = '2014-12-31 23:00:00'

datetime_index = pd.date_range(date_from, date_to, freq='60min')

# global plotting options
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 18})

# %% model creation and solving

es = EnergySystem(groupings=GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows='status_quo_2014_aggr.csv',
                     file_nodes_flows_sequences='status_quo_2014_aggr_seq.csv',
                     delimiter=',')

stopwatch()
om = OperationalModel(es)
print("OM creation time: " + stopwatch())

om.receive_duals()

om.solve(solver='gurobi', solve_kwargs={'tee': True})
print("Optimization time: " + stopwatch())

logging.info('Done!')

logging.info('Check the results')


# %% output: data

myresults = ResultsDataFrame(energy_system=es)

DE_inputs = myresults.slice_unstacked(bus_label="DE_bus_el", type="input",
                                      date_from=date_from, date_to=date_to,
                                      formatted=True)
DE_inputs.rename(columns={'DE_storage_phs': 'DE_storage_phs_out'},
                 inplace=True)

DE_outputs = myresults.slice_unstacked(bus_label="DE_bus_el", type="output",
                                       date_from=date_from, date_to=date_to,
                                       formatted=True)

DE_outputs.rename(columns={'DE_storage_phs': 'DE_storage_phs_in'},
                  inplace=True)

DE_other = myresults.slice_unstacked(bus_label="DE_bus_el", type="other",
                                     date_from=date_from, date_to=date_to,
                                     formatted=True)

DE_overall = pd.concat([DE_inputs, -DE_outputs], axis=1)

if (DE_overall.sum(axis=1).abs() > 0.0001).any():
    print('Bus not balanced')

# # %% output: plotting
# plot_data = DE_overall[
#     ['DE_solar', 'DE_wind',
#      'DE_pp_gas', 'DE_pp_hard_coal', 'DE_pp_lignite', 'DE_pp_uranium',
#      'DE_storage_phs_out', 'DE_shortage',
#      'DE_load', 'DE_storage_phs_in', 'DE_excess']]
# dispatch = plot_data.plot(kind='area', stacked=True, linewidth=0)
# dispatch.set_title('Power Plant Dispatch (Without NTCs)')
# dispatch.set_ylabel('Power in MW')
# dispatch.set_xlabel('Date and Time')
