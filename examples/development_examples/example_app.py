# -*- coding: utf-8 -*-

""" Example application that models Germany as one region for the year 2033.

Data
----

The application uses some data from BNetzA scenario 2033 B. Demand-series
are generated randomly.

Notes
-----
The energy system is build out of objects. It is solved and the results
are written back into the objects.

"""
import matplotlib.pyplot as plt

from oemof.core import energy_system as es
# solph imports
from oemof.solph.optimization_model import OptimizationModel
from oemof.solph import predefined_objectives as predefined_objectives
# base classes import
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer

from oemof.outputlib import to_pandas as tpd
import pandas as pd
from oemof.tools import logger
logger.define_logging()

data = pd.read_csv("example_data.csv", sep=",")
time_index = pd.date_range('1/1/2012', periods=168, freq='H')
simulation = es.Simulation(solver='glpk', timesteps=range(len(time_index)),
                           verbose=False, duals=False,
                           objective_options={
                             'function': predefined_objectives.minimize_cost})
#
energy_system = es.EnergySystem(simulation=simulation, time_idx=time_index)


# emission factors in t/MWh
em_lig = 0.111 * 3.6
em_coal = 0.0917 * 3.6
em_gas = 0.0556 * 3.6
em_oil = 0.0750 * 3.6

# resources
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

# Simple Transformer for b_el
pp_coal = transformer.Simple(uid='pp_coal', inputs=[bcoal], outputs=[b_el],
                             in_max={bcoal.uid: None},
                             out_max=[20.200], eta=[0.39],
                             opex_fix=2, opex_var=25, co2_var=em_coal)
pp_lig = transformer.Simple(uid='pp_lig', inputs=[blig], outputs=[b_el],
                            in_max=[None],
                            out_max=[11.800], eta=[0.41],
                            opex_fix=2, opex_var=19, co2_var=em_lig)
pp_gas = transformer.Simple(uid='pp_gas', inputs=[bgas], outputs=[b_el],
                            in_max=[None], out_max=[41.000], eta=[0.45],
                            opex_fix=2, opex_var=40, co2_var=em_gas)

pp_oil = transformer.Simple(uid='pp_oil', inputs=[boil], outputs=[b_el],
                            in_max=[None],
                            out_max=[0.1000], eta=[0.3],
                            opex_fix=2, opex_var=50, co2_var=em_oil)
# chp (not from BNetzA) eta_el=0.3, eta_th=0.3
pp_chp = transformer.CHP(uid='pp_chp', inputs=[bgas], outputs=[b_el, b_th],
                         in_max=[100],
                         out_max=[40, 30],
                         eta=[0.4, 0.3], opex_fix=0, opex_var=50,
                         co2_var=em_gas)
#storage = transformer.Storage(uid="sto", inputs=[b_el], outputs=[b_el],
#                              out_max=[10], in_max=[10], cap_max=20)


om = OptimizationModel(energysystem=energy_system)
#
om.solve(solve_kwargs={'tee': True,
                       'keepfiles': False},
         solver_cmdline_options={'min': ''})
energy_system.results = om.results()

# plot
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
esplot = tpd.DataFramePlot(energy_system=energy_system)
esplot.slice_unstacked(bus_uid="b_el", type="input")
colorlist = esplot.color_from_dict(cdict)
esplot.plot(color=colorlist, title="January 2016", stacked=True, width=1, lw=0.1,
            kind='bar')
esplot.ax.set_ylabel('Power in MW')
esplot.ax.set_xlabel('Date')
esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m')
esplot.outside_legend(reverse=True)
plt.show()
