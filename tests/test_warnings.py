# -*- coding: utf-8 -

"""Test debugging warning.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/tool_tests.py

SPDX-License-Identifier: MIT
"""

from nose.tools import assert_raises_regexp
import warnings
from oemof import network
from oemof.tools.debugging import SuspiciousUsageWarning


def test_that_the_sink_warnings_actually_get_raised():
    """ Sink doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Sink` constructed without `inputs`."
    with warnings.catch_warnings(record=True) as w:
        network.Sink(outputs={look_out: "A typo!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_that_the_source_warnings_actually_get_raised():
    """ Source doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Source` constructed without `outputs`."
    with warnings.catch_warnings(record=True) as w:
        network.Source(inputs={look_out: "A typo!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_that_the_transformer_warnings_actually_get_raised():
    """ Transformer doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Transformer` constructed without `inputs"
    with warnings.catch_warnings(record=True) as w:
        network.Transformer(outputs={look_out: "No inputs!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)
    msg = "`Transformer` constructed without `outputs"
    with warnings.catch_warnings(record=True) as w:
        network.Transformer(inputs={look_out: "No outputs!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)
