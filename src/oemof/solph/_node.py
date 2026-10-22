# -*- coding: utf-8 -*-

"""
A Node to be used as base class in solph models

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt (DLR)
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

from oemof import network


class Node(network.Node):
    def __init__(
        self,
        label,
        *,
        inputs=None,
        outputs=None,
        parent_node=None,
        custom_properties=None,
    ):
        super().__init__(
            label,
            inputs=inputs,
            outputs=outputs,
            parent_node=parent_node,
            custom_properties=custom_properties,
        )

    def required_blocks(self):
        return []
