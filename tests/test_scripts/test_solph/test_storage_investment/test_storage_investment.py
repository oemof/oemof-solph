# -*- coding: utf-8 -*-

"""
General description:
---------------------

The example models the following energy system:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Converter) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |



This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_scripts/test_solph/
test_storage_investment/test_storage_investment.py

SPDX-License-Identifier: MIT
"""

import logging
import os

import pandas as pd
import pytest
from oemof.tools import economics

from oemof import solph
from oemof.solph import processing
from oemof.solph import views

PP_GAS = None


def test_optimise_storage_size(
    filename="storage_investment.csv", solver="cbc"
):
    global PP_GAS

    logging.info("Initialize the energy system")
    date_time_index = pd.date_range("1/1/2012", periods=400, freq="h")

    es = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=True,
    )

    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data = pd.read_csv(full_filename, sep=",")

    # Buses
    bgas = solph.buses.Bus(label="natural_gas")
    bel = solph.buses.Bus(label="electricity")
    es.add(bgas, bel)

    # Sinks
    es.add(
        solph.components.Sink(
            label="excess_bel", inputs={bel: solph.flows.Flow()}
        )
    )

    es.add(
        solph.components.Sink(
            label="demand",
            inputs={
                bel: solph.flows.Flow(
                    fix=data["demand_el"], nominal_capacity=1
                )
            },
        )
    )

    # Sources
    es.add(
        solph.components.Source(
            label="rgas",
            outputs={
                bgas: solph.flows.Flow(
                    nominal_capacity=194397000 * 400 / 8760,
                    full_load_time_max=1,
                )
            },
        )
    )

    es.add(
        solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(
                    fix=data["wind"], nominal_capacity=1000000
                )
            },
        )
    )

    es.add(
        solph.components.Source(
            label="pv",
            outputs={
                bel: solph.flows.Flow(fix=data["pv"], nominal_capacity=582000)
            },
        )
    )

    # Converter
    PP_GAS = solph.components.Converter(
        label="pp_gas",
        inputs={bgas: solph.flows.Flow()},
        outputs={
            bel: solph.flows.Flow(nominal_capacity=1e11, variable_costs=50)
        },
        conversion_factors={bel: 0.58},
    )
    es.add(PP_GAS)

    # Investment storage
    epc = economics.annuity(capex=1000, n=20, wacc=0.05)
    es.add(
        solph.components.GenericStorage(
            label="storage",
            inputs={bel: solph.flows.Flow(variable_costs=10e10)},
            outputs={bel: solph.flows.Flow(variable_costs=10e10)},
            loss_rate=0.00,
            initial_storage_level=0,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.8,
            nominal_capacity=solph.Investment(
                ep_costs=epc,
                existing=6851,
            ),
        )
    )

    # Solve model
    om = solph.Model(es)
    om.receive_duals()
    om.solve(solver=solver)
    es.results["main"] = processing.results(om)
    es.results["meta"] = processing.meta_results(om)

    # Check dump and restore
    es.dump()


def test_results_with_recent_dump():
    test_optimise_storage_size()
    energysystem = solph.EnergySystem()
    energysystem.restore()

    # Results
    results = energysystem.results["main"]
    meta = energysystem.results["meta"]

    electricity_bus = views.node(results, "electricity")
    my_results = electricity_bus["sequences"].sum(axis=0).to_dict()
    storage = energysystem.groups["storage"]
    my_results["storage_invest"] = results[(storage, None)]["scalars"][
        "invest"
    ]

    stor_invest_dict = {
        "storage_invest": 2040000,
        (("electricity", "None"), "duals"): 10800000000321,
        (("electricity", "demand"), "flow"): 105867395,
        (("electricity", "excess_bel"), "flow"): 211771291,
        (("electricity", "storage"), "flow"): 2350931,
        (("pp_gas", "electricity"), "flow"): 5148414,
        (("pv", "electricity"), "flow"): 7488607,
        (("storage", "electricity"), "flow"): 1880745,
        (("wind", "electricity"), "flow"): 305471851,
    }

    for key in stor_invest_dict.keys():
        assert my_results[key] == pytest.approx(stor_invest_dict[key])

    # Solver results
    assert str(meta["solver"]["Termination condition"]) == "optimal"
    assert meta["solver"]["Error rc"] == 0
    assert str(meta["solver"]["Status"]) == "ok"

    # Problem results
    assert meta["problem"]["Lower bound"] == 4.231675777e17
    assert meta["problem"]["Upper bound"], 4.231675777e17
    assert meta["problem"]["Number of variables"] == 2807
    assert meta["problem"]["Number of constraints"] == 2809
    assert meta["problem"]["Number of nonzeros"] == 1197
    assert meta["problem"]["Number of objectives"] == 1
    assert str(meta["problem"]["Sense"]) == "minimize"

    # Objective function
    assert meta["objective"] == pytest.approx(423167578261115584, abs=0.5)


def test_solph_converter_attributes_before_dump_and_after_restore():
    """dump/restore should preserve all attributes
    of `solph.components.Converter`"""
    test_optimise_storage_size()
    energysystem = solph.EnergySystem()
    energysystem.restore()

    trsf_attr_before_dump = sorted([x for x in dir(PP_GAS) if "__" not in x])

    trsf_attr_after_restore = sorted(
        [x for x in dir(energysystem.groups["pp_gas"]) if "__" not in x]
    )

    # Compare attributes before dump and after restore
    assert trsf_attr_before_dump == trsf_attr_after_restore
