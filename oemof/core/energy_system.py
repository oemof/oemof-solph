# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""

from operator import attrgetter
import logging
import os

import dill as pickle

from oemof.core.network import Entity
from oemof.core.network.entities.components import transports as transport
from oemof.solph.optimization_model import OptimizationModel as OM


def _value_error(s):
    raise ValueError(s)

class Grouping:
    """
    Used to aggregate :class:`entities <oemof.core.network.Entity>` in an
    :class:`energy system <EnergySystem>` into :attr:`groups
    <EnergySystem.groups>`.

    """
    __slots__ = "_insert"

    @staticmethod
    def create(argument):
        if isinstance(argument, Grouping):
            return argument
        if callable(argument):
            return Grouping(argument)
        raise NotImplementedError(
                "Can only create Groupings from Groupings and callables for now.\n" +
                "  Please add a comment to https://github.com/oemof/oemof/issues/60\n" +
                "  If you stumble upon this as this feature is currently being\n" +
                "  developed and any input on how you expect it to work would be\n" +
                "  appreciated")

    #: The default grouping, which is always present in addition to user
    #: defined ones. Stores every :class:`entity <oemof.core.network.Entity>`
    #: in a group of its own under its :attr:`uid
    #: <oemof.core.network.Entity.uid>` and raises an error if another
    #: :class:`entity <oemof.core.network.Entity>` with the same :attr:`uid
    #: <oemof.core.network.Entity.uid>` get's added to the energy system.
    UID = None
    def __init__(self, key, value=lambda e: [e],
                 collide=lambda e, old: old.append(e) or old,
                 insert=None):
        if insert:
            self._insert = insert
            return self
        def insert(e, d):
            k = key(e)
            d[k] = collide(e, d[k]) if k in d else value(e)

        self._insert = insert

    def __call__(self, e, d):
        self._insert(e, d)

Grouping.UID = Grouping(attrgetter('uid'), value=lambda e: e,
                        collide=lambda e, d: _value_error("Duplicate uid: %s" % e.uid))

