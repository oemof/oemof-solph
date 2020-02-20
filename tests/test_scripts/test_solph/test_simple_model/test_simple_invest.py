# -*- coding: utf-8 -*-

""" This example shows how to create an energysystem with oemof objects and
solve it with the solph module. Results are plotted with outputlib.

Data: example_data.csv

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_simple_dispatch/test_simple_dispatch.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose.tools import eq_
import os
import pandas as pd
from oemof.solph import (Sink, Source, Transformer, Bus, Flow, Model,
                         EnergySystem, Investment)
from oemof.tools import economics
from oemof.outputlib import processing, views
from oemof.network import Node


def test_dispatch_example(solver='cbc', periods=24*5):
    """Create an energy system and optimize the dispatch at least costs."""
    Node.registry = None

    filename = os.path.join(os.path.dirname(__file__), 'input_data.csv')
    data = pd.read_csv(filename, sep=",")

    # ######################### create energysystem components ################

    # resource buses
    bcoal = Bus(label='coal', balanced=False)
    bgas = Bus(label='gas', balanced=False)
    boil = Bus(label='oil', balanced=False)
    blig = Bus(label='lignite', balanced=False)

    # electricity and heat
    bel = Bus(label='b_el')
    bth = Bus(label='b_th')

    # an excess and a shortage variable can help to avoid infeasible problems
    excess_el = Sink(label='excess_el', inputs={bel: Flow()})
    # shortage_el = Source(label='shortage_el',
    #                      outputs={bel: Flow(variable_costs=200)})

    # sources
    ep_wind = economics.annuity(capex=1000, n=20, wacc=0.05)
    wind = Source(label='wind', outputs={bel: Flow(
                    actual_value=data['wind'], fixed=True,
                    investment=Investment(ep_costs=ep_wind, existing=100))})

    ep_pv = economics.annuity(capex=1500, n=20, wacc=0.05)
    pv = Source(label='pv', outputs={bel: Flow(
                    actual_value=data['pv'], fixed=True,
                    investment=Investment(ep_costs=ep_pv, existing=80))})

    # demands (electricity/heat)
    demand_el = Sink(label='demand_elec', inputs={bel: Flow(nominal_value=85,
                     actual_value=data['demand_el'], fixed=True)})

    demand_th = Sink(label='demand_therm',
                     inputs={bth: Flow(nominal_value=40,
                                       actual_value=data['demand_th'],
                                       fixed=True)})

    # power plants
    pp_coal = Transformer(label='pp_coal',
                          inputs={bcoal: Flow()},
                          outputs={bel: Flow(nominal_value=20.2,
                                             variable_costs=25)},
                          conversion_factors={bel: 0.39})

    pp_lig = Transformer(label='pp_lig',
                         inputs={blig: Flow()},
                         outputs={bel: Flow(nominal_value=11.8,
                                            variable_costs=19)},
                         conversion_factors={bel: 0.41})

    pp_gas = Transformer(label='pp_gas',
                         inputs={bgas: Flow()},
                         outputs={bel: Flow(nominal_value=41,
                                            variable_costs=40)},
                         conversion_factors={bel: 0.50})

    pp_oil = Transformer(label='pp_oil',
                         inputs={boil: Flow()},
                         outputs={bel: Flow(nominal_value=5,
                                            variable_costs=50)},
                         conversion_factors={bel: 0.28})

    # combined heat and power plant (chp)
    pp_chp = Transformer(label='pp_chp',
                         inputs={bgas: Flow()},
                         outputs={bel: Flow(nominal_value=30,
                                            variable_costs=42),
                                  bth: Flow(nominal_value=40)},
                         conversion_factors={bel: 0.3, bth: 0.4})

    # heatpump with a coefficient of performance (COP) of 3
    b_heat_source = Bus(label='b_heat_source')

    heat_source = Source(label='heat_source', outputs={b_heat_source: Flow()})

    cop = 3
    heat_pump = Transformer(label='el_heat_pump',
                            inputs={bel: Flow(), b_heat_source: Flow()},
                            outputs={bth: Flow(nominal_value=10)},
                            conversion_factors={
                                        bel: 1/3, b_heat_source: (cop-1)/cop})

    datetimeindex = pd.date_range('1/1/2012', periods=periods, freq='H')
    energysystem = EnergySystem(timeindex=datetimeindex)
    energysystem.add(bcoal, bgas, boil, bel, bth, blig, excess_el, wind, pv,
                     demand_el, demand_th, pp_coal, pp_lig, pp_oil, pp_gas,
                     pp_chp, b_heat_source, heat_source, heat_pump)

    # ################################ optimization ###########################

    # create optimization model based on energy_system
    optimization_model = Model(energysystem=energysystem)

    # solve problem
    optimization_model.solve(solver=solver)

    # write back results from optimization object to energysystem
    optimization_model.results()

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
    comp_results['wind_capacity'] = results[(wind, bel)]['scalars'].invest

    test_results = {
        (('wind', 'b_el'), 'flow'): 9239,
        (('pv', 'b_el'), 'flow'): 1147,
        (('b_el', 'demand_elec'), 'flow'): 7440,
        (('b_el', 'excess_el'), 'flow'): 6261,
        (('pp_chp', 'b_el'), 'flow'): 477,
        (('pp_lig', 'b_el'), 'flow'): 850,
        (('pp_gas', 'b_el'), 'flow'): 934,
        (('pp_coal', 'b_el'), 'flow'): 1256,
        (('pp_oil', 'b_el'), 'flow'): 0,
        (('b_el', 'el_heat_pump'), 'flow'): 202,
        'pv_capacity': 44,
        'wind_capacity': 246,
    }

    for key in test_results.keys():
        eq_(int(round(comp_results[key])), int(round(test_results[key])))
