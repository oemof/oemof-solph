
# -*- coding: utf-8 -*-

import pandas as pd

# Default logger of oemof
from oemof.tools import logger
import oemof.solph as solph


t_idx_1 = pd.date_range('1/1/2020', periods=5, freq='H')
t_idx_2 = pd.date_range('1/1/2030', periods=5, freq='H')
t_idx_3 = pd.date_range('1/1/2040', periods=5, freq='H')

timeindex = {'1': t_idx_1, '2': t_idx_2, '3': t_idx_3}

energysystem = solph.EnergySystem(timeindex=timeindex)

# create electricity bus
bel = solph.Bus(label="bel")
bel.sector = 'electricity'


solph.Sink(label='excess_el', inputs={bel: solph.Flow()})


solph.Source(label='wind',
             outputs={bel:
                solph.Flow(actual_value=1,
                           fixed=True,
                           investment=solph.Expansion())})

solph.Source(label="pv",
             outputs={bel:
                solph.Flow(actual_value=1,
                           fixed=True,
                           investment=solph.Expansion())})

solph.Source(
    label="pp_gas",
    outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50,
                             investment=solph.Expansion())},
    conversion_factors={bel: 0.58})

em = solph.ExpansionModel(energysystem)

import pdb; pdb.set_trace()
