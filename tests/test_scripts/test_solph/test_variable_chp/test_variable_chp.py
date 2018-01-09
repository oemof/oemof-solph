# -*- coding: utf-8 -*-

"""
This test contains a ExtractionTurbineCHP class.

"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

from nose.tools import eq_
import logging
import os
import pandas as pd

from oemof import outputlib

from oemof.network import Node
import oemof.solph as solph


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
    bgas = solph.Bus(label="natural_gas")

    # create commodity object for gas resource
    solph.Source(label='rgas', outputs={bgas: solph.Flow(variable_costs=50)})

    # create two electricity buses and two heat buses
    bel = solph.Bus(label="electricity")
    bel2 = solph.Bus(label="electricity_2")
    bth = solph.Bus(label="heat")
    bth2 = solph.Bus(label="heat_2")

    # create excess components for the elec/heat bus to allow overproduction
    solph.Sink(label='excess_bth_2', inputs={bth2: solph.Flow()})
    solph.Sink(label='excess_therm', inputs={bth: solph.Flow()})
    solph.Sink(label='excess_bel_2', inputs={bel2: solph.Flow()})
    solph.Sink(label='excess_elec', inputs={bel: solph.Flow()})

    # create simple sink object for electrical demand for each electrical bus
    solph.Sink(label='demand_elec', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})
    solph.Sink(label='demand_el_2', inputs={bel2: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    # create simple sink object for heat demand for each thermal bus
    solph.Sink(label='demand_therm', inputs={bth: solph.Flow(
        actual_value=data['demand_th'], fixed=True, nominal_value=741000)})
    solph.Sink(label='demand_th_2', inputs={bth2: solph.Flow(
        actual_value=data['demand_th'], fixed=True, nominal_value=741000)})

    # create a fixed transformer to distribute to the heat_2 and elec_2 buses
    solph.Transformer(
        label='fixed_chp_gas',
        inputs={bgas: solph.Flow(nominal_value=10e10)},
        outputs={bel2: solph.Flow(), bth2: solph.Flow()},
        conversion_factors={bel2: 0.3, bth2: 0.5})

    # create a fixed transformer to distribute to the heat and elec buses
    solph.components.ExtractionTurbineCHP(
        label='variable_chp_gas',
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

    optimisation_results = outputlib.processing.results(om)

    myresults = outputlib.views.node(optimisation_results, 'natural_gas')
    sumresults = myresults['sequences'].sum(axis=0)
    maxresults = myresults['sequences'].max(axis=0)

    variable_chp_dict_sum = {
        (('natural_gas', 'fixed_chp_gas'), 'flow'): 3710208,
        (('natural_gas', 'variable_chp_gas'), 'flow'): 2823024,
        (('rgas', 'natural_gas'), 'flow'): 6533232}

    variable_chp_dict_max = {
        (('natural_gas', 'fixed_chp_gas'), 'flow'): 785934,
        (('natural_gas', 'variable_chp_gas'), 'flow'): 630332,
        (('rgas', 'natural_gas'), 'flow'): 1416266}

    for key in variable_chp_dict_max.keys():
        logging.debug("Test the maximum value of {0}".format(key))
        eq_(int(round(maxresults[key])), int(round(variable_chp_dict_max[key])))

    for key in variable_chp_dict_sum.keys():
        logging.debug("Test the summed up value of {0}".format(key))
        eq_(int(round(sumresults[key])), int(round(variable_chp_dict_sum[key])))

    # objective function
    eq_(round(outputlib.processing.meta_results(om)['objective']), 326661590)
