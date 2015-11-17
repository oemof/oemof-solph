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

data = pd.read_csv("example_data_sc160.csv", sep=",")
timesteps = [t for t in range(12)]

# emission factors in t/MWh
em_lig = 0.111 * 3.6
em_coal = 0.0917 * 3.6
em_gas = 0.0556 * 3.6
em_oil = 0.0750 * 3.6

source.FixedSource.model_param.update({'investment': False})
transformer.Storage.model_param.update({'investment': True})

# resources
#bgas = Bus(uid="gas", type="gas", price=70, excess=False)
bgas = Bus(uid="gas", type="gas", price=70, sum_out_limit=194397000,
           balanced=False)
#bgas = Bus(uid="gas", type="gas", price=70)

# electricity and heat
b_el = Bus(uid="b_el", type="el", excess=True)

# renewable sources (only pv onshore)
wind_on = source.FixedSource(uid="wind_on",outputs=[b_el],
                                val=data['wind'],
                                cap_max={b_el.uid: 1000000},
                                out_max={b_el.uid: 1000000},
                                add_out_limit=0,
                                capex=1000,
                                opex_fix=20,
                                lifetime=25,
                                crf=0.08)
#                                wacc={b_el.uid: 0.07})

pv = source.FixedSource(uid="pv", outputs=[b_el], val=data['pv'],
                           cap_max={b_el.uid: 582000},
                           out_max={b_el.uid: 582000},
                           add_out_limit=0,
                           capex=900,
                           opex_fix=15,
                           lifetime=25,
                           crf=0.08)
#                          wacc={b_el.uid: 0.07})

# demands
demand_el = sink.Simple(uid="demand_el", inputs=[b_el],
                        val=data['demand_el'])

# Simple Transformer for b_el
pp_gas = transformer.Simple(uid='pp_gas', inputs=[bgas], outputs=[b_el],
                            in_max={bgas.uid: None}, opex_var=50,
                            out_max={b_el.uid: 10e10}, eta=[0.58])

# chp (not from BNetzA) eta_el=0.3, eta_th=0.3
#pp_chp = transformer.CHP(uid='pp_chp', inputs=[bgas], outputs=[b_el, b_th],
#                         in_max={bgas.uid: 100000},
#                         out_max={b_th.uid: None, b_el.uid: 30000},
#                         eta=[0.4, 0.3], opex_fix=20, opex_var=2,
#                         co2_var=em_gas)

# storage
sto_simple = transformer.Storage(uid='sto_simple', inputs=[b_el],
                                 outputs=[b_el],
                                 eta_in=1, eta_out=0.8, cap_loss=0.00,
                                 opex_fix=35, opex_var=10e10, co2_var=None,
                                 capex=1000,
                                 cap_max=0,
                                 cap_initial=0,
                                 c_rate_in = 1/6,
                                 c_rate_out = 1/6)


#                                 in_max={b_el.uid: 100000},
#                                 out_max={b_el.uid: 200000},

#sto_simple = transformer.Storage(uid='sto_simple', inputs=[b_el],
#                                 outputs=[b_el],
#                                 eta_in=1, eta_out=0.8,
#                                 capex=375,
#                                 opex_fix=10,
#                                 lifetime=10,
#                                 wacc=0.07)
                                 # + c-Rate

# group busses
buses = [bgas, b_el]

# group components
transformers = [pp_gas]
renew_sources = [pv, wind_on]
storages = [sto_simple]
sinks = [demand_el]

components = transformers + renew_sources + storages + sinks
entities = components + buses

om = OptimizationModel(entities=entities, timesteps=timesteps,
                       options={'objective_name': 'minimize_costs'})

om.solve(solver='gurobi', debug=True, tee=True, duals=False)
pp.results_to_objects(om)
# write results to data frame for excel export
components = transformers + renew_sources


if __name__ == "__main__":
    def plot_dispatch(bus_to_plot):
        # plotting: later as multiple pdf with pie-charts and topology?
        import numpy as np
        import matplotlib as mpl
        import matplotlib.cm as cm

        plot_data = renew_sources+transformers+storages

#        plot_data = renew_sources+transformers+transports+storages

        # data preparation
        x = np.arange(len(timesteps))
        y = []
        labels = []
        for c in plot_data:
            if bus_to_plot in c.results['out']:
                y.append(c.results['out'][bus_to_plot])
                labels.append(c.uid)

        # plot production
        fig, ax = plt.subplots()
#        sp = ax.stackplot(x, y,
#                          colors=cm.rainbow(np.linspace(0, 1, len(plot_data))),
#                          linewidth=0)

        sp = ax.stackplot(x, y,
                          colors=('yellow', 'blue', 'grey', 'red'),
                          linewidth=0)

        proxy = [mpl.patches.Rectangle((0, 0), 0, 0,
                                       facecolor=
                                       pol.get_facecolor()[0]) for pol in sp]
        # plot demand
        ax.step(x, demand_el.results['in'][demand_el.inputs[0].uid],
                c="black", lw=2)

        # storage soc (capacity at every timestep)
#        ax.step(x, sto_simple.results['cap'], c='green', lw=2.4)

        # plot storage input
        ax.step(x, (np.asarray(
            sto_simple.results['in'][sto_simple.inputs[0].uid])
            + np.asarray(
                demand_el.results['in'][demand_el.inputs[0].uid])),
            c='red', ls='-', lw=1)

        ax.legend(proxy, labels)
        ax.grid()

        ax.set_xlabel('Timesteps in h')
        ax.set_ylabel('Power in kW')
        ax.set_title('Dispatch')

    def print_results(bus_to_print):
        import numpy as np

        # demand results
        print('sum elec demand: ',
              np.asarray(demand_el.results['in'][bus_to_print]).sum())

        # production results
        print_data = renew_sources+transformers+storages
        sum_production = np.array([])
        for c in print_data:
            print(c)
            res = np.asarray(c.results['out'][bus_to_print])
            sum_production = np.append(sum_production, res)
            print('sum: ', res.sum())
            print('maximum value: ', res.max())

        # only non renewable production results
        transf = np.array([])
        for t in transformers:
            res = np.asarray(t.results['out'][bus_to_print])
            transf = np.append(transf, res)
            print('sum non renewable: ', transf.sum())

        # storage state and capacity
        storage_soc = np.asarray(sto_simple.results['cap'])
        print('sum storage content: ', storage_soc.sum())
        print('storage capacity: ', storage_soc.max())

        # storage load
        storage_load = np.asarray(
            sto_simple.results['in'][sto_simple.inputs[0].uid])
        print('sum storage load: ', storage_load.sum())
        print('maximum storage load: ', storage_load.max())

        # excess
        excess = list()
        for t in om.timesteps:
            excess.append(om.bus.excess_slack['b_el', t].value)

        print('sum excess: ', np.asarray(excess).sum())

        # autarky degree
        print('autarky degree: ', (sum_production.sum()  # production
                                   - transf.sum()  # minus non renewable prod.
                                   - np.asarray(excess).sum() # minus excess
                                   - storage_load.sum()) /  # minus stor. load
                                   np.asarray(demand_el.results['in']
                                              [bus_to_print]).sum())  #  in
                                              # proportion to the demand

    plot_dispatch('b_el')
    plt.show()

    print_results('b_el')
