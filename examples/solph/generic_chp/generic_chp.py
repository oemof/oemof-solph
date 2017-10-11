# -*- coding: utf-8 -*-
"""
Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.
"""

import pandas as pd
import oemof.solph as solph



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

# power plant
pp_gas = solph.LinearTransformer(label='fixed_chp_gas',
                                 conversion_factors={bel: 0.5, bth: 0.5})


# outputs seem to be set correctly
pp_gas.outputs.update({bel: solph.Flow(), bth: solph.Flow()})
print('Outputs: ', {k.label: v for k, v in pp_gas.outputs.items()})

# inputs are changed via bus output and thus empty (and they work)
pp_gas.inputs.update({bgas: solph.Flow()})
print('Inputs: ', {k.label: v for k, v in pp_gas.inputs.items()})

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
