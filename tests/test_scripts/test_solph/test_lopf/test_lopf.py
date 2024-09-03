# -*- coding: utf-8 -*-

"""
This test contains a ElectricalBus and ElectricalLine class.


This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_variable_chp/test_variable_chp.py

SPDX-License-Identifier: MIT
"""

import logging

import pandas as pd
import pytest

from oemof.solph import EnergySystem
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import processing
from oemof.solph import views
from oemof.solph.buses import experimental as exp_bus
from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.flows import Flow
from oemof.solph.flows import experimental as exp_flow


@pytest.mark.skip(reason="Constraints of Electrical Line do not build.")
def test_lopf(solver="cbc"):
    logging.info("Initialize the energy system")

    # create time index for 192 hours in May.
    date_time_index = pd.date_range("5/5/2012", periods=1, freq="h")
    es = EnergySystem(timeindex=date_time_index, infer_last_interval=True)

    ##########################################################################
    # Create oemof.solph objects
    ##########################################################################

    logging.info("Create oemof.solph objects")

    b_el0 = exp_bus.ElectricalBus(label="b_0", v_min=-1, v_max=1)

    b_el1 = exp_bus.ElectricalBus(label="b_1", v_min=-1, v_max=1)

    b_el2 = exp_bus.ElectricalBus(label="b_2", v_min=-1, v_max=1)

    es.add(b_el0, b_el1, b_el2)

    b_el1.inputs[b_el0] = exp_flow.ElectricalLine(
        input=b_el0,
        output=b_el1,
        reactance=0.0001,
        nominal_capacity=Investment(ep_costs=10),
        min=-1,
        max=1,
    )

    b_el2.inputs[b_el1] = exp_flow.ElectricalLine(
        input=b_el1,
        output=b_el2,
        reactance=0.0001,
        nominal_capacity=60,
        min=-1,
        max=1,
    )

    b_el0.inputs[b_el2] = exp_flow.ElectricalLine(
        input=b_el2,
        output=b_el0,
        reactance=0.0001,
        nominal_capacity=60,
        min=-1,
        max=1,
    )

    es.add(
        Source(
            label="gen_0",
            outputs={b_el0: Flow(nominal_capacity=100, variable_costs=50)},
        )
    )

    es.add(
        Source(
            label="gen_1",
            outputs={b_el1: Flow(nominal_capacity=100, variable_costs=25)},
        )
    )

    es.add(
        Sink(
            label="load",
            inputs={b_el2: Flow(nominal_capacity=100, fix=1)},
        )
    )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info("Creating optimisation model")
    om = Model(es)

    logging.info("Running lopf on 3-Node exmaple system")
    om.solve(solver=solver)

    results = processing.results(om, remove_last_time_point=True)

    generators = views.node_output_by_type(results, Source)

    generators_test_results = {
        (es.groups["gen_0"], es.groups["b_0"], "flow"): 20,
        (es.groups["gen_1"], es.groups["b_1"], "flow"): 80,
    }

    for key in generators_test_results.keys():
        logging.debug("Test genertor production of {0}".format(key))
        assert generators[key].iloc[0] == pytest.approx(
            generators_test_results[key]
        )

    assert (
        results[es.groups["b_2"], es.groups["b_0"]]["sequences"]["flow"].iloc[
            0
        ]
        == -40
    )

    assert (
        results[es.groups["b_1"], es.groups["b_2"]]["sequences"]["flow"].iloc[
            0
        ]
        == 60
    )

    assert (
        results[es.groups["b_0"], es.groups["b_1"]]["sequences"]["flow"].iloc[
            0
        ]
        == -20
    )

    # objective function
    assert processing.meta_results(om)["objective"] == pytest.approx(
        3200, abs=0.5
    )
