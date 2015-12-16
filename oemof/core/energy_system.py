# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""

import logging
from oemof.core.network.entities.components import transports as transport
from oemof.solph.optimization_model import OptimizationModel as OM


class EnergySystem:
    r"""Defining an energy supply system to use oemof's solver libraries.

    Note
    ----
    The list of regions is not necessary to use the energy system with solph.

    Parameters
    ----------
    entities : list of core.network objects
        List of all objects of the energy system. All class descriptions can
        be found in the :py:mod:`oemof.core.network` package.
    simulation : core.energy_system.Simulation object
        Simulation object that contains all necessary attributes to start the
        solver library. Defined in the :py:class:`Simulation
        <oemof.core.energy_system.Simulation>` class.
    regions : list of core.energy_system.Region objects
        List of regions defined in the :py:class:`Region
        <oemof.core.energy_system.Simulation>` class.

    Attributes
    ----------
    entities : list of core.network objects
        List of all objects of the energy system. All class descriptions can
        be found in the :py:mod:`oemof.core.network` package.
    simulation : core.energy_system.Simulation object
        Simulation object that contains all necessary attributes to start the
        solver library. Defined in the :py:class:`Simulation
        <oemof.core.energy_system.Simulation>` class.
    regions : list of core.energy_system.Region objects
        List of regions defined in the :py:class:`Region
        <oemof.core.energy_system.Simulation>` class.
    results : dictionary
        A dictionary holding the results produced by the energy system.
        Is `None` while no results are produced.
        Currently only set after a call to :meth:`optimize` after which it
        holds the return value of :meth:`om.results()
        <oemof.solph.optimization_model.OptimizationModel.results>`.
    """
    def __init__(self, **kwargs):
        for attribute in ['regions', 'entities', 'simulation']:
            setattr(self, attribute, kwargs.get(attribute, {}))
        self.results = None

    # TODO: Condense signature (use Buse)
    def connect(self, code1, code2, media, in_max, out_max, eta,
                transport_class):
        """Create a transport object to connect to buses."""
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

    # TODO: Add concept to make it possible to use another solver library.
    def optimize(self, om=None):
        """Start optimizing the energy system using solph.

        Parameters
        ----------
        om : :class:`OptimizationModel <oemof.solph.optimization_model.OptimizationModel>`, optional
            The optimization model used to optimize the :class:`EnergySystem`.
            If not given, an :class:`OptimizationModel
            <oemof.solph.optimization_model.OptimizationModel>` instance local
            to this method is created using the current :class:`EnergySystem`
            instance as an argument.
            You only need to supply this if you want to observe any side
            effects that solving has on the `om`.

        Returns
        -------
        self : :class:`EnergySystem`
        """
        if om is None:
            om = OM(energysystem=self)

        om.solve(solver=self.simulation.solver, debug=self.simulation.debug,
                 tee=self.simulation.stream_solver_output,
                 duals=self.simulation.duals)

        self.results = om.results()
        return self

class Region:
    r"""Defining a region within an energy supply system.

    Note
    ----
    The list of regions is not necessary to use the energy system with solph.

    Parameters
    ----------
    entities : list of core.network objects
        List of all objects of the energy system. All class descriptions can
        be found in the :py:mod:`oemof.core.network` package.
    name : string
        A unique name to identify the region. If possible use typical names for
        regions and english names for countries.
    code : string
        A short unique name to identify the region.
    geom : shapely.geometry object
        The geometry representing the region must be a polygon or a multi
        polygon.

    Attributes
    ----------
    entities : list of core.network objects
        List of all objects of the energy system. All class descriptions can
        be found in the :py:mod:`oemof.core.network` package.
    name : string
        A unique name to identify the region. If possible use typical names for
        regions and english names for countries.
    geom : shapely.geometry object
        The geometry representing the region must be a polygon or a multi
        polygon.
    """
    def __init__(self, **kwargs):
        self.entities = []  # list of entities
        self.add_entities(kwargs.get('entities', []))

        self.name = kwargs.get('name')
        self.geom = kwargs.get('geom')
        self._code = kwargs.get('code')

    # TODO: oder sollte das ein setter sein? Yupp.
    def add_entities(self, entities):
        """Add a list of entities to the existing list of entities.

        For every entity added to a region the region attribute of the entity
        is set

        Parameters
        ----------
        entities : list of core.network objects
        List of all objects of the energy system that belongs to area covered
        by the polygon of the region. All class descriptions can
        be found in the :py:mod:`oemof.core.network` package."""
        # TODO: prevent duplicate entries
        self.entities.extend(entities)
        for entity in entities:
            if self not in entity.regions:
                entity.regions.append(self)

    @property
    def code(self):
        """Creating a short code based on the region name if no code is set."""
        if self._code is None:
            name_parts = self.name.replace('_', ' ').split(' ', 1)
            self._code = ''
            for part in name_parts:
                self._code += part[:1].upper() + part[1:3]
        return self._code


class Simulation:
    r"""Defining the simulation related parameters according to the solver lib.

    Parameters
    ----------
    solver : string
        Name of the solver supported by the used solver library.
        (e.g. 'glpk', 'gurobi')
    debug : boolean
        Set the chosen solver to debug (verbose) mode to get more information.
    stream_solver_output : boolean
        If True, solver output is streamed in python console
    duals : boolean
        If True, results of dual variables and reduced costs will be saved
    objective_options : dictionary
        'function': function to use from
                    :py:mod:`oemof.solph.predefined_objectives`
        'cost_objects': list of str(`class`) elements. Objects of type  `class`
                        are include in cost terms of objective function.
        'revenue_objects': list of str(`class`) elements. . Objects of type
                           `class` are include in revenue terms of
                           objective function.
    timesteps : list or sequence object
         Timesteps to be simulated or optimized in the used library
    relaxed : boolean
        If True, integer variables will be relaxed
        (only relevant for milp-problems)
    """
    def __init__(self, **kwargs):
        ''
        self.solver = kwargs.get('solver', 'glpk')
        self.debug = kwargs.get('debug', False)
        self.stream_solver_output = kwargs.get('stream_solver_output', False)
        self.objective_options = kwargs.get('objective_options', {})
        self.duals = kwargs.get('duals', False)
        self.timesteps = kwargs.get('timesteps', None)
        self.relaxed = kwargs.get('relaxed', False)

        if self.timesteps is None:
            raise ValueError('No timesteps defined!')
