# -*- coding: utf-8 -

"""Tests of the component module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import warnings
from nose import tools
from oemof.solph import Bus, components, Flow, Investment, NonConvex
from oemof.tools.debugging import SuspiciousUsageWarning


# ********* GenericStorage *********

@tools.raises(AttributeError)
def test_generic_storage_1():
    """Duplicate definition inflow."""
    bel = Bus()
    components.GenericStorage(
        label='storage1',
        inputs={bel: Flow(variable_costs=10e10)},
        outputs={bel: Flow(variable_costs=10e10)},
        loss_rate=0.00, initial_storage_level=0,
        invest_relation_input_output=1,
        invest_relation_output_capacity=1,
        invest_relation_input_capacity=1,
        investment=Investment(),
        inflow_conversion_factor=1, outflow_conversion_factor=0.8)


@tools.raises(AttributeError)
def test_generic_storage_2():
    """Nominal value defined with investment model."""
    bel = Bus()
    components.GenericStorage(
        label='storage3',
        nominal_storage_capacity=45,
        inputs={bel: Flow(variable_costs=10e10)},
        outputs={bel: Flow(variable_costs=10e10)},
        loss_rate=0.00, initial_storage_level=0,
        invest_relation_input_capacity=1/6,
        invest_relation_output_capacity=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=Investment(ep_costs=23))


def test_generic_storage_3():
    """Nominal value defined with investment model."""
    bel = Bus()
    components.GenericStorage(
        label='storage4',
        nominal_storage_capacity=45,
        inputs={bel: Flow(nominal_value=23, variable_costs=10e10)},
        outputs={bel: Flow(nominal_value=7.5, variable_costs=10e10)},
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
        components.GenericStorage(
            label='`GenericStorage` with all deprecated parameters',
            **deprecated
        )
    for parameter in deprecated:
        # Make sure every parameter used is mentioned in the exception's
        # message.
        assert parameter in str(caught.exception)
        # Make sure an `AttributeError` is raised for each deprecated
        # parameter.
        tools.assert_raises(
            AttributeError,
            components.GenericStorage,
            **{
                "label": "`GenericStorage` with `{}`".format(parameter),
                parameter: deprecated[parameter],
            }
        )


def test_generic_storage_with_invest_and_fixed_losses_absolute():
    """
    Storage with fixed losses in the investment mode but no minimum or existing
    value is set an AttributeError is raised because this may result in storage
    with zero capacity but fixed losses.
    """
    msg = ("With fixed_losses_absolute > 0, either investment.existing or"
           " investment.minimum has to be non-zero.")
    with tools.assert_raises_regexp(AttributeError, msg):
        bel = Bus()
        components.GenericStorage(
            label='storage4',
            inputs={bel: Flow()},
            outputs={bel: Flow()},
            investment=Investment(ep_costs=23, minimum=0, existing=0),
            fixed_losses_absolute=[0, 0, 4],
            )


# ********* OffsetTransformer *********

def test_offsettransformer_wrong_flow_type():
    """No NonConvexFlow for Inflow defined."""
    with tools.assert_raises_regexp(
            TypeError, 'Input flows must be of type NonConvexFlow!'):
        bgas = Bus(label='gasBus')
        components.OffsetTransformer(
            label='gasboiler',
            inputs={bgas: Flow()},
            coefficients=(-17, 0.9))


def test_offsettransformer_not_enough_coefficients():
    with tools.assert_raises_regexp(
            ValueError,
            'Two coefficients or coefficient series have to be given.'):
        components.OffsetTransformer(
            label='of1',
            coefficients=([1, 4, 7]))


def test_offsettransformer_too_many_coefficients():
    with tools.assert_raises_regexp(
            ValueError,
            'Two coefficients or coefficient series have to be given.'):
        components.OffsetTransformer(
            label='of2',
            coefficients=(1, 4, 7))


def test_offsettransformer_empty():
    """No NonConvexFlow for Inflow defined."""
    components.OffsetTransformer()


def test_offsettransformer__too_many_input_flows():
    """Too many Input Flows defined."""
    with tools.assert_raises_regexp(
            ValueError, 'OffsetTransformer` must not have more than 1'):
        bgas = Bus(label='GasBus')
        bcoal = Bus(label='CoalBus')
        components.OffsetTransformer(
            label='ostf_2_in',
            inputs={
                bgas: Flow(
                    nominal_value=60, min=0.5, max=1.0,
                    nonconvex=NonConvex()),
                bcoal: Flow(
                    nominal_value=30, min=0.3, max=1.0,
                    nonconvex=NonConvex())
            },
            coefficients=(20, 0.5))


def test_offsettransformer_too_many_output_flows():
    """Too many Output Flows defined."""
    with tools.assert_raises_regexp(
            ValueError, 'OffsetTransformer` must not have more than 1'):
        bm1 = Bus(label='my_offset_Bus1')
        bm2 = Bus(label='my_offset_Bus2')

        components.OffsetTransformer(
            label='ostf_2_out',
            inputs={
                bm1: Flow(
                    nominal_value=60, min=0.5, max=1.0,
                    nonconvex=NonConvex())
            },
            outputs={bm1: Flow(),
                     bm2: Flow()},
            coefficients=(20, 0.5))


# ********* GenericCHP *********
def test_generic_chp_without_warning():
    warnings.filterwarnings("error", category=SuspiciousUsageWarning)
    bel = Bus(label='electricityBus')
    bth = Bus(label='heatBus')
    bgas = Bus(label='commodityBus')
    components.GenericCHP(
       label='combined_cycle_extraction_turbine',
       fuel_input={bgas: Flow(
           H_L_FG_share_max=[0.183])},
       electrical_output={bel: Flow(
           P_max_woDH=[155.946],
           P_min_woDH=[68.787],
           Eta_el_max_woDH=[0.525],
           Eta_el_min_woDH=[0.444])},
       heat_output={bth: Flow(
           Q_CW_min=[10.552])},
       Beta=[0.122], back_pressure=False)
    warnings.filterwarnings("always", category=SuspiciousUsageWarning)
