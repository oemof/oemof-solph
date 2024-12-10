# -*- coding: utf-8 -*-

"""
In-development electrical bus component.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: jakob-wo
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from oemof.solph.buses._bus import Bus


class ElectricalBus(Bus):
    r"""An electrical bus object used for linear optimal power flow (LOPF)

    Every (spatial) node has to be connected to a BusBlock.
    This BusBlock is used in combination with ElectricalLine objects
    for linear optimal power flow (lopf) calculations.

    Parameters
    ----------
    slack: boolean
        If True BusBlock is slack bus for electrical network
    v_max: numeric
        Maximum value of voltage angle at electrical bus
    v_min: numeric
        Mininum value of voltage angle at electrical bus

    Note: This component is experimental. Use it with care.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph._bus.BusBlock`
    The objects are also used inside:
     * :py:class:`~oemof.solph.experimental._electrical_line.ElectricalLine`

    """

    def __init__(
        self,
        label=None,
        *,
        v_max,
        v_min,
        inputs=None,
        outputs=None,
        custom_properties=None,
        slack=False,
    ):
        super().__init__(
            label,
            inputs=inputs,
            outputs=outputs,
            custom_properties=custom_properties,
        )
        self.slack = slack
        self.v_max = v_max
        self.v_min = v_min
