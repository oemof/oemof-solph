# -*- coding: utf-8 -

"""Testing the option class NonConvex.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

from oemof.solph import NonConvex


def test_custom_attribute():
    non_convex_object = NonConvex(
        custom_attributes={
            "first_attribute": True,
            "second_attribute": 5,
        }
    )

    assert non_convex_object.first_attribute is True
    assert non_convex_object.second_attribute == 5
