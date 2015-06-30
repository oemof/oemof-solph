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
import pandas as pd

data = pd.read_csv("example_data.csv",sep=",")
timesteps = [t for t in range(24)]

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
b_el2 = cp.Bus(uid="b_el2", type="elec")
b_th = cp.Bus(uid="b_th", type="th")

# renewable sources (only pv onshore)
wind_on = cp.RenewableSource(uid="wind_on", outputs=[b_el],  val=data['wind'],
                          out_max=66300, dispatch=True)
wind_on2 = cp.RenewableSource(uid="wind_on2", outputs=[b_el2],  val=data['wind'],
                          out_max=66300, dispatch=True)
wind_off = cp.RenewableSource(uid="wind_off", outputs=[b_el], val=data['wind'],
                              out_max=25300)
pv = cp.RenewableSource(uid="pv", outputs=[b_el], val=data['pv'],
                        out_max=65300)
# resources
rcoal = cp.Commodity(uid="rcoal", outputs=[bcoal], emmission_factor=em_coal)
rgas = cp.Commodity(uid="rgas", outputs=[bgas], emmission_factor=em_gas)
roil = cp.Commodity(uid="roil", outputs=[boil], emmission_factor=em_oil)
rlig = cp.Commodity(uid="rlig", outputs=[blig], emmission_factor=em_lig)

# demands
demand_el = cp.Sink(uid="demand_el", inputs=[b_el],
                    val=data['demand_el'])
demand_el2 = cp.Sink(uid="demand_el2", inputs=[b_el2],
                    val=data['demand_el'])
demand_th = cp.Sink(uid="demand_th", inputs=[b_th],
                    val=data['demand_th']*100000)
# Simple Transformer for b_el
pp_coal = cp.SimpleTransformer(uid='pp_coal', inputs=[bcoal],
                               outputs=[b_el], in_max=None, out_max=20200,
                               eta=0.39, opex_var=25, co2_var=em_coal)
pp_lig = cp.SimpleTransformer(uid='pp_lig', inputs=[blig],
                              outputs=[b_el], in_max=None, out_max=11800,
                              eta=0.41, opex_var=19, co2_var=em_lig)
pp_gas = cp.SimpleTransformer(uid='pp_gas', inputs=[bgas],
                              outputs=[b_el], in_max=None, out_max=41000,
                              eta=0.45, opex_var=45, co2_var=em_lig)
pp_oil = cp.SimpleTransformer(uid='pp_oil', inputs=[boil],
                              outputs=[b_el], in_max=None, out_max=1000,
                              eta=0.3, opex_var=50, co2_var=em_oil)
# chp (not from BNetzA) eta_el=0.3, eta_th=0.3
pp_chp = cp.SimpleCombinedHeatPower(uid='pp_chp', inputs=[bgas], in_max=100000,
                                    out_max=[None, 30000], eta=[0.4, 0.3],
                                    outputs=[b_th, b_el])

# transport
cable1 = cp.SimpleTransport(uid="cable1", inputs=[b_el], outputs=[b_el2],
                        in_max=700, eta=0.9)
cable2 = cp.SimpleTransport(uid="cable2", inputs=[b_el2], outputs=[b_el],
                        in_max=700, eta=0.8)

# group busses
buses = [bcoal, bgas, boil, blig, b_el, b_el2, b_th]

# group components
transformers = [pp_coal, pp_gas, pp_lig, pp_oil, pp_chp]
commodities = [rcoal, rgas, roil, rlig]
renew_sources = [pv, wind_on, wind_on2, wind_off]
sinks = [demand_th, demand_el]
transports = [cable1, cable2]

components = transformers + commodities + renew_sources + sinks + transports

om = opt_model(buses, components, timesteps=timesteps, invest=False)

instance = solve(model=om, solver='gurobi', debug=False, tee=True)

results_to_objects(entities=transformers+commodities+renew_sources+transports,
                   instance=instance)

# print dispatch of renewable source with dispatch = True (does not work with
# invest at the moment)

#if(True in instance.dispatch.values()):
#    for t in instance.timesteps:
#        print('Wind Dispatch in MW:',
#              instance.renew_dispatch['wind_on', t].value)

if __name__ == "__main__":

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import matplotlib.cm as cm

    data = renew_sources+transformers+transports

    # data preparation
    x = np.arange(len(timesteps))
    y = []
    labels = []
    for c in data:
        if 'b_el' in c.results['Output']:
            y.append(c.results['Output']['b_el'])
            labels.append(c.uid)
            #print(c.uid)

    # plotting
    fig, ax = plt.subplots()
    sp = ax.stackplot(x, y, colors=cm.rainbow(np.linspace(0, 1, len(data))))
    proxy = [mpl.patches.Rectangle((0, 0), 0, 0,
                                   facecolor=
                                   pol.get_facecolor()[0]) for pol in sp]
    ax.legend(proxy, labels)
    ax.grid()
    ax.set_xlabel('Timesteps in h')
    ax.set_ylabel('Power in MW')
    ax.set_title('Dispatch')

    def show_graph(buses=buses, components=components,
                   renew_sources=renew_sources, sinks=sinks,
                   commodities=commodities):
        import networkx as nx
        import matplotlib.pyplot as plt
        g = nx.DiGraph()
        es = components + buses
        g.add_nodes_from([e.uid for e in es])
        g.add_edges_from(get_edges(es))
        graph_pos = nx.fruchterman_reingold_layout(g)
        nx.draw_networkx_nodes(g, graph_pos, [b.uid for b in buses],
                               node_shape="o", node_color="r",
                               node_size=1200)
        nx.draw_networkx_nodes(g, graph_pos, [c.uid for c in components],
                               node_shape="s", node_color="b", node_size=1000)
        nx.draw_networkx_nodes(g, graph_pos, [s.uid for s in renew_sources],
                               node_shape="s", node_color="g", node_size=1000)
        nx.draw_networkx_nodes(g, graph_pos, [s.uid for s in sinks],
                               node_shape="s", node_color="y", node_size=1000)
        nx.draw_networkx_nodes(g, graph_pos, [c.uid for c in commodities],
                               node_shape="s", node_color="black",
                               node_size=1000, alpha=0.8)
        nx.draw_networkx_edges(g, graph_pos, width=1.5)
        nx.draw_networkx_labels(g, graph_pos, font_color='w', font_size=10)
        plt.show()
#    show_graph()
