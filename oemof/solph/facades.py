# -*- coding: utf-8 -*-
""" This module is desined to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application.
"""
from oemof.solph import Source, Flow


class Generator(Source):
    """
    """
    def __init__(self, **kwargs):
        super().__init__()

        self.Pmax = kwargs.get('Pmax', None)

        self.bus = kwargs.get('bus', None)

        self.opex = kwargs.get('opex', 0)

        self.flh = kwargs.get('flh', (None, None))

        self.outputs.update({self.bus: Flow(nominal_value=self.Pmax,
                                            variable_costs=self.opex)})
