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
from optimization_model import *
from network.entities import Bus
from network.entities.components import sinks as sink
from network.entities.components import sources as source
from network.entities.components import transformers as transformer
from network.entities.components import transports as transport

import pandas as pd

data = pd.read_csv("example_data.csv", sep=",")
timesteps = [t for t in range(3)]

# emission factors in t/MWh
em_lig = 0.111 * 3.6
em_coal = 0.0917 * 3.6
em_gas = 0.0556 * 3.6
em_oil = 0.0750 * 3.6

# resources
bcoal = Bus(uid="coal", type="coal")
bgas = Bus(uid="gas", type="gas")
boil = Bus(uid="oil", type="oil")
blig = Bus(uid="lignite", type="lignite")

# electricity and heat
b_el = Bus(uid="b_el", type="elec")
b_el2 = Bus(uid="b_el2", type="elec")
b_th = Bus(uid="b_th", type="th")

dispatch_flag = True
# renewable sources (only pv onshore)
wind_on = source.Renewable(uid="wind_on", outputs=[b_el], val=data['wind'],
                           out_max=66300, dispatch=dispatch_flag)
wind_on2 = source.Renewable(uid="wind_on2", outputs=[b_el2],
                            val=data['wind'], out_max=66300,
                            dispatch=dispatch_flag)
wind_off = source.Renewable(uid="wind_off", outputs=[b_el], val=data['wind'],
                            out_max=25300, dispatch=dispatch_flag)
pv = source.Renewable(uid="pv", outputs=[b_el], val=data['pv'],
                      out_max=65300, dispatch=dispatch_flag)
# resources
rcoal = source.Commodity(uid="rcoal", outputs=[bcoal], emmission_factor=em_coal)
rgas = source.Commodity(uid="rgas", outputs=[bgas], emmission_factor=em_gas)
roil = source.Commodity(uid="roil", outputs=[boil], emmission_factor=em_oil)
rlig = source.Commodity(uid="rlig", outputs=[blig], emmission_factor=em_lig)

# demands
demand_el = sink.Simple(uid="demand_el", inputs=[b_el],
                        val=data['demand_el'])
demand_el2 = sink.Simple(uid="demand_el2", inputs=[b_el2],
                         val=data['demand_el'])
demand_th = sink.Simple(uid="demand_th", inputs=[b_th],
                        val=data['demand_th']*100000)
# Simple Transformer for b_el
pp_coal = transformer.Simple(uid='pp_coal', inputs=[bcoal], outputs=[b_el],
                            param={'in_max': {bcoal.uid: None},
                            'out_max': {b_el.uid: 20200}, 'eta': [0.39]},
                            opex_var=25, co2_var=em_coal)
pp_lig = transformer.Simple(uid='pp_lig', inputs=[blig], outputs=[b_el],
                            param={'in_max': {blig.uid: None},
                           'out_max': {b_el.uid: 11800}, 'eta': [0.41]},
                            opex_var=19, co2_var=em_lig)
pp_gas = transformer.Simple(uid='pp_gas', inputs=[bgas], outputs=[b_el],
                            param={'in_max': {bgas.uid: None},
                                   'out_max': {b_el.uid: 41000},
                                   'eta': [0.45]},
                            opex_var=45, co2_var=em_lig)

pp_oil = transformer.Simple(uid='pp_oil', inputs=[boil], outputs=[b_el],
                            param={'in_max': {boil.uid: None},
                                  'out_max': {b_el.uid: 1000}, 'eta': [0.3]},
                             opex_var=50, co2_var=em_oil)
# chp (not from BNetzA) eta_el=0.3, eta_th=0.3
pp_chp = transformer.CHP(uid='pp_chp', inputs=[bgas], outputs=[b_el, b_th],
                         param={'in_max': {bgas.uid: 100000},
                                'out_max': {b_th.uid: None, b_el.uid: 30000},
                                'eta': [0.4, 0.3]})

# transport
cable1 = transport.Simple(uid="cable1", inputs=[b_el], outputs=[b_el2],
                          param={'in_max': {b_el.uid: 10000},
                                 'out_max': {b_el2.uid: 9000},
                                 'eta': [0.9]})
cable2 = transformer.Simple(uid="cable2", inputs=[b_el2], outputs=[b_el],
                            param={'in_max': {b_el2.uid: 10000},
                                   'out_max': {b_el.uid: 8000},
                                   'eta': [0.8]})

# group busses
buses = [bcoal, bgas, boil, blig, b_el, b_el2, b_th]

# group components
transformers = [pp_coal, pp_lig, pp_gas, pp_oil, pp_chp]
commodities = [rcoal, rgas, roil, rlig]
renew_sources = [pv, wind_on, wind_on2, wind_off]
sinks = [demand_th, demand_el, demand_el2]
transports = [cable1, cable2]

components = transformers + commodities + renew_sources + sinks + transports
entities = components + buses

om = OptimizationModel(entities=entities, timesteps=timesteps,
                       options={'invest': False, 'slack': True})
om.w.pprint()
om.solve(solver='gurobi', debug=True, tee=False, results_to_objects=True)

print(pp_coal.results)
# print dispatch of renewable source with dispatch = True (does not work with
# invest at the moment)

# if(True in instance.dispatch.values()):
#    for t in instance.timesteps:
#        print('Wind Dispatch in MW:',
#              instance.renew_dispatch['wind_on', t].value)

if __name__ == "__main__":

    def plot_dispatch(bus_to_plot):
        # plotting: later as multiple pdf with pie-charts and topology?
        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        import matplotlib.cm as cm

        plot_data = renew_sources+transformers+transports

        # data preparation
        x = np.arange(len(timesteps))
        y = []
        labels = []
        for c in plot_data:
            if bus_to_plot in c.results['Output']:
                y.append(c.results['Output'][bus_to_plot])
                labels.append(c.uid)
                #print(c.uid)

        # plotting
        fig, ax = plt.subplots()
        sp = ax.stackplot(x, y,
                          colors=cm.rainbow(np.linspace(0, 1, len(plot_data))))
        proxy = [mpl.patches.Rectangle((0, 0), 0, 0,
                                       facecolor=
                                       pol.get_facecolor()[0]) for pol in sp]
        ax.legend(proxy, labels)
        ax.grid()
        ax.set_xlabel('Timesteps in h')
        ax.set_ylabel('Power in MW')
        ax.set_title('Dispatch')

    plot_dispatch('b_el')
