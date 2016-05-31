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

labels = nodes_flows['label'].unique()

def create_flow(row):
    # TODO: better use setattr?, catch seq
    dc = {}
    for k, v in vars(Flow()).items():
        if k in row:
            dc[k] = row[k]
    return Flow(dc)

def create_buses(df):
    ''' '''
    labels = df['label'].unique()
    buses = {}

    for i, b in df[~df.isin(labels)].iterrows():
        if b.source == b.source:
            buses[b.source] = Bus(label=b.source)
        elif b.target == b.target:
            buses[b.target] = Bus(label=b.target)
    #TODO: Buses are initialized multiple times, could be a problem, last set
    # key determines bus object, also there must be a better way
    return buses

def obj_for_str(string):
    dc = {'Transformer': LinearTransformer,
          'Storage': Storage,
          'Sink': Sink,
          'Source': Source}
    return dc[string]

def one_node(df):
    ''' '''
    for node_lb in df['label'].unique():
        node_subs = df[df.label == node_lb]
        node_cls_str = next(iter(node_subs['class'])) #TODO: better try except unique
        yield node_cls_str, node_lb, node_subs


entities = []
buses = create_buses(nodes_flows)
for node_cls_str, node_lb, node_subs in one_node(nodes_flows):

    kw = {'inputs':{buses[row.source]: create_flow(row) for i, row in
                node_subs.iterrows() if row.target == node_lb},
                'outputs':{buses[row.target]:create_flow(row) for i, row in
                node_subs.iterrows() if row.source == node_lb},
                'label':node_lb}

    node_cls = obj_for_str(node_cls_str)

    if node_cls_str == 'Transformer':
        kw.update({'conversion_factors':{buses[row.target]:
                        row.conversion_factor for i, row in
                        subs.iterrows() if row.conversion_factor ==\
                                            row.conversion_factor}})
    if node_cls_str == 'Storage':
        #TODO: map row fields to attr
        continue

    node = node_cls(**kw)
    entities.append(node)


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
