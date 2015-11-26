# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""

import logging
from oemof.core.network.entities.components import transports as transport
from oemof.solph.optimization_model import OptimizationModel as OM


class EnergySystem:
    r"""
    """

    def __init__(self, **kwargs):
        ''
        for attribute in ['regions', 'entities', 'simulation']:
            setattr(self, attribute, kwargs.get(attribute, {}))
        self.optimization_model = kwargs.get('optimization_model', None)

    # TODO: Condense signature (use Buse)
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

    def optimize(self):

        if self.optimization_model is None:
            self.optimization_model = OM(energysystem=self)

        self.optimization_model.solve(solver=self.simulation.solver,
                                      debug=self.simulation.debug,
                                      tee=self.simulation.stream_solver_output,
                                      duals=self.simulation.duals)


class Region:
    r"""
    """

    def __init__(self, **kwargs):
        ''
        self.entities = []  # list of entities
        self.add_entities(kwargs.get('entities', []))

        self.name = kwargs.get('name')
        self._code = kwargs.get('code')
        self.geom = kwargs.get('geom')

    # TODO: oder sollte das ein setter sein? Yupp.
    def add_entities(self, entities):
        'add list of components to self.components'
        # TODO: prevent duplicate entries
        self.entities.extend(entities)
        for entity in entities:
            if self not in entity.regions:
                entity.regions.append(self)

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
        self.debug = kwargs.get('debug', False)
        self.stream_solver_output = kwargs.get('stream_solver_output', False)
        self.objective_options = kwargs.get('objective_options', {})
        self.duals = kwargs.get('duals', False)
        self.timesteps = kwargs.get('timesteps', None)
        if self.timesteps is None:
            raise ValueError('No timesteps defined!')
