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


# Define logger
logger.define_logging()

###############################################################################
# read data from csv file and set time index
###############################################################################

logging.info('Read data from csv file and set time index')
data = pd.read_csv("storage_invest.csv", sep=",")
time_index = pd.date_range('1/1/2012', periods=8760, freq='H')

###############################################################################
# initialize the energy system
###############################################################################

logging.info('Initialize the energy system')
simulation = es.Simulation(
    timesteps=range(len(time_index)), verbose=True, solver='glpk',
    objective_options={'function': predefined_objectives.minimize_cost})

energysystem = es.EnergySystem(time_idx=time_index, simulation=simulation)

###############################################################################
# set optimzation options for storage components
###############################################################################

transformer.Storage.optimization_options.update({'investment': True})

###############################################################################
# Create oemof object
###############################################################################

logging.info('Create oemof objects')
# create gas bus
bgas = Bus(uid="bgas",
           type="gas",
           price=70)

# create electricity bus
bel = Bus(uid="bel",
          type="el")

# create excess component for the electricity bus to allow overproduction
excess = sink.Simple(uid="excess", inputs=[bel], bound_type='min')

# create commodity object for gas resource
rgas = source.Commodity(uid='rgas',
                        outputs=[bgas],
                        sum_out_limit=194397000)

# create fixed source object for wind
wind = source.FixedSource(uid="wind",
                          outputs=[bel],
                          val=data['wind'],
                          out_max=[1000000],
                          add_out_limit=0,
                          capex=1000,
                          opex_fix=20,
                          lifetime=25,
                          crf=0.08)

# create fixed source object for pv
pv = source.FixedSource(uid="pv",
                        outputs=[bel],
                        val=data['pv'],
                        out_max=[582000],
                        add_out_limit=0,
                        capex=900,
                        opex_fix=15,
                        lifetime=25,
                        crf=0.08)

# create simple sink object for demand
demand = sink.Simple(uid="demand", inputs=[bel], val=data['demand_el'])

# create simple transformer object for gas powerplant
pp_gas = transformer.Simple(uid='pp_gas',
                            inputs=[bgas], outputs=[bel],
                            opex_var=50, out_max=[10e10], eta=[0.58])

# create storage transformer object for storage
storage = transformer.Storage(uid='sto_simple',
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

###############################################################################
# Optimise the energy system and plot the results
###############################################################################

logging.info('Optimise the energy system')

# If you dumped the energysystem once, you can skip the optimisation with '#'
# and use the restore method.
energysystem.optimize()
#
# energysystem.dump()
# energysystem.restore()

logging.info('Plot the results')

cdict = {'wind': '#5b5bae',
         'pv': '#ffde32',
         'sto_simple': '#42c77a',
         'pp_gas': '#636f6b',
         'demand': '#ce4aff',
         'excess': '#970000'}

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
    bus_uid="bel", cdict=cdict,
    barorder=['pv', 'wind', 'pp_gas', 'sto_simple'],
    lineorder=['demand', 'sto_simple'],
    line_kwa={'linewidth': 4},
    ax=fig.add_subplot(1, 1, 1),
    date_from="2012-06-01 00:00:00",
    date_to="2012-06-8 00:00:00",
    )
myplot.ax.set_ylabel('Power in MW')
myplot.ax.set_xlabel('Date')
myplot.ax.set_title("Electricity bus")
myplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
myplot.outside_legend(handles=handles, labels=labels)

plt.show()
