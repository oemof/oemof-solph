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
    """

    def __init__(
        self, timeindex=None, timeincrement=None, mode="implicit", **kwargs
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

        if mode == "implicit" and timeindex is not None:
            # Add one timestep to the timeindex.
            timeindex = timeindex.union(
                pd.date_range(
                    timeindex[-1] + timeindex.freq,
                    periods=1,
                    freq=timeindex.freq,
                )
            )

        if timeincrement is not None and timeindex is not None:
            raise AttributeError("Don't do it.")

        elif timeincrement is None and timeindex is None:
            pass

        elif timeindex is not None and timeincrement is None:
            df = pd.DataFrame(timeindex)
            timedelta = df.diff()
            timeincrement = (
                (timedelta / np.timedelta64(1, "h"))[1:].set_index(0).index
            )

        if mode == "implicit" and timeindex is not None:
            timeindex = timeindex[1:]

        super().__init__(
            timeindex=timeindex, timeincrement=timeincrement, **kwargs
        )
