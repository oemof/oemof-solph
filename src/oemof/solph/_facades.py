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
    def __init__(self, label, facade_type, *args, **kwargs):
        super().__init__(label=label)
        self.facade_type = facade_type
        self.build_subnetwork()

    def add_subnode(self, *args):
        """Add a subnode to the subnetwork"""
        for sub_component in args:
            # ToDo: Check format of label
            super(SubNetwork).add_subnode(sub_component)

    def build_subnetwork(self):
        """Instanciate and add Node instance to the sub network"""
        pass

    def sub_component_labelling(self, sub_label):
        """
        Method to always keep the Facade instance label in its subcomponents
        """
        return f"{self.label}_{sub_label}"

    def sub_label_error(self, sub_component):
        msg = (
            f"Sublabel ERROR in Facade instance:\n{self.label}, "
            f"{self.facade_type}, {sub_component}, "
            f"{sub_component.custom_properties}"
        )
        raise AttributeError(msg)
