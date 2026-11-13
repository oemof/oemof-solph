# -*- coding: utf-8 -*-

"""linopy versions of the functions in :mod:`oemof.solph.constraints`.

Each function is registered under the name of its Pyomo counterpart;
:func:`oemof.solph.constraints._backend.backend_dispatch` calls it when
the model is a :class:`~oemof.solph.LinopyModel`.

SPDX-License-Identifier: MIT
"""

_CONSTRAINTS = {}


def register_constraint(name):
    """Register `function` as the linopy version of constraint `name`."""

    def decorator(function):
        _CONSTRAINTS[name] = function
        return function

    return decorator


def get_constraint(name):
    """The linopy version of constraint function `name`, or None."""
    return _CONSTRAINTS.get(name)
