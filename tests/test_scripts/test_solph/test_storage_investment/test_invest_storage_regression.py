# -*- coding: utf-8 -*-

"""
This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_scripts/test_solph/
test_storage_investment/test_storage_investment.py

SPDX-License-Identifier: MIT
"""

import logging

import pandas as pd

from oemof import solph
from oemof.solph import views


def test_regression_investment_storage(solver="cbc"):
    """The problem was infeasible if the existing capacity and the maximum was
    defined in the Flow.
    """

    logging.info("Initialize the energy system")
    date_time_index = pd.date_range("1/1/2012", periods=4, freq="h")

    energysystem = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=True
    )

    # Buses
    bgas = solph.buses.Bus(label=("natural", "gas"))
    bel = solph.buses.Bus(label="electricity")
    energysystem.add(bgas, bel)

    energysystem.add(
        solph.components.Sink(
            label="demand",
            inputs={
                bel: solph.flows.Flow(
                    fix=[209643, 207497, 200108, 191892], nominal_capacity=1
                )
            },
        )
    )

    # Sources
    energysystem.add(
        solph.components.Source(
            label="rgas", outputs={bgas: solph.flows.Flow()}
        )
    )

    # Converter
    energysystem.add(
        solph.components.Converter(
            label="pp_gas",
            inputs={bgas: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow(nominal_capacity=300000)},
            conversion_factors={bel: 0.58},
        )
    )

    # Investment storage
    energysystem.add(
        solph.components.GenericStorage(
            label="storage",
            inputs={
                bel: solph.flows.Flow(
                    nominal_capacity=solph.Investment(
                        existing=625046 / 6, maximum=0
                    )
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_capacity=solph.Investment(
                        existing=104174.33, maximum=1
                    )
                )
            },
            loss_rate=0.00,
            initial_storage_level=0,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.8,
            nominal_capacity=solph.Investment(
                ep_costs=50,
                existing=625046,
            ),
        )
    )

    # Solve model
    om = solph.Model(energysystem)
    om.solve(solver=solver)

    # Results
    results = solph.processing.results(om)

    electricity_bus = views.node(results, "electricity")
    my_results = electricity_bus["sequences"].sum(axis=0).to_dict()
    storage = energysystem.groups["storage"]
    my_results["storage_invest"] = results[(storage, None)]["scalars"][
        "invest"
    ]
