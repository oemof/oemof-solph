# -*- coding: utf-8 -*-

"""This example shows how to create an energysystem with oemof objects and
solve it with the solph module.

Data: example_data.csv

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_simple_dispatch/test_simple_dispatch.py

SPDX-License-Identifier: MIT
"""

import os

import pandas as pd
import pytest
from oemof.tools import economics

from oemof.solph import EnergySystem
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import processing
from oemof.solph import views
from oemof.solph.buses import Bus
from oemof.solph.components import Converter
from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.flows import Flow


def test_dispatch_example(solver="cbc", periods=24 * 5):
    """Create an energy system and optimize the dispatch at least costs."""

    filename = os.path.join(os.path.dirname(__file__), "input_data.csv")
    data = pd.read_csv(filename, sep=",")

    # ######################### create energysystem components ################

    # resource buses
    bcoal = Bus(label="coal", balanced=False)
    bgas = Bus(label="gas", balanced=False)
    boil = Bus(label="oil", balanced=False)
    blig = Bus(label="lignite", balanced=False)

    # electricity and heat
    bel = Bus(label="b_el")
    bth = Bus(label="b_th")

    # an excess and a shortage variable can help to avoid infeasible problems
    excess_el = Sink(label="excess_el", inputs={bel: Flow()})
    # shortage_el = Source(label='shortage_el',
    #                      outputs={bel: Flow(variable_costs=200)})

    # sources
    ep_wind = economics.annuity(capex=1000, n=20, wacc=0.05)
    wind = Source(
        label="wind",
        outputs={
            bel: Flow(
                fix=data["wind"],
                nominal_capacity=Investment(ep_costs=ep_wind, existing=100),
            )
        },
    )

    ep_pv = economics.annuity(capex=1500, n=20, wacc=0.05)
    pv = Source(
        label="pv",
        outputs={
            bel: Flow(
                fix=data["pv"],
                nominal_capacity=Investment(ep_costs=ep_pv, existing=80),
            )
        },
    )

    # demands (electricity/heat)
    demand_el = Sink(
        label="demand_elec",
        inputs={bel: Flow(nominal_capacity=85, fix=data["demand_el"])},
    )

    demand_th = Sink(
        label="demand_therm",
        inputs={bth: Flow(nominal_capacity=40, fix=data["demand_th"])},
    )

    # power plants
    pp_coal = Converter(
        label="pp_coal",
        inputs={bcoal: Flow()},
        outputs={bel: Flow(nominal_capacity=20.2, variable_costs=25)},
        conversion_factors={bel: 0.39},
    )

    pp_lig = Converter(
        label="pp_lig",
        inputs={blig: Flow()},
        outputs={bel: Flow(nominal_capacity=11.8, variable_costs=19)},
        conversion_factors={bel: 0.41},
    )

    pp_gas = Converter(
        label="pp_gas",
        inputs={bgas: Flow()},
        outputs={bel: Flow(nominal_capacity=41, variable_costs=40)},
        conversion_factors={bel: 0.50},
    )

    pp_oil = Converter(
        label="pp_oil",
        inputs={boil: Flow()},
        outputs={bel: Flow(nominal_capacity=5, variable_costs=50)},
        conversion_factors={bel: 0.28},
    )

    # combined heat and power plant (chp)
    pp_chp = Converter(
        label="pp_chp",
        inputs={bgas: Flow()},
        outputs={
            bel: Flow(nominal_capacity=30, variable_costs=42),
            bth: Flow(nominal_capacity=40),
        },
        conversion_factors={bel: 0.3, bth: 0.4},
    )

    # heatpump with a coefficient of performance (COP) of 3
    b_heat_source = Bus(label="b_heat_source")

    heat_source = Source(label="heat_source", outputs={b_heat_source: Flow()})

    cop = 3
    heat_pump = Converter(
        label="el_heat_pump",
        inputs={bel: Flow(), b_heat_source: Flow()},
        outputs={bth: Flow(nominal_capacity=10)},
        conversion_factors={bel: 1 / 3, b_heat_source: (cop - 1) / cop},
    )

    datetimeindex = pd.date_range("1/1/2012", periods=periods, freq="h")
    energysystem = EnergySystem(
        timeindex=datetimeindex, infer_last_interval=True
    )
    energysystem.add(
        bcoal,
        bgas,
        boil,
        bel,
        bth,
        blig,
        excess_el,
        wind,
        pv,
        demand_el,
        demand_th,
        pp_coal,
        pp_lig,
        pp_oil,
        pp_gas,
        pp_chp,
        b_heat_source,
        heat_source,
        heat_pump,
    )

    # ################################ optimization ###########################

    # create optimization model based on energy_system
    optimization_model = Model(energysystem=energysystem)

    # solve problem
    optimization_model.solve(solver=solver)

    # write back results from optimization object to energysystem
    optimization_model.results()

    # ################################ results ################################

    # generic result object
    results = processing.results(model=optimization_model)

    # subset of results that includes all flows into and from electrical bus
    # sequences are stored within a pandas.DataFrames and scalars e.g.
    # investment values within a pandas.Series object.
    # in this case the entry data['scalars'] does not exist since no investment
    # variables are used
    data = views.node(results, "b_el")

    # generate results to be evaluated in tests
    comp_results = data["sequences"].sum(axis=0).to_dict()
    comp_results["pv_capacity"] = results[(pv, bel)]["scalars"].invest
    comp_results["wind_capacity"] = results[(wind, bel)]["scalars"].invest

    test_results = {
        (("wind", "b_el"), "flow"): 9239,
        (("pv", "b_el"), "flow"): 1147,
        (("b_el", "demand_elec"), "flow"): 7440,
        (("b_el", "excess_el"), "flow"): 6261,
        (("pp_chp", "b_el"), "flow"): 477,
        (("pp_lig", "b_el"), "flow"): 850,
        (("pp_gas", "b_el"), "flow"): 934,
        (("pp_coal", "b_el"), "flow"): 1256,
        (("pp_oil", "b_el"), "flow"): 0,
        (("b_el", "el_heat_pump"), "flow"): 202,
        "pv_capacity": 44,
        "wind_capacity": 246,
    }

    for key in test_results.keys():
        assert comp_results[key] == pytest.approx(test_results[key], abs=0.5)
