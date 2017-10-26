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

    bcoal = solph.Bus(label="hard_coal")

    # create electricity bus
    bel = solph.Bus(label="electricity")
    bheat = solph.Bus(label="heat")

    # create excess component for the electricity bus to allow overproduction
    solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})
    solph.Sink(label='excess_heat', inputs={bheat: solph.Flow()})
    solph.Source(label='shortage', outputs={bel: solph.Flow(
        variable_costs=500)})
    # solph.Source(label='shortage_heat', outputs={bheat: solph.Flow(
    #     variable_costs=500)})

    # create source object representing the natural gas commodity (annual limit)
    solph.Source(label='rgas', outputs={bgas: solph.Flow()})

    solph.Source(label='rcoal', outputs={bcoal: solph.Flow()})

    # create simple sink object representing the electrical demand
    solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    # create simple sink object representing the electrical demand
    solph.Sink(label='demand_heat', inputs={bheat: solph.Flow(
        actual_value=data['demand_el'] * 0.5, fixed=True, nominal_value=1)})

    # create simple transformer object representing a gas power plant
    solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow(),
                bcoal: solph.Flow()},
        outputs={bel: solph.Flow(), bheat: solph.Flow()},
        conversion_factors={bel: 0.3, bheat: 0.5, bgas: 0.2, bcoal: 0.8})

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

    # check if the new result object is working for custom components
    results = processing.results(om)

    pp_chp = views.node(results, 'pp_gas')

    my_results = pp_chp['sequences'].sum(axis=0).to_dict()

    in_sum = (my_results[(('hard_coal', 'pp_gas'), 'flow')] +
              my_results[(('natural_gas', 'pp_gas'), 'flow')])
    out_sum = (my_results[(('pp_gas', 'electricity'), 'flow')] +
               my_results[(('pp_gas', 'heat'), 'flow')])
    print(in_sum * 0.8, out_sum)
    return my_results


if __name__ == "__main__":
    logger.define_logging()
    pp.pprint(optimise_storage_size())
