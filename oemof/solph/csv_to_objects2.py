# -*- coding: utf-8 -*-

import pandas as pd
from oemof.network import Bus
from oemof.solph import Flow, Storage, LinearTransformer, Sink, Source


# %% new core interface

bel = Bus(label='el_balance')

bcoal = Bus(label='coalbus')

so = Source(label='coalsource', outputs={bcoal: Flow()})

wind = Source(label='wind',
              outputs={bel: Flow(actual_value=[1, 1, 2], nominal_value=2,
                                 fixed_costs=25)})
si = Sink(label='sink', inputs={bel: Flow(max=[0.1, 0.2, 0.9],
                                          nominal_value=10,
                                          fixed=True, actual_value=[1, 2, 3])})

trsf = LinearTransformer(label='trsf', inputs={bcoal: Flow()},
                         outputs={bel: Flow(nominal_value=10,
                                            fixed_costs=5,
                                            variable_costs=10,
                                            summed_max=4,
                                            summed_min=2)},
                         conversion_factors={bel: 0.4})

stor = Storage(label='stor', inputs={bel: Flow()}, outputs={bel: Flow()},
               nominal_capacity=50, inflow_conversion_factor=0.9,
               outflow_conversion_factor=0.8, initial_capacity=0.5,
               capacity_loss=0.001)

# %% approach to create objects by iterating over dataframe

nodes_flows = pd.read_csv('nodes_flows.csv', sep=',')
nodes_flows_seq = pd.read_csv('nodes_flows_seq.csv', sep=',', header=None)
nodes_flows_seq.drop(0, axis=1, inplace=True)
nodes_flows_seq = nodes_flows_seq.transpose()
nodes_flows_seq.set_index([0, 1, 2, 3, 4], inplace=True)
nodes_flows_seq.columns = range(0, len(nodes_flows_seq.columns))

node_dc = {}
for idx, row in nodes_flows.iterrows():

    # save column labels and row values in dict
    row_dc = dict(zip(row.index.values, row.values))

    # create flow and set attributes
    flow = Flow()
    flow_attrs = vars(Flow()).keys()
    for attr in flow_attrs:
        if attr in row_dc.keys() and row_dc[attr]:
            setattr(flow, attr, row_dc[attr])

    # create node with general attributes and save it in dict
    # eval to be substituted due to security issues. but works for now..
    node = eval(row_dc['class'])
    node.label = row_dc['label']

    if node not in node_dc:
        node_dc[row_dc['label']] = node

    # set node attributes
    for attr in row_dc.keys():
        if (attr not in flow_attrs and
           attr not in ('class', 'source', 'target')):
                if row_dc[attr] != 'seq':
                    setattr(node, attr, row_dc[attr])
                else:
                    seq = nodes_flows_seq.loc[row_dc['class'],
                                              row_dc['label'],
                                              row_dc['source'],
                                              row_dc['target'],
                                              attr]
                    seq = [i for i in seq.values]
                    setattr(node, attr, seq)

    # set busses and flows for all sources
    if row_dc['class'] == 'Source':
        if row_dc['target'] not in node_dc.keys():
            node_dc[row_dc['target']] = Bus(label=row_dc['target'])
        node.outputs = {node_dc[row_dc['target']]: flow}

    # set busses and flows for all sinks
    if row_dc['class'] == 'Sink':
        if row_dc['source'] not in node_dc.keys():
            node_dc[row_dc['source']] = Bus(label=row_dc['source'])
        node.inputs = {node_dc[row_dc['source']]: flow}


# %% print stuff
print(node_dc)
for k, v in node_dc.items():
    print(k, v, '\n')
node_dc['storage1'].capacity_loss
