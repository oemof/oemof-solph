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
    timeindex : sequence of ascending numeric values
        Typically a pandas.DatetimeIndex is used,
        but for example also a list of floats works.

    infer_last_interval : bool
        Add an interval to the last time point. The end time of this interval
        is unknown so it does only work for an equidistant DatetimeIndex with
        a 'freq' attribute that is not None. The parameter has no effect on the
        timeincrement parameter.

    periods : list or None
        The periods of a multi-period model.
        If this is explicitly specified, it leads to creating a multi-period
        model, providing a respective user warning as a feedback.

        list of pd.date_range objects carrying the timeindex for the
        respective period;

        For a standard model, periods are not (to be) declared, i.e. None.
        A list with one entry is derived, i.e. [0].

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

    use_remaining_value : bool
        If True, compare the remaining value of an investment to the
        original value (only applicable for multi-period models)

    kwargs
    """

    def __init__(
        self,
        timeindex=None,
        timeincrement=None,
        infer_last_interval=False,
        periods=None,
        tsa_parameters=None,
        use_remaining_value=False,
        groupings=None,
    ):
        # Doing imports at runtime is generally frowned upon, but should work
        # for now. See the TODO in :func:`constraint_grouping
        # <oemof.solph.groupings.constraint_grouping>` for more information.
        from oemof.solph import GROUPINGS

        if groupings is None:
            groupings = []
        groupings = GROUPINGS + groupings

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
        if timeincrement is not None:
            if timeindex is None:
                msg = (
                    "Initialising an EnergySystem using a timeincrement"
                    " is deprecated. Please give a timeindex instead."
                )
                warnings.warn(msg, FutureWarning)
            else:
                if periods is None:
                    msg = (
                        "Specifying the timeincrement and the timeindex"
                        " parameter at the same time is not allowed since"
                        " these might be conflicting to each other."
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
                try:
                    df = pd.DataFrame(timeindex)
                except ValueError:
                    raise ValueError("Invalid timeindex.")
                timedelta = df.diff()
                if isinstance(timeindex, pd.DatetimeIndex):
                    timeincrement = timedelta / np.timedelta64(1, "h")
                else:
                    timeincrement = timedelta
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
            if periods is not None:
                for p in range(len(periods)):
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
            timeincrement, timeindex, periods, tsa_parameters
        )
        super().__init__(
            groupings=groupings,
            timeindex=timeindex,
            timeincrement=timeincrement,
        )

        self.periods = periods
        if self.periods is not None:
            msg = (
                "CAUTION! You specified the 'periods' attribute for your "
                "energy system.\n This will lead to creating "
                "a multi-period optimization modeling which can be "
                "used e.g. for long-term investment modeling.\n"
                "Please be aware that the feature is experimental as of "
                "now. If you find anything suspicious or any bugs, "
                "please report them."
            )
            warnings.warn(msg, debugging.ExperimentalFeatureWarning)
            self._extract_periods_years()
            self._extract_periods_matrix()
            self._extract_end_year_of_optimization()
            self.use_remaining_value = use_remaining_value
        else:
            self.end_year_of_optimization = 1

    def _extract_periods_years(self):
        """Map years in optimization to respective period based on time indices

        Attribute `periods_years` of type list is set. It contains
        the year of the start of each period, relative to the
        start of the optimization run and starting with 0.
        """
        periods_years = [0]
        start_year = self.periods[0].min().year
        for k, v in enumerate(self.periods):
            if k >= 1:
                periods_years.append(v.min().year - start_year)

        self.periods_years = periods_years

    def _extract_periods_matrix(self):
        """Determines a matrix describing the temporal distance to each period.

        Attribute `periods_matrix` of type list np.array is set.
        Rows represent investment/commissioning periods, columns represent
        decommissioning periods. The values describe the temporal distance
        between each investment period to each decommissioning period.
        """
        periods_matrix = []
        period_years = np.array(self.periods_years)
        for v in period_years:
            row = period_years - v
            row = np.where(row < 0, 0, row)
            periods_matrix.append(row)
        self.periods_matrix = np.array(periods_matrix)

    def _extract_end_year_of_optimization(self):
        """Extract the end of the optimization in years

        Attribute `end_year_of_optimization` of int is set.
        """
        duration_last_period = self.get_period_duration(-1)
        self.end_year_of_optimization = (
            self.periods_years[-1] + duration_last_period
        )

    def get_period_duration(self, period):
        """Get duration of a period in full years

        Parameters
        ----------
        period : int
            Period for which the duration in years shall be obtained

        Returns
        -------
        int
            Duration of the period
        """
        return (
            self.periods[period].max().year
            - self.periods[period].min().year
            + 1
        )

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
