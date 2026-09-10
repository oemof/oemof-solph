# -*- coding: utf-8 -*-

"""
Link to connect two Busses.

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

from oemof.network import Node

from ._converter import Converter


class Link(Node):
    """A Link object with 2 inputs and 2 outputs.

    Parameters
    ----------
    inputs : dict
        Dictionary with inflows. Keys must be the starting node(s) of the
        inflow(s).
    outputs : dict
        Dictionary with outflows. Keys must be the ending node(s) of the
        outflow(s).
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of each flow.
        Keys are the connected tuples (input, output) bus objects.
        The dictionary values can either be a scalar or an iterable with length
        of time horizon for simulation.

    Notes
    -----
    The sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.components._link.LinkBlock`

    Examples
    --------

    >>> from oemof import solph
    >>> bel0 = solph.buses.Bus(label="el0")
    >>> bel1 = solph.buses.Bus(label="el1")

    >>> link = solph.components.Link(
    ...    label="transshipment_link",
    ...    inputs={bel0: solph.flows.Flow(nominal_capacity=4),
    ...            bel1: solph.flows.Flow(nominal_capacity=2)},
    ...    outputs={bel0: solph.flows.Flow(),
    ...             bel1: solph.flows.Flow()},
    ...    conversion_factors={(bel0, bel1): 0.8, (bel1, bel0): 0.9})
    """

    def __init__(
        self,
        label=None,
        inputs=None,
        outputs=None,
        parent_node=None,
        conversion_factors=None,
        custom_properties=None,
    ):
        # compatibility with omeof.network w/o explicit named arguments
        if inputs is None:
            inputs = {}
        if outputs is None:
            outputs = {}
        if custom_properties is None:
            custom_properties = {}
        super().__init__(
            label,
            parent_node=parent_node,
            custom_properties=custom_properties,
        )

        msg = (
            "Component `Link` must have exactly "
            + "2 inputs, 2 outputs, and 2 "
            + "conversion factors connecting these. You are initializing "
            + "a `Link`without obeying this specification. "
            + "If this is intended and you know what you are doing you can "
            + "disable the SuspiciousUsageWarning globally."
        )

        if (
            len(inputs) != 2
            or len(outputs) != 2
            or len(conversion_factors) != 2
        ):
            raise ValueError(msg)

        for k, v in conversion_factors.items():
            from_node = k[0]
            to_node = k[1]
            self.subnode(
                Converter,
                f"({k[0].label}) -> {k[1].label})",
                inputs={from_node: inputs[from_node]},
                outputs={to_node: outputs[to_node]},
                conversion_factors={to_node: v},
            )
