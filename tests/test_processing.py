# -*- coding: utf-8 -

"""Tests the processing module of the outputlib.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_processing.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose.tools import eq_
import pandas
from oemof.solph import (
    EnergySystem, Bus, Transformer, Flow, Investment, Sink, Model)
from oemof.solph.components import GenericStorage
from oemof.outputlib import processing


class Parameter_Result_Tests:
    @classmethod
    def setUpClass(cls):
        cls.period = 2
        cls.es = EnergySystem(
            timeindex=pandas.date_range(
                '2016-01-01',
                periods=cls.period,
                freq='H'
            )
        )

        # BUSSES
        b_el1 = Bus(label="b_el1")
        b_el2 = Bus(label="b_el2")
        b_diesel = Bus(label='b_diesel', balanced=False)
        cls.es.add(b_el1, b_el2, b_diesel)

        # TEST DIESEL:
        dg = Transformer(
            label='diesel',
            inputs={b_diesel: Flow(variable_costs=2)},
            outputs={
                b_el1: Flow(
                    variable_costs=1,
                    investment=Investment(ep_costs=0.5)
                )
            },
            conversion_factors={b_el1: 2},
        )

        batt = GenericStorage(
            label='storage',
            inputs={b_el1: Flow(variable_costs=3)},
            outputs={b_el2: Flow(variable_costs=2.5)},
            capacity_loss=0.00,
            initial_capacity=0,
            invest_relation_input_capacity=1/6,
            invest_relation_output_capacity=1/6,
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.8,
            fixed_costs=35,
            investment=Investment(ep_costs=0.4),
        )

        cls.demand_values = [0.0, 100]
        demand = Sink(
            label="demand_el",
            inputs={
                b_el2: Flow(
                    nominal_value=1,
                    actual_value=cls.demand_values,
                    fixed=True
                )
            }
        )
        cls.es.add(dg, batt, demand)
        cls.om = Model(cls.es)
        cls.om.solve()

    def test_flows_with_none_exclusion(self):
        b_el2 = self.es.groups['b_el2']
        demand = self.es.groups['demand_el']
        param_results = processing.param_results(self.es, exclude_none=True)
        eq_(
            param_results[(b_el2, demand)]['scalars'],
            {
                'nominal_value': 1,
                'fixed': True,
                'negative_gradient_costs': 0,
                'positive_gradient_costs': 0,
                'max': 1,
                'min': 0,
                'variable_costs': 0
            }
        )
        eq_(
            param_results[(b_el2, demand)]['sequences'],
            {
                'actual_value': self.demand_values
            }
        )

    def test_flows_without_none_exclusion(self):
        b_el2 = self.es.groups['b_el2']
        demand = self.es.groups['demand_el']
        param_results = processing.param_results(self.om, exclude_none=False)
        scalar_attributes = {
            'nominal_value': 1,
            'fixed': True,
            'negative_gradient_costs': 0,
            'positive_gradient_costs': 0,
            'max': 1,
            'min': 0,
            'variable_costs': 0,
            'positive_gradient_ub': None,
            'negative_gradient_ub': None,
            'flow': None,
            'values': None,
        }
        default_scalars = [
            'nominal_value', 'summed_max', 'summed_min',
            'investment', 'nonconvex', 'integer', 'fixed'
        ]
        for attr in default_scalars:
            if attr not in scalar_attributes:
                scalar_attributes[attr] = None
        eq_(
            param_results[(b_el2, demand)]['scalars'],
            scalar_attributes
        )
        sequences_attributes = {
            'actual_value': self.demand_values,
        }
        default_sequences = [
            'actual_value'
        ]
        for attr in default_sequences:
            if attr not in sequences_attributes:
                sequences_attributes[attr] = [None]
        eq_(
            param_results[(b_el2, demand)]['sequences'],
            sequences_attributes
        )
    
    def test_nodes_with_none_exclusion(self):
        param_results = processing.param_results(
            self.om, exclude_none=True, keys_as_str=True)
        eq_(
            param_results[('storage', 'None')]['scalars'],
            {
                'label': 'storage',
                'initial_capacity': 0,
                'invest_relation_output_capacity': 1/6,
                'invest_relation_input_capacity': 1/6,
                'investment_ep_costs': 0.4,
                'investment_maximum': float('inf'),
                'investment_minimum': 0,
                'investment_existing': 0,
                'capacity_loss': 0,
                'capacity_min': 0,
                'capacity_max': 1,
                'inflow_conversion_factor': 1,
                'outflow_conversion_factor': 0.8,
            }
        )
        eq_(
            param_results[('storage', 'None')]['sequences'],
            {}
        )

    def test_nodes_without_none_exclusion(self):
        diesel = self.es.groups['diesel']
        param_results = processing.param_results(
            self.om, exclude_none=False)
        eq_(
            param_results[(diesel, None)]['scalars'],
            {
                'label': 'diesel',
                'conversion_factors_b_el1': 2,
                'conversion_factors_b_diesel': 1,
            }
        )
        eq_(
            param_results[(diesel, None)]['sequences'],
            {}
        )
