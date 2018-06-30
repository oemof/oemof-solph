# -*- coding: utf-8 -

"""Tests of the component module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose import tools
from oemof import solph


@tools.raises(AttributeError)
def test_generic_storage_1():
    """Duplicate definition inflow."""
    bel = solph.Bus()
    solph.components.GenericStorage(
        label='storage1',
        inputs={bel: solph.Flow(variable_costs=10e10)},
        outputs={bel: solph.Flow(variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        invest_relation_input_output=1,
        invest_relation_output_capacity=1,
        invest_relation_input_capacity=1,
        investment=solph.Investment(),
        inflow_conversion_factor=1, outflow_conversion_factor=0.8)


@tools.raises(AttributeError)
def test_generic_storage_2():
    """Nominal value defined with investment model."""
    bel = solph.Bus()
    solph.components.GenericStorage(
        label='storage3',
        nominal_capacity=45,
        inputs={bel: solph.Flow(variable_costs=10e10)},
        outputs={bel: solph.Flow(variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        invest_relation_input_capacity=1/6,
        invest_relation_output_capacity=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=solph.Investment(ep_costs=23))


def test_generic_storage_3():
    """Nominal value defined with investment model."""
    bel = solph.Bus()
    solph.components.GenericStorage(
        label='storage4',
        nominal_capacity=45,
        inputs={bel: solph.Flow(nominal_value=23, variable_costs=10e10)},
        outputs={bel: solph.Flow(nominal_value=7.5, variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8)
