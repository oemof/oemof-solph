# -*- coding: utf-8 -

"""Testing the option class NonConvex.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""
import pytest

from oemof.solph import NonConvex


def test_custom_attribute():
    non_convex_object1 = NonConvex(
        custom_properties={
            "prop": 1,
            "prop2": 2,
        }
    )
    assert non_convex_object1.custom_properties["prop"] == 1
    assert non_convex_object1.custom_properties["prop2"] == 2

    # --- BEGIN: The following code can be removed for versions >= v0.7 ---
    with pytest.warns(
        FutureWarning,
        match="For backward compatibility,",
    ):
        non_convex_object2 = NonConvex(
            custom_attributes={
                "attribute": 1,
                "prop2": 2,
            }
        )
        assert non_convex_object2.attribute == 1
        assert non_convex_object2.prop2 == 2
        assert non_convex_object2.custom_properties["attribute"] == 1
        assert non_convex_object2.custom_properties["prop2"] == 2

    with pytest.raises(
        AttributeError,
        match="Both options cannot be set at the same time.",
    ):
        NonConvex(
            custom_attributes={"attribute": 1},
            custom_properties={"prop": 1},
        )
    # --- END ---
