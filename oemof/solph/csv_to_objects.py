# -*- coding: utf-8 -*-

import pandas as pd
import oemof.network as on
from oemof.solph import Flow


bel = on.Bus(label='el_balance')
bcoal = on.Bus(label='coalbus')

so = on.Source(label='coalsource', outputs={bcoal: Flow()})

wind = on.Source(label='wind',
                 outputs={bel: Flow(actual_value=[1, 1, 2], nominal_value=2,
                                    fixed_costs=25)})
si = on.Sink(label='sink',
             inputs={bel: Flow(max=[0.1, 0.2, 0.9], nominal_value=10,
                               fixed=True, actual_value=[1, 2, 3])})

nodes_flows = pd.read_csv('nodes_flows.csv', sep=',')

# first get distinct values for class and label



# then operate on these subsets

def create_nodes(row):
    if row['class'] == 'Sink':
        node = on.Source(label=str(row['label']))
    else:
        node = 'something different'
    return node
result = nodes_flows.apply(create_nodes, axis=1)
print(result)

#if hasattr(a, 'property'):

nodes_flows_seq = pd.read_csv('nodes_flows_seq.csv', sep=',', header=None)
nodes_flows_seq.drop(0, axis=1, inplace=True)
nodes_flows_seq = nodes_flows_seq.transpose()


#trsf = on.LinearTransformer(label='trsf', inputs={bcoal:Flow()},
#                         outputs={bel:Flow(nominal_value=10,
#                                           fixed_costs=5,
#                                           variable_costs=10,
#                                           summed_max=4,
#                                           summed_min=2)},
#                         conversion_factors={bel: 0.4})
#
#stor = on.Storage(label='stor', inputs={bel: Flow()}, outputs={bel:Flow()},
#               nominal_capacity=50, inflow_conversion_factor=0.9,
#               outflow_conversion_factor=0.8, initial_capacity=0.5,
#               capacity_loss=0.001)