# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `GenericCAES` can be used.

"""

import matplotlib.pyplot as plt
import pandas as pd
import oemof.solph as solph
from oemof.outputlib import processing, views


# read sequence data
file_name = 'generic_caes.csv'
data = pd.read_csv(file_name, sep=",")

# select periods
periods = len(data)-1

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)

# resources
bgas = solph.Bus(label='bgas')

rgas = solph.Source(label='rgas', outputs={bgas: solph.Flow()})

# heat
bth = solph.Bus(label='bth')

source_th = solph.Source(label='source_th',
                         outputs={bth: solph.Flow(variable_costs=100)})

demand_th = solph.Sink(label='demand_th', inputs={bth: solph.Flow()})

# power
bel = solph.Bus(label='bel')

source_el = solph.Source(label='source_el',
                         outputs={bel: solph.Flow(variable_costs=100)})

# demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
#                        variable_costs=data['price_el'])})
demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(fixed=True,
                       actual_value=data['demand_el'], nominal_value=100)})

# generic caes plant
caes = solph.custom.GenericCAES(
    label='compressed_air_energy_storage',
    fuel_input={bgas: solph.Flow()},
    electrical_output={bel: solph.Flow()},
    heat_output={bth: solph.Flow()},
    fixed_costs=0)

# create an optimization problem and solve it
om = solph.OperationalModel(es)

# debugging
#om.write('generic_caes.lp', io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver='gurobi', solve_kwargs={'tee': True})

# create result object
results = processing.results(om)

# store as csv
#data = results[(caes,)]['sequences'].to_csv('results_' + file_name)

# plot CAES (line)
data = results[(caes,)]['sequences']
ax = data.plot(kind='line', drawstyle='steps-post', grid=True)
ax.set_xlabel('Time')
ax.set_ylabel('(MW)')
plt.show()

# plot bus
data = views.node(results, 'bel')
ax = data['sequences'].plot(kind='line', drawstyle='steps-post', grid=True)
ax.set_title('Dispatch')
ax.set_xlabel('')
ax.set_ylabel('Power (MW)')
plt.show()
