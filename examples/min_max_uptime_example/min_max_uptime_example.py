# -*- coding: utf-8 -*-
"""
Example that shows how to use a combination of minimum and maximum uptime.

SPDX-FileCopyrightText: Johannes Röder <johannes.roeder@uni-bremen.de>

SPDX-License-Identifier: MIT
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


from oemof.solph import components
from oemof.solph import Flow, Bus, EnergySystem, Model
from oemof.solph._options import Investment, NonConvex

import oemof.network
from oemof.solph import processing, views
from oemof.solph import helpers
import logging


data_demand = [1, 2, 4, 5, 6, 4, 3, 2, 6, 7,
               7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
               8, 8, 2, 1, 0, 5, 6]

# select periods
periods = len(data_demand)

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = EnergySystem(timeindex=idx)
# oemof.network.Node.registry = es

# bus_0 = solph.Bus(label='bus_0')
bus_1 = Bus(label='bus')

es.add(bus_1)

es.add(components.Source(
    label='NonConvexSource',
    outputs={bus_1: Flow(
        variable_costs=10,
        nominal_value=4,
        min=1,
        nonconvex=NonConvex(
            minimum_downtime=2,
            minimum_uptime=3,
            maximum_uptime=3,
        ),
    )},
))

es.add(components.Source(
    label='Shortage_Source',
    outputs={bus_1: Flow(
        variable_costs=1000,
    )},
))

es.add(components.Sink(label='demand', inputs={
    bus_1: Flow(fix=data_demand,  nominal_value=1)}))


# create an optimization problem and solve it
om = Model(es)

# export lp file
filename = os.path.join(
    helpers.extend_basic_path('lp_files'), 'NonconvexDSM.lp')
logging.info('Store lp-file in {0}.'.format(filename))
om.write(filename, io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver='cbc', solve_kwargs={'tee': True})

# create result object


results = processing.results(om)

bus1 = views.node(results, 'bus')["sequences"]
bus1.plot(kind='line', drawstyle='steps-mid')
plt.legend()
plt.show()
