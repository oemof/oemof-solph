# -*- coding: utf-8 -

"""Test debugging warning.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/tool_tests.py

SPDX-License-Identifier: MIT
"""

import warnings

import pytest

from oemof import solph
from oemof.network import network
from oemof.tools.debugging import SuspiciousUsageWarning


@pytest.fixture()
def warning_fixture():
    """Explicitly activate the warnings."""
    warnings.filterwarnings("always", category=SuspiciousUsageWarning)


def test_that_the_sink_warnings_actually_get_raised(warning_fixture):
    """ Sink doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = ("Attribute <inputs> is missing in Node <test_sink> of <class"
           " 'oemof.solph.network.Sink'>")
    with warnings.catch_warnings(record=True) as w:
        solph.Sink(label='test_sink', outputs={look_out: "A typo!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_filtered_warning(warning_fixture):
    """ Sink doesn't warn about potentially erroneous usage.
    """
    warnings.filterwarnings("ignore", category=SuspiciousUsageWarning)
    look_out = network.Bus()
    with warnings.catch_warnings(record=True) as w:
        network.Sink(outputs={look_out: "A typo!"})
        assert len(w) == 0


def test_that_the_source_warnings_actually_get_raised(warning_fixture):
    """ Source doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = ("Attribute <outputs> is missing in Node <test_source> of <class"
           " 'oemof.solph.network.Source'>.")
    with warnings.catch_warnings(record=True) as w:
        solph.Source(label='test_source', inputs={look_out: "A typo!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_that_the_solph_source_warnings_actually_get_raised(warning_fixture):
    """ Source doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = ("Attribute <outputs> is missing in Node <solph_sink> of <class"
           " 'oemof.solph.network.Source'>.")
    with warnings.catch_warnings(record=True) as w:
        solph.Source(label="solph_sink", inputs={look_out: "A typo!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_that_the_transformer_warnings_actually_get_raised(warning_fixture):
    """ Transformer doesn't warn about potentially erroneous usage.
    """
    look_out = network.Bus()
    msg = ("Attribute <inputs> is missing in Node <no input> of <class"
           " 'oemof.solph.network.Transformer'>.")
    with warnings.catch_warnings(record=True) as w:
        solph.Transformer(label='no input', outputs={look_out: "No inputs!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)
    msg = ("Attribute <outputs> is missing in Node <no output> of <class"
           " 'oemof.solph.network.Transformer'>.")
    with warnings.catch_warnings(record=True) as w:
        solph.Transformer(label='no output',
                          inputs={look_out: "No outputs!"})
        assert len(w) == 1
        assert msg in str(w[-1].message)
