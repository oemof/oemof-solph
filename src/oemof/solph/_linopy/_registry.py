# -*- coding: utf-8 -*-

"""Registry mapping solph constraint blocks to linopy builders.

The Pyomo backend instantiates one block class per constraint group
(e.g. :class:`~oemof.solph.buses._bus.BusBlock`). The linopy backend uses
the same groups and looks up a builder function per block class instead.

SPDX-License-Identifier: MIT
"""

_BUILDERS = {}


def register_builder(block_class):
    """Register a linopy builder for a solph constraint block class.

    The decorated function is called as ``builder(model, group)`` with the
    :class:`~oemof.solph._linopy.LinopyModel` under construction and the
    members of the constraint group, exactly as
    ``block._create(group=...)`` receives them in the Pyomo backend: nodes
    for component blocks, ``(source, target, flow)`` triples for flow
    blocks.

    Third-party components with their own Pyomo block can add linopy
    support the same way.

    Examples
    --------
    >>> from oemof.solph._linopy import register_builder
    >>> class MyBlock:
    ...     pass
    >>> @register_builder(MyBlock)
    ... def build_my_block(model, group):
    ...     pass
    >>> unregister_builder(MyBlock)
    """

    def decorator(function):
        _BUILDERS[block_class] = function
        return function

    return decorator


def unregister_builder(block_class):
    """Remove the builder registered for `block_class` (if any)."""
    _BUILDERS.pop(block_class, None)


def get_builder(block_class):
    """Return the builder registered for `block_class`, or None."""
    return _BUILDERS.get(block_class)


def has_builder(block_class):
    """Whether the linopy backend can build `block_class`."""
    return block_class in _BUILDERS
