# -*- coding: utf-8 -*-
"""
Example that illustrates how to use component `GenericCHP` can be used.

In this case it is used to model a combined cycle extraction turbine.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_generic_caes/test_generic_caes.py

SPDX-License-Identifier: MIT
"""

import os

import pandas as pd
import pytest

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import processing
from oemof.solph import views
from oemof.solph.buses import Bus
from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.components.experimental import GenericCAES
from oemof.solph.flows import Flow


def test_gen_caes():
    # read sequence data
    full_filename = os.path.join(os.path.dirname(__file__), "generic_caes.csv")
    data = pd.read_csv(full_filename)

    # select periods
    periods = len(data)

    # create an energy system
    idx = pd.date_range("1/1/2017", periods=periods, freq="h")
    es = EnergySystem(timeindex=idx, infer_last_interval=True)

    # resources
    bgas = Bus(label="bgas")
    es.add(bgas)

    es.add(Source(label="rgas", outputs={bgas: Flow(variable_costs=20)}))

    # power
    bel_source = Bus(label="bel_source")
    es.add(bel_source)
    es.add(
        Source(
            label="source_el",
            outputs={bel_source: Flow(variable_costs=data["price_el_source"])},
        )
    )

    bel_sink = Bus(label="bel_sink")
    es.add(bel_sink)
    es.add(
        Sink(
            label="sink_el",
            inputs={bel_sink: Flow(variable_costs=data["price_el_sink"])},
        )
    )

    # dictionary with parameters for a specific CAES plant
    # based on thermal modelling and linearization techniques
    concept = {
        "cav_e_in_b": 0,
        "cav_e_in_m": 0.6457267578,
        "cav_e_out_b": 0,
        "cav_e_out_m": 0.3739636077,
        "cav_eta_temp": 1.0,
        "cav_level_max": 211.11,
        "cmp_p_max_b": 86.0918959849,
        "cmp_p_max_m": 0.0679999932,
        "cmp_p_min": 1,
        "cmp_q_out_b": -19.3996965679,
        "cmp_q_out_m": 1.1066036114,
        "cmp_q_tes_share": 0,
        "exp_p_max_b": 46.1294016678,
        "exp_p_max_m": 0.2528340303,
        "exp_p_min": 1,
        "exp_q_in_b": -2.2073411014,
        "exp_q_in_m": 1.129249765,
        "exp_q_tes_share": 0,
        "tes_eta_temp": 1.0,
        "tes_level_max": 0.0,
    }

    # generic compressed air energy storage (caes) plant
    es.add(
        GenericCAES(
            label="caes",
            electrical_input={bel_source: Flow()},
            fuel_input={bgas: Flow()},
            electrical_output={bel_sink: Flow()},
            params=concept,
        )
    )

    # create an optimization problem and solve it
    om = Model(es)

    # solve model
    om.solve(solver="cbc")

    # create result object
    results = processing.results(om)

    data = (
        views.node(results, "caes", keep_none_type=True)["sequences"]
        .sum(axis=0)
        .to_dict()
    )

    test_dict = {
        (("caes", None), "cav_level"): 25658.82964382,
        (("caes", None), "exp_p"): 5020.801997000007,
        (("caes", None), "exp_q_fuel_in"): 5170.880360999999,
        (("caes", None), "tes_e_out"): 0.0,
        (("caes", None), "exp_st"): 226.0,
        (("bgas", "caes"), "flow"): 5170.880360999999,
        (("caes", None), "cav_e_out"): 1877.5972265299995,
        (("caes", None), "exp_p_max"): 17512.352336,
        (("caes", None), "cmp_q_waste"): 2499.9125993000007,
        (("caes", None), "cmp_p"): 2907.7271520000004,
        (("caes", None), "exp_q_add_in"): 0.0,
        (("caes", None), "cmp_st"): 37.0,
        (("caes", None), "cmp_q_out_sum"): 2499.9125993000007,
        (("caes", None), "tes_level"): 0.0,
        (("caes", None), "tes_e_in"): 0.0,
        (("caes", None), "exp_q_in_sum"): 5170.880360999999,
        (("caes", None), "cmp_p_max"): 22320.76334300001,
        (("caes", "bel_sink"), "flow"): 5020.801997000007,
        (("bel_source", "caes"), "flow"): 2907.7271520000004,
        (("caes", None), "cav_e_in"): 1877.597226,
    }

    for key in test_dict.keys():
        assert data[key] == pytest.approx(test_dict[key])
