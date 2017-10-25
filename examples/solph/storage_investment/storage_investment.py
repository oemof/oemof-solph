# -*- coding: utf-8 -*-

"""
General description:
---------------------

The example models the following energy system:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |


"""

###############################################################################
# imports
###############################################################################

# Default logger of oemof
from oemof.tools import logger
from oemof.tools import helpers
from oemof.tools import economics

import oemof.solph as solph
from oemof.outputlib import processing, views

import logging
import os
import pandas as pd
import pprint as pp

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def optimise_storage_size(filename="storage_investment.csv", solver='cbc',
                          debug=True, number_timesteps=24 * 7 * 8,
                          tee_switch=True, silent=False):

    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2012', periods=number_timesteps,
                                    freq='H')

    energysystem = solph.EnergySystem(timeindex=date_time_index)

    # Read data file
    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data = pd.read_csv(full_filename, sep=",")

    ##########################################################################
    # Create oemof object
    ##########################################################################

    logging.info('Create oemof objects')
    # create natural gas bus
    bgas = solph.Bus(label="natural_gas")

    # create electricity bus
    bel = solph.Bus(label="electricity")

    # create excess component for the electricity bus to allow overproduction
    solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})

    # create source object representing the natural gas commodity (annual limit)
    solph.Source(label='rgas', outputs={bgas: solph.Flow(
        nominal_value=194397000 * number_timesteps / 8760, summed_max=1)})

    # create fixed source object representing wind power plants
    solph.Source(label='wind', outputs={bel: solph.Flow(
        actual_value=data['wind'], nominal_value=1000000, fixed=True,
        fixed_costs=20)})

    # create fixed source object representing pv power plants
    solph.Source(label='pv', outputs={bel: solph.Flow(
        actual_value=data['pv'], nominal_value=582000, fixed=True,
        fixed_costs=15)})

    # create simple sink object representing the electrical demand
    solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    # create simple transformer object representing a gas power plant
    solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
        conversion_factors={bel: 0.58})

    # If the period is one year the equivalent periodical costs (epc) of an
    # investment are equal to the annuity. Use oemof's economic tools.
    epc = economics.annuity(capex=1000, n=20, wacc=0.05)

    # create storage object representing a battery
    storage = solph.components.GenericStorage(
        label='storage',
        inputs={bel: solph.Flow(variable_costs=10e10)},
        outputs={bel: solph.Flow(variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        fixed_costs=35,
        investment=solph.Investment(ep_costs=epc),
    )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    # initialise the operational model
    om = solph.OperationalModel(energysystem)
    # if debug is true an lp-file will be written
    if debug:
        filename = os.path.join(
            helpers.extend_basic_path('lp_files'), 'storage_invest.lp')
        logging.info('Store lp-file in {0}.'.format(filename))
        om.write(filename, io_options={'symbolic_solver_labels': True})

    # if tee_switch is true solver messages will be displayed
    logging.info('Solve the optimization problem')
    om.solve(solver=solver, solve_kwargs={'tee': tee_switch})

    # Check dump and restore
    energysystem.dump()
    energysystem = solph.EnergySystem(timeindex=date_time_index)
    energysystem.restore()

    # check if the new result object is working for custom components
    results = processing.results(om)

    if not silent:
        print(results[(storage,)]['sequences'].head())
        print(results[(storage,)]['scalars'])
    custom_storage = views.node(results, 'storage')
    electricity_bus = views.node(results, 'electricity')

    if plt is not None and not silent:
        custom_storage['sequences'].plot(kind='line', drawstyle='steps-post')
        plt.show()
        electricity_bus['sequences'].plot(kind='line', drawstyle='steps-post')
        plt.show()

    my_results = electricity_bus['sequences'].sum(axis=0).to_dict()
    my_results['storage_invest'] = results[(storage,)]['scalars']['invest']

    if not silent:
        meta_results = processing.meta_results(om)
        pp.pprint(meta_results)

    return my_results


if __name__ == "__main__":
    logger.define_logging()
    pp.pprint(optimise_storage_size())
