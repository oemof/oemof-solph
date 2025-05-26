# -*- coding: utf-8 -

"""Test the definition of the time index of the model.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>

SPDX-License-Identifier: MIT
"""
import datetime
import random

import pandas as pd
import pytest

from oemof import solph
from oemof.solph import EnergySystem
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import flows

def _setup_energy_system(dtindex, timeincrement=None):
    es = EnergySystem(
        timeindex=dtindex,
        timeincrement=timeincrement,
        infer_last_interval=False,
    )

    # BUSSES
    b_el1 = buses.Bus(label="b_el1")
    b_diesel = buses.Bus(label="b_diesel", balanced=False)
    es.add(b_el1, b_diesel)

    # TEST DIESEL:
    dg = cmp.Converter(
        label="diesel_generator",
        inputs={b_diesel: flows.Flow(variable_costs=2)},
        outputs={
            b_el1: flows.Flow(
                variable_costs=1, nominal_capacity=Investment(ep_costs=500)
            )
        },
        conversion_factors={b_el1: 0.5},
    )

    batt = cmp.GenericStorage(
        label="storage",
        nominal_capacity=1000,
        inputs={b_el1: flows.Flow(variable_costs=3)},
        outputs={b_el1: flows.Flow(variable_costs=2.5)},
        loss_rate=0.00,
        invest_relation_input_capacity=1 / 6,
        invest_relation_output_capacity=1 / 6,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.9,
    )

    random.seed(1)
    demand_values = random.sample(range(40, 120), 72)
    demand = cmp.Sink(
        label="demand_el",
        inputs={
            b_el1: flows.Flow(
                nominal_capacity=1,
                fix=demand_values,
            )
        },
    )
    es.add(dg, batt, demand)

    return es

class TestParameterResult:
    @classmethod
    def setup_class(cls):
        dtindex1 = pd.date_range("1/1/2012", periods=24, freq="h")
        dtindex2 = pd.date_range("1/2/2012", periods=49, freq="30min")
        dtindex = dtindex1.union(dtindex2)
        es = _setup_energy_system(dtindex)
        model = Model(es)
        model.receive_duals()
        model.solve()
        results = solph.Results(model)
        cls.flows = results["flow"]
        cls.storage_content = results["storage_content"]
        cls.es = es
        cls.model = model

    def test_timesteps_timeincrements_with_storage_charging(self):

        assert (
            self.storage_content.iloc[0] == self.storage_content.iloc[-1]
        ).all()

        charge = self.flows[(self.es.node["b_el1"], self.es.node["storage"])]
        # Calculate the next storage content and verify it with the storage
        # content of the results (charging).
        # Charging - timestep (ts) with its timeincrement (ti)
        time = [(23, 1), (24, 0.5)]
        for ts, ti in time:
            content_manual = self.storage_content.iloc[ts, 0] + charge.iloc[
                ts
            ] * ti
            content_model = self.storage_content.iloc[ts + 1, 0]
            assert content_manual == pytest.approx(content_model)
            assert self.es.timeincrement[ts] == ti

    def test_timesteps_timeincrements_with_storage_discharging(self):
        # Storage content at the last time point is equal to the content of
        # the first time point because the storage is balanced.
        assert (
            self.storage_content.iloc[0] == self.storage_content.iloc[-1]
        ).all()

        discharge = self.flows[
            (self.es.node["storage"], self.es.node["b_el1"])
        ]

        # Calculate the next storage content and verify it with the storage
        # content of the results (discharging).
        # Discharging - timestep (ts) with its timeincrement (ti)
        time = [(7, 1), (40, 0.5)]

        for ts, ti in time:
            content_manual = (
                self.storage_content.iloc[ts, 0]
                - (discharge.iloc[ts] + (discharge.iloc[ts] * 1 / 9)) * ti
            )
            content_model = self.storage_content.iloc[ts + 1, 0]
            assert content_manual == pytest.approx(content_model)
            assert self.es.timeincrement[ts] == ti

    def test_timeincrements(self):
        assert self.es.timeincrement.sum() == 48

    def test_time_index_with_last_time_point(self):
        storage_content = self.storage_content[self.es.node["storage"]]
        assert storage_content.iloc[0] == storage_content.iloc[-1]

        charge = self.flows[(self.es.node["b_el1"], self.es.node["storage"])]
        assert storage_content.index[0] == datetime.datetime(
            2012, 1, 1, 0, 0, 0
        )
        assert charge.index[0] == datetime.datetime(2012, 1, 1, 0, 0, 0)
        assert storage_content.index[-1] == datetime.datetime(
            2012, 1, 3, 0, 0, 0
        )
        assert charge.index[-1] == datetime.datetime(2012, 1, 2, 23, 30, 0)


def test_numeric_index():
    es = _setup_energy_system(dtindex=None, timeincrement=24 * [1]+ 48 * [0.5])

    model = Model(es)
    model.receive_duals()
    model.solve()
    results = solph.Results(model)
    flow = results["flow"]

    assert flow.index[0] == 0
    assert flow.index[-1] == pytest.approx(47.5)
    assert len(flow) == 72

    storage_content = results["storage_content"]
    assert (storage_content.iloc[0] == storage_content.iloc[-1]).all()
    assert len(storage_content) == 73

    charge = flow[(es.node["b_el1"], es.node["storage"])]
    # Calculate the next storage content and verify it with the storage
    # content of the results (charging).
    # Charging - timestep (ts) with its timeincrement (ti)
    time = [(23, 1), (24, 0.5)]
    for ts, ti in time:
        content_manual = storage_content.iloc[ts, 0] + charge.iloc[
            ts
        ] * ti
        content_model = storage_content.iloc[ts + 1, 0]
        assert content_manual == pytest.approx(content_model)
        assert es.timeincrement[ts] == ti
