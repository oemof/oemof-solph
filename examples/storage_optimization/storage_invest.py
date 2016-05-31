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
import matplotlib.pyplot as plt
import pandas as pd
import logging

# import solph module to create/process optimization model instance
from oemof.solph import predefined_objectives as predefined_objectives

# Outputlib
from oemof.outputlib import to_pandas as tpd

# Default logger of oemof
from oemof.tools import logger

# import oemof base classes to create energy system objects
from oemof.core import energy_system as es
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer


def initialise_energysystem(number_timesteps=8760):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    time_index = pd.date_range('1/1/2012', periods=number_timesteps,
                               freq='H')
    simulation = es.Simulation(
        timesteps=range(len(time_index)), verbose=True, solver='glpk',
        objective_options={'function': predefined_objectives.minimize_cost})
    return es.EnergySystem(time_idx=time_index, simulation=simulation)


def optimise_storage_size(energysystem, filename="storage_invest.csv"):
    # Read data file
    data = pd.read_csv(filename, sep=",")

    ##########################################################################
    # set optimzation options for storage components
    ##########################################################################

    transformer.Storage.optimization_options.update({'investment': True})

    ##########################################################################
    # Create oemof object
    ##########################################################################

    logging.info('Create oemof objects')
    # create gas bus
    bgas = Bus(uid="bgas",
               type="gas",
               price=70,
               balanced=True,
               excess=False)

    # create electricity bus
    bel = Bus(uid="bel",
              type="el",
              excess=True)

    # create commodity object for gas resource
    source.Commodity(uid='rgas',
                     outputs=[bgas],
                     sum_out_limit=194397000)

    # create fixed source object for wind
    source.FixedSource(uid="wind",
                       outputs=[bel],
                       val=data['wind'],
                       out_max=[1000000],
                       add_out_limit=0,
                       capex=1000,
                       opex_fix=20,
                       lifetime=25,
                       crf=0.08)

    # create fixed source object for pv
    source.FixedSource(uid="pv",
                       outputs=[bel],
                       val=data['pv'],
                       out_max=[582000],
                       add_out_limit=0,
                       capex=900,
                       opex_fix=15,
                       lifetime=25,
                       crf=0.08)

    # create simple sink object for demand
    sink.Simple(uid="demand", inputs=[bel], val=data['demand_el'])

    # create simple transformer object for gas powerplant
    transformer.Simple(uid='pp_gas',
                       inputs=[bgas], outputs=[bel],
                       opex_var=50, out_max=[10e10], eta=[0.58])

    # create storage transformer object for storage
    transformer.Storage(uid='sto_simple',
                        inputs=[bel],
                        outputs=[bel],
                        eta_in=1,
                        eta_out=0.8,
                        cap_loss=0.00,
                        opex_fix=35,
                        opex_var=10e10,
                        capex=1000,
                        cap_max=0,
                        cap_initial=0,
                        c_rate_in=1/6,
                        c_rate_out=1/6)

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    # If you dumped the energysystem once, you can skip the optimisation
    # with '#' and use the restore method.
    energysystem.optimize()

    return energysystem


def get_result_dict(energysystem):
    logging.info('Check the results')
    storage = [e for e in energysystem.entities if e.uid == 'sto_simple'][0]
    myresults = tpd.DataFramePlot(energy_system=energysystem)

    pp_gas = myresults.slice_by(bus_uid='bel', bus_type='el',
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
        bus_uid='bel', cdict=cdict,
        barorder=['pv', 'wind', 'pp_gas', 'sto_simple'],
        lineorder=['demand', 'sto_simple', 'bel_excess'],
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
