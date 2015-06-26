# -*- coding: utf-8 -*-
"""
This example uses some data from BNetzA scenario 2033 B.
(Germany as 1 "region")

The demand-series are generated randomly

The energy system is build out of objects. It is solved and the results
are written back into the objects.
"""

from optimization_model import *
import components as cp
import random


timesteps = [t for t in range(5)]

# emission factors in t/MWh
em_lig = 0.111 / 3.6
em_coal = 0.0917 / 3.6
em_gas = 0.0556 / 3.6
em_oil = 0.0750 / 3.6

# resources
bcoal = cp.Bus(uid="coal", type="coal")
bgas = cp.Bus(uid="gas", type="gas")
boil = cp.Bus(uid="oil", type="oil")
blig = cp.Bus(uid="lignite", type="lignite")

# electricity and heat
b_el = cp.Bus(uid="b_el", type="elec")
b_th = cp.Bus(uid="b_th", type="th")

# renewable sources (only pv onshore)
wind_on = cp.RenewableSource(uid="wind", outputs=[b_el],
                          val=[random.gauss(0.5, 0.1) for i in timesteps],
                          out_max=66300)
wind_off = cp.RenewableSource(uid="wind", outputs=[b_el],
                              val=[random.gauss(0.5, 0.1) for i in timesteps],
                              out_max=25300)
pv = cp.RenewableSource(uid="pv", outputs=[b_el],
                        val=[random.gauss(0.5, 0.1) for i in timesteps],
                        out_max=65300)
# resources
rcoal = cp.Commodity(uid="rcoal", outputs=[bcoal], emmission_factor=em_coal)
rgas = cp.Commodity(uid="rgas", outputs=[bgas], emmission_factor=em_gas)
roil = cp.Commodity(uid="roil", outputs=[boil], emmission_factor=em_oil)
rlig = cp.Commodity(uid="rlig", outputs=[blig], emmission_factor=em_lig)

# demands
demand_el = cp.Sink(uid="demand_el", inputs=[b_el],
                    val=[random.gauss(100000, 5000) for i in timesteps])
demand_th = cp.Sink(uid="demand_th", inputs=[b_th],
                    val=[random.gauss(20000, 5000) for i in timesteps])
# Simple Transformer for b_el
pp_coal = cp.SimpleTransformer(uid='pp_coal', inputs=[bcoal],
                               outputs=[b_el], in_max=None, out_max=20200,
                               eta=0.39, opex_var=20, co2_var=em_coal)
pp_lig = cp.SimpleTransformer(uid='pp_lig', inputs=[blig],
                              outputs=[b_el], in_max=None, out_max=11800,
                              eta=0.41, opex_var=19, co2_var=em_lig)
pp_gas = cp.SimpleTransformer(uid='pp_gas', inputs=[bgas],
                              outputs=[b_el], in_max=None, out_max=41000,
                              eta=0.45, opex_var=35, co2_var=em_lig)
pp_oil = cp.SimpleTransformer(uid='pp_oil', inputs=[boil],
                              outputs=[b_el], in_max=None, out_max=1000,
                              eta=0.3, opex_var=50, co2_var=em_pet)
# chp (not from BNetzA) eta_el=0.3, eta_th=0.3
pp_chp = cp.SimpleCombinedHeatPower(uid='pp_chp', inputs=[bgas], in_max=100000,
                                    out_max=[None, 30000], eta=[0.4, 0.3],
                                    outputs=[b_th, b_el])
# group busses
buses = [bcoal, bgas, boil, blig, b_el, b_th]

# group components
transformers = [pp_coal, pp_gas, pp_lig, pp_oil, pp_chp]
commodities = [rcoal, rgas, roil, rlig]
renew_sources = [wind_on, wind_off, pv]
sinks = [demand_th, demand_el]

components = transformers + commodities + renew_sources + sinks

om = opt_model(buses, components, timesteps=timesteps, invest=False)

# create model instance
instance = om.create()


instance = solve_opt_model(instance=instance, solver='gurobi',
                           options={'stream': True}, debug=False)


# post processing
#for idx in instance.w_add:
#    print('Add cap of '+ str(idx) + ': ' +str(instance.w_add[idx].value))
#for idx in instance.bus_slack:
#    print('Slack of '+str(idx[0])+': '+ str(instance.bus_slack[idx].value))

# get variable values and store in objects
temp_comp = transformers + renew_sources + commodities
for c in temp_comp:
    c.results['output'] = []
    for t in timesteps:
        o = [o.uid for o in c.outputs[:]][0]
        c.results['output'].append(instance.w[c.uid, o, t].value)


# plot results
import pylab as pl
import numpy as np
import matplotlib as mpl

fig, ax = pl.subplots()
n = len([c for c in temp_comp])
colors = mpl.cm.rainbow(np.linspace(0, 1, n))
for color, c in zip(colors, [c for c in temp_comp]):
    ax.step(timesteps, c.results['output'], color=color, label=c.uid)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
pl.grid()
pl.xlabel('Timesteps in h')
pl.ylabel('Power in MW')
#pl.show()

