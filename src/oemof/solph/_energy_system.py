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

import collections
import itertools
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

    investment_times : list or None
        The points in time investments can be made. Defaults to timeindex[0].
        If multiple times are specified, it leads to creating a multi-period
        model.

    tsa_parameters : list of dicts, dict or None
        Parameter can be set in order to use aggregated timeseries from TSAM.
        If multi-period model is used, one dict per period has to be set.
        If no multi-period (aka single period) approach is selected, a single
        dict can be provided.
        If parameter is None, model is set up as usual.

        Dict must contain keys `timesteps_per_period`
        (from TSAMs `hoursPerPeriod`), `order` (from TSAMs `clusterOrder`) and
        `occurrences` (from TSAMs `clusterPeriodNoOccur`).
        When activated, storage equations and flow rules for full_load_time
        will be adapted. Note that timeseries for components have to
        be set up as already aggregated timeseries.

    kwargs
    """

    def __init__(
        self,
        timeindex=None,
        timeincrement=None,
        infer_last_interval=None,
        investment_times=None,
        tsa_parameters=None,
        groupings=None,
    ):
        # Doing imports at runtime is generally frowned upon, but should work
        # for now. See the TODO in :func:`constraint_grouping
        # <oemof.solph.groupings.constraint_grouping>` for more information.
        from oemof.solph import GROUPINGS

        if groupings is None:
            groupings = []
        groupings = GROUPINGS + groupings

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
            if investment_times is None:
                msg = (
                    "Specifying the timeincrement and the timeindex parameter "
                    "at the same time is not allowed since these might be "
                    "conflicting to each other."
                )
                raise AttributeError(msg)
            else:
                msg = (
                    "Ensure that your timeindex and timeincrement are "
                    "consistent."
                )
                warnings.warn(msg, debugging.ExperimentalFeatureWarning)

        elif timeindex is not None and timeincrement is None:
            if tsa_parameters is not None:
                pass
            else:
                df = pd.DataFrame(timeindex)
                timedelta = df.diff()
                timeincrement = timedelta / np.timedelta64(1, "h")

                # we want a series (squeeze)
                # without the first item (no delta defined for first entry)
                # but starting with index 0 (reset)
                timeincrement = timeincrement.squeeze()[1:].reset_index(
                    drop=True
                )

        if timeincrement is not None and (pd.Series(timeincrement) <= 0).any():
            msg = (
                "The time increment is inconsistent. Negative values and zero "
                "are not allowed.\nThis is caused by a inconsistent "
                "timeincrement parameter or an incorrect timeindex."
            )
            raise TypeError(msg)
        if tsa_parameters is not None:
            msg = (
                "CAUTION! You specified the 'tsa_parameters' attribute for "
                "your energy system.\n This will lead to setting up "
                "energysystem with aggregated timeseries. "
                "Storages and flows will be adapted accordingly.\n"
                "Please be aware that the feature is experimental as of "
                "now. If you find anything suspicious or any bugs, "
                "please report them."
            )
            warnings.warn(msg, debugging.SuspiciousUsageWarning)

            if isinstance(tsa_parameters, dict):
                # Set up tsa_parameters for single period:
                tsa_parameters = [tsa_parameters]

            # Construct occurrences of typical periods
            if investment_times is not None:
                for p in range(len(investment_times)):
                    tsa_parameters[p]["occurrences"] = collections.Counter(
                        tsa_parameters[p]["order"]
                    )
            else:
                tsa_parameters[0]["occurrences"] = collections.Counter(
                    tsa_parameters[0]["order"]
                )

            # If segmentation is used, timesteps is set to number of
            # segmentations per period.
            # Otherwise, default timesteps_per_period is used.
            for params in tsa_parameters:
                if "segments" in params:
                    params["timesteps"] = int(
                        len(params["segments"]) / len(params["occurrences"])
                    )
                else:
                    params["timesteps"] = params["timesteps_per_period"]
        self.tsa_parameters = tsa_parameters

        timeincrement = self._init_timeincrement(
            timeincrement, timeindex, investment_times, tsa_parameters
        )
        super().__init__(
            groupings=groupings,
            timeindex=timeindex,
            timeincrement=timeincrement,
        )

        self.investment_times = investment_times

    @staticmethod
    def _init_timeincrement(timeincrement, timeindex, periods, tsa_parameters):
        """Check and initialize timeincrement"""

        # Timeincrement in TSAM mode
        if (
            timeincrement is not None
            and tsa_parameters is not None
            and any("segments" in params for params in tsa_parameters)
        ):
            msg = (
                "You must not specify timeincrement in TSAM mode. "
                "TSAM will define timeincrement itself."
            )
            raise AttributeError(msg)
        if (
            tsa_parameters is not None
            and any("segments" in params for params in tsa_parameters)
            and not all("segments" in params for params in tsa_parameters)
        ):
            msg = (
                "You have to set up segmentation in all periods, "
                "if you want to use segmentation in TSAM mode"
            )
            raise AttributeError(msg)
        if tsa_parameters is not None and all(
            "segments" in params for params in tsa_parameters
        ):
            # Concatenate segments from TSAM parameters to get timeincrement
            return list(
                itertools.chain(
                    *[params["segments"].values() for params in tsa_parameters]
                )
            )

        elif timeindex is not None and timeincrement is None:
            df = pd.DataFrame(timeindex)
            timedelta = df.diff()
            timeincrement = timedelta / np.timedelta64(1, "h")

            # we want a series (squeeze)
            # without the first item (no delta defined for first entry)
            # but starting with index 0 (reset)
            return timeincrement.squeeze()[1:].reset_index(drop=True)

        return timeincrement
