# -*- coding: utf-8 -*-

"""
General description:
---------------------

This example is not a real use case of an energy system but an example to show
how a variable combined heat and power plant (chp) works in contrast to a fixed
chp (eg. block device). Both chp plants distribute power and heat to a separate
heat and power Bus with a heat and power demand. The plot shows that the fixed
chp plant produces heat and power excess and therefore needs more natural gas.

"""

###############################################################################
# imports
###############################################################################

# Outputlib
from oemof import outputlib

# Default logger of oemof
from oemof.tools import logger
from oemof.tools import helpers
import oemof.solph as solph

# import oemof base classes to create energy system objects
import logging
import os
import pandas as pd

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def run_variable_chp_example(number_timesteps=192,
                             filename="variable_chp.csv", solver='cbc',
                             debug=True, tee_switch=True):
    logging.info('Initialize the energy system')

    # create time index for 192 hours in May.
    date_time_index = pd.date_range('5/5/2012', periods=number_timesteps,
                                    freq='H')
    energysystem = solph.EnergySystem(timeindex=date_time_index)

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

    # This is just a dummy transformer with a nominal input of zero
    solph.Transformer(
        label='fixed_chp_gas',
        inputs={bgas: solph.Flow(nominal_value=0)},
        outputs={bel: solph.Flow(), bth: solph.Flow()},
        conversion_factors={bel: 0.3, bth: 0.5})

    # create a fixed transformer to distribute to the heat_2 and elec_2 buses
    solph.Transformer(
        label='fixed_chp_gas_2',
        inputs={bgas: solph.Flow(nominal_value=10e10)},
        outputs={bel2: solph.Flow(), bth2: solph.Flow()},
        conversion_factors={bel2: 0.3, bth2: 0.5})

    # create a fixed transformer to distribute to the heat and elec buses
    solph.components.VariableFractionTransformer(
        label='variable_chp_gas',
        inputs={bgas: solph.Flow(nominal_value=10e10)},
        outputs={bel: solph.Flow(), bth: solph.Flow()},
        conversion_factors={bel: 0.3, bth: 0.5},
        conversion_factor_single_flow={bel: 0.5}
        )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = solph.OperationalModel(energysystem)

    if debug:
        filename = os.path.join(
            helpers.extend_basic_path('lp_files'), 'variable_chp.lp')
        logging.info('Store lp-file in {0}.'.format(filename))
        om.write(filename, io_options={'symbolic_solver_labels': True})

    logging.info('Solve the optimization problem')
    om.solve(solver=solver, solve_kwargs={'tee': tee_switch})

    optimisation_results = outputlib.processing.results(om)

    myresults = outputlib.views.node(optimisation_results, 'natural_gas')
    myresults = myresults['sequences'].sum(axis=0).to_dict()
    myresults['objective'] = outputlib.processing.meta_results(om)['objective']

    return myresults


if __name__ == "__main__":
    logger.define_logging()
    results = run_variable_chp_example()
    import pprint as pp
    pp.pprint(results)
