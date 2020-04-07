# -*- coding: utf-8 -

"""Regression tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/regression_tests.py

SPDX-License-Identifier: MIT
"""

from nose.tools import ok_
from oemof import solph


def test_version_metadata():
    ok_(solph.__version__)
