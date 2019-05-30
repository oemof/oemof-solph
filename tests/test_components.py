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
        loss_rate=0.00, initial_storage_level=0,
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
        nominal_storage_capacity=45,
        inputs={bel: solph.Flow(variable_costs=10e10)},
        outputs={bel: solph.Flow(variable_costs=10e10)},
        loss_rate=0.00, initial_storage_level=0,
        invest_relation_input_capacity=1/6,
        invest_relation_output_capacity=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=solph.Investment(ep_costs=23))


def test_generic_storage_3():
    """Nominal value defined with investment model."""
    bel = solph.Bus()
    solph.components.GenericStorage(
        label='storage4',
        nominal_storage_capacity=45,
        inputs={bel: solph.Flow(nominal_value=23, variable_costs=10e10)},
        outputs={bel: solph.Flow(nominal_value=7.5, variable_costs=10e10)},
        loss_rate=0.00, initial_storage_level=0,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8)


def test_offsettransformer_wrong_flow_type():
    """No NonConvexFlow for Inflow defined."""
    with tools.assert_raises_regexp(
            TypeError, 'Input flows must be of type NonConvexFlow!'):
        bgas = solph.Bus(label='gasBus')
        bth = solph.Bus(label='thermalBus')
        solph.components.OffsetTransformer(
            label='gasboiler',
            inputs={bgas: solph.Flow(
                nominal_value=100,
                max=1,
                min=0.32,
            )},
            outputs={bth: solph.Flow()},
            coefficients=[-17, 0.9])


def test_offsettransformer__too_many_input_flows():
    """Too many Input Flows defined."""
    with tools.assert_raises_regexp(
            ValueError, 'OffsetTransformer` must not have more than 1'):
        bgas = solph.Bus(label='GasBus')
        bcoal = solph.Bus(label='CoalBus')
        bel = solph.Bus(label='ElectricityBus')
        solph.components.OffsetTransformer(
            label='ostf',
            inputs={
                bgas: solph.Flow(
                    nominal_value=60, min=0.5, max=1.0,
                    nonconvex=solph.NonConvex()),
                bcoal: solph.Flow(
                    nominal_value=30, min=0.3, max=1.0,
                    nonconvex=solph.NonConvex())
            },
            outputs={bel: solph.Flow()},
            coefficients=(20, 0.5))


def test_offsettransformer_too_many_output_flows():
    """Too many Output Flows defined."""
    with tools.assert_raises_regexp(
            ValueError, 'OffsetTransformer` must not have more than 1'):
        bgas = solph.Bus(label='GasBus')
        bth = solph.Bus(label='CoalBus')
        bel = solph.Bus(label='ElectricityBus')
        solph.components.OffsetTransformer(
            label='ostf',
            inputs={
                bgas: solph.Flow(
                    nominal_value=60, min=0.5, max=1.0,
                    nonconvex=solph.NonConvex())
            },
            outputs={bel: solph.Flow(),
                     bth: solph.Flow()},
            coefficients=(20, 0.5))
