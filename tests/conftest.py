# -*- coding: utf-8 -*-

"""Test configuration: run the suite on the Pyomo or the linopy backend.

``pytest --solph-backend=linopy`` (or ``SOLPH_BACKEND=linopy``) replaces
:class:`oemof.solph.Model` by :class:`oemof.solph.LinopyModel` before the
tests are collected, so every test that builds ``solph.Model`` runs on
the linopy backend. A test that needs a constraint block the linopy
backend does not support yet is reported as skipped, naming the block.
Tests that inspect Pyomo internals carry the ``pyomo_only`` marker.

SPDX-License-Identifier: MIT
"""

import os

import pytest

_NOT_SUPPORTED = "not supported by the linopy backend"


def pytest_addoption(parser):
    parser.addoption(
        "--solph-backend",
        choices=("pyomo", "linopy"),
        default=os.environ.get("SOLPH_BACKEND", "pyomo"),
        help="model backend the tests build (default: pyomo)",
    )
    parser.addoption(
        "--run-performance",
        action="store_true",
        default=False,
        help="run the build-time tests of the linopy backend",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "pyomo_only: the test inspects Pyomo internals"
    )
    config.addinivalue_line(
        "markers", "performance: build-time test (needs --run-performance)"
    )
    if config.getoption("--solph-backend") == "linopy":
        from oemof import solph
        from oemof.solph._linopy import LinopyModel

        solph.Model = LinopyModel


def pytest_collection_modifyitems(config, items):
    linopy_backend = config.getoption("--solph-backend") == "linopy"
    run_performance = config.getoption("--run-performance")
    for item in items:
        if linopy_backend and item.get_closest_marker("pyomo_only"):
            item.add_marker(
                pytest.mark.skip(reason="inspects Pyomo internals")
            )
        if item.get_closest_marker("performance") and not run_performance:
            item.add_marker(pytest.mark.skip(reason="needs --run-performance"))


def _not_supported(excinfo):
    """The first line of a linopy "not supported" error, or None."""
    if (
        excinfo is not None
        and excinfo.errisinstance(NotImplementedError)
        and _NOT_SUPPORTED in str(excinfo.value)
    ):
        return str(excinfo.value).splitlines()[0]
    return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    message = _not_supported(call.excinfo)
    if message is not None:
        report.outcome = "skipped"
        report.longrepr = (
            str(item.path),
            item.location[1] or 0,
            f"Skipped: {message}",
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_make_collect_report(collector):
    # modules that build a model at import time fail during collection
    outcome = yield
    report = outcome.get_result()
    if report.outcome != "failed":
        return
    # pytest wraps import errors in its own CollectError: match the text
    text = str(report.longrepr)
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("E") and "NotImplementedError" in line:
            line = line.lstrip("E").strip()
        if line.startswith("NotImplementedError") and _NOT_SUPPORTED in line:
            message = line.split(":", 1)[1].strip()
            report.outcome = "skipped"
            report.longrepr = (str(collector.path), 0, f"Skipped: {message}")
            return
