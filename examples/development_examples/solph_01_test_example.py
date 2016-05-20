# -*- coding: utf-8 -*-

import logging

from oemof.tools import logger
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import (Bus, Source, Sink, Flow, Investment, LinearTransformer,
                        Storage)
from oemof.solph import OperationalModel



logger.define_logging()

es = core_es.EnergySystem(groupings=solph.GROUPINGS,
                          time_idx=[1, 2, 3])

ebus = Bus(label="el")

gasbus = Bus(label="gas")

so = Source(
    label="source",
    outputs={ebus: Flow(actual_value=[10, 5, 10], fixed=True,
                        investement=Investment(maximum=1000))})

si = Sink(
    label="sink",
    inputs={ebus: Flow(min=[0, 0, 0], max=[0.1, 0.2, 0.9], nominal_value=10,
                       fixed=True)})

ltransf = LinearTransformer(
    label="trsf",
    inputs={gasbus: Flow()},
    outputs={ebus: Flow(max=[1.0, 0.8, 0.9], nominal_value=100)},
    conversion_factors={ebus: 0.5})

estorage = Storage(
    label="storage",
    inputs={ebus: Flow()}, outputs={ebus: Flow(nominal_value=100)},
    nominal_capacity=500, capacity_loss=0.1, nominal_input_capacity_ratio=0.2,
    nominal_output_capacity_ratio=0.5, inflow_conversion_factor=1,
    outflow_conversion_factor=1)

date_time_index = pd.date_range('1/1/2011', periods=3, freq='60min')
om = OperationalModel(es, timeindex=date_time_index)
om.solve(solve_kwargs={'tee': True})
om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})

om.pprint()

logging.info('Done!')
