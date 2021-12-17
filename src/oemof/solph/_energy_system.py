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
import warnings

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
    """

    def __init__(self, multi_period=False, periods=None, **kwargs):
        """Initialize an EnergySystem

        Parameters
        ----------
        multi_period : boolean
            If True, a multi period model is used; defaults to False

        periods : dict
            The periods of a multi period model
            Keys are years as integer values,
            values are the respective number of the period starting with zero
        """
        # Doing imports at runtime is generally frowned upon, but should work
        # for now. See the TODO in :func:`constraint_grouping
        # <oemof.solph.groupings.constraint_grouping>` for more information.
        from oemof.solph import GROUPINGS

        kwargs["groupings"] = GROUPINGS + kwargs.get("groupings", [])

        super().__init__(**kwargs)

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
        self.periods = self._add_periods(periods)
        self._extract_periods_lengths_gap_and_years()

    def _add_periods(self, periods):
        """Returns periods to be added to the energy system

        * For a standard model, periods only contain one value.
        * For a multi-period model, periods are based on the years used in the
          timeindex. As a default, each year in the timeindex is mapped to
          its own period.

        Parameters
        ----------
        periods : dict
            Periods of a (multi-period) model
            Keys are years as integer values,
            values are the periods defined by their first and last timestep.
            For a standard model, only one period is used.

        Returns
        -------
        periods : dict
            Periods of the energy system
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
                periods[number] = pd.date_range(start, end, freq="H")
        else:
            for k in periods.keys():
                if not isinstance(k, int):
                    raise ValueError("Period keys must be of type int.")

        return periods

    # TODO: Check if length and gap are needed (no decommissions within period)
    def _extract_periods_lengths_gap_and_years(self):
        """Determine length of one and difference between subsequent periods
        and map periods to simulation years starting with 0

        * `periods_length` contains the length of a period in full years
        * `periods_gap` is the difference in years between subsequent periods,
          attributed to the prior one
        * `periods_years` is the simulation year corresponding to the start
          of a period, starting with 0
        """
        periods_gap = {}
        if not self.multi_period:
            periods_length = {0: 1}
            periods_years = {0: 0}
        else:
            periods_length = {}
            periods_years = {0: 0}

            previous_end = None
            for k, v in self.periods.items():
                periods_length[k] = v.max().year - v.min().year + 1
                if k >= 1:
                    periods_gap[k - 1] = v.min().year - previous_end.year - 1
                    periods_years[k] = sum(
                        periods_length[kk] + periods_gap[kk] for kk in range(k)
                    )
                previous_end = v.max()

        self.periods_length = periods_length
        self.periods_gap = periods_gap
        self.periods_years = periods_years
