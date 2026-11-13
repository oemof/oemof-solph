# -*- coding: utf-8 -*-

"""linopy builders for Link, VariableSplitConverter (and
ExtractionTurbineCHP), GenericCHP and PiecewiseLinearConverter.

SPDX-License-Identifier: MIT
"""

import numpy as np
import xarray as xr

from oemof.solph._linopy._data import to_array
from oemof.solph._linopy._indexing import expression
from oemof.solph._linopy._indexing import take
from oemof.solph._linopy._registry import register_builder
from oemof.solph.components._generic_chp import GenericCHPBlock
from oemof.solph.components._link import LinkBlock
from oemof.solph.components._variable_split_converter import (
    VariableSplitConverterBlock,
)
from oemof.solph.components.experimental._piecewise_linear_converter import (
    PiecewiseLinearConverterBlock,
)


def _da(values, dims):
    values = np.asarray(values, dtype=float)
    return xr.DataArray(
        values,
        dims=dims,
        coords={d: np.arange(n) for d, n in zip(dims, values.shape)},
    )


@register_builder(LinkBlock)
def build_links(model, group):
    """flow[n, out, t] == c(t) * flow[in, n, t] per conversion factor."""
    n_steps = len(model.TIMESTEPS)
    out_pos, in_pos, factor = [], [], []
    for n in group:
        for (source, target), c in n.conversion_factors.items():
            try:
                out_pos.append(model.flow_position(n, target))
                in_pos.append(model.flow_position(source, n))
            except KeyError:
                raise KeyError(
                    "Error in constraint creation "
                    f"from: {source}, to: {target}, via: {n}. "
                    "Check if all connected buses match "
                    "the conversion factors.",
                )
            factor.append(to_array(c, n_steps, "conversion_factors"))
    labels = model.flow.labels.values
    lhs = expression(
        model.linopy,
        [
            (take(labels, out_pos), 1.0),
            (take(labels, in_pos), -np.array(factor)),
        ],
        ("link_relation", "timestep"),
    )
    model.add_constraints("LinkBlock.relation", lhs, "=", 0)


@register_builder(VariableSplitConverterBlock)
def build_variable_split_converters(model, group):
    """The line through two operating points and the interval between
    them, see VariableSplitConverterBlock."""
    n_steps = len(model.TIMESTEPS)
    labels = model.flow.labels.values
    inflow, out_a, out_b = [], [], []
    a1, b1, a2, b2 = [], [], [], []
    for n in group:
        source = list(n.inputs)[0]
        output_a, output_b = list(n.outputs.keys())
        inflow.append(model.flow_position(source, n))
        out_a.append(model.flow_position(n, output_a))
        out_b.append(model.flow_position(n, output_b))
        a1.append(to_array(n.conversion_factors[output_a], n_steps))
        b1.append(to_array(n.conversion_factors[output_b], n_steps))
        a2.append(
            to_array(n.conversion_factors_secondary_state[output_a], n_steps)
        )
        b2.append(
            to_array(n.conversion_factors_secondary_state[output_b], n_steps)
        )
    a1, b1, a2, b2 = map(np.array, (a1, b1, a2, b2))
    coef_out_b = b1 - b2  # coefficient of output a
    coef_out_a = a2 - a1  # coefficient of output b
    coef_in = a2 * b1 - a1 * b2
    flow_in, flow_a, flow_b = (
        take(labels, inflow),
        take(labels, out_a),
        take(labels, out_b),
    )
    dims = ("split_converter", "timestep")

    def add(name, terms, sign, mask=None):
        lhs = expression(model.linopy, terms, dims)
        name = f"VariableSplitConverterBlock.{name}"
        if mask is None:
            model.add_constraints(name, lhs, sign, 0)
        else:
            model.add_masked_constraints(name, lhs, sign, 0, mask)

    add(
        "input_output_relation",
        [(flow_a, coef_out_b), (flow_b, coef_out_a), (flow_in, -coef_in)],
        "=",
    )
    add(
        "out_b_lower_bound",
        [(flow_in, np.minimum(b1, b2)), (flow_b, -1.0)],
        "<=",
    )
    add(
        "out_b_upper_bound",
        [(flow_b, 1.0), (flow_in, -np.maximum(b1, b2))],
        "<=",
    )
    equal = np.array([bool(n.allow_equal_states) for n in group])[:, None]
    mask = equal & (coef_out_b == 0)
    if mask.any():
        add(
            "out_a_lower_bound",
            [(flow_in, np.minimum(a1, a2)), (flow_a, -1.0)],
            "<=",
            mask,
        )
        add(
            "out_a_upper_bound",
            [(flow_a, 1.0), (flow_in, -np.maximum(a1, a2))],
            "<=",
            mask,
        )


