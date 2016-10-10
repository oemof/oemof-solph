# -*- coding: utf-8 -*-
"""
This script shows how to a an individual constraint to the oemof solph
OperationalModel.
The constraint we add forces a flow to be greater or equal a certain share
of all inflows of its target bus

10.10.2016
simon.hilpert@uni-flensburg.de
"""
import pyomo.environ as po
import pandas as pd
from oemof.solph import (Sink, LinearTransformer, Bus, Flow,
                         OperationalModel, EnergySystem, GROUPINGS)

####### creating an oemof solph optimization model, nothing special here ######
# create an energy system object for the oemof solph nodes
es = EnergySystem(groupings=GROUPINGS,
                  time_idx=pd.date_range('1/1/2012', periods=4, freq='H'))
# add some nodes
boil = Bus(label="oil", balanced=False)
blig = Bus(label="lignite", balanced=False)
b_el = Bus(label="b_el")

Sink(label="Sink",
     inputs={b_el: Flow(nominal_value=40,
                        actual_value=[0.5, 0.4, 0.3, 1],
                        fixed=True)})
pp_oil = LinearTransformer(label='pp_oil',
                           inputs={boil: Flow()},
                           outputs={b_el: Flow(nominal_value=50,
                                               variable_costs=25)},
                           conversion_factors={b_el: 0.39})
LinearTransformer(label='pp_lig',
                  inputs={blig: Flow()},
                  outputs={b_el: Flow(nominal_value=50,
                                      variable_costs=10)},
                  conversion_factors={b_el: 0.41})
# cretae the model
om = OperationalModel(es=es)

# all flows are stored in a dictionary 'flows' as an attribute of the model
# keys are (source, target) and values are the flow objects.
# add a user specific attribute to a flow that we will use inside the constr.
om.flows[(boil, pp_oil)].outflow_share = [1, 0.5, 0, 0.3]

# Now we are going to add a 'submodel' and add a user specific constraint
# first we add ad pyomo Block() instance that we can use to add our constraints
# Then, we add this Block to our previous defined OperationalModel instance
# and add a constraint

# an emtpy concrete model as container or submodel for added constraints etc.
myblock = po.Block()
# create a pyomo set with the flows (i.e. list of tulpes),
# there will of course be only one flow inside this set, the one we used to
# add outflow_share
myblock.MYFLOWS = po.Set(initialize=[k for (k,v) in om.flows.items()
                                     if hasattr(v, 'inflow_share')])

# add the submodel to the oemof OperationalModel instance
om.add_component('MyBlock', myblock)
# pyomo rule definition
# here we can use all objects from the block or the om object, in this case
# we don't need anything from the block except the newly defined set MYFLOWS
def _inflow_share_rule(m, s, e, t):
    """
    """
    expr = (om.flow[s, e, t] >= om.flows[s, e].outflow_share[t] *
           sum(om.flow[i, o, t] for (i, o) in om.FLOWS if o==e))
    return expr
myblock.inflow_share = po.Constraint(myblock.MYFLOWS, om.TIMESTEPS,
                                      rule=_inflow_share_rule)
# solve and write results to dictionary
# you may print the model with om.pprint()
om.solve()
results = om.results()