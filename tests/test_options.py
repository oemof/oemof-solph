"""Tests of the _options module.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import pytest
from oemof.tools import debugging

from oemof import solph


def test_check_age_and_lifetime():
    """Check error being thrown if age > lifetime"""
    msg = "A unit's age must be smaller than its expected lifetime."
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(nominal_capacity=solph.Investment(age=41, lifetime=40))


def test_check_invest_attributes_nonconvex():
    """Check error being thrown if nonconvex parameter is not of type bool"""
    msg = (
        "The `nonconvex` parameter of the `Investment` class has to be of type"
        + " boolean, not <class 'oemof.solph._options.NonConvex'>."
    )
    with pytest.raises(AttributeError, match=msg):
        solph.Flow(
            nominal_capacity=solph.Investment(
                maximum=1, nonconvex=solph.NonConvex()
            )
        )


def test_check_nonconvex():
    """
    Check warning being thrown if minimum and offset are zero and nonconvex
    is set
    """
    with pytest.warns(debugging.SuspiciousUsageWarning):
        solph.Flow(
            nominal_capacity=solph.Investment(
                maximum=1, minimum=0, offset=0, nonconvex=True
            )
        )


def test_investment_custom_properties():
    investment1 = solph.Investment(custom_properties={"prop": 1})
    assert investment1.custom_properties["prop"] == 1

    # --- BEGIN: The following code can be removed for versions >= v0.7 ---
    with pytest.warns(
        FutureWarning,
        match="For backward compatibility,",
    ):
        investment2 = solph.Investment(custom_attributes={"attribute": 1})
        assert investment2.attribute == 1
        assert investment2.custom_properties["attribute"] == 1

    with pytest.raises(
        AttributeError,
        match="Both options cannot be set at the same time.",
    ):
        solph.Investment(
            custom_attributes={"attribute": 1},
            custom_properties={"prop": 1},
        )
    # --- END ---
