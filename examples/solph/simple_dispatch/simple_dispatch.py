# -*- coding: utf-8 -*-

""" This example shows how to create an energysystem with oemof objects and
solve it with the solph module. Results are plotted with outputlib.
Some functions are only for testing purposes. The main stuff going on
is pretty straightforward.

Data: example_data.csv
"""
# ############################### imports #####################################
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os

# solph imports
from oemof.solph import (Sink, Source, LinearTransformer, LinearN1Transformer,
                         Bus, Flow, OperationalModel, EnergySystem)
import oemof.outputlib as output
from oemof.tools import logger

# ####################### data & initialization ###############################


def initialise_energysystem(periods=2000):
    """
    """
    datetimeindex = pd.date_range('1/1/2012', periods=periods, freq='H')

    return EnergySystem(timeindex=datetimeindex)


# ######################### create energysystem components ####################
def simulate(energysystem, filename=None, solver='cbc', tee_switch=True,
             keep=True):
    """
    """
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), 'input_data.csv')
    logging.info("Creating objects")
    data = pd.read_csv(filename, sep=",")
    # resource buses
    bcoal = Bus(label="coal", balanced=False)
    bgas = Bus(label="gas", balanced=False)
    boil = Bus(label="oil", balanced=False)
    blig = Bus(label="lignite", balanced=False)

    # electricity and heat
    b_el = Bus(label="b_el")
    b_th = Bus(label="b_th")

    # adding an excess variable can help to avoid infeasible problems
    Sink(label="excess", inputs={b_el: Flow()})

    # adding an excess variable can help to avoid infeasible problems
    # Source(label="shortage", outputs={b_el: Flow(variable_costs=200)})

    # Sources
    Source(label="wind",
           outputs={b_el: Flow(actual_value=data['wind'],
                               nominal_value=66.3,
                               fixed=True)})

    Source(label="pv",
           outputs={b_el: Flow(actual_value=data['pv'],
                               nominal_value=65.3,
                               fixed=True)})

    # Demands (electricity/heat)
    Sink(label="demand_el",
         inputs={b_el: Flow(nominal_value=85,
                            actual_value=data['demand_el'],
                            fixed=True)})

    Sink(label="demand_th",
         inputs={b_th: Flow(nominal_value=40,
                            actual_value=data['demand_th'],
                            fixed=True)})

    # Power plants
    LinearTransformer(label='pp_coal',
                      inputs={bcoal: Flow()},
                      outputs={b_el: Flow(nominal_value=20.2,
                                          variable_costs=25)},
                      conversion_factors={b_el: 0.39})

    LinearTransformer(label='pp_lig',
                      inputs={blig: Flow()},
                      outputs={b_el: Flow(nominal_value=11.8,
                                          variable_costs=19)},
                      conversion_factors={b_el: 0.41})

    LinearTransformer(label='pp_gas',
                      inputs={bgas: Flow()},
                      outputs={b_el: Flow(nominal_value=41,
                                          variable_costs=40)},
                      conversion_factors={b_el: 0.50})

    LinearTransformer(label='pp_oil',
                      inputs={boil: Flow()},
                      outputs={b_el: Flow(nominal_value=5,
                                          variable_costs=50)},
                      conversion_factors={b_el: 0.28})

    # CHP
    LinearTransformer(label='pp_chp',
                      inputs={bgas: Flow()},
                      outputs={b_el: Flow(nominal_value=30,
                                          variable_costs=42),
                               b_th: Flow(nominal_value=40)},
                      conversion_factors={b_el: 0.3, b_th: 0.4})

    # Heatpump with a coefficient of performance (COP) of 3
    b_heat_source = Bus(label="b_heat_source")

    Source(label="heat_source", outputs={b_heat_source: Flow()})

    cop = 3
    LinearN1Transformer(label='heat_pump',
                        inputs={b_el: Flow(), b_heat_source: Flow()},
                        outputs={b_th: Flow(nominal_value=10)},
                        conversion_factors={b_el: cop,
                                            b_heat_source: cop/(cop-1)})

# ################################ optimization ###############################
    # create Optimization model based on energy_system
    logging.info("Create optimization problem")
    om = OperationalModel(es=energysystem)

    # solve with specific optimization options (passed to pyomo)
    logging.info("Solve optimization problem")
    om.solve(solver=solver,
             solve_kwargs={'tee': tee_switch, 'keepfiles': keep})

    # write back results from optimization object to energysystem
    om.results()

    return om


# ################################ Plotting ###################################
def plot_results(energysystem):
    logging.info("Plot results")
    # define colors
    cdict = {'wind': '#00bfff', 'pv': '#ffd700', 'pp_gas': '#8b1a1a',
             'pp_coal': '#838b8b', 'pp_lig': '#8b7355', 'pp_oil': '#000000',
             'pp_chp': '#20b2aa', 'demand_el': '#fff8dc'}

    # create multiindex dataframe with result values
    esplot = output.DataFramePlot(energy_system=energysystem)

    # select input results of electrical bus (i.e. power delivered by plants)
    esplot.slice_unstacked(bus_label="b_el", type="to_bus",
                           date_from='2012-01-01 00:00:00',
                           date_to='2012-01-07 00:00:00')

    # set colorlist for esplot
    colorlist = esplot.color_from_dict(cdict)

    esplot.plot(color=colorlist, title="January 2016", stacked=True, width=1,
                lw=0.1, kind='bar')
    esplot.ax.set_ylabel('Power in MW')
    esplot.ax.set_xlabel('Date')
    esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m')
    esplot.outside_legend(reverse=True)
    plt.show()


def get_results(energysystem):
    """Shows how to extract single time series from DataFrame.

    Parameters
    ----------
    energysystem : solph.EnergySystem

    Returns
    -------
    dict : Some results.
    """
    logging.info('Check the results')

    myresults = output.DataFramePlot(energy_system=energysystem)

    grouped = myresults.groupby(level=[0, 1, 2]).sum()
    rdict = {r + (k,): v
             for r, kv in grouped.iterrows()
             for k, v in kv.to_dict().items()}

    rdict['objective'] = energysystem.results.objective

    return rdict


def run_simple_dispatch_example(**kwargs):
    import pprint as pp
    logger.define_logging()
    esys = initialise_energysystem()
    simulate(esys, **kwargs)
    plot_results(esys)
    pp.pprint(get_results(esys))

if __name__ == "__main__":
    run_simple_dispatch_example()
