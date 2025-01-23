# -*- coding: utf-8 -

"""Tests the console_test module, without the test_oemof function.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_processing.py

SPDX-License-Identifier: MIT
"""
from oemof.solph import _console_scripts as console_scripts


def test_console_scripts():
    # this is just a smoke test
    console_scripts.check_oemof_installation()


def test_solver_check():
    solver_list = ["cbc", "invalid solver"]
    results = console_scripts._check_oemof_installation(solver_list)

    assert isinstance(results, dict)
    assert list(results.keys()) == solver_list
    assert not results["invalid solver"]
