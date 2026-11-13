# -*- coding: utf-8 -*-

"""Dispatch of the constraint functions to the model's backend.

SPDX-FileCopyrightText: oemof e.V. and contributors

SPDX-License-Identifier: MIT
"""

import functools


def backend_dispatch(function):
    """Call the linopy version of a constraint function for linopy models.

    The functions in :mod:`oemof.solph.constraints` take the model as
    their first argument. For a :class:`~oemof.solph.LinopyModel` the
    implementation registered under the same name in
    :mod:`oemof.solph._linopy.constraints` is called instead; if there is
    none yet, a NotImplementedError says so.
    """

    @functools.wraps(function)
    def wrapper(model, *args, **kwargs):
        if getattr(model, "BACKEND", "pyomo") == "linopy":
            from oemof.solph._linopy.constraints import get_constraint

            implementation = get_constraint(function.__name__)
            if implementation is None:
                msg = (
                    f"solph.constraints.{function.__name__} is not "
                    "supported by the linopy backend yet."
                )
                raise NotImplementedError(msg)
            return implementation(model, *args, **kwargs)
        return function(model, *args, **kwargs)

    return wrapper
