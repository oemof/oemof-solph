# -*- coding: utf-8 -*-

""" This example shows how to create an energysystem with oemof objects and
solve it with the solph module. Results are plotted with outputlib.

Data: example_data.csv
"""
################################# imports #####################################
import pandas as pd
import matplotlib.pyplot as plt

# solph imports
from oemof.solph import (Sink, Source, LinearTransformer, Bus, Flow,
                         OperationalModel, EnergySystem, GROUPINGS)
from oemof.outputlib import to_pandas as tpd
from oemof.tools import logger
logger.define_logging()

######################### data & initialization ###############################
data = pd.read_csv("example_data.csv", sep=",")

datetimeindex = pd.date_range('1/1/2012', periods=4, freq='H')

# create (with out entities) energysystem
energysystem = EnergySystem(groupings=GROUPINGS)

########################### create energysystem components ####################

# resource busses
bcoal = Bus(label="coal", balanced=False)
bgas = Bus(label="gas", balanced=False)
boil = Bus(label="oil", balanced=False)
blig = Bus(label="lignite", balanced=False)

# electricity and heat
b_el = Bus(label="b_el")
b_th = Bus(label="b_th")

excess = Sink(label="excess", inputs={b_el: Flow()})
#shortage = Source(label="shortage", outputs={b_el: Flow()})

# renewable sources (only pv onshore)
wind_on = Source(label="wind_on",
                 outputs={b_el: Flow(actual_value=data['wind'],
                                     nominal_value=66.3,
                                     fixed=False)})

pv = Source(label="pv",
            outputs={b_el: Flow(actual_value=data['pv'],
                                nominal_value= 65.3,
                                fixed=True)})

# demands
demand_el = Sink(label="demand_el",
                 inputs={b_el: Flow(nominal_value=77,
                                    actual_value=data['demand_el'],
                                    fixed=True)})

demand_th = Sink(label="demand_th",
                 inputs={b_th: Flow(nominal_value=40,
                                    actual_value=data['demand_th'],
                                    fixed=True)})

# Transformers
pp_coal = LinearTransformer(label='pp_coal',
                            inputs={bcoal: Flow()},
                            outputs={b_el: Flow(nominal_value=20.2,
                                                variable_costs=25)},
                            conversion_factors = {b_el: 0.39})

pp_lig = LinearTransformer(label='pp_lig',
                           inputs={blig: Flow()},
                           outputs={b_el: Flow(nominal_value=11.8,
                                               variable_costs=19)},
                           conversion_factors = {b_el: 0.41})

pp_gas = LinearTransformer(label='pp_gas',
                           inputs={bgas: Flow()},
                           outputs={b_el: Flow(nominal_value=41,
                                               variable_costs=40)},
                           conversion_factors = {b_el: 0.50})

pp_oil = LinearTransformer(label='pp_oil',
                           inputs={boil: Flow()},
                           outputs={b_el: Flow(nominal_value=0.1,
                                               variable_costs=50)},
                           conversion_factors = {b_el: 0.28})

# chp note: order of outputs must match order of 'eta' (see. documentation)
pp_chp = LinearTransformer(label='pp_chp',
                           inputs={bgas: Flow()},
                           outputs={b_el: Flow(nominal_value=30,
                                               variable_costs=42),
                                    b_th: Flow(nominal_value=40)},
                           conversion_factors = {b_el: 0.3, b_th: 0.4})

################################# optimization ################################
# create Optimization model based on energy_system
om = OperationalModel(es=energysystem, timeindex=datetimeindex)

# solve with specific optimization options (passed to pyomo)
om.solve(solve_kwargs={'tee': True,
                       'keepfiles': False})

# write back results from optimization object to energysystem
om.results()


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
esplot = tpd.DataFramePlot(energy_system=energysystem)
# select input results of electrical bus (i.e. power delivered by plants)
esplot.slice_unstacked(bus_label="b_el", type="input")
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
