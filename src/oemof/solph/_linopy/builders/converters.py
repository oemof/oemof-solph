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
from oemof.solph.components._offset_converter import OffsetConverterBlock


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


@register_builder(OffsetConverterBlock)
def build_offset_converters(model, group):
    """``P(t) = P_ref(t) * m(t) + status_nominal_ref(t) * y0(t)`` for every
    flow of an OffsetConverter that is not the (nonconvex) reference."""
    n_steps = len(model.TIMESTEPS)
    labels = model.flow.labels.values
    status_nominal = getattr(model, "nonconvex_status_nominal", {})
    ref_labels, sn_labels, flow_labels, slope, offset = [], [], [], [], []
    for n in group:
        ref = n._reference_node
        ref_key = (ref, n) if n._reference_node_at_input else (n, ref)
        others = [(i, n) for i in n.inputs if i != ref]
        others += [(n, o) for o in n.outputs if o != ref]
        for key in others:
            other = key[0] if key[1] is n else key[1]
            ref_labels.append(labels[model.flow_position(*ref_key)])
            sn_labels.append(status_nominal[ref_key])
            flow_labels.append(labels[model.flow_position(*key)])
            slope.append(
                to_array(n.conversion_factors[other], n_steps, "conversion")
            )
            offset.append(
                to_array(n.normed_offsets[other], n_steps, "normed_offsets")
            )
    if not ref_labels:
        return
    lhs = expression(
        model.linopy,
        [
            (np.array(ref_labels), np.array(slope)),
            (np.array(sn_labels), np.array(offset)),
            (np.array(flow_labels), -1.0),
        ],
        ("offset_relation", "timestep"),
    )
    model.add_constraints("OffsetConverterBlock.relation", lhs, "=", 0)
