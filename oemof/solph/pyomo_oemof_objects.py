# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:23:56 2016

@author: simon
"""

from pyomo.environ import *
import oemof.solph as os
from oemof.core import energy_system as oces


es = oces.EnergySystem(time_idx=[1,2,3])

lt = len(es.time_idx)


bel = os.Bus(label="el")
# TODO: Resolve error by 'unsused' busses??
#bth = Bus(label="th")

bcoal = os.Bus(label="coalbus")

so = os.Source(label="coalsource",
            outputs={bcoal: os.Flow(max=[None]*lt,
                                 actual_value=[None]*lt,
                                 nominal_value=None)})

si = os.Sink(label="sink", inputs={bel: os.Flow(min=[0]*lt,
                                          max=[0.1, 0.2, 0.9],
                                          nominal_value=10, fixed=True,
                                          actual_value=[1, 2, 3])})

trsf = os.LinearTransformer(label='trsf', inputs={
                                     bcoal:os.Flow(min=[0]*lt,
                                                max=[1]*lt,
                                                nominal_value=None,
                                                actual_value=[None]*lt)},
                         outputs={bel:os.Flow(min=[0.5, 0.5, 0.5],
                                           max=[1, 1, 1],
                                           nominal_value=10,
                                           actual_value=[None]*lt),
                                  bcoal:os.Flow(min=[0.5, 0.4, 0.4],
                                             max=[1, 1, 1],
                                             nominal_value=30,
                                             actual_value=[None]*lt)},
                         conversion_factors={bel: [0.4]*lt,
                                             bcoal: [0.5]*lt})

m = ConcreteModel()

# flow set index be tuple of objects
m.FLOWS = Set(initialize=[(source, target) for source in es.nodes
                                           for target in source.outputs], ordered=True)

m.TIMESTEPS = Set(initialize=range(len(es.time_idx)), ordered=True)

# flow variable indexed by tuples of objects and timesteps  (causes the error)
m.flows = Var(m.FLOWS, m.TIMESTEPS)

m.objective = Objective(expr=1)

try:
    m.write('problem_oemof_objects.lp')
except:
    raise ValueError("THIS FAILS, See message above WHY ;)")



