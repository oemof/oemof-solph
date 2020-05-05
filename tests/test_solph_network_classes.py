# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_solph_network_classes.py

SPDX-License-Identifier: MIT
"""

from nose.tools import assert_raises
from nose.tools import eq_
from nose.tools import ok_
import pytest
from oemof import solph


class TestTransformerClass:
    @classmethod
    def setup_class(cls):
        """Setup default values"""
        cls.bus = solph.Bus()

    def test_empty_transformer(self):
        transf = solph.Transformer()
        assert isinstance(transf.conversion_factors, dict)
        assert len(transf.conversion_factors.keys()) == 0

    def test_default_conversion_factor(self):
        transf = solph.Transformer(inputs={self.bus: solph.Flow()})
        assert transf.conversion_factors[self.bus][2] == 1

    def test_sequence_conversion_factor_from_scalar(self):
        transf = solph.Transformer(inputs={self.bus: solph.Flow()},
                                   conversion_factors={self.bus: 2})
        assert transf.conversion_factors[self.bus][6] == 2

    def test_sequence_conversion_factor_from_list_correct_length(self):
        transf = solph.Transformer(inputs={self.bus: solph.Flow()},
                                   conversion_factors={self.bus: [2]})
        assert len(transf.conversion_factors[self.bus]) == 1

    def test_sequence_conversion_factor_from_list_wrong_length(self):
        transf = solph.Transformer(inputs={self.bus: solph.Flow()},
                                   conversion_factors={self.bus: [2]})
        with pytest.raises(IndexError):
            self.a = transf.conversion_factors[self.bus][6]


def test_wrong_combination_invest_and_nominal_value():
    msg = "Using the investment object the nominal_value"
    with pytest.raises(ValueError, match=msg):
        solph.Flow(investment=solph.Investment(), nominal_value=4)


def test_wrong_combination_of_options():
    msg = "Investment flows cannot be combined with nonconvex flows!"
    with pytest.raises(ValueError, match=msg):
        solph.Flow(investment=solph.Investment(), nonconvex=solph.NonConvex())


def test_error_of_deprecated_fixed_costs():
    msg = "The `fixed_costs` attribute has been removed with v0.2!"
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(fixed_costs=34)
