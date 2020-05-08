# -*- coding: utf-8 -*-

"""
This test contains a ExtractionTurbineCHP class.


This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_variable_chp/test_variable_chp.py

SPDX-License-Identifier: MIT
"""

import logging
import os

import pandas as pd
from nose.tools import eq_
from oemof import solph
from oemof.network.network import Node
from oemof.solph import views


def test_variable_chp(filename="variable_chp.csv", solver='cbc'):
    logging.info('Initialize the energy system')

    # create time index for 192 hours in May.
    date_time_index = pd.date_range('5/5/2012', periods=5, freq='H')
    energysystem = solph.EnergySystem(timeindex=date_time_index)
    Node.registry = energysystem

    # Read data file with heat and electrical demand (192 hours)
    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data = pd.read_csv(full_filename, sep=",")

    ##########################################################################
    # Create oemof.solph objects
    ##########################################################################

    logging.info('Create oemof.solph objects')

    # create natural gas bus
    bgas = solph.Bus(label=('natural', 'gas'))

    # create commodity object for gas resource
    solph.Source(label=('commodity', 'gas'),
                 outputs={bgas: solph.Flow(variable_costs=50)})

    # create two electricity buses and two heat buses
    bel = solph.Bus(label=('electricity', 1))
    bel2 = solph.Bus(label=('electricity', 2))
    bth = solph.Bus(label=('heat', 1))
    bth2 = solph.Bus(label=('heat', 2))

    # create excess components for the elec/heat bus to allow overproduction
    solph.Sink(label=('excess', 'bth_2'), inputs={bth2: solph.Flow()})
    solph.Sink(label=('excess', 'bth_1'), inputs={bth: solph.Flow()})
    solph.Sink(label=('excess', 'bel_2'), inputs={bel2: solph.Flow()})
    solph.Sink(label=('excess', 'bel_1'), inputs={bel: solph.Flow()})

    # create simple sink object for electrical demand for each electrical bus
    solph.Sink(label=('demand', 'elec1'), inputs={bel: solph.Flow(
        fix=data['demand_el'], nominal_value=1)})
    solph.Sink(label=('demand', 'elec2'), inputs={bel2: solph.Flow(
        fix=data['demand_el'], nominal_value=1)})

    # create simple sink object for heat demand for each thermal bus
    solph.Sink(label=('demand', 'therm1'), inputs={bth: solph.Flow(
        fix=data['demand_th'], nominal_value=741000)})
    solph.Sink(label=('demand', 'therm2'), inputs={bth2: solph.Flow(
        fix=data['demand_th'], nominal_value=741000)})

    # create a fixed transformer to distribute to the heat_2 and elec_2 buses
    solph.Transformer(
        label=('fixed_chp', 'gas'),
        inputs={bgas: solph.Flow(nominal_value=10e10)},
        outputs={bel2: solph.Flow(), bth2: solph.Flow()},
        conversion_factors={bel2: 0.3, bth2: 0.5})

    # create a fixed transformer to distribute to the heat and elec buses
    solph.components.ExtractionTurbineCHP(
        label=('variable_chp', 'gas'),
        inputs={bgas: solph.Flow(nominal_value=10e10)},
        outputs={bel: solph.Flow(), bth: solph.Flow()},
        conversion_factors={bel: 0.3, bth: 0.5},
        conversion_factor_full_condensation={bel: 0.5}
        )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = solph.Model(energysystem)

    logging.info('Solve the optimization problem')
    om.solve(solver=solver)

    optimisation_results = solph.processing.results(om)
    parameter = solph.processing.parameter_as_dict(energysystem)

    myresults = views.node(optimisation_results, "('natural', 'gas')")
    sumresults = myresults['sequences'].sum(axis=0)
    maxresults = myresults['sequences'].max(axis=0)

    variable_chp_dict_sum = {
        (("('natural', 'gas')", "('variable_chp', 'gas')"), 'flow'): 2823024,
        (("('natural', 'gas')", "('fixed_chp', 'gas')"), 'flow'): 3710208,
        (("('commodity', 'gas')", "('natural', 'gas')"), 'flow'): 6533232}

    variable_chp_dict_max = {
        (("('natural', 'gas')", "('variable_chp', 'gas')"), 'flow'): 630332,
        (("('natural', 'gas')", "('fixed_chp', 'gas')"), 'flow'): 785934,
        (("('commodity', 'gas')", "('natural', 'gas')"), 'flow'): 1416266}

    for key in variable_chp_dict_max.keys():
        logging.debug("Test the maximum value of {0}".format(key))
        eq_(int(round(maxresults[key])),
            int(round(variable_chp_dict_max[key])))

    for key in variable_chp_dict_sum.keys():
        logging.debug("Test the summed up value of {0}".format(key))
        eq_(int(round(sumresults[key])),
            int(round(variable_chp_dict_sum[key])))

    eq_(parameter[(energysystem.groups["('fixed_chp', 'gas')"], None)]
        ['scalars']['label'], "('fixed_chp', 'gas')")
    eq_(parameter[(energysystem.groups["('fixed_chp', 'gas')"], None)]
        ['scalars']["conversion_factors_('electricity', 2)"], 0.3)

    # objective function
    eq_(round(solph.processing.meta_results(om)['objective']), 326661590)
