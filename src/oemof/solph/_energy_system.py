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

from oemof.network import energy_system as es


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
        self.multi_period = multi_period
        self._add_periods(periods)

    def _add_periods(self, periods):
        """Add periods to the energy system

        * For a single model, periods only contain one value.
        * For a multi period model, periods must equal to years used in the
          timeindex. As a default, each year in the timeindex is mapped to
          its own period.

        Parameters
        ----------
        periods : dict
            The periods of a multi period model
            Keys are years as integer values,
            values are the respective number of the period starting with zero
        """
        if not self.multi_period:
            periods = {"single_period": 0}
        elif periods is None:
            years = sorted(
                list(
                    set(getattr(self.timeindex, 'year'))
                )
            )
            periods = dict(zip(years, range(len(years))))
        self.periods = periods
