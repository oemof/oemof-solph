# -*- coding: utf-8 -

"""Test the definition of the time index of the model.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>

SPDX-License-Identifier: MIT
"""
import datetime
import random

import pandas as pd
import pytest

from oemof.solph import EnergySystem
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import flows
from oemof.solph import processing


class TestParameterResult:
    @classmethod
    def setup_class(cls):
        dtindex1 = pd.date_range("1/1/2012", periods=24, freq="h")
        dtindex2 = pd.date_range("1/2/2012", periods=49, freq="30min")
        dtindex = dtindex1.union(dtindex2)
        es = EnergySystem(timeindex=dtindex, infer_last_interval=False)

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
        model = Model(es)
        model.receive_duals()
        model.solve()
        results = processing.results(model, remove_last_time_point=False)
        cls.flows = {k: v for k, v in results.items() if k[1] is not None}
        cls.comp = {k: v for k, v in results.items() if k[1] is None}
        cls.es = es
        cls.model = model

    def test_timesteps_timeincrements_with_storage_charging(self):
        storage_content = [
            v["sequences"]["storage_content"]
            for k, v in self.comp.items()
            if k[0].label == "storage"
        ][0]
        assert storage_content.iloc[0] == storage_content.iloc[-1]

        charge = [
            v["sequences"]["flow"]
            for k, v in self.flows.items()
            if k[1].label == "storage"
        ][0]
        # Calculate the next storage content and verify it with the storage
        # content of the results (charging).
        # Charging - timestep (ts) with its timeincrement (ti)
        time = [(23, 1), (24, 0.5)]
        for ts, ti in time:
            assert storage_content.iloc[ts] + charge.iloc[
                ts
            ] * ti == pytest.approx(storage_content.iloc[ts + 1])
            assert self.es.timeincrement[ts] == ti
        assert charge.isnull().any()

    def test_timesteps_timeincrements_with_storage_discharging(self):
        storage_content = [
            v["sequences"]["storage_content"]
            for k, v in self.comp.items()
            if k[0].label == "storage"
        ][0]
        # Storage content at the last time point is equal to the content of
        # the first time point because the storage is balanced.
        assert storage_content.iloc[0] == storage_content.iloc[-1]

        discharge = [
            v["sequences"]["flow"]
            for k, v in self.flows.items()
            if k[0].label == "storage"
        ][0]

        # Calculate the next storage content and verify it with the storage
        # content of the results (discharging).
        # Discharging - timestep (ts) with its timeincrement (ti)
        time = [(7, 1), (40, 0.5)]
        for ts, ti in time:
            assert (
                storage_content.iloc[ts]
                - (discharge.iloc[ts] + (discharge.iloc[ts] * 1 / 9)) * ti
            ) == pytest.approx(storage_content.iloc[ts + 1])
            assert self.es.timeincrement[ts] == ti

    def test_timeincrements(self):
        assert self.es.timeincrement.sum() == 48

    def test_without_last_time_point(self):
        results = processing.results(self.model, remove_last_time_point=True)
        flow = {k: v for k, v in results.items() if k[1] is not None}
        comp = {k: v for k, v in results.items() if k[1] is None}
        storage_content = [
            v["sequences"]["storage_content"]
            for k, v in comp.items()
            if k[0].label == "storage"
        ][0]
        charge = [
            v["sequences"]["flow"]
            for k, v in flow.items()
            if k[1].label == "storage"
        ][0]
        # The first and the last value are not the same because the last value
        # of the storage is missing. Adding the charging of the last time step
        # will result the final storage content, which is equal to the first
        assert storage_content.iloc[0] != storage_content.iloc[-1]
        assert (
            storage_content.iloc[0]
            == storage_content.iloc[-1] + charge.iloc[-1] / 2
        )
        assert not charge.isnull().any()
        assert storage_content.index[0] == datetime.datetime(
            2012, 1, 1, 0, 0, 0
        )
        assert charge.index[0] == datetime.datetime(2012, 1, 1, 0, 0, 0)
        assert storage_content.index[-1] == datetime.datetime(
            2012, 1, 2, 23, 30, 0
        )
        assert charge.index[-1] == datetime.datetime(2012, 1, 2, 23, 30, 0)

    def test_time_index_with_last_time_point(self):
        storage_content = [
            v["sequences"]["storage_content"]
            for k, v in self.comp.items()
            if k[0].label == "storage"
        ][0]
        assert storage_content.iloc[0] == storage_content.iloc[-1]

        charge = [
            v["sequences"]["flow"]
            for k, v in self.flows.items()
            if k[1].label == "storage"
        ][0]
        assert storage_content.index[0] == datetime.datetime(
            2012, 1, 1, 0, 0, 0
        )
        assert charge.index[0] == datetime.datetime(2012, 1, 1, 0, 0, 0)
        assert storage_content.index[-1] == datetime.datetime(
            2012, 1, 3, 0, 0, 0
        )
        assert charge.index[-1] == datetime.datetime(2012, 1, 3, 0, 0, 0)

    def test_numeric_index(self):
        self.es.timeindex = None
        model = Model(self.es)
        model.receive_duals()
        model.solve()
        results = processing.results(self.model)
        flow = {k: v for k, v in results.items() if k[1] is not None}
        diesel_generator_out = [
            v["sequences"]["flow"]
            for k, v in flow.items()
            if k[0].label == "diesel_generator"
        ][0]
        assert diesel_generator_out.index[0] == 0
        assert diesel_generator_out.index[-1] == 72
        assert len(diesel_generator_out.index) == 73

        storage_content = [
            v["sequences"]["storage_content"]
            for k, v in self.comp.items()
            if k[0].label == "storage"
        ][0]
        assert storage_content.iloc[0] == storage_content.iloc[-1]

        charge = [
            v["sequences"]["flow"]
            for k, v in self.flows.items()
            if k[1].label == "storage"
        ][0]
        # Calculate the next storage content and verify it with the storage
        # content of the results (charging).
        # Charging - timestep (ts) with its timeincrement (ti)
        time = [(23, 1), (24, 0.5)]
        for ts, ti in time:
            assert (
                storage_content.iloc[ts] + charge.iloc[ts] * ti
            ) == pytest.approx(storage_content.iloc[ts + 1])
            assert self.es.timeincrement[ts] == ti
        assert charge.isnull().any()
