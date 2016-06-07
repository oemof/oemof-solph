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

es = core_es.EnergySystem(groupings=solph.GROUPINGS,
                          time_idx=[i for i in range(0, timesteps_max)])

datetime_index = pd.date_range('1/1/2016', periods=timesteps_max, freq='60min')


nodes = NodesFromCSV(file_nodes_flows='nodes_flows.csv',
                     file_nodes_flows_sequences='nodes_flows_seq.csv',
                     delimiter=';')

om = OperationalModel(es, timeindex=datetime_index)

om.solve(solve_kwargs={'tee': True})

om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})

om.pprint()

logging.info('Done!')


print(nodes)
