# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""

import logging
from oemof.core.network.entities.components import transports as transport


class EnergySystem:
    r"""
    """

    def __init__(self, **kwargs):
        ''
        for attribute in ['regions', 'entities', 'simulation']:
          setattr(self, attribute, kwargs.get(attribute, {}))





class EnergyRegion:
    r"""
    """

    def __init__(self, **kwargs):
        ''
        # Diese Attribute enthalten Hilfsgrößen, die beim Erstellen oder bei
        # der Auswertung von Nutzen sind.
        self.name = kwargs.get('name')
        self._code = kwargs.get('code')
        self.geom = kwargs.get('geom')
        self.year = kwargs.get('year')

    @property
    def code(self):
        if self._code is None:
            name_parts = self.name.replace('_', ' ').split(' ', 1)
            self._code = ''
            for part in name_parts:
                self._code += part[:1].upper() + part[1:3]
        return self._code


class Simulation:
    r"""
    """

    def __init__(self, **kwargs):
        ''
        self.solver = kwargs.get('solver', 'glpk')
        self.optim_module = kwargs.get('optim_modul', 'solph')

        if self.optim_module == 'solph':
            pass

