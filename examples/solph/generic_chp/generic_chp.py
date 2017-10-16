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
                         outputs={bth: solph.Flow()})

demand_th = solph.Sink(label='demand_th', inputs={bth: solph.Flow(fixed=True,
                       actual_value=data['demand_el'], nominal_value=100)})

# power
bel = solph.Bus(label='bel')

demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
                       variable_costs=data['price_el'])})

# power plant (working as expected)
pp_working = solph.LinearTransformer(
        label='chp_gas_working',
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=100, variable_costs=2),
                 bth: solph.Flow(nominal_value=100, variable_costs=2)},
        conversion_factors={bel: 0.3, bth: 0.5})

# power plant (error with subsequently set outputs)
pp_not_working = solph.LinearTransformer(label='chp_gas_not_working',
                                         conversion_factors={bel: 0.5,
                                                             bth: 0.5})

# in/outputs seem to be set correctly
# but only input flows occur in bus balances
# see LP file!
pp_not_working.outputs.update({bel: solph.Flow(nominal_value=100,
                                               variable_costs=2),
                               bth: solph.Flow(nominal_value=100,
                                               variable_costs=2)})
pp_not_working.inputs.update({bgas: solph.Flow()})

print('### inputs/outputs after updating outputs manually')
for node in [bel, bgas, bth, pp_working, pp_not_working]:
    print('Node', node.label)
    print('Outputs: ', {k.label: v for k, v in node.outputs.items()})
    print('Inputs: ', {k.label: v for k, v in node.inputs.items()})

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
# weirdly, the flows are existent and included in the objective function...
