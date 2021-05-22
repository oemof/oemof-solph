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


class TestTransformerClass:
    @classmethod
    def setup_class(cls):
        """Setup default values"""
        cls.bus = solph.Bus()
        warnings.filterwarnings("ignore", category=SuspiciousUsageWarning)

    @classmethod
    def teardown_class(cls):
        warnings.filterwarnings("always", category=SuspiciousUsageWarning)

    def test_empty_transformer(self):
        transf = solph.Transformer()
        assert isinstance(transf.conversion_factors, dict)
        assert len(transf.conversion_factors.keys()) == 0

    def test_default_conversion_factor(self):
        transf = solph.Transformer(inputs={self.bus: solph.Flow()})
        assert transf.conversion_factors[self.bus][2] == 1

    def test_sequence_conversion_factor_from_scalar(self):
        transf = solph.Transformer(
            inputs={self.bus: solph.Flow()}, conversion_factors={self.bus: 2}
        )
        assert transf.conversion_factors[self.bus][6] == 2

    def test_sequence_conversion_factor_from_list_correct_length(self):
        transf = solph.Transformer(
            inputs={self.bus: solph.Flow()}, conversion_factors={self.bus: [2]}
        )
        assert len(transf.conversion_factors[self.bus]) == 1

    def test_sequence_conversion_factor_from_list_wrong_length(self):
        transf = solph.Transformer(
            inputs={self.bus: solph.Flow()}, conversion_factors={self.bus: [2]}
        )
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


def test_wrong_combination_of_multiperiod_options_1():
    msg = ("Values for 'offset' and 'existing' are given in"
           " investment attributes. \n These two options cannot be "
           "considered at the same time.")
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(multiperiodinvestment=solph.MultiPeriodInvestment(
            existing=100,
            nonconvex=True,
            lifetime=20
        ))


def test_wrong_combination_of_multiperiod_options_2():
    msg = ("Please provide an maximum investment value in case of "
           "nonconvex investment, which is in the "
           "expected magnitude.\n"
           "Very high maximum values as maximum investment "
           "limit might lead to numeric issues, so that no investment "
           "is done, although it is the optimal solution!")
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(multiperiodinvestment=solph.MultiPeriodInvestment(
            nonconvex=True,
            lifetime=20
        ))


def test_wrong_combination_of_multiperiod_options_3():
    msg = ("If `nonconvex` is `False`, the `offset` parameter will be"
           " ignored.")
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(multiperiodinvestment=solph.MultiPeriodInvestment(
            nonconvex=False,
            offset=100,
            lifetime=20
        ))


def test_wrong_combination_of_multiperiod_options_4():
    msg = ("A unit's age must be smaller than its "
           "expected lifetime.")
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(multiperiodinvestment=solph.MultiPeriodInvestment(
            age=21,
            lifetime=20
        ))


def test_wrong_combination_of_multiperiod_options_5():
    msg = ("Either use a standard investment flow for "
           "standard investment models or a "
           "multiperiodinvestment flow "
           "for MultiPeriodModels.\n"
           "Combining both is not feasible!")
    with pytest.raises(ValueError, match=msg):
        solph.Flow(
            multiperiodinvestment=solph.MultiPeriodInvestment(lifetime=20),
            investment=solph.Investment()
        )


def test_wrong_combination_of_multiperiod_options_6():
    msg = ("In a MultiPeriodModel, a flow can either "
           "be defined to be a flow for dispatch only,\n"
           "when setting the attribute `multiperiod` to "
           "True,\nor it can be defined to be used for "
           "investments,\nwhen a `multiperiodinvestment` "
           "object is declared.\nCombining both is not "
           "feasible!")
    with pytest.raises(ValueError, match=msg):
        solph.Flow(
            multiperiodinvestment=solph.MultiPeriodInvestment(lifetime=20),
            multiperiod=True
        )


def test_calc_max_up_down_1():
    test_flow = solph.Flow(
        nonconvex=solph.NonConvex(minimum_uptime=3,
                                  minimum_downtime=None)
    )
    test_flow.nonconvex._calculate_max_up_down()
    assert (test_flow.nonconvex.minimum_uptime
            == test_flow.nonconvex._max_up_down)


def test_calc_max_up_down_2():
    test_flow = solph.Flow(
        nonconvex=solph.NonConvex(minimum_uptime=None,
                                  minimum_downtime=5)
    )
    test_flow.nonconvex._calculate_max_up_down()
    assert (test_flow.nonconvex.minimum_downtime
            == test_flow.nonconvex._max_up_down)


def test_flow_with_fix_and_min_max():
    msg = "It is not allowed to define min/max if fix is defined."
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(fix=[1, 3], min=[0, 5])
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(fix=[1, 3], max=[0, 5])
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(fix=[1, 3], max=[0, 5], min=[4, 9])


def test_min_max_values_for_bidirectional_flow():
    a = solph.Flow(bidirectional=True)  # use default values
    b = solph.Flow(bidirectional=True, min=-0.9, max=0.9)
    assert a.bidirectional
    assert a.max[0] == 1
    assert a.min[0] == -1
    assert b.max[0] == 0.9
    assert b.min[0] == -0.9


def test_deprecated_actual_value():
    """Deprecated error for actual_warning is not raised correctly."""
    msg = "The `actual_value` attribute has been renamed to `fix`"
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(actual_value=5)


def test_warning_fixed_costs_attribute():
    msg = ("Be aware that the fixed costs attribute is only\n"
           "meant to be used for MultiPeriodModels.\n"
           "It has been decided to remove the `fixed_costs` "
           "attribute with v0.2 for regular uses!")
    with warnings.catch_warnings(record=True) as w:
        solph.Flow(fixed_costs=10)
        assert len(w) != 0
        assert msg == str(w[-1].message)


def test_warning_fixed_still_used():
    """If fixed attribute is still used, a warning is raised."""
    msg = (
        "The `fixed` attribute is deprecated.\nIf you have defined "
        "the `fix` attribute the flow variable will be fixed.\n"
        "The `fixed` attribute does not change anything."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.Flow(fixed=True)
        assert len(w) != 0
        assert msg == str(w[-1].message)


def test_setting_kwargs():
    test_flow = solph.Flow(superpower=3, awesomeness=5)
    assert(test_flow.superpower == 3)
    assert(test_flow.awesomeness == 5)
