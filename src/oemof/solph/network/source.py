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

from ._helpers import check_node_object_for_missing_attribute


class Source(on.Source):
    """An object with one output flow."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        check_node_object_for_missing_attribute(self, "outputs")

    def constraint_group(self):
        pass
