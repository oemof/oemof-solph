# -*- coding: utf-8 -*-

import logging

from oemof.tools import logger
from oemof.core import energy_system as core_es

from oemof.solph import Bus
from oemof.solph import Source
from oemof.solph import Sink
from oemof.solph import Flow
from oemof.solph import Investment
from oemof.solph import LinearTransformer
from oemof.solph import Storage
from oemof.solph import constraint_grouping
from oemof.solph import objective_grouping
from oemof.solph import OperationalModel


logger.define_logging()

es = core_es.EnergySystem(groupings=[constraint_grouping, objective_grouping],
                       time_idx=[1, 2, 3])

ebus = Bus(label="el")

gasbus = Bus(label="gas")

so = Source(outputs={ebus: Flow(actual_value=[10, 5, 10], fixed=True,
                                investement=Investment(maximum=1000))})

si = Sink(inputs={ebus: Flow(
    min=[0, 0, 0], max=[0.1, 0.2, 0.9], nominal_value=10, fixed=True)})

ltransf = LinearTransformer(
    inputs={gasbus: Flow()},
    outputs={ebus: Flow(max=[1.0, 0.8, 0.9], nominal_value=100)})

estorage = Storage(
    inputs={ebus: Flow()}, outputs={ebus: Flow(nominal_value=100)},
    nominal_capacity=500, capacity_loss=0.1, nominal_input_capacity_ratio=0.2,
    nominal_output_capacity_ratio=0.5, inflow_conversion_factor=1,
    outflow_conversion_factor=1)

om = OperationalModel(es)

om.pprint()

logging.info('Done!')
