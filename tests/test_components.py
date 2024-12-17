# -*- coding: utf-8 -

"""Tests of the component module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import warnings

import pytest
from oemof.tools.debugging import SuspiciousUsageWarning

from oemof.solph import Investment
from oemof.solph import NonConvex
from oemof.solph import components
from oemof.solph.buses import Bus
from oemof.solph.flows import Flow

# ********* GenericStorage *********


def test_generic_storage_1():
    """Duplicate definition inflow."""
    bel = Bus()
    with pytest.raises(AttributeError, match="Overdetermined."):
        components.GenericStorage(
            label="storage1",
            inputs={bel: Flow(variable_costs=10e10)},
            outputs={bel: Flow(variable_costs=10e10)},
            loss_rate=0.00,
            initial_storage_level=0,
            invest_relation_input_output=1,
            invest_relation_output_capacity=1,
            invest_relation_input_capacity=1,
            nominal_capacity=Investment(),
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.8,
        )


def test_generic_storage_3():
    """Nominal capacity defined with investment model."""
    bel = Bus()
    components.GenericStorage(
        label="storage4",
        nominal_capacity=45,
        inputs={bel: Flow(nominal_capacity=23, variable_costs=10e10)},
        outputs={bel: Flow(nominal_capacity=7.5, variable_costs=10e10)},
        loss_rate=0.00,
        initial_storage_level=0,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )


def test_generic_storage_4():
    """Infeasible parameter combination for initial_storage_level"""
    bel = Bus()
    with pytest.raises(
        ValueError, match="initial_storage_level must be greater"
    ):
        components.GenericStorage(
            label="storage4",
            nominal_capacity=10,
            inputs={bel: Flow(variable_costs=10e10)},
            outputs={bel: Flow(variable_costs=10e10)},
            loss_rate=0.00,
            initial_storage_level=0,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.8,
        )


def test_generic_storage_with_non_convex_investment():
    """Tests error if `offset` and `existing` attribute are given."""
    with pytest.raises(
        AttributeError, match=r"Values for 'offset' and 'existing' are given"
    ):
        bel = Bus()
        components.GenericStorage(
            label="storage4",
            inputs={bel: Flow()},
            outputs={bel: Flow()},
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            nominal_capacity=Investment(
                nonconvex=True, existing=5, maximum=25
            ),
        )


def test_generic_storage_with_non_convex_invest_maximum():
    """No investment maximum at nonconvex investment."""
    with pytest.raises(
        AttributeError, match=r"Please provide a maximum investment value"
    ):
        bel = Bus()
        components.GenericStorage(
            label="storage6",
            inputs={bel: Flow()},
            outputs={bel: Flow()},
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            nominal_capacity=Investment(nonconvex=True),
        )


def test_generic_storage_with_convex_invest_offset():
    """Offset value is given and nonconvex is False."""
    with pytest.raises(
        AttributeError, match=r"If `nonconvex` is `False`, the `offset`"
    ):
        bel = Bus()
        components.GenericStorage(
            label="storage6",
            inputs={bel: Flow()},
            outputs={bel: Flow()},
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            nominal_capacity=Investment(offset=10),
        )


def test_generic_storage_with_invest_and_fixed_losses_absolute():
    """
    Storage with fixed losses in the investment mode but no minimum or existing
    value is set an AttributeError is raised because this may result in storage
    with zero capacity but fixed losses.
    """
    msg = (
        r"With fixed_losses_absolute > 0, either investment.existing or"
        " investment.minimum has to be non-zero."
    )
    with pytest.raises(AttributeError, match=msg):
        bel = Bus()
        components.GenericStorage(
            label="storage4",
            inputs={bel: Flow()},
            outputs={bel: Flow()},
            nominal_capacity=Investment(ep_costs=23, minimum=0, existing=0),
            fixed_losses_absolute=[0, 0, 4],
        )


def test_generic_storage_without_inputs():
    with pytest.warns(SuspiciousUsageWarning):
        components.GenericStorage(label="storage5")


def test_generic_storage_too_many_inputs():
    msg = r"Only one input flow allowed in the GenericStorage storage6"
    bel1 = Bus()
    bel2 = Bus()
    with pytest.raises(AttributeError, match=msg):
        components.GenericStorage(
            label="storage6",
            inputs={bel1: Flow(), bel2: Flow()},
            outputs={bel2: Flow()},
        )


def test_generic_storage_too_many_outputs():
    msg = r"Only one output flow allowed in the GenericStorage storage7"
    bel1 = Bus()
    bel2 = Bus()
    with pytest.raises(AttributeError, match=msg):
        components.GenericStorage(
            label="storage7",
            inputs={bel1: Flow()},
            outputs={bel1: Flow(), bel2: Flow()},
        )


# ********* OffsetConverter *********


def test_offsetconverter_without_nonconvex():
    """No NonConvex attribute is defined for any of the attached flows."""
    with pytest.raises(
        ValueError,
        match=(
            "Exactly one flow of the `OffsetConverter` must have the "
            "`NonConvex` attribute."
        ),
    ):
        b_diesel = Bus(label="bus_diesel")
        b_el = Bus(label="bus_electricity")
        components.OffsetConverter(
            label="diesel_genset",
            inputs={b_diesel: Flow()},
            outputs={b_el: Flow()},
        )


def test_offsetconverter_multiple_nonconvex():
    """NonConvex attribute is defined for more than one flow."""
    with pytest.raises(
        ValueError,
        match=(
            "Exactly one flow of the `OffsetConverter` must have the "
            "`NonConvex` attribute."
        ),
    ):
        b_diesel = Bus(label="bus_diesel")
        b_heat = Bus(label="bus_heat")
        components.OffsetConverter(
            inputs={b_diesel: Flow(nonconvex=NonConvex())},
            outputs={b_heat: Flow(nonconvex=NonConvex())},
        )


def test_offsetconverter_investment_not_on_nonconvex():
    """Investment attribute is defined for a not NonConvex flow."""
    with pytest.raises(
        TypeError,
        match=(
            "`Investment` attribute must be defined only for the NonConvex "
            "flow!"
        ),
    ):
        b_diesel = Bus(label="bus_diesel")
        b_heat = Bus(label="bus_heat")
        components.OffsetConverter(
            inputs={b_diesel: Flow(nominal_capacity=Investment(maximum=1))},
            outputs={b_heat: Flow(nonconvex=NonConvex())},
        )


# ********* GenericCHP *********
def test_generic_chp_without_warning():
    warnings.filterwarnings("error", category=SuspiciousUsageWarning)
    bel = Bus(label="electricityBus")
    bth = Bus(label="heatBus")
    bgas = Bus(label="commodityBus")
    components.GenericCHP(
        label="combined_cycle_extraction_turbine",
        fuel_input={
            bgas: Flow(custom_attributes={"H_L_FG_share_max": [0.183]})
        },
        electrical_output={
            bel: Flow(
                custom_attributes={
                    "P_max_woDH": [155.946],
                    "P_min_woDH": [68.787],
                    "Eta_el_max_woDH": [0.525],
                    "Eta_el_min_woDH": [0.444],
                }
            )
        },
        heat_output={bth: Flow(custom_attributes={"Q_CW_min": [10.552]})},
        beta=[0.122],
        back_pressure=False,
    )
    warnings.filterwarnings("always", category=SuspiciousUsageWarning)
