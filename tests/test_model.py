# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_network_classes.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import pandas as pd
from oemof.solph import Sink, Source, Bus, Flow, Model, EnergySystem


def test_dispatch_example(solver='cbc'):
    """Create an energy system and optimize the dispatch at least costs."""
    datetimeindex = pd.date_range('1/1/2012', periods=3, freq='H')
    es = EnergySystem(timeindex=datetimeindex)
    
    bel = Bus(label='b_el')
    es.add(bel)
    es.add(Source(label='src', outputs={bel: Flow(actual_value=[1, 2, 3],
           nominal_value=1, fixed=True)}))

    es.add(Sink(label='demand_elec', inputs={bel: Flow(nominal_value=1,
                actual_value=[1, 2, 3], fixed=True)}))

    optimization_model = Model(energysystem=es)
    optimization_model.solve(solver=solver)

    # write back results from optimization object to energysystem
    optimization_model.results()
