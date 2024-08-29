# -*- coding: utf-8 -

"""Testing the flows.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import warnings

import pytest

from oemof.solph import NonConvex
from oemof.solph.flows import Flow


def test_summed_max_future_warning():
    """Can be removed with v0.6."""
    msg = "The parameter 'summed_max' is deprecated and will be removed"
    with warnings.catch_warnings(record=True) as w:
        Flow(nominal_value=1, summed_max=2)
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_summed_min_future_warning():
    """Can be removed with v0.6."""
    msg = "The parameter 'summed_min' is deprecated and will be removed"
    with warnings.catch_warnings(record=True) as w:
        Flow(nominal_value=1, summed_min=2)
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_source_with_full_load_time_max():
    Flow(nominal_value=1, full_load_time_max=2)


def test_nonconvex_positive_gradient_error():
    """Testing nonconvex positive gradient error."""
    msg = (
        "You specified a positive gradient in your nonconvex "
        "option. This cannot be combined with a positive or a "
        "negative gradient for a standard flow!"
    )

    with pytest.raises(ValueError, match=msg):
        Flow(
            nonconvex=NonConvex(
                positive_gradient_limit=0.03,
            ),
            positive_gradient_limit=0.03,
        )


def test_non_convex_negative_gradient_error():
    """Testing non-convex positive gradient error."""
    msg = (
        "You specified a negative gradient in your nonconvex "
        "option. This cannot be combined with a positive or a "
        "negative gradient for a standard flow!"
    )

    with pytest.raises(ValueError, match=msg):
        Flow(
            nonconvex=NonConvex(
                negative_gradient_limit=0.03,
            ),
            positive_gradient_limit=0.03,
        )


def test_fix_sequence():
    flow = Flow(nominal_value=4, fix=[0.3, 0.2, 0.7])

    assert flow.fix[0] == 0.3
    assert flow.fix[1] == 0.2
    assert flow.fix[2] == 0.7


def test_fix_sequence_non_nominal():
    """Attribute fix needs nominal_value"""
    with pytest.raises(AttributeError):
        Flow(fix=[0.3, 0.2, 0.7])
