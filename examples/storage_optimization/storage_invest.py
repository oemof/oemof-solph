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

# Outputlib
from oemof.outputlib import to_pandas as tpd

# Default logger of oemof
from oemof.tools import logger

# import oemof base classes to create energy system objects
import logging
import pandas as pd
import matplotlib.pyplot as plt
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import (Bus, Source, Sink, Flow, LinearTransformer, Storage)
from oemof.solph import Investment
from oemof.solph import OperationalModel


def initialise_energysystem(number_timesteps=876):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2012', periods=number_timesteps,
                                    freq='H')

    return core_es.EnergySystem(groupings=solph.GROUPINGS,
                                time_idx=date_time_index)


def optimise_storage_size(energysystem, filename="storage_invest.csv"):
    # Read data file
    data = pd.read_csv(filename, sep=",")

    ##########################################################################
    # Create oemof object
    ##########################################################################

    logging.info('Create oemof objects')
    # create gas bus
    bgas = Bus(label="gas_balance")

    # create electricity bus
    bel = Bus(label="el_balance")

    # create excess component for the electricity bus to allow overproduction
    Sink(label='excess_bel', inputs={bel: Flow()})

    # create commodity object for gas resource
    Source(label='rgas', outputs={bgas: Flow(summed_max=194397000,
                                             nominal_value=1)})

    # create fixed source object for wind
    Source(label='wind', outputs={bel: Flow(actual_value=data['wind'],
                                            nominal_value=1000000,
                                            fixed=True, fixed_costs=20)})

    # create fixed source object for pv
    Source(label='pv', outputs={bel: Flow(actual_value=data['pv'],
                                          nominal_value=582000,
                                          fixed=True, variable_costs=15)})

    # create simple sink object for demand
    Sink(label='demand', inputs={bel: Flow(actual_value=data['demand_el'],
                                           fixed=True)})

    # create simple transformer object for gas powerplant
    LinearTransformer(
        label="pp_gas",
        inputs={bgas: Flow()},
        outputs={bel: Flow(nominal_value=10e10, variable_costs=50)},
        conversion_factors={bel: 0.58})

    # create storage transformer object for storage
    Storage(
        label='storage',
        inputs={bel: Flow()}, outputs={bel: Flow()},
        nominal_capacity=500, capacity_loss=0.00, initial_capacity=0,
        nominal_input_capacity_ratio=1 / 6, nominal_output_capacity_ratio=1 / 6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=Investment(),
    )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = OperationalModel(energysystem, timeindex=energysystem.time_idx)

    logging.info('Solve the optimization problem')
    om.solve(solve_kwargs={'tee': True})

    logging.info('Store lp-file')
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})

    return energysystem


def get_result_dict(energysystem):
    logging.info('Check the results')
    storage = [e for e in energysystem.entities if e.uid == 'sto_simple'][0]
    myresults = tpd.DataFramePlot(energy_system=energysystem)

    pp_gas = myresults.slice_by(bus_uid='el_balance', bus_type='el',
                                type='input', obj_uid='pp_gas',
                                date_from='2012-01-01 00:00:00',
                                date_to='2012-12-31 23:00:00')

    demand = myresults.slice_by(bus_uid='bel', bus_type='el',
                                type='output', obj_uid='demand',
                                date_from='2012-01-01 00:00:00',
                                date_to='2012-12-31 23:00:00')

    wind = myresults.slice_by(bus_uid='bel', bus_type='el',
                              type='input', obj_uid='wind',
                              date_from='2012-01-01 00:00:00',
                              date_to='2012-12-31 23:00:00')

    pv = myresults.slice_by(bus_uid='bel', bus_type='el',
                            type='input', obj_uid='pv',
                            date_from='2012-01-01 00:00:00',
                            date_to='2012-12-31 23:00:00')

    return {'pp_gas_sum': pp_gas.sum(),
            'demand_sum': demand.sum(),
            'demand_max': demand.max(),
            'wind_sum': wind.sum(),
            'wind_inst': wind.max()/0.99989,
            'pv_sum': pv.sum(),
            'pv_inst': pv.max()/0.76474,
            'storage_cap': energysystem.results[storage].add_cap,
            'objective': energysystem.results.objective}


def create_plots(energysystem):

    logging.info('Plot the results')

    cdict = {'wind': '#5b5bae',
             'pv': '#ffde32',
             'sto_simple': '#42c77a',
             'pp_gas': '#636f6b',
             'demand': '#ce4aff'}

    # Plotting the input flows of the electricity bus for January
    myplot = tpd.DataFramePlot(energy_system=energysystem)
    myplot.slice_unstacked(bus_uid="bel", type="input",
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-01-31 00:00:00")
    colorlist = myplot.color_from_dict(cdict)
    myplot.plot(color=colorlist, linewidth=2, title="January 2012")
    myplot.ax.legend(loc='upper right')
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.set_datetime_ticks(date_format='%d-%m-%Y', tick_distance=24*7)

    # Plotting the output flows of the electricity bus for January
    myplot.slice_unstacked(bus_uid="bel", type="output")
    myplot.plot(title="Year 2016", colormap='Spectral', linewidth=2)
    myplot.ax.legend(loc='upper right')
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.set_datetime_ticks()

    plt.show()

    # Plotting a combined stacked plot
    fig = plt.figure(figsize=(24, 14))
    plt.rc('legend', **{'fontsize': 19})
    plt.rcParams.update({'font.size': 19})
    plt.style.use('grayscale')

    handles, labels = myplot.io_plot(
        bus_label='el_balance', cdict=cdict,
        barorder=['pv', 'wind', 'pp_gas', 'storage'],
        lineorder=['demand', 'storage', 'excess_bel'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(1, 1, 1),
        date_from="2012-01-01 00:00:00",
        date_to="2012-01-8 00:00:00",
        )
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.ax.set_title("Electricity bus")
    myplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    myplot.outside_legend(handles=handles, labels=labels)

    plt.show()

if __name__ == "__main__":
    logger.define_logging()
    esys = initialise_energysystem()
    esys = optimise_storage_size(esys)
    # esys.dump()
    # esys.restore()
    create_plots(esys)
