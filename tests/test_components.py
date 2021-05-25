# -*- coding: utf-8 -

"""Tests of the component module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import warnings

import pytest
from oemof.solph import Bus
from oemof.solph import Flow
from oemof.solph import Investment
from oemof.solph import NonConvex
from oemof.solph import components
from oemof.tools.debugging import SuspiciousUsageWarning

# ********* GenericStorage *********


def test_generic_storage_1():
    """Duplicate definition inflow."""
    bel = Bus()
    with pytest.raises(AttributeError, match="Overdetermined."):
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


def test_generic_storage_2():
    """Nominal value defined with investment model."""
    bel = Bus()
    with pytest.raises(AttributeError, match="If an investment object"):
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
    with pytest.raises(AttributeError) as caught:
        components.GenericStorage(
            label='`GenericStorage` with all deprecated parameters',
            **deprecated
        )
    for parameter in deprecated:
        # Make sure every parameter used is mentioned in the exception's
        # message.
        assert parameter in str(caught.value)
        # Make sure an `AttributeError` is raised for each deprecated
        # parameter.
        pytest.raises(
            AttributeError,
            components.GenericStorage,
            **{
                "label": "`GenericStorage` with `{}`".format(parameter),
                parameter: deprecated[parameter],
            })


def test_generic_storage_with_non_convex_investment():
    """Tests error if `offset` and `existing` attribute are given."""
    with pytest.raises(
            AttributeError,
            match=r"Values for 'offset' and 'existing' are given"):
        bel = Bus()
        components.GenericStorage(
            label='storage4',
            inputs={bel: Flow()},
            outputs={bel: Flow()},
            invest_relation_input_capacity=1/6,
            invest_relation_output_capacity=1/6,
            investment=Investment(nonconvex=True, existing=5, maximum=25))


def test_generic_storage_with_non_convex_invest_maximum():
    """No investment maximum at nonconvex investment."""
    with pytest.raises(
            AttributeError,
            match=r"Please provide an maximum investment value"):
        bel = Bus()
        components.GenericStorage(
            label='storage6',
            inputs={bel: Flow()},
            outputs={bel: Flow()},
            invest_relation_input_capacity=1/6,
            invest_relation_output_capacity=1/6,
            investment=Investment(nonconvex=True))


def test_generic_storage_with_convex_invest_offset():
    """Offset value is given and nonconvex is False."""
    with pytest.raises(
            AttributeError, match=r"If `nonconvex` is `False`, the `offset`"):
        bel = Bus()
        components.GenericStorage(
            label='storage6',
            inputs={bel: Flow()},
            outputs={bel: Flow()},
            invest_relation_input_capacity=1/6,
            invest_relation_output_capacity=1/6,
            investment=Investment(offset=10))


def test_generic_storage_with_invest_and_fixed_losses_absolute():
    """
    Storage with fixed losses in the investment mode but no minimum or existing
    value is set an AttributeError is raised because this may result in storage
    with zero capacity but fixed losses.
    """
    msg = (r"With fixed_losses_absolute > 0, either investment.existing or"
           " investment.minimum has to be non-zero.")
    with pytest.raises(AttributeError, match=msg):
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
    with pytest.raises(
            TypeError, match=r'Input flows must be of type NonConvexFlow!'):
        bgas = Bus(label='gasBus')
        components.OffsetTransformer(
            label='gasboiler',
            inputs={bgas: Flow()},
            coefficients=(-17, 0.9))


def test_offsettransformer_not_enough_coefficients():
    with pytest.raises(
            ValueError,
            match=r'Two coefficients or coefficient series have to be given.'):
        components.OffsetTransformer(
            label='of1',
            coefficients=([1, 4, 7]))


def test_offsettransformer_too_many_coefficients():
    with pytest.raises(
            ValueError,
            match=r'Two coefficients or coefficient series have to be given.'):
        components.OffsetTransformer(
            label='of2',
            coefficients=(1, 4, 7))


def test_offsettransformer_empty():
    """No NonConvexFlow for Inflow defined."""
    components.OffsetTransformer()


def test_offsettransformer__too_many_input_flows():
    """Too many Input Flows defined."""
    with pytest.raises(ValueError,
                       match=r"OffsetTransformer` must not have more than 1"):
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
    with pytest.raises(
            ValueError, match='OffsetTransformer` must not have more than 1'):
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
