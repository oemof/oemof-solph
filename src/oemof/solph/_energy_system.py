# -*- coding: utf-8 -*-

"""
solph version of oemof.network.energy_system

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

import calendar
import warnings

import numpy as np
import pandas as pd
from oemof.network import energy_system as es
from oemof.tools import debugging


class EnergySystem(es.EnergySystem):
    """A variant of the class EnergySystem from
    <oemof.network.network.energy_system.EnergySystem> specially tailored to
    solph.

    In order to work in tandem with solph, instances of this class always use
    solph.GROUPINGS <oemof.solph.GROUPINGS>. If custom groupings are
    supplied via the `groupings` keyword argument, solph.GROUPINGS
    <oemof.solph.GROUPINGS> is prepended to those.

    If you know what you are doing and want to use solph without
    solph.GROUPINGS <oemof.solph.GROUPINGS>, you can just use
    EnergySystem <oemof.network.network.energy_system.EnergySystem>` of
    oemof.network directly.

    Parameters
    ----------
    timeindex : pandas.DatetimeIndex

    timeincrement : iterable

    infer_last_interval : bool
        Add an interval to the last time point. The end time of this interval
        is unknown so it does only work for an equidistant DatetimeIndex with
        a 'freq' attribute that is not None. The parameter has no effect on the
        timeincrement parameter.

    multi_period : boolean
        If True, a multi-period model is used; defaults to False

    periods : dict
        The periods of a multi-period model;
        Keys are the numbers of the respective period, starting with zero,
        values are pd.date_range objects carrying the timeindex for the
        respective period;
        For a standard model, periods only holds one entry, i.e. {0: 0}

    freq : str
        The frequency of a multi-period model;
        Defaults to "H"

    kwargs
    """

    def __init__(
        self,
        timeindex=None,
        timeincrement=None,
        infer_last_interval=None,
        multi_period=False,
        periods=None,
        freq="H",
        **kwargs,
    ):
        # Doing imports at runtime is generally frowned upon, but should work
        # for now. See the TODO in :func:`constraint_grouping
        # <oemof.solph.groupings.constraint_grouping>` for more information.
        from oemof.solph import GROUPINGS

        kwargs["groupings"] = GROUPINGS + kwargs.get("groupings", [])

        if not (
            isinstance(timeindex, pd.DatetimeIndex)
            or isinstance(timeindex, type(None))
        ):
            msg = (
                "Parameter 'timeindex' has to be of type "
                "pandas.DatetimeIndex or NoneType and not of type {0}"
            )
            raise TypeError(msg.format(type(timeindex)))

        if infer_last_interval is None and timeindex is not None:
            msg = (
                "The default behaviour will change in future versions.\n"
                "At the moment the last interval of an equidistant time "
                "index is added implicitly by default. Set "
                "'infer_last_interval' explicitly 'True' or 'False' to avoid "
                "this warning. In future versions 'False' will be the default"
                "behaviour"
            )
            warnings.warn(msg, FutureWarning)
            infer_last_interval = True

        if infer_last_interval is True and timeindex is not None:
            # Add one time interval to the timeindex by adding one time point.
            if timeindex.freq is None:
                msg = (
                    "You cannot infer the last interval if the 'freq' "
                    "attribute of your DatetimeIndex is None. Set "
                    " 'infer_last_interval=False' or specify a DatetimeIndex "
                    "with a valid frequency."
                )
                raise AttributeError(msg)

            timeindex = timeindex.union(
                pd.date_range(
                    timeindex[-1] + timeindex.freq,
                    periods=1,
                    freq=timeindex.freq,
                )
            )

        # catch wrong combinations and infer timeincrement from timeindex.
        if timeincrement is not None and timeindex is not None:
            if not multi_period:
                msg = (
                    "Specifying the timeincrement and the timeindex parameter "
                    "at the same time is not allowed since these might be "
                    "conflicting to each other."
                )
                raise AttributeError(msg)
            else:
                msg = (
                    "Ensure that your timeindex and timeincrement are "
                    "consistent.\nIf you are not considering non-equidistant "
                    "timeindices, consider only specifying a timeindex."
                )
                warnings.warn(msg, debugging.SuspiciousUsageWarning)

        elif timeindex is not None and timeincrement is None:
            df = pd.DataFrame(timeindex)
            timedelta = df.diff()
            timeincrement = pd.Series(
                (timedelta / np.timedelta64(1, "h"))[1:].set_index(0).index
            )

        if timeincrement is not None and (pd.Series(timeincrement) <= 0).any():
            msg = (
                "The time increment is inconsistent. Negative values and zero "
                "is not allowed.\nThis is caused by a inconsistent "
                "timeincrement parameter or an incorrect timeindex."
            )
            raise TypeError(msg)

        super().__init__(
            timeindex=timeindex, timeincrement=timeincrement, **kwargs
        )

        if multi_period:
            msg = (
                "CAUTION! You specified 'multi_period=True' for your "
                "energy system.\n This will lead to creating "
                "a multi-period optimization modeling which can be "
                "used e.g. for long-term investment modeling.\n"
                "Please be aware that the feature is experimental as of "
                "now. If you find anything suspicious or any bugs, "
                "please report them."
            )
            warnings.warn(msg, debugging.SuspiciousUsageWarning)
        self.multi_period = multi_period
        self.periods = self._add_periods(periods, freq)
        self._extract_periods_years()

    def _add_periods(self, periods, freq="H"):
        """Returns periods to be added to the energy system

        * For a standard model, periods only contain one value {0: 0}
        * For a multi-period model, periods are indexed with integer values
          starting from zero. The keys are the time indices for the resective
          period given by a pd.date_range object. As a default,
          each year in the timeindex is mapped to its own period.

        Parameters
        ----------
        periods : dict
            Periods of a (multi-period) model
            Keys are periods as increasing integer values, starting from 0,
            values are the periods defined by a pd.date_range object;
            For a standard model, only one period is used.

        freq : str
            The frequency of a multi-period model;
            Defaults to "H"

        Returns
        -------
        periods : dict
            Periods of the energy system (to ensure it being set)
        """
        if not self.multi_period:
            periods = {0: 0}
        elif periods is None:
            years = sorted(list(set(getattr(self.timeindex, "year"))))

            periods = {}
            filter_series = self.timeindex.to_series()
            for number, year in enumerate(years):
                start = filter_series.loc[
                    filter_series.index.year == year
                ].min()
                end = filter_series.loc[filter_series.index.year == year].max()
                periods[number] = pd.date_range(start, end, freq=freq)
        else:
            for k in periods.keys():
                if not isinstance(k, int):
                    raise ValueError("Period keys must be of type int.")

        return periods

    def _extract_periods_years(self):
        """Map simulation years to the respective period based on time indices

        Returns
        -------
        periods_years: dict
            the simulation year of the start of each a period,
            relative to the start of the optimization rund and starting with 0
        """
        periods_years = {0: 0}
        if self.multi_period:
            start_year = self.periods[0].min().year
            for k, v in self.periods.items():
                if k >= 1:
                    periods_years[k] = v.min().year - start_year

        self.periods_years = periods_years


def create_time_index(year, interval=1, number=None):
    """
    Create a datetime index for one year.

    Notes
    -----
    To create 8760 hourly intervals for a non leap year a datetime index with
    8761 time points need to be created. So the number of time steps is always
    the number of intervals plus one.

    Parameters
    ----------
    year : int
        The year of the index.
    interval : float
        The time interval in hours e.g. 0.5 for 30min or 2 for a two hour
        interval (default: 1).
    number : int
        The number of time intervals. By default number is calculated to create
        an index of one year. For a shorter or longer period the number of
        intervals can be set by the user.

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
            hoy = 8784
        else:
            hoy = 8760
        number = round(hoy / interval)
    return pd.date_range(
        f"1/1/{year}", periods=number + 1, freq=f"{interval}H"
    )
