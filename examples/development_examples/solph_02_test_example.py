# -*- coding: utf-8 -*-


from oemof.core import energy_system as oces
from oemof.solph import Bus, Source, Sink, Flow, LinearTransformer, OperationalModel
import oemof.solph.constraints as cblocks


def constraint_grouping(node):
    if isinstance(node, Bus) and 'el' in str(node):
        return cblocks.BusBalance
    if isinstance(node, LinearTransformer):
        return cblocks.LinearRelation

def objective_grouping(node):
    if isinstance(node, LinearTransformer):
        return cblocks.outflowcosts


es = oces.EnergySystem(groupings=[constraint_grouping, objective_grouping],
                       time_idx=[1,2,3])

lt = len(es.time_idx)

ebus = Bus(label="el")

#e2bus = Bus(label="el2")
gasbus = Bus(label="gas")

so = Source(outputs={ebus: Flow(actual_value=[10, 5, 10], fixed=True)})

si = Sink(inputs={ebus: Flow(max=[0.1, 0.2, 0.9], nominal_value=10,
                             fixed=True)})

ltransf = LinearTransformer(inputs={gasbus: Flow()},
                            outputs={ebus: Flow(nominal_value=100)},
                            conversion_factors={ebus: 0.5})

om = OperationalModel(es)


