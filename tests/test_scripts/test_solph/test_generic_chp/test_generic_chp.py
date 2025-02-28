# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `GenericCHP` can be used.

In this case it is used to model a combined cycle extraction turbine.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_generic_chp/test_generic_chp.py

SPDX-License-Identifier: MIT
"""

import os

import pandas as pd
import pytest

from oemof import solph as solph
from oemof.solph import processing
from oemof.solph import views


def test_gen_chp():
    # read sequence data
    full_filename = os.path.join(os.path.dirname(__file__), "ccet.csv")
    data = pd.read_csv(full_filename)

    # select periods
    periods = len(data)

    # create an energy system
    idx = pd.date_range("1/1/2017", periods=periods, freq="h")
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=True)

    # resources
    bgas = solph.buses.Bus(label="bgas")
    es.add(bgas)

    es.add(
        solph.components.Source(
            label="rgas", outputs={bgas: solph.flows.Flow()}
        )
    )

    # heat
    bth = solph.buses.Bus(label="bth")
    es.add(bth)

    es.add(
        solph.components.Source(
            label="source_th",
            outputs={bth: solph.flows.Flow(variable_costs=1000)},
        )
    )

    es.add(
        solph.components.Sink(
            label="demand_th",
            inputs={
                bth: solph.flows.Flow(
                    fix=data["demand_th"], nominal_capacity=200
                )
            },
        )
    )

    # power
    bel = solph.buses.Bus(label="bel")
    es.add(bel)

    es.add(
        solph.components.Sink(
            label="demand_el",
            inputs={bel: solph.flows.Flow(variable_costs=data["price_el"])},
        )
    )

    # generic chp
    # (for back pressure characteristics Q_CW_min=0 and back_pressure=True)
    es.add(
        solph.components.GenericCHP(
            label="combined_cycle_extraction_turbine",
            fuel_input={
                bgas: solph.flows.Flow(
                    custom_attributes={
                        "H_L_FG_share_max": data["H_L_FG_share_max"]
                    }
                )
            },
            electrical_output={
                bel: solph.flows.Flow(
                    custom_attributes={
                        "P_max_woDH": data["P_max_woDH"],
                        "P_min_woDH": data["P_min_woDH"],
                        "Eta_el_max_woDH": data["Eta_el_max_woDH"],
                        "Eta_el_min_woDH": data["Eta_el_min_woDH"],
                    }
                )
            },
            heat_output={
                bth: solph.flows.Flow(
                    custom_attributes={"Q_CW_min": data["Q_CW_min"]}
                )
            },
            beta=data["beta"],
            back_pressure=False,
        )
    )

    # create an optimization problem and solve it
    om = solph.Model(es)

    # solve model
    om.solve(solver="cbc")

    # create result object
    results = processing.results(om)

    data = views.node(results, "bth")["sequences"].sum(axis=0).to_dict()

    test_dict = {
        (("bth", "demand_th"), "flow"): 20000.0,
        (("combined_cycle_extraction_turbine", "bth"), "flow"): 14070.15215799,
        (("source_th", "bth"), "flow"): 5929.8478649200015,
    }

    for key in test_dict.keys():
        assert data[key] == pytest.approx(test_dict[key])
