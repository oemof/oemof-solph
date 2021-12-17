# -*- coding: utf-8 -*-

"""
solph version of oemof.network.energy_system

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

import numpy as np
import pandas as pd
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

    Parameters
    ----------
    timeindex : pandas.DatetimeIndex

    timeincrement : iterable

    timemode
    kwargs
    """

    def __init__(
        self,
        timeindex=None,
        timeincrement=None,
        infer_last_interval=True,
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
                "pandas.datetimeindex or NoneType and not of type {0}"
            )
            raise TypeError(msg.format(type(timeindex)))

        if infer_last_interval is True:
            self.timemode = "implicit"
        else:
            self.timemode = "explicit"

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
            msg = (
                "Specifying the timeincrement and the timeindex parameter at "
                "the same time is not allowed since these might be "
                "conflicting to each other."
            )
            raise AttributeError(msg)

        elif timeincrement is None and timeindex is None:
            msg = (
                "You have to either define the parameter timeincrement or "
                "timeindex to initialise a valid EnergySystem."
            )
            raise AttributeError(msg)

        elif timeindex is not None and timeincrement is None:
            df = pd.DataFrame(timeindex)
            timedelta = df.diff()
            timeincrement = (
                (timedelta / np.timedelta64(1, "h"))[1:].set_index(0).index
            )

        super().__init__(
            timeindex=timeindex, timeincrement=timeincrement, **kwargs
        )
