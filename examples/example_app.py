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

from oemof.solph.optimization_model import OptimizationModel
from oemof.solph import postprocessing as pp
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer
from oemof.core.network.entities.components import transports as transport

import pandas as pd
import logging
logging.basicConfig(filename='example_app.log', level=logging.DEBUG)

data = pd.read_csv("example_data.csv", sep=",")
timesteps = [t for t in range(2)]

# emission factors in t/MWh
em_lig = 0.111 * 3.6
em_coal = 0.0917 * 3.6
em_gas = 0.0556 * 3.6
em_oil = 0.0750 * 3.6

# resources
bcoal = Bus(uid="coal", type="coal", price=20, sum_out_limit=10e10)
bgas = Bus(uid="gas", type="gas", price=35, sum_out_limit=10e10)
boil = Bus(uid="oil", type="oil", price=40,  sum_out_limit=10e10)
blig = Bus(uid="lignite", type="lignite", price=15,  sum_out_limit=10e10)

# electricity and heat
b_el = Bus(uid="b_el", type="el")
b_el2 = Bus(uid="b_el2", type="el")
b_th = Bus(uid="b_th", type="th")

# renewable sources (only pv onshore)
wind_on = source.DispatchSource(uid="wind_on", outputs=[b_el],
                                val=data['wind'],
                                out_max={b_el.uid: 66300}, dispatch_ex=10)
wind_on2 = source.DispatchSource(uid="wind_on2", outputs=[b_el2],
                                 val=data['wind'], out_max={b_el2.uid: 66300})
wind_off = source.DispatchSource(uid="wind_off", outputs=[b_el],
                                 val=data['wind'], out_max={b_el.uid: 25300})
pv = source.DispatchSource(uid="pv", outputs=[b_el], val=data['pv'],
                           out_max={b_el.uid: 65300})

# demands
demand_el = sink.Simple(uid="demand_el", inputs=[b_el],
                        val=data['demand_el'])
demand_el2 = sink.Simple(uid="demand_el2", inputs=[b_el2],
                         val=data['demand_el'])
demand_th = sink.Simple(uid="demand_th", inputs=[b_th],
                        val=data['demand_th']*100000)
# Simple Transformer for b_el
pp_coal = transformer.Simple(uid='pp_coal', inputs=[bcoal], outputs=[b_el],
                             in_max={bcoal.uid: None},
                             out_max={b_el.uid: 20200}, eta=[0.39],
                             opex_fix=2, opex_var=25, co2_var=em_coal)
pp_lig = transformer.Simple(uid='pp_lig', inputs=[blig], outputs=[b_el],
                            in_max={blig.uid: None},
                            out_max={b_el.uid: 11800}, eta=[0.41],
                            opex_fix=2, opex_var=19, co2_var=em_lig)
pp_gas = transformer.Simple(uid='pp_gas', inputs=[bgas], outputs=[b_el],
                            in_max={bgas.uid: None},
                            out_max={b_el.uid: 41000}, eta=[0.45],
                            opex_fix=2, opex_var=19, co2_var=em_gas)

pp_oil = transformer.Simple(uid='pp_oil', inputs=[boil], outputs=[b_el],
                            in_max={boil.uid: None},
                            out_max={b_el.uid: 1000}, eta=[0.3],
                            opex_fix=2, opex_var=40, co2_var=em_oil)
# chp (not from BNetzA) eta_el=0.3, eta_th=0.3
pp_chp = transformer.CHP(uid='pp_chp', inputs=[bgas], outputs=[b_el, b_th],
                         in_max={bgas.uid: 100000},
                         out_max={b_th.uid: None, b_el.uid: 30000},
                         eta=[0.4, 0.3], opex_fix=0, opex_var=40,
                         co2_var=em_gas)

# storage
sto_simple = transformer.Storage(uid='sto_simple', inputs=[b_el],
                                 outputs=[b_el], in_max={b_el.uid: 100000},
                                 out_max={b_el.uid: 200000},
                                 cap_max=700000, cap_min=0,
                                 eta_in=0.8, eta_out=0.8, cap_loss=0.01,
                                 opex_fix=35, opex_var=2, co2_var=None)
# transport
cable1 = transport.Simple(uid="cable1", inputs=[b_el], outputs=[b_el2],
                          in_max={b_el.uid: 10000},
                          out_max={b_el2.uid: 9000}, eta=[0.9],
                          opex_fix=5)

cable2 = transport.Simple(uid="cable2", inputs=[b_el2], outputs=[b_el],
                          in_max={b_el2.uid: 10000}, out_max={b_el.uid: 8000},
                          eta=[0.8], opex_fix=5)

# group busses
buses = [bcoal, bgas, boil, blig, b_el, b_el2, b_th]

# group components
transformers = [pp_coal, pp_lig, pp_gas, pp_oil, pp_chp]
renew_sources = [pv, wind_on, wind_on2, wind_off]
storages = [sto_simple]
sinks = [demand_th, demand_el, demand_el2]
transports = [cable1, cable2]

components = transformers + renew_sources + sinks + transports + storages
entities = components + buses

om = OptimizationModel(entities=entities, timesteps=timesteps,
                       options={'invest': False,
                                'slack': {'excess': False, 'shortage': True},
                                'milp' : False})

om.solve(solver='gurobi', debug=True, tee=True, duals=False)
pp.results_to_objects(om)
#pp.results_to_excel(om)
# write results to data frame for excel export
components = transformers + renew_sources


if __name__ == "__main__":
    def plot_dispatch(bus_to_plot):
        # plotting: later as multiple pdf with pie-charts and topology?
        import numpy as np
        import matplotlib as mpl
        import matplotlib.cm as cm

        plot_data = renew_sources+transformers+transports+storages

        # data preparation
        x = np.arange(len(timesteps))
        y = []
        labels = []
        for c in plot_data:
            if bus_to_plot in c.results['out']:
                y.append(c.results['out'][bus_to_plot])
                labels.append(c.uid)

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
    plt.show()
