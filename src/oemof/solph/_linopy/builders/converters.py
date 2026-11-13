# -*- coding: utf-8 -*-

"""linopy builders for converter components.

SPDX-License-Identifier: MIT
"""

import numpy as np

from oemof.solph._linopy._data import to_array
from oemof.solph._linopy._indexing import expression
from oemof.solph._linopy._indexing import take
from oemof.solph._linopy._registry import register_builder
from oemof.solph.components._converter import ConverterBlock


@register_builder(ConverterBlock)
def build_converters(model, group):
    """Input/output relations of :class:`~oemof.solph.components.Converter`:
    ``flow[i, n, t] * cf[o][t] == flow[n, o, t] * cf[i][t]`` for every pair
    of an input i and an output o."""
    n_steps = len(model.TIMESTEPS)
    in_pos, out_pos, in_coef, out_coef, relations = [], [], [], [], []
    for n in group:
        for o in n.outputs:
            for i in n.inputs:
                relations.append((n, i, o))
                in_pos.append(model.flow_position(i, n))
                out_pos.append(model.flow_position(n, o))
                in_coef.append(
                    to_array(n.conversion_factors[o], n_steps, "conversion")
                )
                out_coef.append(
                    to_array(n.conversion_factors[i], n_steps, "conversion")
                )
    if not relations:
        return
    labels = model.flow.labels.values
    lhs = expression(
        model.linopy,
        [
            (take(labels, in_pos), np.asarray(in_coef)),
            (take(labels, out_pos), -np.asarray(out_coef)),
        ],
        ("relation", "timestep"),
    )
    model.add_constraints("ConverterBlock.relation", lhs, "=", 0)