class EnergySystem:
    r"""Defining an energy supply system to use oemof's solver libraries.

    Note
    ----
    The list of regions is not necessary to use the energy system with solph.

    Parameters
    ----------
    entities : list of :class:`Entity <oemof.core.network.Entity>`, optional
        A list containing the already existing :class:`Entities
        <oemof.core.network.Entity>` that should be part of the energy system.
        Stored in the :attr:`entities` attribute.
        Defaults to `[]` if not supplied.
    simulation : core.energy_system.Simulation object
        Simulation object that contains all necessary attributes to start the
        solver library. Defined in the :py:class:`Simulation
        <oemof.core.energy_system.Simulation>` class.
    regions : list of core.energy_system.Region objects
        List of regions defined in the :py:class:`Region
        <oemof.core.energy_system.Simulation>` class.
    time_idx : pandas.index, optional
        Define the time range and increment for the energy system. This is an
        optional parameter but might be import for other functions/methods that
        use the EnergySystem class as an input parameter.
    groupings : list
        The elements of this list are used to construct :class:`Groupings
        <oemof.core.energy_system.Grouping>` or they are used directly if they
        are instances of :class:`Grouping <oemof.core.energy_system.Grouping>`.
        These groupings are then used to aggregate the entities added to this
        energy system into :attr:`groups`.
        By default, there'll always be one group for each :attr:`uid
        <oemof.core.network.Entity.uid>` containing exactly the entity with the
        given :attr:`uid <oemof.core.network.Entity.uid>`.
        See the :ref:`examples <energy-system-examples>` for more information.

    Attributes
    ----------
    entities : list of :class:`Entity <oemof.core.network.Entity>`
        A list containing the :class:`Entities <oemof.core.network.Entity>`
        that comprise the energy system. If this :class:`EnergySystem` is
        set as the :attr:`registry <oemof.core.network.Entity.registry>`
        attribute, which is done automatically on :class:`EnergySystem`
        construction, newly created :class:`Entities
        <oemof.core.network.Entity>` are automatically added to this list on
        construction.
    groups : dict
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
        See the documentation of that method for a detailed description of the
        structure of the results dictionary.
    time_idx : pandas.index, optional
        Define the time range and increment for the energy system. This is an
        optional atribute but might be import for other functions/methods that
        use the EnergySystem class as an input parameter.


    .. _energy-system-examples:
    Examples
    --------

    Regardles of additional groupings, :class:`entities
    <oemof.core.network.Entity>` will always be grouped by their :attr:`uid
    <oemof.core.network.Entity.uid>`:

    >>> from oemof.core.network import Entity
    >>> from oemof.core.network.entities import Bus, Component
    >>> es = EnergySystem()
    >>> bus = Bus(uid='electricity')
    >>> bus is es.groups['electricity']
    True

    For simple user defined groupings, you can just supply a function that
    computes a key from an :class:`entity <oemof.core.network.Entity>` and the
    resulting groups will be lists of :class:`entity
    <oemof.core.network.Entity>` stored under the returned keys, like in this
    example, where :class:`entities <oemof.core.network.Entity>` are grouped by
    their `type`:

    >>> es = EnergySystem(groupings=[type])
    >>> buses = [Bus(uid="Bus {}".format(i)) for i in range(9)]
    >>> components = [Component(uid="Component {}".format(i)) for i in range(9)]
    >>> buses == es.groups[Bus]
    True
    >>> components == es.groups[Component]
    True

    """
    def __init__(self, **kwargs):
        for attribute in ['regions', 'entities', 'simulation']:
            setattr(self, attribute, kwargs.get(attribute, []))

        Entity.registry = self
        self.groups = {}
        self._groupings = [Grouping.UID] + [ Grouping.create(g)
                                             for g in kwargs.get('groupings', [])]
        for e in self.entities:
            for g in self._groupings:
                g(e, self.groups)
        self.results = kwargs.get('results')
        self.time_idx = kwargs.get('time_idx')

    def add(self, entity):
        """ Add an `entity` to this energy system.
        """
        self.entities.append(entity)
        for g in self._groupings:
            g(entity, self.groups)

    # TODO: Condense signature (use Buse)
    def connect(self, bus1, bus2, in_max, out_max, eta, transport_class):
        """Create two transport objects to connect two buses of the same type
        in both directions.

        Parameters
        ----------
        bus1, bus2 : core.network.Bus object
            Two buses to be connected.
        eta : float
            Constant efficiency of the transport.
        in_max : float
            Maximum input the transport can handle, in $MW$.
        out_max : float
            Maximum output which can possibly be obtained when using the
            transport, in $MW$.
        transport_class class
            Transport class to use for the connection
        """
        if not transport_class == transport.Simple:
            logging.error('')
            raise(TypeError(
                "Sorry, `EnergySystem.connect` currently only works with" +
                "a `transport_class` argument of" + str(transport.Simple)))
        for bus_a, bus_b in [(bus1, bus2), (bus2, bus1)]:
            uid = str('transport_' + bus_a.uid + bus_b.uid)
            transport_class(uid=uid, outputs=[bus_a], inputs=[bus_b],
                            out_max=[out_max], in_max=[in_max], eta=[eta])

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
                 verbose=self.simulation.verbose,
                 duals=self.simulation.duals,
                 solve_kwargs=self.simulation.solve_kwargs)

        self.results = om.results()
        return self

    def dump(self, dpath=None, filename=None, keep_weather=True):
        r""" Dump an EnergySystem instance.
        """
        if dpath is None:
            bpath = os.path.join(os.path.expanduser("~"), '.oemof')
            if not os.path.isdir(bpath):
                os.mkdir(bpath)
            dpath = os.path.join(bpath, 'dumps')
            if not os.path.isdir(dpath):
                os.mkdir(dpath)

        if filename is None:
            filename = 'es_dump.oemof'

        pickle.dump(self.__dict__, open(os.path.join(dpath, filename), 'wb'))

        msg = ('Attributes dumped to: {0}'.format(os.path.join(
            dpath, filename)))
        logging.debug(msg)
        return msg

    def restore(self, dpath=None, filename=None):
        r""" Restore an EnergySystem instance.
        """
        logging.info(
            "Restoring attributes will overwrite existing attributes.")
        if dpath is None:
            dpath = os.path.join(os.path.expanduser("~"), '.oemof', 'dumps')

        if filename is None:
            filename = 'es_dump.oemof'

        self.__dict__ = pickle.load(open(os.path.join(dpath, filename), "rb"))
        msg = ('Attributes restored from: {0}'.format(os.path.join(
            dpath, filename)))
        logging.debug(msg)
        return msg


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
            List of all objects of the energy system that belongs to area
            covered by the polygon of the region. All class descriptions can
            be found in the :py:mod:`oemof.core.network` package.
        """

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
    verbose : boolean
        If True, solver output etc. is streamed in python console
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
    fast_build : boolean
        If True, the standard way of pyomo constraint building is skipped and
        a different function is used.
        (Warning: No guarantee that all expected 'standard' pyomo model
        functionalities work for the constructed model!)
    """
    def __init__(self, **kwargs):
        ''
        self.solver = kwargs.get('solver', 'glpk')
        self.debug = kwargs.get('debug', False)
        self.verbose = kwargs.get('verbose', False)
        self.objective_options = kwargs.get('objective_options', {})
        self.duals = kwargs.get('duals', False)
        self.timesteps = kwargs.get('timesteps')
        self.relaxed = kwargs.get('relaxed', False)
        self.fast_build = kwargs.get('fast_build', False)
        self.solve_kwargs = kwargs.get('solve_kwargs', {})

        if self.timesteps is None:
            raise ValueError('No timesteps defined!')
