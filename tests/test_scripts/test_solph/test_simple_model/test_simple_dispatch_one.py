# -*- coding: utf-8 -*-

""" This example shows how to create an energysystem with oemof objects and
solve it with the solph module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_simple_dispatch/test_simple_dispatch.py

SPDX-License-Identifier: MIT
"""

from nose.tools import eq_
from oemof.network.network import Node
from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph import Sink
from oemof.solph import Source
from oemof.solph import Transformer
from oemof.solph import processing
from oemof.solph import views


def test_dispatch_one_time_step(solver='cbc'):
    """Create an energy system and optimize the dispatch at least costs."""

    # ######################### create energysystem components ################
    Node.registry = None

    # resource buses
    bgas = Bus(label='gas', balanced=False)

    # electricity and heat
    bel = Bus(label='b_el')
    bth = Bus(label='b_th')

    # an excess and a shortage variable can help to avoid infeasible problems
    excess_el = Sink(label='excess_el', inputs={bel: Flow()})

    # sources
    wind = Source(label='wind', outputs={bel: Flow(
        fix=0.5, nominal_value=66.3)})

    # demands (electricity/heat)
    demand_el = Sink(label='demand_elec', inputs={bel: Flow(nominal_value=85,
                     fix=0.3)})

    demand_th = Sink(label='demand_therm',
                     inputs={bth: Flow(nominal_value=40,
                                       fix=0.2)})

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
    heat_pump = Transformer(label='heat_pump',
                            inputs={bel: Flow(), b_heat_source: Flow()},
                            outputs={bth: Flow(nominal_value=10)},
                            conversion_factors={
                                        bel: 1/3, b_heat_source: (cop-1)/cop})

    energysystem = EnergySystem(timeindex=[1])
    energysystem.add(bgas, bel, bth, excess_el, wind, demand_el, demand_th,
                     pp_chp, b_heat_source, heat_source, heat_pump)

    # ################################ optimization ###########################

    # create optimization model based on energy_system
    optimization_model = Model(energysystem=energysystem, timeincrement=1)

    # solve problem
    optimization_model.solve(solver=solver)

    # write back results from optimization object to energysystem
    optimization_model.results()

    # ################################ results ################################
    data = views.node(processing.results(om=optimization_model), 'b_el')

    # generate results to be evaluated in tests
    results = data['sequences'].sum(axis=0).to_dict()

    test_results = {
        (('wind', 'b_el'), 'flow'): 33,
        (('b_el', 'demand_elec'), 'flow'): 26,
        (('b_el', 'excess_el'), 'flow'): 5,
        (('b_el', 'heat_pump'), 'flow'): 3,
    }

    for key in test_results.keys():
        eq_(int(round(results[key])), int(round(test_results[key])))
