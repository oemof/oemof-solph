# -*- coding: utf-8 -*-

from oemof.core import energy_system as oces
import pandas as pd

nodes = pd.read_csv('nodes.csv', sep=',')



nodes.index = pd.date_range('1/1/2015', periods=len(df), freq='H')



es = oces.EnergySystem(groupings=GROUPINGS,
                       time_idx=[1,2,3])

lt = len(es.time_idx)

bel = Bus(label="el_balance")
bcoal = Bus(label="coalbus")

so = Source(label="coalsource",
            outputs={bcoal: Flow()})

wind = Source(label="wind", outputs={
    bel:Flow(actual_value=[1, 1, 2],
             nominal_value=2,
             fixed_costs=25,
             investment=Investment(maximum=100, epc=200))
    }
)

si = Sink(label="sink", inputs={bel: Flow(max=[0.1, 0.2, 0.9],
                                          nominal_value=10, fixed=True,
                                          actual_value=[1, 2, 3])})

trsf = LinearTransformer(label='trsf', inputs={bcoal:Flow()},
                         outputs={bel:Flow(nominal_value=10,
                                           fixed_costs=5,
                                           variable_costs=10,
                                           summed_max=4,
                                           summed_min=2)},
                         conversion_factors={bel: 0.4})
stor = Storage(label="stor", inputs={bel: Flow()}, outputs={bel:Flow()},
               nominal_capacity=50, inflow_conversion_factor=0.9,
               outflow_conversion_factor=0.8, initial_capacity=0.5,
               capacity_loss=0.001)

date_time_index = pd.date_range('1/1/2011', periods=3, freq='60min')
om = OperationalModel(es, timeindex=date_time_index)
om.solve(solve_kwargs={'tee': True})
om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})
#om.pprint()
