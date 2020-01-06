# -*- coding: utf-8 -

"""Test debugging warning.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/tool_tests.py

SPDX-License-Identifier: MIT
"""

from nose.tools import eq_, ok_
import warnings
from oemof import network
from oemof.tools.debugging import SuspiciousUsageWarning


def test_that_the_sink_warnings_actually_get_raised():
    """ Sink doesn't warn about potentially erroneous usage.
    """
    warnings.filterwarnings("always", category=SuspiciousUsageWarning)
    look_out = network.Bus()
    msg = "`Sink` constructed without `inputs`."
    with warnings.catch_warnings(record=True) as w:
        network.Sink(outputs={look_out: "A typo!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))


def test_filtered_warning():
    """ Sink doesn't warn about potentially erroneous usage.
    """
    warnings.filterwarnings("ignore", category=SuspiciousUsageWarning)
    look_out = network.Bus()
    with warnings.catch_warnings(record=True) as w:
        network.Sink(outputs={look_out: "A typo!"})
        ok_(len(w) == 0)
    warnings.filterwarnings("always", category=SuspiciousUsageWarning)


def test_that_the_source_warnings_actually_get_raised():
    """ Source doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Source` constructed without `outputs`."
    with warnings.catch_warnings(record=True) as w:
        network.Source(inputs={look_out: "A typo!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))


def test_that_the_transformer_warnings_actually_get_raised():
    """ Transformer doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Transformer` constructed without `inputs`.\n"
    with warnings.catch_warnings(record=True) as w:
        network.Transformer(outputs={look_out: "No inputs!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))
    msg = "`Transformer` constructed without `outputs`.\n"
    with warnings.catch_warnings(record=True) as w:
        network.Transformer(inputs={look_out: "No outputs!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))
