# -*- coding: utf-8 -*-

"""
This script shows how to a an individual constraint to the oemof solph
Model.
The constraint we add forces a flow to be greater or equal a certain share
of all inflows of its target bus. Moreover we will set an emission constraint.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_scripts/test_solph/
test_flexible_modelling/test_add_constraints.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose.tools import ok_
import logging
import pyomo.environ as po
import pandas as pd
from oemof.network import Node
from oemof.solph import (Sink, Transformer, Bus, Flow,
                         Model, EnergySystem)


def test_add_constraints_example(solver='cbc', nologg=False):
    if not nologg:
        logging.basicConfig(level=logging.INFO)
    # ##### creating an oemof solph optimization model, nothing special here ##
    # create an energy system object for the oemof solph nodes
    es = EnergySystem(timeindex=pd.date_range('1/1/2012', periods=4, freq='H'))
    Node.registry = es
    # add some nodes
    boil = Bus(label="oil", balanced=False)
    blig = Bus(label="lignite", balanced=False)
    b_el = Bus(label="b_el")

    Sink(label="Sink",
         inputs={b_el: Flow(nominal_value=40,
                            actual_value=[0.5, 0.4, 0.3, 1],
                            fixed=True)})
    pp_oil = Transformer(label='pp_oil',
                         inputs={boil: Flow()},
                         outputs={b_el: Flow(nominal_value=50,
                                             variable_costs=25)},
                         conversion_factors={b_el: 0.39})
    Transformer(label='pp_lig',
                inputs={blig: Flow()},
                outputs={b_el: Flow(nominal_value=50,
                                    variable_costs=10)},
                conversion_factors={b_el: 0.41})

    # create the model
    om = Model(energysystem=es)

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
    # Model instance and add the constraints.
    myblock = po.Block()

    # create a pyomo set with the flows (i.e. list of tuples),
    # there will of course be only one flow inside this set, the one we used to
    # add outflow_share
    myblock.MYFLOWS = po.Set(initialize=[k for (k, v) in om.flows.items()
                                         if hasattr(v, 'outflow_share')])

    # pyomo does not need a po.Set, we can use a simple list as well
    myblock.COMMODITYFLOWS = [k for (k, v) in om.flows.items()
                              if hasattr(v, 'emission_factor')]

    # add the sub-model to the oemof Model instance
    om.add_component('MyBlock', myblock)

    def _inflow_share_rule(m, s, e, t):
        """pyomo rule definition: Here we can use all objects from the block or
        the om object, in this case we don't need anything from the block
        except the newly defined set MYFLOWS.
        """
        expr = (om.flow[s, e, t] >= om.flows[s, e].outflow_share[t] *
                sum(om.flow[i, o, t] for (i, o) in om.FLOWS if o == e))
        return expr

    myblock.inflow_share = po.Constraint(myblock.MYFLOWS, om.TIMESTEPS,
                                         rule=_inflow_share_rule)
    # add emission constraint
    myblock.emission_constr = po.Constraint(expr=(
            sum(om.flow[i, o, t]
                for (i, o) in myblock.COMMODITYFLOWS
                for t in om.TIMESTEPS) <= emission_limit))

    # solve and write results to dictionary
    # you may print the model with om.pprint()
    ok_(om.solve(solver=solver))
    logging.info("Successfully finished.")
