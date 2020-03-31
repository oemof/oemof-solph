# -*- coding: utf-8 -

"""Test debugging warning.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/tool_tests.py

SPDX-License-Identifier: MIT
"""

import warnings

from nose.tools import eq_
from nose.tools import ok_
from nose.tools import with_setup
from oemof import solph
from oemof.network import network
from oemof.tools.debugging import SuspiciousUsageWarning


def setup_func():
    """Explicitly activate the warnings."""
    warnings.filterwarnings("always", category=SuspiciousUsageWarning)


@with_setup(setup_func)
def test_that_the_sink_warnings_actually_get_raised():
    """ Sink doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Sink` 'test_sink' constructed without `inputs`."
    with warnings.catch_warnings(record=True) as w:
        solph.Sink(label='test_sink', outputs={look_out: "A typo!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))


@with_setup(setup_func)
def test_filtered_warning():
    """ Sink doesn't warn about potentially erroneous usage.
    """
    warnings.filterwarnings("ignore", category=SuspiciousUsageWarning)
    look_out = network.Bus()
    with warnings.catch_warnings(record=True) as w:
        network.Sink(outputs={look_out: "A typo!"})
        ok_(len(w) == 0)


@with_setup(setup_func)
def test_that_the_source_warnings_actually_get_raised():
    """ Source doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Source` 'test_source' constructed without `outputs`."
    with warnings.catch_warnings(record=True) as w:
        solph.Source(label='test_source', inputs={look_out: "A typo!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))


@with_setup(setup_func)
def test_that_the_solph_source_warnings_actually_get_raised():
    """ Source doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Source` 'solph_sink' constructed without `outputs`."
    with warnings.catch_warnings(record=True) as w:
        solph.Source(label="solph_sink", inputs={look_out: "A typo!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))


@with_setup(setup_func)
def test_that_the_transformer_warnings_actually_get_raised():
    """ Transformer doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = "`Transformer` 'no input' constructed without `inputs`."
    with warnings.catch_warnings(record=True) as w:
        solph.Transformer(label='no input', outputs={look_out: "No inputs!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))
    msg = "`Transformer` 'no output' constructed without `outputs`."
    with warnings.catch_warnings(record=True) as w:
        solph.Transformer(label='no output',
                          inputs={look_out: "No outputs!"})
        ok_(len(w) == 1)
        eq_(msg, str(w[-1].message))
