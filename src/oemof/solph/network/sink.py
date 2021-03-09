# -*- coding: utf-8 -*-

"""Classes used to model energy supply systems within solph.

Classes are derived from oemof core network classes and adapted for specific
optimization tasks. An energy system is modelled as a graph/network of nodes
with very specific constraints on which types of nodes are allowed to be
connected.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

from oemof.network import network as on

from ._helpers import check_node_object_for_missing_attribute


class Sink(on.Sink):
    """An object with one input flow."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        check_node_object_for_missing_attribute(self, "inputs")

    def constraint_group(self):
        pass
