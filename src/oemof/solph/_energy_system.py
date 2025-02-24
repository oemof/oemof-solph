# -*- coding: utf-8 -*-

"""
solph version of oemof.network.energy_system

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

import collections
import warnings

import numpy as np
import pandas as pd
from oemof import network
from oemof.tools import debugging


class EnergySystem(network.energy_system.EnergySystem):
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
    timeindex : pandas.DatetimeIndex or TimeSeriesAggregation object
        When a TimeSeriesAggregation object is passed,
        storage equations and flow rules for full_load_time
        will be adapted. Note that timeseries for components have to
        be set up as already aggregated timeseries.

    infer_last_interval : bool
        Add an interval to the last time point of a pandas.DatetimeIndex
        given as timeindex. As the end time of this interval is unknown,
        it does only work for an equidistant DatetimeIndex with
        a 'freq' attribute that is not None.
        cannot be set for TimeSeriesAggregation, as interval length is already
        defined.

    investment_times : list or None
        The points in time, investments can be made.

    kwargs
    """

    def __init__(
        self,
        timeindex,
        infer_last_interval=None,
        investment_times=None,
        groupings=None,
    ):
        # Doing imports at runtime is generally frowned upon, but should work
        # for now. See the TODO in :func:`constraint_grouping
        # <oemof.solph.groupings.constraint_grouping>` for more information.
        from oemof.solph import GROUPINGS

        if groupings is None:
            groupings = []
        groupings = GROUPINGS + groupings

        (timeincrement, plain_timeindex, tsa_parameters) = (
            self._organise_timeaxis(
                timeindex,
                infer_last_interval,
            )
        )

        self.tsa_parameters = tsa_parameters

        super().__init__(
            groupings=groupings,
            timeindex=plain_timeindex,
            timeincrement=timeincrement,
        )

        self.end_year_of_optimization = 1

    @staticmethod
    def _calculate_timeincrement(timeindex):
        df = pd.DataFrame(timeindex)
        timedelta = df.diff()
        timeincrement = timedelta / np.timedelta64(1, "h")

        # we want a series (squeeze)
        # without the first item (no delta defined for first entry)
        # but starting with index 0 (reset)
        timeincrement = timeincrement.squeeze()[1:].reset_index(drop=True)
        return timeincrement

    @staticmethod
    def _organise_timeaxis(timeindex, infer_last_interval):
        """Check and initialize timeincrement"""

        if isinstance(timeindex, pd.DatetimeIndex):
            plain_timeindex = timeindex
            if infer_last_interval is True:
                # Add one interval to the timeindex by adding one time point.
                if plain_timeindex.freq is None:
                    msg = (
                        "You cannot infer the last interval if the 'freq' "
                        "attribute of your DatetimeIndex is None. Set "
                        " 'infer_last_interval=False' or specify a "
                        "DatetimeIndex with a valid frequency."
                    )
                    raise AttributeError(msg)

                plain_timeindex = plain_timeindex.union(
                    pd.date_range(
                        plain_timeindex[-1] + plain_timeindex.freq,
                        periods=1,
                        freq=plain_timeindex.freq,
                    )
                )
            tsa_parameters = {
                "occurrences": [1],
                "order": [0],
                "timesteps_per_period": len(timeindex),
            }
            time_increment = EnergySystem._calculate_timeincrement(
                plain_timeindex
            )
        else:
            msg = (
                "CAUTION! You specified TimeSeriesAggregation for "
                "your energy system.\n This will lead to setting up "
                "energysystem with aggregated timeseries. "
                "Storages and flows will be adapted accordingly.\n"
                "Please be aware that the feature is experimental as of "
                "now. If you find anything suspicious or any bugs, "
                "please report them."
            )
            warnings.warn(msg, debugging.ExperimentalFeatureWarning)
            try:
                plain_timeindex = timeindex.timeIndex

                time_increment = list(
                    timeindex.segmentDurationDict["Segment Duration"].values()
                )

                time_increment = (
                    np.array(time_increment) * timeindex.resolution
                )

                tsa_parameters = {
                    "occurrences": collections.Counter(timeindex.clusterOrder),
                    "order": timeindex.clusterOrder,
                    "timesteps_per_period": int(
                        round(timeindex.hoursPerPeriod // timeindex.resolution)
                    ),
                }

            except:
                raise TypeError(
                    "timeindex needs to be either of type pd.DatetimeIndex or "
                    "of type TimeSeriesAggregation (or compatible)."
                )
            if infer_last_interval is True:
                msg = (
                    "You cannot infer the last interval "
                    "for aggregated time series."
                )
                raise AttributeError(msg)

        return time_increment, plain_timeindex, tsa_parameters
