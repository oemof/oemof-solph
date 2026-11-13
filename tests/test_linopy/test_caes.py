# -*- coding: utf-8 -*-

"""Equivalence of the linopy and the Pyomo backend: the experimental
GenericCAES (MILP), based on tests/test_scripts/test_solph/
test_generic_caes.

SPDX-License-Identifier: MIT
"""

import os

import pandas as pd
import pytest

from oemof import solph
from oemof.solph.components.experimental import GenericCAES

pytest.importorskip("linopy")

import oemof.solph._linopy.builders.caes  # noqa: E402, F401

from .equivalence import assert_backends_agree  # noqa: E402

DATA = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "test_scripts",
    "test_solph",
    "test_generic_caes",
    "generic_caes.csv",
)

CONCEPT = {
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


def caes_system(n_steps=None, concept=None, second=None):
    """The CAES test system; optionally a second CAES with other
    parameters, so that the builder handles several nodes."""
    data = pd.read_csv(DATA)
    if n_steps is not None:
        data = data.iloc[:n_steps]

    def build():
        idx = pd.date_range("1/1/2017", periods=len(data), freq="h")
        es = solph.EnergySystem(timeindex=idx, infer_last_interval=True)
        bgas = solph.Bus(label="bgas")
        bel_source = solph.Bus(label="bel_source")
        bel_sink = solph.Bus(label="bel_sink")
        es.add(bgas, bel_source, bel_sink)
        es.add(
            solph.components.Source(
                label="rgas", outputs={bgas: solph.Flow(variable_costs=20)}
            ),
            solph.components.Source(
                label="source_el",
                outputs={
                    bel_source: solph.Flow(
                        variable_costs=data["price_el_source"].to_numpy()
                    )
                },
            ),
            solph.components.Sink(
                label="sink_el",
                inputs={
                    bel_sink: solph.Flow(
                        variable_costs=data["price_el_sink"].to_numpy()
                    )
                },
            ),
            GenericCAES(
                label="caes",
                electrical_input={bel_source: solph.Flow()},
                fuel_input={bgas: solph.Flow()},
                electrical_output={bel_sink: solph.Flow()},
                params=concept or CONCEPT,
            ),
        )
        if second is not None:
            es.add(
                GenericCAES(
                    label="caes 2",
                    electrical_input={bel_source: solph.Flow()},
                    fuel_input={bgas: solph.Flow()},
                    electrical_output={bel_sink: solph.Flow()},
                    params=second,
                )
            )
        return es

    return build


def test_generic_caes():
    assert_backends_agree(caes_system(), solver="highs", compare=("flow",))


def test_generic_caes_with_tes_and_two_plants():
    # thermal storage, heat shares, a lossy cavern and constant exergy
    # flows on a second plant
    second = dict(
        CONCEPT,
        cav_e_in_b=0.5,
        cav_e_out_b=0.2,
        cav_eta_temp=1.01,
        cav_level_max=150.0,
        cmp_q_tes_share=0.4,
        exp_q_tes_share=0.6,
        tes_level_max=50.0,
    )
    assert_backends_agree(
        caes_system(n_steps=72, second=second), solver="highs", compare=()
    )
