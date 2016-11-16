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


def initialise_energy_system(number_timesteps=8760):
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2012', periods=number_timesteps,
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
    bth = solph.Bus(label="heat")

    # create excess component for the elec/heat bus to allow overproduction
    solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})
    solph.Sink(label='excess_bth', inputs={bth: solph.Flow()})

    # create simple sink object for electrical demand
    solph.Sink(label='demand_el', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    # create simple sink object for heat demand
    solph.Sink(label='demand_th', inputs={bth: solph.Flow(
        actual_value=data['demand_th'] * 741000, fixed=True, nominal_value=1)})

    # create simple transformer object for gas powerplant
    solph.LinearTransformer(
        label="elec_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10)},
        conversion_factors={bel: 0.38})

    # solph.LinearTransformer(
    #     label='chp_gas',
    #     inputs={bgas: solph.Flow()},
    #     outputs={bel: solph.Flow(nominal_value=3e10),
    #              bth: solph.Flow(nominal_value=5e10)},
    #     conversion_factors={bel: 0.3, bth: 0.5})

    # create simple transformer object for gas powerplant
    solph.LinearTransformer(
        label="heat_gas",
        inputs={bgas: solph.Flow()},
        outputs={bth: solph.Flow(nominal_value=10e10)},
        conversion_factors={bth: 0.8})

    solph.VariableFractionTransformer(
        label='chp_gas',
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=3e10),
                 bth: solph.Flow(nominal_value=4e10)},
        conversion_factors={bel: 0.3, bth: 0.514},
        power_loss_index={bel: 0.12}, efficiency_condensing={bel: 0.55}
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

    cdict = {'chp_gas': '#42c77a',
             'elec_gas': '#636f6b',
             'heat_gas': '#12341f',
             'demand_th': '#5b5bae',
             'demand_el': '#ce4aff',
             'excess_bth': '#ffde32',
             'excess_bel': '#555555'}

    # Plotting the input flows of the electricity bus for January
    myplot = outputlib.DataFramePlot(energy_system=energysystem)
    myplot.slice_unstacked(bus_label="electricity", type="to_bus")
    colorlist = myplot.color_from_dict(cdict)
    myplot.plot(color=colorlist, linewidth=2, title="January 2012")
    myplot.ax.legend(loc='upper right')
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.set_datetime_ticks(date_format='%d-%m-%Y', tick_distance=24*7)

    # Plotting the output flows of the electricity bus for January
    myplot.slice_unstacked(bus_label="electricity", type="from_bus")
    myplot.plot(title="Year 2016", colormap='Spectral', linewidth=2)
    myplot.ax.legend(loc='upper right')
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.set_datetime_ticks()

    plt.show()

    # Plotting a combined stacked plot
    fig = plt.figure()
    plt.rc('legend', **{'fontsize': 19})
    plt.rcParams.update({'font.size': 19})
    plt.style.use('grayscale')

    handles, labels = myplot.io_plot(
        bus_label='electricity', cdict=cdict,
        barorder=['chp_gas', 'elec_gas'],
        lineorder=['demand_el', 'excess_bel'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(2, 1, 1),
        date_from="2012-05-01 00:00:00",
        date_to="2012-05-15 00:00:00",
        )
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.ax.set_title("Electricity bus")
    myplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    myplot.outside_legend(handles=handles, labels=labels)

    handles, labels = myplot.io_plot(
        bus_label='heat', cdict=cdict,
        barorder=['chp_gas', 'heat_gas'],
        lineorder=['demand_th', 'excess_bth'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(2, 1, 2),
        date_from="2012-05-01 00:00:00",
        date_to="2012-05-15 00:00:00",
    )
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.ax.set_title("Electricity bus")
    myplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    myplot.outside_legend(handles=handles, labels=labels)

    plt.show()


def run_storage_investment_example(**kwargs):
    logger.define_logging()
    plot_only = False

    esys = initialise_energy_system(8760)
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
