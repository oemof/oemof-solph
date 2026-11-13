# -*- coding: utf-8 -*-

"""Experimental linopy backend for oemof.solph.

:class:`LinopyModel` builds the optimisation problem of an
:class:`~oemof.solph.EnergySystem` with linopy instead of Pyomo. Both
backends read the same energy system; the user picks one by the model
class. Constraint blocks are ported one by one: a block without a linopy
builder raises :class:`NotImplementedError` when the model is built.

Requires the optional dependency ``linopy`` (``pip install
oemof.solph[linopy]``).

SPDX-License-Identifier: MIT
"""

from oemof.solph._linopy import builders  # noqa: F401  (registers builders)
from oemof.solph._linopy._model import LinopyModel
from oemof.solph._linopy._registry import get_builder
from oemof.solph._linopy._registry import has_builder
from oemof.solph._linopy._registry import register_builder
from oemof.solph._linopy._registry import unregister_builder

__all__ = [
    "LinopyModel",
    "get_builder",
    "has_builder",
    "register_builder",
    "unregister_builder",
]
