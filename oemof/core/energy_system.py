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
        for attribute in ['regions', 'global_buses', 'sim', 'connections']:
          setattr(self, attribute, kwargs.get(attribute, {}))

    def add_region(self, region):
        ''
        self.regions[region.code] = region

    def connect(self, code1, code2, media, in_max, out_max, eta,
                transport_class):
        ''
        if not transport_class == transport.Simple:
            raise(TypeError(
                    "Sorry, `EnergySystem.connect` currently only works with" +
                    "a `transport_class` argument of" + str(transport.Simple)))
        for reg_out, reg_in in [(code1, code2), (code2, code1)]:
            logging.debug('Creating simple {2} from {0} to {1}'.format(
                    reg_out, reg_in, transport_class))
            uid = '_'.join([reg_out, reg_in, media])
            self.connections[uid] = transport_class(
                uid=uid,
                outputs=[self.regions[reg_out].buses['_'.join(
                    ['b', reg_out, media])]],
                inputs=[self.regions[reg_in].buses['_'.join(
                    ['b', reg_in, media])]],
                out_max={'_'.join(['b', reg_out, media]): out_max},
                in_max={'_'.join(['b', reg_in, media]): in_max},
                eta=[eta]
                )


class EnergyRegion:
    r"""
    """

    def __init__(self, **kwargs):
        ''
        # Diese Attribute müssen definitiv vorhanden sein, damit solph läuft.
        self.renew_pps = kwargs.get('renew_pps', [])  # list of entities
        self.conv_pps = kwargs.get('conv_pss', [])  # list of entities
        self.sinks = kwargs.get('sinks', [])  # list of sinks
        self.buses = kwargs.get('buses', {})  # dict of buses

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
        pass
