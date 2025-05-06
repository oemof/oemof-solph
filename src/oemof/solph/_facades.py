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
    def __init__(self,*args,**kwargs):
        self.facade_type = None

    def add_subnode(self,*args):
        """Add a subnode to the subnetwork"""
        for sub_component in args:
            sub_component.label = self._sub_component_labelling(sub_component.label)
            super(self).add_subnode(sub_component)

    def build_subnetwork(self):
        """Instanciate and add Node instance to the sub network"""
        pass

    def _sub_component_labelling(self, sub_component_label):
        """Method to always keep the Facade instance label in its subcomponents"""
        return f"{self.label}_{sub_component_label}"
