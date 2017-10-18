# -*- coding: utf-8 -*-
"""
This script shows how to a an individual constraint to the oemof solph
OperationalModel.
The constraint we add forces a flow to be greater or equal a certain share
of all inflows of its target bus. Moreover we will set an emission constraint.

31.10.2016
simon.hilpert@uni-flensburg.de
"""
import logging
import pyomo.environ as po
import pandas as pd
from oemof.solph import (Sink, LinearTransformer, Bus, Flow,
                         OperationalModel, EnergySystem)


def run_add_constraints_example(solver='cbc', nologg=False):
    if not nologg:
        logging.basicConfig(level=logging.INFO)
    # ##### creating an oemof solph optimization model, nothing special here ###
    # create an energy system object for the oemof solph nodes
    es = EnergySystem(timeindex=pd.date_range('1/1/2012', periods=4, freq='H'))
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

    # create the model
    om = OperationalModel(es=es)

    # add specific emission values to flow objects if source is a commodity bus
    for s, t in om.flows.keys():
        if s is boil:
            om.flows[s, t].emission_factor = 0.27  # t/MWh
        if s is blig:
            om.flows[s, t].emission_factor = 0.39  # t/MWh
    emission_limit = 60e3

    # add the outflow share
    om.flows[(boil, pp_oil)].outflow_share = [1, 0.5, 0, 0.3]

    # Now we are going to add a 'sub-model' and add a user specific constraint
    # first we add ad pyomo Block() instance that we can use to add our
    # constraints. Then, we add this Block to our previous defined
    # OperationalModel instance and add the constraints.
    myblock = po.Block()

    # create a pyomo set with the flows (i.e. list of tuples),
    # there will of course be only one flow inside this set, the one we used to
    # add outflow_share
    myblock.MYFLOWS = po.Set(initialize=[k for (k, v) in om.flows.items()
                                         if hasattr(v, 'outflow_share')])

    # pyomo does not need a po.Set, we can use a simple list as well
    myblock.COMMODITYFLOWS = [k for (k, v) in om.flows.items()
                              if hasattr(v, 'emission_factor')]

    # add the sub-model to the oemof OperationalModel instance
    om.add_component('MyBlock', myblock)

    def _inflow_share_rule(m, s, e, a, t):
        """pyomo rule definition: Here we can use all objects from the block or
        the om object, in this case we don't need anything from the block except
         the newly defined set MYFLOWS.
        """
        expr = (om.flow[s, e, a, t] >= om.flows[s, e].outflow_share[t] *
                sum(om.flow[i, o, a, t] for (i, o) in om.FLOWS if o == e))
        return expr

    myblock.inflow_share = po.Constraint(myblock.MYFLOWS, om.TIMEINDEX,
                                         rule=_inflow_share_rule)
    # add emission constraint
    myblock.emission_constr = po.Constraint(expr=(
            sum(om.flow[i, o, a, t]
                for (i, o) in myblock.COMMODITYFLOWS
                for a, t in om.TIMEINDEX) <= emission_limit))

    # solve and write results to dictionary
    # you may print the model with om.pprint()
    om.solve(solver=solver)
    logging.info("Successfully finished.")

if __name__ == "__main__":
    run_add_constraints_example()
