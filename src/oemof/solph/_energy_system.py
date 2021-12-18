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
        self._extract_periods_years()

    def _add_periods(self, periods):
        """Returns periods to be added to the energy system

        * For a standard model, periods only contain one value {0: 0}
        * For a multi-period model, periods are based on the years used in the
          timeindex. As a default, each year in the timeindex is mapped to
          its own period.

        Parameters
        ----------
        periods : dict
            Periods of a (multi-period) model
            Keys are periods as increasing integer values, starting from 0,
            values are the periods defined by a pandas.date_range
            For a standard model, only one period is used.

        Returns
        -------
        periods : dict
            Periods of the energy system (ensure it being set)
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

    def _extract_periods_years(self):
        """Map simulation years to the respective period based on timeindices

        * `periods_years` is the simulation year corresponding to the start
          of a period, starting with 0
        """
        periods_years = {0: 0}
        if self.multi_period:
            start_year = self.periods[0].min().year
            for k, v in self.periods.items():
                if k >= 1:
                    periods_years[k] = v.min().year - start_year

        self.periods_years = periods_years
