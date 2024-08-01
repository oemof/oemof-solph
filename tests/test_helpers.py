# -*- coding: utf-8 -*-

"""This module is designed to test the helper functions..

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>

SPDX-License-Identifier: MIT

"""

import os

import pytest

from oemof.solph import create_time_index
from oemof.solph import helpers


def test_creation_of_extended_path():
    """Creation of a sub-folder based on the base path failed."""
    p = helpers.extend_basic_path("test_subfolder_X345qw34_tmp")
    assert os.path.isdir(p)
    os.rmdir(p)


def test_create_time_index():
    assert len(create_time_index(2014)) == 8761
    assert len(create_time_index(2012)) == 8785  # leap year
    assert len(create_time_index(2014, interval=0.5)) == 17521
    assert len(create_time_index(2014, interval=0.5, number=10)) == 11
    assert len(create_time_index(2014, number=10)) == 11
    assert (
        str(create_time_index(2014, interval=0.5, number=10)[-1])
        == "2014-01-01 05:00:00"
    )
    assert (
        str(create_time_index(2014, interval=2, number=10)[-1])
        == "2014-01-01 20:00:00"
    )
    assert (
        str(create_time_index(interval=0.5, number=10, start="2025-01-02")[-1])
        == "2025-01-02 05:00:00"
    )
    with pytest.raises(ValueError, match="mutually exclusive"):
        create_time_index(year=2015, start="2025-01-02")
