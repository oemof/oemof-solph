# -*- coding: utf-8 -*-

import pandas as pd
import oemof.network as on
from oemof.network import Bus
from oemof.solph import Flow, Storage, LinearTransformer, Sink, Source


bel = Bus(label='el_balance')
bcoal = Bus(label='coalbus')

so = Source(label='coalsource', outputs={bcoal: Flow()})

wind = Source(label='wind',
              outputs={bel: Flow(actual_value=[1, 1, 2], nominal_value=2,
                                 fixed_costs=25)})
si = Sink(label='sink',
             inputs={bel: Flow(max=[0.1, 0.2, 0.9], nominal_value=10,
                               fixed=True, actual_value=[1, 2, 3])})

trsf = LinearTransformer(label='trsf', inputs={bcoal:Flow()},
                         outputs={bel:Flow(nominal_value=10,
                                           fixed_costs=5,
                                           variable_costs=10,
                                           summed_max=4,
                                           summed_min=2)},
                         conversion_factors={bel: 0.4})

stor = Storage(label='stor', inputs={bel: Flow()}, outputs={bel:Flow()},
               nominal_capacity=50, inflow_conversion_factor=0.9,
               outflow_conversion_factor=0.8, initial_capacity=0.5,
               capacity_loss=0.001)

nodes_flows = pd.read_csv('nodes_flows.csv', sep=',')
nodes_flows_seq = pd.read_csv('nodes_flows_seq.csv', sep=',', header=None)
nodes_flows_seq.drop(0, axis=1, inplace=True)
nodes_flows_seq = nodes_flows_seq.transpose()


def create_flow(row):
    f = Flow()
    dc = {} # TODO: better use setattr?
    for k, v in vars(f).items():
        if k in row:
            dc[k] = row[k]
    return Flow(dc)

strcls = {'Transformer': LinearTransformer,
          'Storage': Storage,
          'Sink': Sink,
          'Source': Source}

labels = nodes_flows['label'].unique()
for lb in labels:
    idx = nodes_flows.label == lb
    node_df = nodes_flows[idx]
    k = next(iter(node_df['class'])) #TODO: better try except unique
    # initiate node obj
    node_cls = strcls[k]
    #TODO: if Transformer, Storage additional attr
    node = node_cls(inputs = {row.target: create_flow(row) for i, row in
                              node_df.iterrows() if row.source == lb},
                outputs = {row.source:create_flow(row) for i, row in
                           node_df.iterrows() if row.target == lb})
    #TODO: can't figure out a weak ref error, flow initialisation works fine
    # dict expects component as key and not a string!

# first get distinct values for class and label
# then operate on these subsets

#def create_nodes(row):
#    if row['class'] == 'Sink':
#        node = Source(label=str(row['label']))
##        node.outputs = {row['target']: Flow(actual_value=row['actual_value'],
##                        nominal_value=row['actual_value'])}
#    else:
#        node = 'something different'
#    return node
#result = nodes_flows.apply(create_nodes, axis=1)
#print(result)

#if hasattr(a, 'property'):