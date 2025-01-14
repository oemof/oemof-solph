# -*- coding: utf-8 -*-

"""
This test contains a ExtractionTurbineCHP class.


This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_variable_chp/test_variable_chp.py

SPDX-License-Identifier: MIT
"""

import logging
import os

import pandas as pd
import pytest

from oemof import solph
from oemof.solph import views


def test_variable_chp(filename="variable_chp.csv", solver="cbc"):
    logging.info("Initialize the energy system")

    # create time index for 192 hours in May.
    date_time_index = pd.date_range("5/5/2012", periods=5, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=True
    )

    # Read data file with heat and electrical demand (192 hours)
    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data = pd.read_csv(full_filename, sep=",")

    ##########################################################################
    # Create oemof.solph objects
    ##########################################################################

    logging.info("Create oemof.solph objects")

    # create natural gas bus
    bgas = solph.buses.Bus(label=("natural", "gas"))
    energysystem.add(bgas)

    # create commodity object for gas resource
    energysystem.add(
        solph.components.Source(
            label=("commodity", "gas"),
            outputs={bgas: solph.flows.Flow(variable_costs=50)},
        )
    )

    # create two electricity buses and two heat buses
    bel = solph.buses.Bus(label=("electricity", 1))
    bel2 = solph.buses.Bus(label=("electricity", 2))
    bth = solph.buses.Bus(label=("heat", 1))
    bth2 = solph.buses.Bus(label=("heat", 2))
    energysystem.add(bel, bel2, bth, bth2)

    # create excess components for the elec/heat bus to allow overproduction
    energysystem.add(
        solph.components.Sink(
            label=("excess", "bth_2"), inputs={bth2: solph.flows.Flow()}
        )
    )
    energysystem.add(
        solph.components.Sink(
            label=("excess", "bth_1"), inputs={bth: solph.flows.Flow()}
        )
    )
    energysystem.add(
        solph.components.Sink(
            label=("excess", "bel_2"), inputs={bel2: solph.flows.Flow()}
        )
    )
    energysystem.add(
        solph.components.Sink(
            label=("excess", "bel_1"), inputs={bel: solph.flows.Flow()}
        )
    )

    # create simple sink object for electrical demand for each electrical bus
    energysystem.add(
        solph.components.Sink(
            label=("demand", "elec1"),
            inputs={
                bel: solph.flows.Flow(
                    fix=data["demand_el"], nominal_capacity=1
                )
            },
        )
    )
    energysystem.add(
        solph.components.Sink(
            label=("demand", "elec2"),
            inputs={
                bel2: solph.flows.Flow(
                    fix=data["demand_el"], nominal_capacity=1
                )
            },
        )
    )

    # create simple sink object for heat demand for each thermal bus
    energysystem.add(
        solph.components.Sink(
            label=("demand", "therm1"),
            inputs={
                bth: solph.flows.Flow(
                    fix=data["demand_th"], nominal_capacity=741000
                )
            },
        )
    )
    energysystem.add(
        solph.components.Sink(
            label=("demand", "therm2"),
            inputs={
                bth2: solph.flows.Flow(
                    fix=data["demand_th"], nominal_capacity=741000
                )
            },
        )
    )

    # create a fixed converter to distribute to the heat_2 and elec_2 buses
    energysystem.add(
        solph.components.Converter(
            label=("fixed_chp", "gas"),
            inputs={bgas: solph.flows.Flow(nominal_capacity=1e11)},
            outputs={bel2: solph.flows.Flow(), bth2: solph.flows.Flow()},
            conversion_factors={bel2: 0.3, bth2: 0.5},
        )
    )

    # create a fixed converter to distribute to the heat and elec buses
    energysystem.add(
        solph.components.ExtractionTurbineCHP(
            label=("variable_chp", "gas"),
            inputs={bgas: solph.flows.Flow(nominal_capacity=1e11)},
            outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
            conversion_factors={bel: 0.3, bth: 0.5},
            conversion_factor_full_condensation={bel: 0.5},
        )
    )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info("Optimise the energy system")

    om = solph.Model(energysystem)

    logging.info("Solve the optimization problem")
    om.solve(solver=solver)

    optimisation_results = solph.processing.results(om)
    parameter = solph.processing.parameter_as_dict(energysystem)

    myresults = views.node(optimisation_results, "('natural', 'gas')")
    sumresults = myresults["sequences"].sum(axis=0)
    maxresults = myresults["sequences"].max(axis=0)

    variable_chp_dict_sum = {
        (("('natural', 'gas')", "('variable_chp', 'gas')"), "flow"): 2823024,
        (("('natural', 'gas')", "('fixed_chp', 'gas')"), "flow"): 3710208,
        (("('commodity', 'gas')", "('natural', 'gas')"), "flow"): 6533232,
    }

    variable_chp_dict_max = {
        (("('natural', 'gas')", "('variable_chp', 'gas')"), "flow"): 630332,
        (("('natural', 'gas')", "('fixed_chp', 'gas')"), "flow"): 785934,
        (("('commodity', 'gas')", "('natural', 'gas')"), "flow"): 1416266,
    }

    for key in variable_chp_dict_max.keys():
        logging.debug("Test the maximum value of {0}".format(key))
        assert maxresults[[key]].iloc[0] == pytest.approx(
            variable_chp_dict_max[key]
        )

    for key in variable_chp_dict_sum.keys():
        logging.debug("Test the summed up value of {0}".format(key))
        assert sumresults[[key]].iloc[0] == pytest.approx(
            variable_chp_dict_sum[key]
        )

    assert (
        parameter[(energysystem.groups["('fixed_chp', 'gas')"], None)][
            "scalars"
        ]["label"]
        == "('fixed_chp', 'gas')"
    )
    assert (
        parameter[(energysystem.groups["('fixed_chp', 'gas')"], None)][
            "scalars"
        ]["conversion_factors_('electricity', 2)"]
    ) == pytest.approx(0.3)

    # objective function
    assert solph.processing.meta_results(om)["objective"] == pytest.approx(
        326661590, abs=0.5
    )
