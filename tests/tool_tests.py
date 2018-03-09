# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/tool_tests.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import os

from nose.tools import ok_

from oemof.tools import logger
from oemof.tools import helpers
from oemof.tools import economics


def test_helpers():
    ok_(os.path.isdir(os.path.join(os.path.expanduser('~'), '.oemof')))
    new_dir = helpers.extend_basic_path('test_xf67456_dir')
    ok_(os.path.isdir(new_dir))
    os.rmdir(new_dir)
    ok_(not os.path.isdir(new_dir))


def test_logger():
    filepath = logger.define_logging()
    ok_(isinstance(filepath, str))
    ok_(filepath[-9:] == 'oemof.log')
    ok_(os.path.isfile(filepath))


def test_economics():
    ok_(round(economics.annuity(1000, 10, 0.1)) == 163)
