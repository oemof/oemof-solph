# -*- coding: utf-8 -

"""Testing the flows.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_components.py

SPDX-License-Identifier: MIT
"""

import pytest

from oemof.solph.flows import Flow


def test_error_in_gradient_attribute():
    msg = "Only the key 'ub' is allowed for the '{0}' attribute"
    with pytest.raises(AttributeError, match=msg.format("negative_gradient")):
        Flow(negative_gradient={"costs": 5})
    with pytest.raises(AttributeError, match=msg.format("positive_gradient")):
        Flow(positive_gradient={"something": 5})
