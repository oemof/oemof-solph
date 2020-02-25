# -*- coding: utf-8 -*-

""" This example shows how to create an energysystem with oemof objects and
solve it with the solph module. Results are plotted with outputlib.

Data: example_data.csv

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_simple_dispatch/test_simple_dispatch.py

SPDX-License-Identifier: MIT
"""

from nose.tools import eq_
import os
import pandas as pd
from oemof.solph import (Sink, Source, Transformer, Bus, Flow, Model,
                         EnergySystem, Investment)
from oemof.tools import economics
from oemof.outputlib import processing, views
from oemof.network import Node


def test_dispatch_example(solver='cbc', periods=10):
    """Invest in a flow with a `fix` sequence containing values > 1."""
    Node.registry = None

    filename = os.path.join(os.path.dirname(__file__), 'input_data.csv')
    data = pd.read_csv(filename, sep=",")

    # ######################### create energysystem components ################

    # electricity and heat
    bel = Bus(label='b_el')

    # an excess and a shortage variable can help to avoid infeasible problems
    excess_el = Sink(
        label='excess_el',
        inputs={bel: Flow()}
    )

    # shortage_el = Source(label='shortage_el',
    #                      outputs={bel: Flow(variable_costs=200)})

    # sources
    ep_pv = economics.annuity(capex=1500, n=20, wacc=0.05)

    pv = Source(
        label='pv',
        outputs={
            bel: Flow(
                fix=data['pv'],
                investment=Investment(ep_costs=ep_pv)
            )
        }
    )

    # demands (electricity/heat)
    demand_el = Sink(
        label='demand_elec',
        inputs={
            bel: Flow(
                nominal_value=85,
                fix=data['demand_el']
            )
        }
    )

    datetimeindex = pd.date_range('1/1/2012', periods=periods, freq='H')

    energysystem = EnergySystem(timeindex=datetimeindex)

    energysystem.add(bel, excess_el, pv, demand_el)

    # ################################ optimization ###########################

    # create optimization model based on energy_system
    optimization_model = Model(energysystem=energysystem)

    # solve problem
    optimization_model.solve(solver=solver)

    # ################################ results ################################

    # generic result object
    results = processing.results(om=optimization_model)

    # subset of results that includes all flows into and from electrical bus
    # sequences are stored within a pandas.DataFrames and scalars e.g.
    # investment values within a pandas.Series object.
    # in this case the entry data['scalars'] does not exist since no investment
    # variables are used
    data = views.node(results, 'b_el')

    # generate results to be evaluated in tests
    comp_results = data['sequences'].sum(axis=0).to_dict()
    comp_results['pv_capacity'] = results[(pv, bel)]['scalars'].invest

    assert comp_results[(('pv', 'b_el'), 'flow')] > 0

    # test_results = {
    #     (('pv', 'b_el'), 'flow'): 2150.5,
    #     (('b_el', 'demand_elec'), 'flow'): 436.05,
    #     (('b_el', 'excess_el'), 'flow'): 1714.45,
    #     'pv_capacity': 467.5,
    # }

    # for key in test_results.keys():
    #     eq_(int(round(comp_results[key])), int(round(test_results[key])))
