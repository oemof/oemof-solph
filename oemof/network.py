from functools import total_ordering
from weakref import WeakKeyDictionary as WKD, WeakSet as WS
"""
This package (along with its subpackages) contains the classes used to model
energy systems. An energy system is modelled as a graph/network of entities
with very specific constraints on which types of entities are allowed to be
connected.

"""


class _Edges():
    """ Internal utility class keeping track of known edges.

    As this is currently quite dirty and hackish, it should be treated as an
    internal implementation detail with an unstable interface. Maye it can be
    converted to a fully fledged useful :python:`Edge` class later on, but for
    now it simply hides most of the dirty secrets of the :class:`Node` class.

    """
    _in_edges = WKD()
    _flows = WKD()
    def __getitem__(self, key):
        self._flows[key] = self._flows.get(key, WKD())
        return self._flows[key]
    def __setitem__(self, key, value):
        source, target = key
        self._in_edges[target] = self._in_edges.get(target, WS())
        self._in_edges[target].add(source)
        self._flows[source] = self._flows.get(source, WKD())
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

    registry = None
    __slots__ = ["__weakref__", "_label"]

    def __init__(self, *args, **kwargs):
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
        if __class__.registry is not None:
            __class__.registry.add(self)

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
                            else "<{} #0x{:x}>".format(type(self).__name__,
                                                       id(self)))

    @property
    def inputs(self):
        # TODO: Accessing :class:`Flow`'s `_in_edges` is kinda ugly.
        #       Find a way to replace it.
        #       This can also have unintuitive behaviour sinc adding new
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

