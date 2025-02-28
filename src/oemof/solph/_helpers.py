# -*- coding: utf-8 -*-

"""
Private helper functions.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: David Fuhrländer
SPDX-FileCopyrightText: Johannes Röder

SPDX-License-Identifier: MIT

"""

import calendar
import datetime
from warnings import warn

import pandas as pd
from oemof.tools import debugging


def check_node_object_for_missing_attribute(obj, attribute):
    """Raises a predefined warning if object does not have attribute.

    Arguments
    ---------

    obj : python object
    attribute : (string) name of the attribute to test for

    """
    if not getattr(obj, attribute):
        warn_if_missing_attribute(obj, attribute)


def warn_if_missing_attribute(obj, attribute):
    """Raises warning if attribute is missing for given object"""
    msg = (
        "Attribute <{0}> is missing in Node <{1}> of {2}.\n"
        "If this is intended and you know what you are doing you can"
        "disable the SuspiciousUsageWarning globally."
    )
    warn(
        msg.format(attribute, obj.label, type(obj)),
        debugging.SuspiciousUsageWarning,
    )


def create_time_index(
    year: int = None,
    interval: float = 1,
    number: int = None,
    start: datetime.date = None,
):
    """
    Create a datetime index for one year.

    Notes
    -----
    To create 8760 hourly intervals for a non leap year a datetime index with
    8761 time points need to be created. So the number of time steps is always
    the number of intervals plus one.

    Parameters
    ----------
    year : int, datetime
        The year of the index.
        Used to automatically set start and number for the specific year.
    interval : float
        The time interval in hours e.g. 0.5 for 30min or 2 for a two hour
        interval (default: 1).
    number : int
        The number of time intervals. By default number is calculated to create
        an index of one year. For a shorter or longer period the number of
        intervals can be set by the user.
    start : datetime.datetime or datetime.date
        Optional start time. If start is not set, 00:00 of the first day of
        the given year is the start time.

    Examples
    --------
    >>> len(create_time_index(2014))
    8761
    >>> len(create_time_index(2012))  # leap year
    8785
    >>> len(create_time_index(2014, interval=0.5))
    17521
    >>> len(create_time_index(2014, interval=0.5, number=10))
    11
    >>> len(create_time_index(2014, number=10))
    11
    >>> str(create_time_index(2014, interval=0.5, number=10)[-1])
    '2014-01-01 05:00:00'
    >>> str(create_time_index(2014, interval=2, number=10)[-1])
    '2014-01-01 20:00:00'
    """
    if number is None:
        if calendar.isleap(year):
            hours_in_year = 8784
        else:
            hours_in_year = 8760
        number = round(hours_in_year / interval)
    if start is not None:
        if year is not None:
            raise ValueError(
                "Arguments 'start' and 'year' are mutually exclusive."
            )
    else:
        start = f"1/1/{year}"
    try:
        time_index = pd.date_range(
            start, periods=number + 1, freq=f"{interval}h"
        )
    except ValueError:
        # Pandas <2.2 compatibility
        time_index = pd.date_range(
            start, periods=number + 1, freq=f"{interval}H"
        )
    return time_index
