# -*- coding: utf-8 -

"""Regression tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/regression_tests.py

SPDX-License-Identifier: MIT
"""

import logging

import pandas as pd
import pytest

from oemof import solph
from oemof import tools
from oemof.solph._models import LoggingError


def test_version_metadata():
    assert solph.__version__


def test_wrong_logging_level():
    datetimeindex = pd.date_range("1/1/2012", periods=12, freq="h")
    es = solph.EnergySystem(timeindex=datetimeindex, infer_last_interval=True)
    tools.logger.define_logging()
    my_logger = logging.getLogger()
    my_logger.setLevel("DEBUG")
    with pytest.raises(LoggingError, match="The root logger level is 'DEBUG'"):
        solph.Model(es)
    my_logger.setLevel("WARNING")
