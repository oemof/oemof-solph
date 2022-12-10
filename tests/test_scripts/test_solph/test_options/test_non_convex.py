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


def test_max_up_down():
    non_convex_object1 = NonConvex(
        minimum_uptime=5,
        minimum_downtime=4,
    )
    assert non_convex_object1.max_up_down == 5

    non_convex_object1 = NonConvex(
        minimum_downtime=4,
    )
    assert non_convex_object1.max_up_down == 4

    non_convex_object1 = NonConvex(
        minimum_uptime=5,
    )
    assert non_convex_object1.max_up_down == 5

    non_convex_object1 = NonConvex()
    assert non_convex_object1.max_up_down == 0
