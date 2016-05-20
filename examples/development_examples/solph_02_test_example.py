# -*- coding: utf-8 -*-


from oemof.core import energy_system as oces
from oemof.solph import Bus, Source, Sink, Flow, LinearTransformer, OperationalModel
import oemof.solph.constraints as cblocks
import pyomo.environ as pyomo

def constraint_grouping(node):
    if isinstance(node, Bus) and 'balance' in str(node):
        return cblocks.BusBalance
    if isinstance(node, LinearTransformer):
        return cblocks.LinearRelation

def objective_grouping(node):
    if isinstance(node, LinearTransformer):
        return cblocks.outflowcosts

################################ 1st Energysystem #############################
es1 = oces.EnergySystem(groupings=[constraint_grouping, objective_grouping],
                       time_idx=[1, 2, 3])

elbus = Bus(label="electrical_balance")
gasbus = Bus(label="gas")

so = Source(label="sink", outputs={elbus: Flow(actual_value=[10, 5, 10],
                                               fixed=True)})
si = Sink(label="source", inputs={elbus: Flow(max=[0.1, 0.2, 0.9],
                                              nominal_value=10, fixed=True)})
transf = LinearTransformer(label="trsf", inputs={gasbus: Flow()},
                           outputs={elbus: Flow(nominal_value=100)},
                           conversion_factors={elbus: 0.5})
om1 = OperationalModel(es1)

############################ 2nd Energy system ################################
es2 = oces.EnergySystem(groupings=[constraint_grouping, objective_grouping],
                        time_idx=[1, 2, 3])
gasbus = Bus(label="gas")
elbus = Bus(label="electrical_balance")
thbus = Bus(label="heat_balance")

chp = LinearTransformer(label="chp",
                        inputs={gasbus: Flow()},
                        outputs={elbus: Flow(nominal_value=100), thbus: Flow()},
                        conversion_factors={elbus: 0.3, thbus: 0.5})

om2 = OperationalModel(es2)

####################### Optimization Model to merge problem ###################
master = pyomo.ConcreteModel()
master.om1 = om1
master.om2 = om2
master.om1.IN = pyomo.Connector()
master.om1.in_flow = pyomo.Var()
master.om1.out_flow = pyomo.Var()
master.om1.IN.add(master.om1.out_flow)
master.om1.IN.add(master.om1.in_flow)

master.om2.port = pyomo.Connector()
master.om2.in_flow = pyomo.Var()
master.om2.out_flow = pyomo.Var()
master.om2.port.add(master.om2.in_flow)
master.om2.port.add(master.om2.out_flow)

master.connection = pyomo.Constraint(expr=master.om2.port==master.om1.IN)

master.objective = pyomo.Objective(expr=master.om1.objective.expr +
                                        master.om2.objective.expr)
om1.del_component('objective')
om2.del_component('objective')

from pyomo.core.base.connector import ConnectorExpander

ConnectorExpander().apply(instance=master)

master.write(filename='merge_problem.lp', io_options={'symbolic_solver_labels':True})


