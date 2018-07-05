# -*- coding: utf-8 -*-

"""This package (along with its subpackages) contains the classes used to model
energy systems. An energy system is modelled as a graph/network of entities
with very specific constraints on which types of entities are allowed to be
connected.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/network.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from collections import namedtuple as NT, MutableMapping as MM, UserDict as UD
from contextlib import contextmanager
from functools import total_ordering
from weakref import WeakKeyDictionary as WeKeDi, WeakSet as WeSe

# TODO:
#
#   * Make inputs and outputs updatetable again to fix tests.
#   * Document `in_edges` and `out_edges` attributes.
#   * Remove `_Edges` and `flow`.
#   * Finally get rid of `Entity`.
#


class Inputs(MM):
    """ A special helper to map `n1.inputs[n2]` to `n2.outputs[n1]`.
    """
    def __init__(self, target):
        self.target = target

    def __getitem__(self, key):
        return key.outputs.__getitem__(self.target)

    def __delitem__(self, key):
        return key.outputs.__delitem__(self.target)

    def __setitem__(self, key, value):
        return key.outputs.__setitem__(self.target, value)

    def __iter__(self):
        return iter(self.target._in_edges)

    def __len__(self):
        return self.target._in_edges.__len__()

    def __repr__(self):
        return repr("<{0.__module__}.{0.__name__}: {1!r}>"
                    .format(type(self), dict(self)))


class Outputs(UD):
    """ Helper that intercepts modifications to update `Inputs` symmetrically.
    """
    def __init__(self, source):
        self.source = source
        super().__init__()

    def __delitem__(self, key):
        key._in_edges.remove(self.source)
        return super().__delitem__(key)

    def __setitem__(self, key, value):
        key._in_edges.add(self.source)
        return super().__setitem__(key, value)


class _Edges(MM):
    """ Internal utility class keeping track of known edges.

    As this is currently quite dirty and hackish, it should be treated as an
    internal implementation detail with an unstable interface. Maye it can be
    converted to a fully fledged useful :python:`Edge` class later on, but for
    now it simply hides most of the dirty secrets of the :class:`Node` class.

    """
    _in_edges = WeKeDi()
    _out_edges = WeKeDi()
    # TODO: Either figure out how to use weak references here, or convert the
    #       whole graph datastructure to normal dictionaries.
    #       Background: I had to stop wrestling with the garbage collector,
    #                   because python doesn't allow weak references to tuples
    #                   and I couldn't figure out a way to key edges in a way
    #                   that the endpoints of the edge get garbage collected
    #                   once no other references to them exist anymore.
    #       I guess the best way would be to use normal dictionarier, stop
    #       using a global variable for all edges and put a member variable
    #       for all it's edges on an energy system.
    _flows = {}

    def __delitem__(self, key):
        source, target = key

        # TODO: Refactor this to not have duplicate code.
        self._in_edges[target].remove(source)
        if not self._in_edges[target]:
          del self._in_edges[target]

        self._out_edges[source].remove(target)
        if not self._out_edges[source]:
          del self._out_edges[source]

        del self._flows[key]

    def __getitem__(self, key):
        return self._flows.__getitem__(key)

    def __setitem__(self, key, value):
        source, target = key
        # TODO: Refactor this to remove duplicate code.
        self._in_edges[target] = self._in_edges.get(target, WeSe())
        self._in_edges[target].add(source)

        self._out_edges[source] = self._out_edges.get(source, WeSe())
        self._out_edges[source].add(target)

        self._flows.__setitem__(key, value)

    def __call__(self, source=None, target=None):
        if ((source is None) and (target is None)):
            return None
        if (source is None):
            return Inputs(self, target)
        if (target is None):
            return Outputs(self, source)
        return self._flows[source, target]

    def __iter__(self):
        return self._flows.__iter__()

    def __len__(self):
        return self._flows.__len__()


flow = _Edges()


@total_ordering
class Node:
    """ Represents a Node in an energy system graph.

    Abstract superclass of the two general types of nodes of an energy system
    graph, collecting attributes and operations common to all types of nodes.
    Users should neither instantiate nor subclass this, but use
    :class:`Component`, :class:`Bus`, :class:`Edge` or one of their subclasses
    instead.

    .. role:: python(code)
      :language: python

    Parameters
    ----------
    label: `hashable`, optional
        Used as the string representation of this node. If this parameter is
        not an instance of :class:`str` it will be converted to a string and
        the result will be used as this node's :attr:`label`, which should be
        unique with respect to the other nodes in the energy system graph this
        node belongs to. If this parameter is not supplied, the string
        representation of this node will instead be generated based on this
        nodes `class` and `id`.
    inputs: list or dict, optional
        Either a list of this nodes' input nodes or a dictionary mapping input
        nodes to corresponding inflows (i.e. input values).
    outputs: list or dict, optional
        Either a list of this nodes' output nodes or a dictionary mapping
        output nodes to corresponding outflows (i.e. output values).

    Attributes
    ----------
    __slots__: str or iterable of str
        See the Python documentation on `__slots__
        <https://docs.python.org/3/reference/datamodel.html#slots>`_ for more
        information.
    """

    # TODO: Doing this _state/__getstate__/__setstate__ dance is
    #       necessary to fix issues #186 and #203. But there must be
    #       some more elegant solution. So in the long run, either this,
    #       or dump/restore should be refactored so that storing the
    #       initialization arguments is not necessary.
    #       The culprit seems to be that inputs/outputs are actually
    #       stored in the `_Edge` class and pickle can't make that jump.
    #       But more sophisticated research and minimal test cases are
    #       needed to confirm that.

    registry = None
    __slots__ = ["__weakref__", "_label", "_state", "in_edges", "out_edges"]

    def __init__(self, *args, **kwargs):
        self.__setstate__((args, kwargs))
        if __class__.registry is not None:
            __class__.registry.add(self)

    def __getstate__(self):
        return self._state

    def __setstate__(self, state):
        self._state = state
        args, kwargs = state
        for optional in ['label']:
            if optional in kwargs:
                setattr(self, '_' + optional, kwargs[optional])
        self.in_edges = set()
        for i in kwargs.get('inputs', {}):
            assert isinstance(i, Node), \
                   "Input {} of {} not a Node, but a {}."\
                   .format(i, self, type(i))
            try:
                flow = kwargs['inputs'].get(i)
            except AttributeError:
                flow = None
            self.in_edges.add(
                    globals()['Edge'](input=i, output=self, flow=flow))
        self.out_edges = set()
        for o in kwargs.get('outputs', {}):
            assert isinstance(o, Node), \
                   "Output {} of {} not a Node, but a {}."\
                   .format(o, self, type(o))
            try:
                flow = kwargs['outputs'].get(o)
            except AttributeError:
                flow = None
            self.out_edges.add(
                    globals()['Edge'](input=self, output=o, flow=flow))

        """
        This could be slightly more efficient than the loops above, but doesn't
        play well with the assertions:

        inputs = kwargs.get('inputs', {})
        self.in_edges = {
                Edge(input=i, output=self,
                    flow=None if not isinstance(inputs, MM) else inputs[i])
                for i in inputs}

        outputs = kwargs.get('outputs', {})
        self.out_edges = {
                Edge(input=self, output=o,
                    flow=None if not isinstance(outputs, MM) else outputs[o])
                for o in outputs}
        self.edges = self.in_edges.union(self.out_edges)
        """

    def __eq__(self, other):
        return id(self) == id(other)

    def __lt__(self, other):
        if other is None:
            return False
        return self.label < other.label

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        return str(self.label)

    def __repr__(self):
        return repr("<{0.__module__}.{0.__name__}: {1!r}>"
                    .format(type(self), self.label))

    @property
    def label(self):
        """ object :
        If this node was given a `label` on construction, this
        attribute holds the actual object passed as a parameter. Otherwise
        :py:`node.label` is a synonym for :py:`str(node)`.
        """
        return (self._label if hasattr(self, "_label")
                else "<{} #0x{:x}>".format(type(self).__name__, id(self)))

    @property
    def inputs(self):
        """ dict:
        Dictionary mapping input :class:`Nodes <Node>` :obj:`n` to
        :class:`Edge`s from :obj:`n` into :obj:`self`.
        If :obj:`self` is an :class:`Edge`, returns a dict containing the
        :class:`Edge`'s single input node as the key and the flow as the value.
        """
        return ({edge.input: edge for edge in self.in_edges}
                if not hasattr(self, "input")
                else {self.input: self.flow})


    @property
    def outputs(self):
        """ dict:
        Dictionary mapping output :class:`Nodes <Node>` :obj:`n` to
        :class:`Edges` from :obj:`self` into :obj:`n`.
        If :obj:`self` is an :class:`Edge`, returns a dict containing the
        :class:`Edge`'s single output node as the key and the flow as the value.
        """
        return ({edge.output: edge for edge in self.out_edges}
                if not hasattr(self, "output")
                else {self.output: self.flow})


class Edge(Node):
    """ :class:`Bus`es/:class:`Component`s are always connected by an :class:`Edge`.

    :class:`Edge`s connect a single non-:class:`Edge` Node with another. They
    are directed and have a (sequence of) value(s) attached to them so they can
    be used to represent a flow from a source/an input to a target/an output.

    Parameters
    ----------
    input, output: :class:`Bus` or :class:`Component`
    flow: object, optional
        The (list of) objec(s) representing the flow from this objects input
        into it's output.

    Note that all of these parameters are also set as attributes with the same
    name.
    """
    # TODO: Figure out how to distinguish different kinds of flows between the
    #       same nodes. We have at least the following two options:
    #
    #         * Allow multiple `Edge`s with the same input and output. For this
    #           to work with groupings, we would have to put another attribute
    #           on `Edge` `label`s distinguishing these parallel edges from
    #           each other.
    #         * Don't allow parallel edges, forcing the user to either have
    #           complex objects like xarray `Dataet`s as flow values, or to add
    #           more `Bus`es/`Component`s.
    #
    Label = NT("Edge", ['input', 'output'])
    def __init__(self, input, output, flow=None):
        super().__init__(label=Edge.Label(input, output))
        self.flow = flow
        self.input = input
        self.output = output
        input.out_edges.add(self)
        output.in_edges.add(self)


class Bus(Node):
    pass


class Component(Node):
    pass


class Sink(Component):
    pass


class Source(Component):
    pass


class Transformer(Component):
    pass


# TODO: Adhere to PEP 0257 by listing the exported classes with a short
#       summary.
class Entity:
    r"""
    The most abstract type of vertex in an energy system graph. Since each
    entity in an energy system has to be uniquely identifiable and
    connected (either via input or via output) to at least one other
    entity, these properties are collected here so that they are shared
    with descendant classes.

    Parameters
    ----------
    uid : string or tuple
        Unique component identifier of the entity.
    inputs : list
        List of Entities acting as input to this Entity.
    outputs : list
        List of Entities acting as output from this Entity.
    geo_data : shapely.geometry object
        Geo-spatial data with informations for location/region-shape. The
        geometry can be a polygon/multi-polygon for regions, a line fore
        transport objects or a point for objects such as transformer sources.

    Attributes
    ----------
    registry: :class:`EnergySystem <oemof.core.energy_system.EnergySystem>`
        The central registry keeping track of all :class:`Node's <Node>`
        created. If this is `None`, :class:`Node` instances are not
        kept track of. Assign an :class:`EnergySystem
        <oemof.core.energy_system.EnergySystem>` to this attribute to have it
        become the a :class:`node <Node>` registry, i.e. all :class:`nodes
        <Node>` created are added to its :attr:`nodes
        <oemof.core.energy_system.EnergySystem.nodes>`
        property on construction.
    """
    optimization_options = {}

    registry = None

    def __init__(self, **kwargs):
        # TODO: @Günni:
        # add default argument values to docstrings (if it's possible).
        self.uid = kwargs["uid"]
        self.inputs = kwargs.get("inputs", [])
        self.outputs = kwargs.get("outputs", [])
        for e_in in self.inputs:
            if self not in e_in.outputs:
                e_in.outputs.append(self)
        for e_out in self.outputs:
            if self not in e_out.inputs:
                e_out.inputs.append(self)
        self.geo_data = kwargs.get("geo_data", None)
        self.regions = []
        self.add_regions(kwargs.get('regions', []))
        if __class__.registry is not None:
            __class__.registry.add(self)

        # TODO: @Gunni Yupp! Add docstring.
    def add_regions(self, regions):
        """Add regions to self.regions
        """
        self.regions.extend(regions)
        for region in regions:
            if self not in region.entities:
                region.entities.append(self)

    def __str__(self):
        # TODO: @Günni: Unused privat method. No Docstring.
        return "<{0} #{1}>".format(type(self).__name__, self.uid)


@contextmanager
def registry_changed_to(r):
    """ Override registry during execution of a block and restore it afterwards.
    """
    backup = Node.registry
    Node.registry = None
    yield
    Node.registry = backup


def temporarily_modifies_registry(function):
    """ Backup registry before and restore it after execution of `function`.
    """
    def result(*xs, **ks):
        with registry_disabled():
            return f(*xs, **ks)
    return result

