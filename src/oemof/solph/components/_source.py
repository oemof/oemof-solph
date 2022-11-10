# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Source

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

from oemof.network import network as on

from oemof.solph._helpers import check_node_object_for_missing_attribute


class Source(on.Source):
    """An object with one output flow."""

    def __init__(self, label=None, outputs=None, **kwargs):
        if outputs is None:
            outputs = {}

        super().__init__(label=label, outputs=outputs, **kwargs)
        check_node_object_for_missing_attribute(self, "outputs")

    def constraint_group(self):
        pass