@register_builder(GenericCHPBlock)
def build_generic_chps(model, group):
    """GenericCHP, equation by equation as GenericCHPBlock."""
    block = "GenericCHPBlock"
    n_steps = len(model.TIMESTEPS)
    labels = model.flow.labels.values
    dims = ("generic_chp", "timestep")

    def var(name, binary=False):
        return model.add_variables(
            f"{block}.{name}",
            entities=group,
            entity_dim="generic_chp",
            index="timestep",
            lower=0,
            binary=binary,
        ).labels.values

    H_F, H_L_FG_max, H_L_FG_min = (
        var("H_F"),
        var("H_L_FG_max"),
        var("H_L_FG_min"),
    )
    P_woDH, P, Q, Y = var("P_woDH"), var("P"), var("Q"), var("Y", binary=True)

    def steps(values):
        return np.array([to_array(v, n_steps) for v in values])

    fuel = [list(n.fuel_input.keys())[0] for n in group]
    heat = [list(n.heat_output.keys())[0] for n in group]
    el = [list(n.electrical_output.keys())[0] for n in group]
    fuel_flow = take(
        labels, [model.flow_position(f, n) for f, n in zip(fuel, group)]
    )
    heat_flow = take(
        labels, [model.flow_position(n, h) for n, h in zip(group, heat)]
    )
    el_flow = take(
        labels, [model.flow_position(n, e) for n, e in zip(group, el)]
    )
    el_props = [
        list(n.electrical_output.values())[0].custom_properties for n in group
    ]
    fuel_options = [list(n.fuel_input.values())[0] for n in group]
    heat_options = [list(n.heat_output.values())[0] for n in group]
    alpha0 = steps([n.alphas[0] for n in group])
    alpha1 = steps([n.alphas[1] for n in group])
    beta = steps([n.beta for n in group])
    p_max = steps([p["P_max_woDH"] for p in el_props])
    eta_max = steps([p["Eta_el_max_woDH"] for p in el_props])
    p_min = steps([p["P_min_woDH"] for p in el_props])
    eta_min = steps([p["Eta_el_min_woDH"] for p in el_props])
    share_max = steps(
        [f.custom_properties["H_L_FG_share_max"] for f in fuel_options]
    )
    q_cw_min = steps([h.custom_properties["Q_CW_min"] for h in heat_options])

    def add(name, terms, sign, mask=None):
        lhs = expression(model.linopy, terms, dims)
        name = f"{block}.{name}"
        if mask is None:
            model.add_constraints(name, lhs, sign, 0)
        else:
            model.add_masked_constraints(name, lhs, sign, 0, mask)

    add("H_flow", [(H_F, 1.0), (fuel_flow, -1.0)], "=")
    add("Q_flow", [(Q, 1.0), (heat_flow, -1.0)], "=")
    add("P_flow", [(P, 1.0), (el_flow, -1.0)], "=")
    add("H_F_1", [(H_F, -1.0), (Y, alpha0), (P_woDH, alpha1)], "=")
    add(
        "H_F_2",
        [(H_F, -1.0), (Y, alpha0), (P, alpha1), (Q, alpha1 * beta)],
        "=",
    )
    add("H_F_3", [(H_F, 1.0), (Y, -p_max / eta_max)], "<=")
    add("H_F_4", [(H_F, 1.0), (Y, -p_min / eta_min)], ">=")
    add("H_L_FG_max_def", [(H_L_FG_max, -1.0), (H_F, share_max)], "=")
    # back-pressure units run on the line, others below it
    terms = [(P, 1.0), (Q, 1.0), (H_L_FG_max, 1.0), (Y, q_cw_min), (H_F, -1.0)]
    back_pressure = np.array([n.back_pressure is True for n in group])
    sign = np.where(back_pressure[:, None], "=", "<=").repeat(n_steps, axis=1)
    lhs = expression(model.linopy, terms, dims)
    model.add_constraints(f"{block}.Q_max_res", lhs, _sign_da(sign, dims), 0)

    # as in the Pyomo block, the minimum is only set up if the fuel flow
    # object (not its custom_properties) has H_L_FG_share_min
    with_min = np.array(
        [bool(getattr(f, "H_L_FG_share_min", None)) for f in fuel_options]
    )
    if with_min.any():
        share_min = steps(
            [
                f.custom_properties["H_L_FG_share_min"] if m else 0
                for f, m in zip(fuel_options, with_min)
            ]
        )
        q_cw = steps(
            [h.Q_CW_min if m else 0 for h, m in zip(heat_options, with_min)]
        )
        mask = np.repeat(with_min[:, None], n_steps, axis=1)
        add(
            "H_L_FG_min_def",
            [(H_L_FG_min, -1.0), (H_F, share_min)],
            "=",
            mask,
        )
        add(
            "Q_min_res",
            [(P, 1.0), (Q, 1.0), (H_L_FG_min, 1.0), (Y, q_cw), (H_F, -1.0)],
            ">=",
            mask,
        )


