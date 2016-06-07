# -*- coding: utf-8 -*-

import math
import logging
import pandas as pd

from oemof.tools import logger
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import OperationalModel
from oemof.solph.options import NodesFromCSV


logger.define_logging()

timesteps_max = 8760

es = core_es.EnergySystem(groupings=solph.GROUPINGS)

datetime_index = pd.date_range('1/1/2016', periods=timesteps_max, freq='60min')

nodes = NodesFromCSV(file_nodes_flows='nodes_flows.csv',
                     file_nodes_flows_sequences='nodes_flows_seq.csv',
                     delimiter=';')

print(nodes)

# print out nodes
# errors: confused labels for sources
for k, v in nodes.items():
    attrs = dir(v)
    print('\n OBJ:', k, v)
    print('--------------------')
    for i in attrs:
        if '_' not in i:
            print(i, ':', getattr(v, str(i)))

#om = OperationalModel(es, timeindex=datetime_index)
#
#om.solve(solve_kwargs={'tee': True})
#
#om.write('optimization_problem.lp',
#         io_options={'symbolic_solver_labels': True})
#
#om.pprint()
#
#logging.info('Done!')
