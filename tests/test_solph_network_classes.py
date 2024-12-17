# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_solph_network_classes.py

SPDX-License-Identifier: MIT
"""

import warnings

import pytest
from oemof.tools.debugging import SuspiciousUsageWarning

from oemof import solph


class TestConverterClass:
    @classmethod
    def setup_class(cls):
        """Setup default values"""
        cls.bus = solph.buses.Bus()

    @pytest.mark.filterwarnings("ignore::UserWarning")
    def test_empty_converter(self):
        converter = solph.components.Converter()
        assert isinstance(converter.conversion_factors, dict)
        assert len(converter.conversion_factors.keys()) == 0

    def test_default_conversion_factor(self):
        converter = solph.components.Converter(
            inputs={self.bus: solph.flows.Flow()},
            outputs={self.bus: solph.flows.Flow()},
        )
        assert converter.conversion_factors[self.bus][2] == 1

    def test_sequence_conversion_factor_from_scalar(self):
        converter = solph.components.Converter(
            inputs={self.bus: solph.flows.Flow()},
            outputs={self.bus: solph.flows.Flow()},
            conversion_factors={self.bus: 2},
        )
        assert converter.conversion_factors[self.bus][6] == 2

    def test_sequence_conversion_factor_from_list_correct_length(self):
        converter = solph.components.Converter(
            inputs={self.bus: solph.flows.Flow()},
            outputs={self.bus: solph.flows.Flow()},
            conversion_factors={self.bus: [2]},
        )
        assert len(converter.conversion_factors[self.bus]) == 1

    def test_sequence_conversion_factor_from_list_wrong_length(self):
        converter = solph.components.Converter(
            inputs={self.bus: solph.flows.Flow()},
            outputs={self.bus: solph.flows.Flow()},
            conversion_factors={self.bus: [2]},
        )
        with pytest.raises(IndexError):
            self.a = converter.conversion_factors[self.bus][6]

    def test_converter_missing_output_create_empty_dict(self):
        with pytest.warns(SuspiciousUsageWarning):
            converter = solph.components.Converter(inputs={})
            assert converter.outputs == {}

    def test_converter_missing_input_create_empty_dict(self):
        with pytest.warns(SuspiciousUsageWarning):
            converter = solph.components.Converter(outputs={})
            assert converter.inputs == {}


def test_fixed_costs_warning():
    msg = (
        "Be aware that the fixed costs attribute is only\n"
        "meant to be used for multi-period models to depict "
        "fixed costs that occur on a yearly basis.\n"
        "If you wish to set up a multi-period model, explicitly "
        "set the `periods` attribute of your energy system.\n"
        "It has been decided to remove the `fixed_costs` "
        "attribute with v0.2 for regular uses.\n"
        "If you specify `fixed_costs` for a regular model, "
        "this will simply be silently ignored."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.flows.Flow(fixed_costs=34)
        assert len(w) != 0
        assert msg == str(w[-1].message)


def test_flow_with_fix_and_min_max():
    msg = "It is not allowed to define `min`/`max` if `fix` is defined."
    with pytest.raises(AttributeError, match=msg):
        solph.flows.Flow(fix=[1, 3], min=[0, 5])
    with pytest.raises(AttributeError, match=msg):
        solph.flows.Flow(fix=[1, 3], max=[0, 5])
    with pytest.raises(AttributeError, match=msg):
        solph.flows.Flow(fix=[1, 3], max=[0, 5], min=[4, 9])


def test_infinite_values():
    msg1 = "nominal_capacity must be a finite value"
    msg2 = "max must be a finite value"
    with pytest.raises(ValueError, match=msg1):
        solph.flows.Flow(nominal_capacity=float("+inf"))
    with pytest.raises(ValueError, match=msg2):
        solph.flows.Flow(nominal_capacity=1, max=float("+inf"))


def test_attributes_needing_nominal_value_get_it():
    with pytest.raises(AttributeError, match="If fix is set in a flow "):
        solph.flows.Flow(fix=0.3)

    with pytest.raises(AttributeError, match="If max is set in a flow "):
        solph.flows.Flow(max=0.3)

    with pytest.raises(AttributeError, match="If min is set in a flow "):
        solph.flows.Flow(min=0.3)

    with pytest.raises(
        AttributeError, match="If full_load_time_max is set in a flow "
    ):
        solph.flows.Flow(full_load_time_max=0.3)

    with pytest.raises(
        AttributeError, match="If full_load_time_min is set in a flow "
    ):
        solph.flows.Flow(full_load_time_min=0.3)


def test_min_max_values_for_bidirectional_flow():
    a = solph.flows.Flow(bidirectional=True)  # use default values
    b = solph.flows.Flow(
        bidirectional=True, nominal_capacity=1, min=-0.8, max=0.9
    )
    assert a.bidirectional
    assert a.max[0] == 1
    assert a.min[0] == -1
    assert b.bidirectional
    assert b.max[0] == 0.9
    assert b.min[0] == -0.8
