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
            investment=Investment(),
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.8,
        )


def test_generic_storage_2():
    """Nominal value defined with investment model."""
    bel = Bus()
    with pytest.raises(
        AttributeError,
        match="For backward compatibility, the option investment overwrites",
    ):
        components.GenericStorage(
            label="storage3",
            nominal_storage_capacity=45,
            inputs={bel: Flow(variable_costs=10e10)},
            outputs={bel: Flow(variable_costs=10e10)},
            loss_rate=0.00,
            initial_storage_level=0,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.8,
            investment=Investment(ep_costs=23),
        )


def test_generic_storage_3():
    """Nominal value defined with investment model."""
    bel = Bus()
    components.GenericStorage(
        label="storage4",
        nominal_storage_capacity=45,
        inputs={bel: Flow(nominal_value=23, variable_costs=10e10)},
        outputs={bel: Flow(nominal_value=7.5, variable_costs=10e10)},
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
            nominal_storage_capacity=10,
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
            investment=Investment(nonconvex=True, existing=5, maximum=25),
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
            investment=Investment(nonconvex=True),
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
            investment=Investment(offset=10),
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
            investment=Investment(ep_costs=23, minimum=0, existing=0),
            fixed_losses_absolute=[0, 0, 4],
        )


def test_generic_storage_without_inputs():
    components.GenericStorage(label="storage5")


def test_generic_storage_too_many_inputs():
    msg = r"Only one input flow allowed in the GenericStorage storage6"
    bel1 = Bus()
    bel2 = Bus()
    with pytest.raises(AttributeError, match=msg):
        components.GenericStorage(
            label="storage6", inputs={bel1: Flow(), bel2: Flow()}
        )


def test_generic_storage_too_many_outputs():
    msg = r"Only one output flow allowed in the GenericStorage storage7"
    bel1 = Bus()
    bel2 = Bus()
    with pytest.raises(AttributeError, match=msg):
        components.GenericStorage(
            label="storage7", outputs={bel1: Flow(), bel2: Flow()}
        )


# ********* OffsetConverter *********


def test_offsetconverter_without_nonconvex():
    """No NonConvex attribute is defined for the output flow."""
    with pytest.raises(
        TypeError, match="Output flow must have the `NonConvex` attribute!"
    ):
        b_el = Bus(label="bus_electricity")
        components.OffsetConverter(
            label="diesel_genset",
            inputs={b_el: Flow()},
            outputs={b_el: Flow()},
            coefficients=(2.5, 0.5),
        )


def test_offsetconverter_nonconvex_on_inputs():
    """NonConvex attribute is defined for the input flow."""
    with pytest.raises(
        TypeError,
        match="`NonConvex` attribute must be defined only for the output "
        + "flow!",
    ):
        b_diesel = Bus(label="bus_diesel")
        components.OffsetConverter(
            inputs={b_diesel: Flow(nonconvex=NonConvex())},
            outputs={b_diesel: Flow(nonconvex=NonConvex())},
            coefficients=(2.5, 0.5),
        )


def test_offsetconverter_investment_on_inputs():
    """Investment attribute is defined for the input flow."""
    with pytest.raises(
        TypeError,
        match="`Investment` attribute must be defined only for the output "
        + "flow!",
    ):
        b_diesel = Bus(label="bus_diesel")
        components.OffsetConverter(
            inputs={b_diesel: Flow(investment=Investment())},
            outputs={
                b_diesel: Flow(
                    nonconvex=NonConvex(), investment=Investment(maximum=1)
                )
            },
            coefficients=(2.5, 0.5),
        )


def test_offsetconverter_not_enough_coefficients():
    with pytest.raises(
        ValueError,
        match="Two coefficients or coefficient series have to be given.",
    ):
        bus = Bus(label="Bus")
        components.OffsetConverter(
            label="of1",
            inputs={bus: Flow()},
            outputs={bus: Flow(nonconvex=NonConvex())},
            coefficients=([1, 4, 7]),
        )


def test_offsetconverter_too_many_coefficients():
    with pytest.raises(
        ValueError,
        match="Two coefficients or coefficient series have to be given.",
    ):
        bus = Bus(label="Bus")
        components.OffsetConverter(
            label="of2",
            inputs={bus: Flow()},
            outputs={bus: Flow(nonconvex=NonConvex())},
            coefficients=(1, 4, 7),
        )


def test_offsettransformer__too_many_input_flows():
    """Too many Input Flows defined."""
    with pytest.raises(
        ValueError,
        match="Component `OffsetConverter` must not have more than 1 input "
        + "and 1 output!",
    ):
        b_gas = Bus(label="bus_gas")
        b_coal = Bus(label="bus_coal")
        components.OffsetConverter(
            inputs={
                b_gas: Flow(),
                b_coal: Flow(),
            },
            outputs={b_coal: Flow(nonconvex=NonConvex())},
            coefficients=(20, 0.5),
        )


def test_offsetconverter_too_many_output_flows():
    """Too many Output Flows defined."""
    with pytest.raises(
        ValueError,
        match="Component `OffsetConverter` must not have more than 1 input "
        + "and 1 output!",
    ):
        b_el = Bus(label="bus_electricity")
        b_th = Bus(label="bus_thermal")

        components.OffsetConverter(
            inputs={
                b_el: Flow(),
            },
            outputs={
                b_el: Flow(nonconvex=NonConvex()),
                b_th: Flow(nonconvex=NonConvex()),
            },
            coefficients=(20, 0.5),
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
