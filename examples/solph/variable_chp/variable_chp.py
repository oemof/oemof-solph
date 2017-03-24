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
import warnings

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def initialise_energy_system(number_timesteps=192):
    """Create an energy system"""
    logging.info('Initialize the energy system')

    # create time index for 192 hours in May.
    date_time_index = pd.date_range('5/5/2012', periods=number_timesteps,
                                    freq='H')
    return solph.EnergySystem(timeindex=date_time_index)


def optimise_storage_size(energysystem, filename="variable_chp.csv",
                          solver='cbc', debug=True, tee_switch=True):

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
    solph.LinearTransformer(
        label='fixed_chp_gas',
        inputs={bgas: solph.Flow(nominal_value=0)},
        outputs={bel: solph.Flow(), bth: solph.Flow()},
        conversion_factors={bel: 0.3, bth: 0.5})

    # create a fixed transformer to distribute to the heat_2 and elec_2 buses
    solph.LinearTransformer(
        label='fixed_chp_gas_2',
        inputs={bgas: solph.Flow(nominal_value=10e10)},
        outputs={bel2: solph.Flow(), bth2: solph.Flow()},
        conversion_factors={bel2: 0.3, bth2: 0.5})

    # create a fixed transformer to distribute to the heat and elec buses
    solph.VariableFractionTransformer(
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

    return energysystem


def get_result_dict(energysystem):
    """Get some representative results.

    Parameters
    ----------
    energysystem : solph.EnergySystem

    Returns
    -------
    dict : Results of the optimisation.

    """
    logging.info('Check the results')
    myresults = outputlib.ResultsDataFrame(energy_system=energysystem)

    res = dict()

    res['natural_gas'] = myresults.slice_by(
        bus_typ='natural_gas', obj_label='rgas', type='to_bus').sum()[0]
    res['input_variable_chp'] = myresults.slice_by(
        bus_typ='natural_gas', obj_label='variable_chp_gas', type='from_bus'
        ).sum()[0]
    res['input_fixed_chp'] = myresults.slice_by(
        bus_typ='natural_gas', obj_label='fixed_chp_gas_2', type='from_bus'
        ).sum()[0]
    res['objective'] = energysystem.results.objective
    return res


def create_plots(energysystem):
    """Create a plot with 6 tiles that shows the difference between the
    LinearTransformer and the VariableFractionTransformer used for chp plants.

    Parameters
    ----------
    energysystem : solph.EnergySystem
    """
    logging.info('Plot the results')

    cdict = {'variable_chp_gas': '#42c77a',
             'fixed_chp_gas': '#20b4b6',
             'fixed_chp_gas_2': '#20b4b6',
             'heat_gas': '#12341f',
             'demand_therm': '#5b5bae',
             'demand_th_2': '#5b5bae',
             'demand_elec': '#5b5bae',
             'demand_el_2': '#5b5bae',
             'free': '#ffde32',
             'excess_therm': '#f22222',
             'excess_bth_2': '#f22222',
             'excess_elec': '#f22222',
             'excess_bel_2': '#f22222'}

    myplot = outputlib.DataFramePlot(energy_system=energysystem)

    # Plotting
    fig = plt.figure(figsize=(18, 9))
    plt.rc('legend', **{'fontsize': 13})
    plt.rcParams.update({'font.size': 13})
    fig.subplots_adjust(left=0.07, bottom=0.12, right=0.86, top=0.93,
                        wspace=0.03, hspace=0.2)

    # subplot of electricity bus (fixed chp) [1]
    myplot.io_plot(
        bus_label='electricity_2', cdict=cdict,
        barorder=['fixed_chp_gas_2'],
        lineorder=['demand_el_2', 'excess_bel_2'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(3, 2, 1))
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('')
    myplot.ax.get_xaxis().set_visible(False)
    myplot.ax.set_title("Electricity output (fixed chp)")
    myplot.ax.legend_.remove()

    # subplot of electricity bus (variable chp) [2]
    handles, labels = myplot.io_plot(
        bus_label='electricity', cdict=cdict,
        barorder=['variable_chp_gas', 'fixed_chp_gas'],
        lineorder=['demand_elec', 'excess_elec'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(3, 2, 2))
    myplot.ax.get_yaxis().set_visible(False)
    myplot.ax.set_xlabel('')
    myplot.ax.get_xaxis().set_visible(False)
    myplot.ax.set_title("Electricity output (variable chp)")
    myplot.outside_legend(handles=handles, labels=labels, plotshare=1)

    # subplot of heat bus (fixed chp) [3]
    myplot.io_plot(
        bus_label='heat_2', cdict=cdict,
        barorder=['fixed_chp_gas_2'],
        lineorder=['demand_th_2', 'excess_bth_2'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(3, 2, 3))
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_ylim([0, 600000])
    myplot.ax.get_xaxis().set_visible(False)
    myplot.ax.set_title("Heat output (fixed chp)")
    myplot.ax.legend_.remove()

    # subplot of heat bus (variable chp) [4]
    handles, labels = myplot.io_plot(
        bus_label='heat', cdict=cdict,
        barorder=['variable_chp_gas', 'fixed_chp_gas', 'heat_gas'],
        lineorder=['demand_therm', 'excess_therm'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(3, 2, 4))
    myplot.ax.set_ylim([0, 600000])
    myplot.ax.get_yaxis().set_visible(False)
    myplot.ax.get_xaxis().set_visible(False)
    myplot.ax.set_title("Heat output (variable chp)")
    myplot.outside_legend(handles=handles, labels=labels, plotshare=1)

    # subplot of efficiency (fixed chp) [5]
    ngas = myplot.loc['natural_gas', 'from_bus', 'fixed_chp_gas_2']['val']
    elec = myplot.loc['electricity_2', 'to_bus', 'fixed_chp_gas_2']['val']
    heat = myplot.loc['heat_2', 'to_bus', 'fixed_chp_gas_2']['val']
    e_ef = elec.div(ngas)
    h_ef = heat.div(ngas)
    df = pd.concat([h_ef, e_ef], axis=1)
    my_ax = df.plot(ax=fig.add_subplot(3, 2, 5), linewidth=2)
    my_ax.set_ylabel('efficiency')
    my_ax.set_ylim([0, 0.55])
    my_ax.set_xlabel('Date')
    my_ax.set_title('Efficiency (fixed chp)')
    my_ax.legend_.remove()

    # subplot of efficiency (variable chp) [6]
    ngas = myplot.loc['natural_gas', 'from_bus', 'variable_chp_gas']['val']
    elec = myplot.loc['electricity', 'to_bus', 'variable_chp_gas']['val']
    heat = myplot.loc['heat', 'to_bus', 'variable_chp_gas']['val']
    e_ef = elec.div(ngas)
    h_ef = heat.div(ngas)
    e_ef.name = 'electricity           '
    h_ef.name = 'heat'
    df = pd.concat([h_ef, e_ef], axis=1)
    my_ax = df.plot(ax=fig.add_subplot(3, 2, 6), linewidth=2)
    my_ax.set_ylim([0, 0.55])
    my_ax.get_yaxis().set_visible(False)
    my_ax.set_xlabel('Date')
    my_ax.set_title('Efficiency (variable chp)')
    box = my_ax.get_position()
    my_ax.set_position([box.x0, box.y0, box.width * 1, box.height])
    my_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

    plt.show()


def run_variable_chp_example(**kwargs):
    logger.define_logging()
    plot_only = False  # set to True if you want to plot your stored results

    # Switch to True to show the solver output
    kwargs.setdefault('tee_switch', False)

    esys = initialise_energy_system()
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

    for k, v in get_result_dict(esys).items():
        logging.info('{0}: {1}'.format(k, v))


if __name__ == "__main__":
    run_variable_chp_example()
