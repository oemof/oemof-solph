# -*- coding: utf-8 -*-

""" This example shows how to create an energysystem with oemof objects and
solve it with the solph module. Results are plotted with outputlib.

Data: example_data.csv
"""
################################# imports #####################################
import pandas as pd
import matplotlib.pyplot as plt

# base classes import
from oemof.core import energy_system as es
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer

# solph imports
from oemof.solph.optimization_model import OptimizationModel
from oemof.solph import predefined_objectives as predefined_objectives
# results and plotting
from oemof.outputlib import to_pandas as tpd

# logging
from oemof.tools import logger
logger.define_logging()

######################### data & initialization ###############################
data = pd.read_csv("example_data.csv", sep=",")

time_index = pd.date_range('1/1/2012', periods=168, freq='H')
# create simulation object
simulation = es.Simulation(solver='glpk', timesteps=range(len(time_index)),
                           verbose=False, duals=False,
                           objective_options={
                             'function': predefined_objectives.minimize_cost})
# create (with out entities) energysystem
energy_system = es.EnergySystem(simulation=simulation, time_idx=time_index)


# emission factors in t/MWh
em_lig = 0.111 * 3.6
em_coal = 0.0917 * 3.6
em_gas = 0.0556 * 3.6
em_oil = 0.0750 * 3.6

########################### create energysystem components ####################

# resource busses
bcoal = Bus(uid="coal", type="coal", price=20, balanced=False, excess=False)
bgas = Bus(uid="gas", type="gas", price=35, balanced=False, excess=False)
boil = Bus(uid="oil", type="oil", price=40,  balanced=False, excess=False)
blig = Bus(uid="lignite", type="lignite", balanced=False, price=15,
           excess=False)

# electricity and heat
b_el = Bus(uid="b_el", type="el", excess=False,
           shortage=True, shortage_costs=99999)
b_th = Bus(uid="b_th", type="th", excess=True, excess_costs=0)

# renewable sources (only pv onshore)
wind_on = source.DispatchSource(uid="wind_on", outputs=[b_el],
                                val=data['wind'],
                                out_max=[66.300], opex_var=0, opex_fix=10)
pv = source.DispatchSource(uid="pv", outputs=[b_el], val=data['pv'],
                           out_max=[65.300])

# demands
demand_el = sink.Simple(uid="demand_el", inputs=[b_el],
                        val=data['demand_el']/1000)
demand_th = sink.Simple(uid="demand_th", inputs=[b_th],
                        val=data['demand_th']*50)

# Transformers
pp_coal = transformer.Simple(uid='pp_coal', inputs=[bcoal], outputs=[b_el],
                             in_max=[None], out_max=[20.200], eta=[0.39],
                             opex_fix=2, opex_var=25, co2_var=em_coal)

pp_lig = transformer.Simple(uid='pp_lig', inputs=[blig], outputs=[b_el],
                            in_max=[None], out_max=[11.800], eta=[0.41],
                            opex_fix=2, opex_var=19, co2_var=em_lig)

pp_gas = transformer.Simple(uid='pp_gas', inputs=[bgas], outputs=[b_el],
                            in_max=[None], out_max=[41.000], eta=[0.45],
                            opex_fix=2, opex_var=40, co2_var=em_gas)

pp_oil = transformer.Simple(uid='pp_oil', inputs=[boil], outputs=[b_el],
                            in_max=[None], out_max=[0.1000], eta=[0.3],
                            opex_fix=2, opex_var=50, co2_var=em_oil)
# chp note: order of outputs must match order of 'eta' (see. documentation)
pp_chp = transformer.CHP(uid='pp_chp', inputs=[bgas], outputs=[b_el, b_th],
                         in_max=[100], out_max=[40, 30],
                         eta=[0.4, 0.3], opex_fix=0, opex_var=50,
                         co2_var=em_gas)

################################# optimization ################################
# create Optimization model based on energy_system
om = OptimizationModel(energysystem=energy_system)

# solve with specific optimization options (passed to pyomo)
om.solve(solve_kwargs={'tee': True,
                       'keepfiles': False},
         solver_cmdline_options={'min': ''})
# write back results from optimization object to energysystem for
# post-processing
energy_system.results = om.results()


################################## Plotting ###################################
# define colors
cdict = {'wind_on': '#00bfff',
         'pv': '#ffd700',
         #'sto': '#42c77a',
         'pp_gas': '#8b1a1a',
         'pp_coal': '#838b8b',
         'pp_lig': '#8b7355',
         'pp_oil': '#000000',
         'pp_chp': '#20b2aa',
         'demand_el': '#fff8dc'}
# use outputlib
# create multiindex dataframe with result values
esplot = tpd.DataFramePlot(energy_system=energy_system)
# select input results of electrical bus (i.e. power delivered by plants)
esplot.slice_unstacked(bus_uid="b_el", type="input")
# set colorlist for esplot
colorlist = esplot.color_from_dict(cdict)
# plot
esplot.plot(color=colorlist, title="January 2016", stacked=True, width=1,
            lw=0.1, kind='bar')
esplot.ax.set_ylabel('Power in MW')
esplot.ax.set_xlabel('Date')
esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m')
esplot.outside_legend(reverse=True)
plt.show()
