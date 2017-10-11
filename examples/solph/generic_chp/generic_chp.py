# -*- coding: utf-8 -*-
"""
Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.
"""

import matplotlib.pyplot as plt
import pandas as pd
import oemof.solph as solph
from oemof.outputlib import processing, views


# read sequence data
data = pd.read_csv('data.csv', sep=",")

# select periods
periods = len(data[1:3])

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)

# resources
bgas = solph.Bus(label='bgas')

rgas = solph.Source(label='rgas', outputs={bgas: solph.Flow()})

# heat
bth = solph.Bus(label='bth')

source_th = solph.Source(label='source_th',
                         outputs={bth: solph.Flow(variable_costs=1000)})

demand_th = solph.Sink(label='demand_th', inputs={bth: solph.Flow(fixed=True,
                       actual_value=data['demand_el'], nominal_value=100)})

# power
bel = solph.Bus(label='bel')

demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
                       variable_costs=data['price_el'])})

# generic chp
ccgt = solph.custom.GenericCHP(label='pp_generic_chp',
                               fuel_input={bgas: solph.Flow(foo='bar')},
                               electrical_output={bel: solph.Flow(
                                                     P_max_woDH=[217.35 for p in range(0, periods)],
                                                     P_min_woDH=[89.10 for p in range(0, periods)],
                                                     Eta_el_max_woDH=[0.57 for p in range(0, periods)],
                                                     Eta_el_min_woDH=[0.47 for p in range(0, periods)])},
                               heat_output={bth: solph.Flow(Q_CW_min=[27.85 for p in range(0, periods)], variable_costs=1)},
                               Beta=[0.12 for p in range(0, periods)])

# inputs are changed via bus output and thus empty (and they work)
print({k: dir(v) for k, v in ccgt.inputs.items()})

# outputs seem to be set correctly
print({k: dir(v) for k, v in ccgt.outputs.items()})

# create an optimization problem and solve it
om = solph.OperationalModel(es)

# debugging
#om.pprint()
om.write('my_model.lp', io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver='glpk', solve_kwargs={'tee': True})

# @gnn, simnh: have a look at the LP-file!
# why are the flows into the heat and electrical bus not included in the
# respective balances?! because inputs and outputs are changed subsequently!?
# -> see in the network classes constructor (custom.py)
# weirdly, the flows are existent and included in the objective function...
