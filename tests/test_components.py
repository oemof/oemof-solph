# -*- coding: utf-8 -

"""Tests of the component module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from nose import tools
from oemof import solph


# ********* GenericStorage *********

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


def test_generic_storage_with_old_parameters():
    deprecated = {
        'nominal_capacity': 45,
        'initial_capacity': 0,
        'capacity_loss': 0,
        'capacity_min': 0,
        'capacity_max': 0,
    }
    # Make sure an `AttributeError` is raised if we supply all deprecated
    # parameters.
    with tools.assert_raises(AttributeError) as caught:
        solph.components.GenericStorage(
            label='`GenericStorage` with all deprecated parameters',
            **deprecated
        )
    for parameter in deprecated:
        # Make sure every parameter used is mentioned in the exception's
        # message.
        assert parameter in str(caught.exception)
        # Make sure an `AttributeError` is raised for each deprecated parameter
        tools.assert_raises(
            AttributeError,
            solph.components.GenericStorage,
            **{
                "label": "`GenericStorage` with `{}`".format(parameter),
                parameter: deprecated[parameter],
            })


def test_generic_storage_with_non_convex_investment():
    """No NonConvexFlow for Inflow defined."""
    with tools.assert_raises_regexp(
            AttributeError, "Values for 'offset' and 'existing' are given"):
        bel = solph.Bus()
        solph.components.GenericStorage(
            label='storage4',
            inputs={bel: solph.Flow()},
            outputs={bel: solph.Flow()},
            invest_relation_input_capacity=1/6,
            invest_relation_output_capacity=1/6,
            investment=solph.Investment(nonconvex=True, existing=5))


# ********* OffsetTransformer *********

def test_offsettransformer_wrong_flow_type():
    """No NonConvexFlow for Inflow defined."""
    with tools.assert_raises_regexp(
            TypeError, 'Input flows must be of type NonConvexFlow!'):
        bgas = solph.Bus(label='gasBus')
        solph.components.OffsetTransformer(
            label='gasboiler',
            inputs={bgas: solph.Flow()},
            coefficients=(-17, 0.9))


def test_offsettransformer_not_enough_coefficients():
    with tools.assert_raises_regexp(
            ValueError,
            'Two coefficients or coefficient series have to be given.'):
        solph.components.OffsetTransformer(
            label='of1',
            coefficients=([1, 4, 7]))


def test_offsettransformer_too_many_coefficients():
    with tools.assert_raises_regexp(
            ValueError,
            'Two coefficients or coefficient series have to be given.'):
        solph.components.OffsetTransformer(
            label='of2',
            coefficients=(1, 4, 7))


def test_offsettransformer_empty():
    """No NonConvexFlow for Inflow defined."""
    solph.components.OffsetTransformer()


def test_offsettransformer__too_many_input_flows():
    """Too many Input Flows defined."""
    with tools.assert_raises_regexp(
            ValueError, 'OffsetTransformer` must not have more than 1'):
        bgas = solph.Bus(label='GasBus')
        bcoal = solph.Bus(label='CoalBus')
        solph.components.OffsetTransformer(
            label='ostf_2_in',
            inputs={
                bgas: solph.Flow(
                    nominal_value=60, min=0.5, max=1.0,
                    nonconvex=solph.NonConvex()),
                bcoal: solph.Flow(
                    nominal_value=30, min=0.3, max=1.0,
                    nonconvex=solph.NonConvex())
            },
            coefficients=(20, 0.5))


def test_offsettransformer_too_many_output_flows():
    """Too many Output Flows defined."""
    with tools.assert_raises_regexp(
            ValueError, 'OffsetTransformer` must not have more than 1'):
        bm1 = solph.Bus(label='my_offset_Bus1')
        bm2 = solph.Bus(label='my_offset_Bus2')

        solph.components.OffsetTransformer(
            label='ostf_2_out',
            inputs={
                bm1: solph.Flow(
                    nominal_value=60, min=0.5, max=1.0,
                    nonconvex=solph.NonConvex())
            },
            outputs={bm1: solph.Flow(),
                     bm2: solph.Flow()},
            coefficients=(20, 0.5))
