# -*- coding: utf-8 -*-

"""
Solph Facade based on oemof.network.SubNetwork

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Pierre-François Duc

SPDX-License-Identifier: MIT

"""

from oemof.network import SubNetwork


class Facade(SubNetwork):
    # attributes
    def __init__(self, label, facade_type, *args, parent_node=None, **kwargs):
        super().__init__(label=label, parent_node=parent_node)
        self.facade_type = facade_type
        self.define_subnetwork()

    def define_subnetwork(self):
        pass

    def add_subnetwork(self):
        """Instanciate and add Node instance to the sub network"""
        pass

    def sub_label_error(self, sub_component):
        msg = (
            f"Sublabel ERROR in Facade instance:\n{self.label}, "
            f"{self.facade_type}, {sub_component}, "
            f"{sub_component.custom_properties}"
        )
        raise AttributeError(msg)
