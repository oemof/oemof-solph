# -*- coding: utf-8 -

"""Test debugging warning.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/tool_tests.py

SPDX-License-Identifier: MIT
"""

from nose.tools import assert_raises

from oemof import network
from oemof.tools.debugging import SuspiciousUsageWarning


def test_that_the_sink_warnings_actually_get_raised():
    """ Sink doesn't warn about potentially erroneous usage.
    """
    with assert_raises(
        SuspiciousUsageWarning, msg="Sink constructed without `inputs`."
    ):
        network.Sink(imputs={"Look out!": "A typo!"})