def _sign_da(signs, dims):
    return xr.DataArray(
        signs,
        dims=dims,
        coords={d: np.arange(n) for d, n in zip(dims, signs.shape)},
    )


# Pyomo's piecewise representations and the linopy method used for them.
# All are exact formulations of the same piecewise function; "incremental"
# needs no SOS support from the solver.
PIECEWISE_METHODS = {"SOS2": "sos2"}


@register_builder(PiecewiseLinearConverterBlock)
def build_piecewise_linear_converters(model, group):
    """inflow/outflow variables bounded by the breakpoints, equal to the
    flows, and outflow = f(inflow) as a piecewise linear function."""
    block = "PiecewiseLinearConverterBlock"
    labels = model.flow.labels.values
    lower_in = np.array([min(n.in_breakpoints) for n in group])[:, None]
    upper_in = np.array([max(n.in_breakpoints) for n in group])[:, None]
    lower_out = np.array(
        [n.conversion_function(min(n.in_breakpoints)) for n in group]
    )[:, None]
    upper_out = np.array(
        [n.conversion_function(max(n.in_breakpoints)) for n in group]
    )[:, None]
    inflow = model.add_variables(
        f"{block}.inflow",
        entities=group,
        entity_dim="piecewise_converter",
        index="timestep",
        lower=lower_in,
        upper=upper_in,
    )
    outflow = model.add_variables(
        f"{block}.outflow",
        entities=group,
        entity_dim="piecewise_converter",
        index="timestep",
        lower=lower_out,
        upper=upper_out,
    )
    dims = ("piecewise_converter", "timestep")
    in_flow = take(
        labels, [model.flow_position(list(n.inputs)[0], n) for n in group]
    )
    out_flow = take(
        labels, [model.flow_position(n, list(n.outputs)[0]) for n in group]
    )
    model.add_constraints(
        f"{block}.equate_in",
        expression(
            model.linopy, [(in_flow, -1.0), (inflow.labels.values, 1.0)], dims
        ),
        "=",
        0,
    )
    model.add_constraints(
        f"{block}.equate_out",
        expression(
            model.linopy,
            [(out_flow, -1.0), (outflow.labels.values, 1.0)],
            dims,
        ),
        "=",
        0,
    )
    for k, n in enumerate(group):
        x = list(n.in_breakpoints)
        y = [n.conversion_function(v) for v in x]
        model.linopy.add_piecewise_formulation(
            (outflow.isel(piecewise_converter=k), y),
            (inflow.isel(piecewise_converter=k), x),
            method=PIECEWISE_METHODS.get(n.pw_repn, "incremental"),
            name=f"{block}.piecewise_{k}",
        )
