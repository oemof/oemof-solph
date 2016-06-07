# -*- coding: utf-8 -*-

import math
import logging
import pandas as pd

from oemof.tools import logger
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import OperationalModel
from oemof.solph.options import NodesFromCSV


nodes = NodesFromCSV(file_nodes_flows='nodes_flows.csv',
                     file_nodes_flows_sequences='nodes_flows_seq.csv',
                     delimiter=';')

print(nodes)
