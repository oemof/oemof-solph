# -*- coding: utf-8 -*-

import logging
import pandas as pd

from oemof.tools import logger
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import OperationalModel
from oemof.solph.options import NodesFromCSV
from oemof.outputlib import to_pandas as tpd
from collections import Iterable


logger.define_logging()

timesteps_max = 25

datetime_index = pd.date_range('1/1/2012', periods=timesteps_max, freq='60min')

es = core_es.EnergySystem(groupings=solph.GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows='nodes_flows.csv',
                     file_nodes_flows_sequences='nodes_flows_seq_minimal.csv',
                     delimiter=',')

# print out nodes
for k, v in nodes.items():
    attrs = dir(v)
    print('\n OBJ:', k, type(v))
    print('--------------------')
    for i in attrs:
        if '_' not in i:
            # dirty hack to print weakref dicts by converting to list
            o = getattr(v, str(i))
            if isinstance(o, Iterable) and not isinstance(o, str):
                o = list(o)
            print(i, ':', o)

om = OperationalModel(es, timeindex=datetime_index)

om.solve(solver='gurobi', solve_kwargs={'tee': True})

om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})

logging.info('Done!')

logging.info('Check the results')

myresults = tpd.DataFramePlot(energy_system=es)

chp1_in = myresults.slice_by(obj_label='chp1', type='input',
                             date_from='2012-01-01 00:00:00',
                             date_to='2012-12-31 23:00:00')

chp1_out = myresults.slice_by(obj_label='chp1', type='output',
                              date_from='2012-01-01 00:00:00',
                              date_to='2012-12-31 23:00:00')

demand = myresults.slice_by(obj_label='demand1',
                            date_from='2012-01-01 00:00:00',
                            date_to='2012-12-31 23:00:00')

wind = myresults.slice_by(obj_label='wind1',
                          date_from='2012-01-01 00:00:00',
                          date_to='2012-12-31 23:00:00')

pv = myresults.slice_by(obj_label='solar1',
                        date_from='2012-01-01 00:00:00',
                        date_to='2012-12-31 23:00:00')


logging.info('Plot the results')

cdict = {'wind1': '#5b5bae',
         'colar1': '#ffde32',
         'storage1': '#42c77a',
         'chp1': '#636f6b',
         'demand1': '#ce4aff'}

# Plotting the input flows of the electricity bus for January
myplot = tpd.DataFramePlot(energy_system=es)
myplot.slice_unstacked(bus_label="bus_el1", type="input",
                       date_from="2012-01-01 00:00:00",
                       date_to="2012-01-31 00:00:00")
colorlist = myplot.color_from_dict(cdict)
myplot.plot(color=colorlist, linewidth=2, title="January 2012")
myplot.ax.legend(loc='upper right')
myplot.ax.set_ylabel('Power in MW')
myplot.ax.set_xlabel('Date')
myplot.set_datetime_ticks(date_format='%d-%m-%Y', tick_distance=24*7)
