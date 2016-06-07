# -*- coding: utf-8 -*-

import math
import logging
import pandas as pd

from oemof.tools import logger
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph.network import (Bus, Source, Sink, Flow, Investment,
                                 LinearTransformer, Storage)
from oemof.solph import OperationalModel
from oemof.solph.options import Sequence


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

nodes = {}

for i, r in nodes_flows.iterrows():

    # save column labels and row values in dict
    row = dict(zip(r.index.values, r.values))

    # create flow
    flow = Flow()
    flow_attrs = vars(Flow()).keys()
    for attr in flow_attrs:
        if attr in row.keys() and row[attr]:
            if row[attr] != 'seq':
                setattr(flow, attr, Sequence(row[attr]))  # solph seq
            else:
                seq = nodes_flows_seq.loc[row['class'],
                                          row['label'],
                                          row['source'],
                                          row['target'],
                                          attr]
                seq = [i for i in seq.values]
                setattr(flow, attr, seq)

    # create node (eval to be substituted due to security issues)
    node = eval(row['class'])
    node.label = row['label']

    # set node attributes (must be in the first line of node entries in csv)
    for attr in row.keys():
        if (attr not in flow_attrs and
           attr not in ('class', 'label', 'source', 'target',
                        'conversion_factors')):
                if row[attr] != 'seq':
                    setattr(node, attr, Sequence(row[attr]))  # solph seq
                else:
                    seq = nodes_flows_seq.loc[row['class'],
                                              row['label'],
                                              row['source'],
                                              row['target'],
                                              attr]
                    seq = [i for i in seq.values]
                    setattr(node, attr, seq)

    # create an input entry for the current line
    if row['label'] == row['target']:
        if row['source'] not in nodes.keys():
            nodes[row['source']] = Bus(label=row['source'])
        inputs = {nodes[row['source']]: flow}
    else:
        inputs = {}

    # set output entry for the current line
    if row['label'] == row['source']:
        if row['target'] not in nodes.keys():
            nodes[row['target']] = Bus(label=row['target'])
        outputs = {nodes[row['target']]: flow}
    else:
        outputs = {}

    # set conversion_factor entry for the current line
    if row['target'] and not math.isnan(row['conversion_factors']):
        conversion_factors = {nodes[row['target']]:
                              row['conversion_factors']}
    else:
        pass
        conversion_factors = {}

    # add node to dict and assign attributes depending on
    # if there are multiple lines per node or not
    if node.label in nodes.keys():
        node.inputs.update(inputs)
        node.outputs.update(outputs)
        node.conversion_factors.update(conversion_factors)
    else:
        node.inputs = inputs
        node.outputs = outputs
        node.conversion_factors = conversion_factors
        nodes[node.label] = node

# %% print stuff

# Nodes with in and outputs
for k, v in nodes.items():
    if type(v).__name__ != 'Bus':
        print('Label: ', v.label)
        print('Inputs: ', v.inputs)
        print('Outputs:', v.outputs)

print('Conversion factors:')
print(nodes['chp1'].conversion_factors)

print('Sequence for capacity loss of storage1:')
print(nodes['storage1'].capacity_loss)


print('Sequences for output flow of solar1:')
for k, v in nodes['solar1'].outputs.items():
    print(k, v.actual_value)
