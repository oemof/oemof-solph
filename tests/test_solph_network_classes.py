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
        solph.Flow(investment=solph.Investment(), nominal_value=4)
    with assert_raises(ValueError):
        solph.Flow(investment=solph.Investment(), nonconvex=solph.NonConvex())
    with assert_raises(AttributeError):
        solph.Flow(fixed_costs=34)
