from functools import total_ordering
from weakref import WeakKeyDictionary as WeKeDi, WeakSet as WeSe
"""
This package (along with its subpackages) contains the classes used to model
energy systems. An energy system is modelled as a graph/network of entities
with very specific constraints on which types of entities are allowed to be
connected.

"""


class _Edges:
    """ Internal utility class keeping track of known edges.

    As this is currently quite dirty and hackish, it should be treated as an
    internal implementation detail with an unstable interface. Maye it can be
    converted to a fully fledged useful :python:`Edge` class later on, but for
    now it simply hides most of the dirty secrets of the :class:`Node` class.

    """
    _in_edges = WeKeDi()
    _flows = WeKeDi()

    def __getitem__(self, key):
        self._flows[key] = self._flows.get(key, WeKeDi())
        return self._flows[key]

    def __setitem__(self, key, value):
        source, target = key
        self._in_edges[target] = self._in_edges.get(target, WeSe())
        self._in_edges[target].add(source)
        self._flows[source] = self._flows.get(source, WeKeDi())
        self._flows[source][target] = value

    def __call__(self, *keys):
        result = self
        for k in keys:
            result = result[k]
        return result


flow = _Edges()


@total_ordering
class Node:
    """ Represents a Node in an energy system graph.

    Abstract superclass of the two general types of nodes of an energy system
    graph, collecting attributes and operations common to all types of nodes.
    Users should neither instantiate nor subclass this, but use
    :class:`Component`, :class:`Bus` or one of their subclasses instead.

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
    flow: function, optional
        A function taking this node and a target node as a parameter (i.e.
        something of the form :python:`def f(self, target)`), returning the
        flow originating from this node into :python:`target`.

    Attributes
    ----------
    label: object
        If this node was given a `label` on construction, this attribute holds
        the actual object passed as a parameter. Otherwise py:``node.label`` is
        a synonym for ``str(node)``.
    inputs: dict
        Dictionary mapping input :class:`Node`s `n` to flows from `n` into
        `self`.
    outputs: dict
        Dictionary mapping output :class:`Node`s `n` to flows from `self` into
        `n`.

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
    __slots__ = ["__weakref__", "_label", "_state"]

    def __init__(self, *args, **kwargs):
        self._state = (args, kwargs)
        self.__setstate__(self._state)
        if __class__.registry is not None:
            __class__.registry.add(self)

    def __getstate__(self):
        return self._state

    def __setstate__(self, state):
        args, kwargs = state
        for optional in ['label']:
            if optional in kwargs:
                setattr(self, '_' + optional, kwargs[optional])
        for i in kwargs.get('inputs', {}):
            try:
                flow[i, self] = kwargs['inputs'].get(i)
            except AttributeError:
                flow[i, self] = None
        for o in kwargs.get('outputs', {}):
            try:
                flow[self, o] = kwargs['outputs'].get(o)
            except AttributeError:
                flow[self, o] = None

    def __eq__(self, other):
        return id(self) == id(other)

    def __lt__(self, other):
        return self.label < other.label

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        return str(self.label)

    @property
    def label(self):
        return (self._label if hasattr(self, "_label")
                else "<{} #0x{:x}>".format(type(self).__name__, id(self)))

    @property
    def inputs(self):
        # TODO: Accessing :class:`Flow`'s `_in_edges` is kinda ugly.
        #       Find a way to replace it.
        #       This can also have unintuitive behaviour since adding new
        #       associations to the returned mapping will NOT add a new input
        #       flow to this node.
        return {k: flow(k, self) for k in flow._in_edges.get(self, ())}

    @property
    def outputs(self):
        return flow(self)


class Bus(Node):
    __slots__ = ()


class Component(Node):
    __slots__ = ()


class Sink(Component):
    __slots__ = ()


class Source(Component):
    __slots__ = ()


class Transformer(Component):
    __slots__ = ()


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
        The central registry keeping track of all :class:`Entities <Entity>`
        created. If this is `None`, :class:`Entity` instances are not
        kept track of. When you instantiate an :class:`EnergySystem
        <oemof.core.energy_system.EnergySystem>` it automatically becomes the
        entity registry, i.e. all entities created are added to its
        :attr:`entities <oemof.core.energy_system.EnergySystem.entities>`
        attribute on construction.
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
