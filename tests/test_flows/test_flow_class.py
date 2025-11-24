# -*- coding: utf-8 -

"""Testing the flows.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import pytest

from oemof.solph import NonConvex
from oemof.solph.flows import Flow


def test_custom_properties():
    flow1 = Flow(custom_properties={"prop": 1})
    assert flow1.custom_properties["prop"] == 1

    # --- BEGIN: The following code can be removed for versions >= v0.7 ---
    with pytest.warns(
        FutureWarning,
        match="For backward compatibility,",
    ):
        flow2 = Flow(custom_attributes={"attribute": 1})
        assert flow2.attribute == 1
        assert flow2.custom_properties["attribute"] == 1

    with pytest.raises(
        AttributeError,
        match="Both options cannot be set at the same time.",
    ):
        Flow(
            custom_attributes={"attribute": 1},
            custom_properties={"prop": 1},
        )
    # --- END ---


def test_source_with_full_load_time_max():
    # TODO: This does not test anything?
    Flow(nominal_capacity=1, full_load_time_max=2)


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
    flow = Flow(nominal_capacity=4, fix=[0.3, 0.2, 0.7])

    assert flow.fix[0] == 0.3
    assert flow.fix[1] == 0.2
    assert flow.fix[2] == 0.7


def test_fix_sequence_non_nominal():
    # TODO: This is possibly a duplication with test_solph_network_classes.py
    """Attribute fix needs nominal_capacity"""
    with pytest.raises(AttributeError):
        Flow(fix=[0.3, 0.2, 0.7])


def test_bidirectional_with_positive_min():
    with pytest.raises(
        AttributeError,
        match="If `bidirectional` is set to `True`",
    ):
        Flow(bidirectional=True, min=0.1, nominal_capacity=1)


def test_unidirectional_explicit_with_negative_min():
    with pytest.raises(
        AttributeError, match="If `bidirectional` is set to `False`"
    ):
        Flow(bidirectional=False, min=-0.1)


def test_unidirectional_implicit_with_negative_min():
    with pytest.raises(
        AttributeError, match="If `bidirectional` is set to `False`"
    ):
        Flow(min=-0.1)
