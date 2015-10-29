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
        self.regions = kwargs.get('regions', {})  # list of region objects
        self.global_busses = kwargs.get('regions', {})  # list of busses
        self.sim = kwargs.get('sim')  # simulation object
        self.connections = kwargs.get('connections', {})

    def add_region(self, region):
        ''
        self.regions[region.code] = region

    def connect(self, code1, code2, media, in_max, out_max, eta, classtype):
        ''
        def trans_simp(self, reg_out, reg_in, media, in_max, out_max, eta):
            logging.debug('Creating simple connection from {0} to {1}'.format(
                code1, code2))
            return transport.Simple(
                uid='_'.join([reg_out, reg_in, media]),
                outputs=[self.regions[reg_out].busses['_'.join(
                    ['b', reg_out, media])]],
                inputs=[self.regions[reg_in].busses['_'.join(
                    ['b', reg_in, media])]],
                out_max={'_'.join(['b', reg_out, media]): out_max},
                in_max={'_'.join(['b', reg_in, media]): in_max},
                eta=[eta]
                )
        if classtype == 'simple':
            c1 = trans_simp(self, code1, code2, media, in_max, out_max, eta)
            c2 = trans_simp(self, code2, code1, media, in_max, out_max, eta)
        else:
            raise('error')

        self.connections['_'.join([code1, code2, media])] = c1
        self.connections['_'.join([code2, code1, media])] = c2


class EnergyRegion:
    r"""
    """

    def __init__(self, **kwargs):
        ''
        # Diese Attribute müssen definitiv vorhanden sein, damit solph läuft.
        self.renew_pps = kwargs.get('renew_pps', [])  # list of entities
        self.conv_pps = kwargs.get('conv_pss', [])  # list of entities
        self.sinks = kwargs.get('sinks', [])  # list of sinks
        self.busses = kwargs.get('busses', {})  # dict of busses

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
