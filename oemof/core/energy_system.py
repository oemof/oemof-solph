# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""

import logging
from oemof.solph.optimization_model import OptimizationModel as OM


class EnergySystem:
    r"""
    """

    def __init__(self, **kwargs):
        ''
        for attribute in ['regions', 'entities', 'simulation']:
            setattr(self, attribute, kwargs.get(attribute, {}))
        self.optimization_model = kwargs.get('optimization_model', None)

    def optimize(self):

       if self.optimization_model is None:
           self.optimization_model = OM(energysystem=self)

       self.optimization_model.solve(solver=self.simulation.solver,
                                     debug=self.simulation.debug,
                                     tee=self.simulation.stream_solver_output)




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

    # TODO: oder sollte das ein setter sein? Yupp.
    def add_entities(self, entities):
        'add list of components to self.components'
        # TODO: prevent duplicate entries
        self.entities.extend(entities)
        for entity in entities:
            if self not in entity.regions:
                entity.regions.append(self)
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
        self.debug  = kwargs.get('debug', False)
        self.stream_solver_output = kwargs.get('stream_solver_output', False)
        self.objective_name = kwargs.get('objective_name', 'minimize_costs')

        self.timesteps = kwargs.get('timesteps', None)
        if self.timesteps is None:
            raise ValueError('No timesteps defined!')


