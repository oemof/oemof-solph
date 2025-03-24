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


def test_check_nonconvex():
    """
    Check warning being thrown if minimum and offset are zero and nonconvex
    is set
    """
    with pytest.warns(debugging.SuspiciousUsageWarning):
        solph.Flow(
            nominal_capacity=solph.Investment(
                minimum=0, offset=0, nonconvex=solph.NonConvex()
            )
        )
