# -*- coding: utf-8 -*-
"""
Simple energy system optimization  problem with multiple energy systems

Tested with oemof version 0.0.5

Info:
simon.hilpert@fh-flensburg.de
"""
from oemof.solph import predefined_objectives as predefined_objectives
from oemof.core import energy_system as es
from oemof.core.network.entities.buses import Bus
import oemof.core.network.entities.components as cp
import pandas as pd

# time_index is needed for energy system
time_index = pd.date_range('1/1/2012', periods=3, freq='H')

# setting sumulation parameters
simulation = es.Simulation(timesteps=range(len(time_index)),
                           verbose=True, solver='glpk',
                           objective_options={'function':
                                          predefined_objectives.minimize_cost})
# first system
sys1 = es.EnergySystem(time_idx=time_index, simulation=simulation)
bel1 = Bus(uid="bel1", type="el", shortage_costs=70, balanced=True,
           shortage=True)
demand1 = cp.sinks.Simple(uid="demand", inputs=[bel1], val=[1,2,3])

# second system
sys2 = es.EnergySystem()
bel2 = Bus(uid="bel2", type="el", shortage_costs=70, balanced=True,
           shortage=True)
demand2 = cp.sinks.Simple(uid="demand1", inputs=[bel2], val=[4,5,6])

# "merge" sys1 and sys2
sys3 = es.EnergySystem(time_idx=time_index, simulation=simulation)
sys3.entities = sys1.entities + sys2.entities

# connect buses with transport
sys3.connect(bel1, bel2, in_max=10, out_max=10, eta=0.9,
             transport_class=cp.transports.Simple)

# optimize system 3
sys3.optimize()
