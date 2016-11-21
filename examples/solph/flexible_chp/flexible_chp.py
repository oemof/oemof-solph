# -*- coding: utf-8 -*-

"""
General description:
---------------------

The example models the following energy system:

                  input/output  bgas     bel      bth
                       |          |        |       |
                       |          |        |       |
                       |          |        |       |
 rgas(Commodity)       |--------->|        |       |
                       |          |        |       |
 demand_el(Sink)       |<------------------|       |
                       |          |        |       |
 demand_th (Sink)      |<--------------------------|
                       |          |        |       |
                       |<---------|        |       |
 chp_gas(Transformer)  |------------------>|       |
                       |-------------------------->|
                       |          |        |       |
 heat_gas(Transformer) |<---------|        |       |
                       |-------------------------->|
                       |          |        |       |
 elec_gas(Transformer) |<---------|        |       |
                       |------------------>|       |
                       |          |        |       |


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
import warnings

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def initialise_energy_system(number_timesteps=192):
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('5/5/2012', periods=number_timesteps,
                                    freq='H')

    return solph.EnergySystem(timeindex=date_time_index)


def optimise_storage_size(energysystem, filename="flexible_chp.csv",
                          solver='cbc', debug=True, tee_switch=True):

    # Read data file
    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data = pd.read_csv(full_filename, sep=",")

    ##########################################################################
    # Create oemof object
    ##########################################################################

    logging.info('Create oemof objects')
    # create gas bus
    bgas = solph.Bus(label="natural_gas")

    # create commodity object for gas resource
    solph.Source(label='rgas', outputs={bgas: solph.Flow(variable_costs=50)})

    # create electricity bus
    bel = solph.Bus(label="electricity")
    bel2 = solph.Bus(label="electricity_2")
    bth = solph.Bus(label="heat")
    bth2 = solph.Bus(label="heat_2")

    # create excess component for the elec/heat bus to allow overproduction
    solph.Sink(label='excess_bth_2', inputs={bth2: solph.Flow()})
    solph.Sink(label='excess_bth', inputs={bth: solph.Flow()})
    solph.Sink(label='excess_bel_2', inputs={bel2: solph.Flow()})
    solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})

    # create simple sink object for electrical demand
    solph.Sink(label='demand_el', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})
    solph.Sink(label='demand_el_2', inputs={bel2: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    # create simple sink object for heat demand
    solph.Sink(label='demand_th', inputs={bth: solph.Flow(
        actual_value=data['demand_th'], fixed=True, nominal_value=741000)})
    solph.Sink(label='demand_th_2', inputs={bth2: solph.Flow(
        actual_value=data['demand_th'], fixed=True, nominal_value=741000)})

    solph.LinearTransformer(
        label='fixed_chp_gas',
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=0),
                 bth: solph.Flow(nominal_value=0)},
        conversion_factors={bel: 0.3, bth: 0.5})

    # create simple transformer object for gas powerplant
    # solph.LinearTransformer(
    #      label="heat_gas",
    #      inputs={bgas: solph.Flow()},
    #      outputs={bth2: solph.Flow(nominal_value=10e10)},
    #      conversion_factors={bth2: 0.8})

    solph.LinearTransformer(
        label='fixed_chp_gas_2',
        inputs={bgas: solph.Flow()},
        outputs={bel2: solph.Flow(nominal_value=3e10),
                 bth2: solph.Flow(nominal_value=4e10)},
        conversion_factors={bel2: 0.3, bth2: 0.5})

    solph.VariableFractionTransformer(
        label='variable_chp_gas',
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=3e10),
                 bth: solph.Flow(nominal_value=4e10)},
        conversion_factors={bel: 0.3, bth: 0.5},
        main_flow_loss_index={bel: 0.4}, efficiency_condensing={bel: 0.5}
        )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = solph.OperationalModel(energysystem)

    if debug:
        filename = os.path.join(
            helpers.extend_basic_path('lp_files'), 'storage_invest.lp')
        logging.info('Store lp-file in {0}.'.format(filename))
        om.write(filename, io_options={'symbolic_solver_labels': True})

    logging.info('Solve the optimization problem')
    om.solve(solver=solver, solve_kwargs={'tee': tee_switch})

    return energysystem


def create_plots(energysystem):

    logging.info('Plot the results')

    cdict = {'variable_chp_gas': '#42c77a',
             'fixed_chp_gas': '#20b4b6',
             'fixed_chp_gas_2': '#20b4b6',
             'heat_gas': '#12341f',
             'demand_th': '#5b5bae',
             'demand_th_2': '#5b5bae',
             'demand_el': '#5b5bae',
             'demand_el_2': '#5b5bae',
             'free': '#ffde32',
             'excess_bth': '#f22222',
             'excess_bth_2': '#f22222',
             'excess_bel': '#f22222',
             'excess_bel_2': '#f22222'}

    myplot = outputlib.DataFramePlot(energy_system=energysystem)

    # Plotting a combined stacked plot
    fig = plt.figure(figsize=(18, 9))
    plt.rc('legend', **{'fontsize': 13})
    plt.rcParams.update({'font.size': 13})

    handles, labels = myplot.io_plot(
        bus_label='electricity', cdict=cdict,
        barorder=['variable_chp_gas', 'fixed_chp_gas'],
        lineorder=['demand_el', 'excess_bel'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(2, 2, 2))
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('')
    myplot.ax.set_title("Electricity output (flexible chp)")
    myplot.ax.get_xaxis().set_visible(False)
    myplot.outside_legend(handles=handles, labels=labels)

    handles, labels = myplot.io_plot(
        bus_label='heat', cdict=cdict,
        barorder=['variable_chp_gas', 'fixed_chp_gas', 'heat_gas'],
        lineorder=['demand_th', 'excess_bth'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(2, 2, 4))
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.ax.set_ylim([0, 600000])
    myplot.ax.set_title("Heat output (flexible chp)")
    myplot.set_datetime_ticks(tick_distance=48, date_format='%d-%m-%y')
    myplot.outside_legend(handles=handles, labels=labels)

    myplot.io_plot(
        bus_label='electricity_2', cdict=cdict,
        barorder=['variable_chp_gas', 'fixed_chp_gas_2'],
        lineorder=['demand_el_2', 'excess_bel_2'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(2, 2, 1))
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('')
    myplot.ax.get_xaxis().set_visible(False)
    myplot.ax.set_title("Electricity output (fixed chp)")
    myplot.ax.legend_.remove()

    myplot.io_plot(
        bus_label='heat_2', cdict=cdict,
        barorder=['fixed_chp_gas_2'],
        lineorder=['demand_th_2', 'excess_bth_2'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(2, 2, 3))
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_ylim([0, 600000])
    myplot.ax.set_xlabel('Date')
    myplot.ax.set_title("Heat output (fixed chp)")
    myplot.set_datetime_ticks(tick_distance=48, date_format='%d-%m-%y')
    myplot.ax.legend_.remove()

    plt.show()


def run_storage_investment_example(**kwargs):
    logger.define_logging()
    plot_only = False

    esys = initialise_energy_system(192)
    if not plot_only:
        esys = optimise_storage_size(esys, **kwargs)
        esys.dump()
    else:
        esys.restore()

    if plt is not None:
        create_plots(esys)
    else:
        msg = ("\nIt is not possible to plot the results, due to a missing " +
               "python package: 'matplotlib'. \nType 'pip install " +
               "matplotlib' to see the plots.")
        warnings.warn(msg)


if __name__ == "__main__":
    run_storage_investment_example()
