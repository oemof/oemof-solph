# -*- coding: utf-8 -*-

"""linopy builder for the experimental generic compressed air energy
storage (:class:`~oemof.solph.components.experimental.GenericCAES`).

The equations follow the Pyomo block
:class:`~oemof.solph.components.experimental._generic_caes.GenericCAESBlock`
term by term, including its peculiarities: the cavern exergy flows add
their y-intersections as constants (not multiplied by the status), the
cavern outflow depends on the expansion power, and the spot market
variables are created without any constraint.

SPDX-License-Identifier: MIT
"""

import numpy as np
import xarray as xr

from oemof.solph._linopy._indexing import expression
from oemof.solph._linopy._indexing import take
from oemof.solph._linopy._registry import register_builder
from oemof.solph.components.experimental._generic_caes import GenericCAESBlock

BLOCK = "GenericCAESBlock"
DIM = "generic_caes"

_BINARIES = ("cmp_st", "exp_st")
_VARIABLES = (
    "cmp_st",
    "cmp_p",
    "cmp_p_max",
    "cmp_q_out_sum",
    "cmp_q_waste",
    "exp_st",
    "exp_p",
    "exp_p_max",
    "exp_q_in_sum",
    "exp_q_fuel_in",
    "exp_q_add_in",
    "cav_level",
    "cav_e_in",
    "cav_e_out",
    "tes_level",
    "tes_e_in",
    "tes_e_out",
    "exp_p_spot",
    "cmp_p_spot",
)


@register_builder(GenericCAESBlock)
def build_generic_caes(model, group):
    nodes = list(group)
    n_steps = len(model.TIMESTEPS)
    tau = np.broadcast_to(model.timeincrement_array, (len(nodes), n_steps))

    def param(key):
        return np.array([float(n.params[key]) for n in nodes])[:, None]

    # --- variables --------------------------------------------------------
    v = {}
    for name in _VARIABLES:
        binary = name in _BINARIES
        v[name] = model.add_variables(
            f"{BLOCK}.{name}",
            entities=nodes,
            entity_dim=DIM,
            index="timestep",
            lower=0,
            upper=1 if binary else np.inf,
            binary=binary,
        ).labels.values

    def previous(labels):
        prev = np.roll(labels, 1, axis=1)
        prev[:, 0] = -1
        return prev

    flows = model.flow.labels.values
    el_in = take(
        flows,
        [
            model.flow_position(next(iter(n.electrical_input)), n)
            for n in nodes
        ],
    )
    el_out = take(
        flows,
        [
            model.flow_position(n, next(iter(n.electrical_output)))
            for n in nodes
        ],
    )
    fuel_in = take(
        flows,
        [model.flow_position(next(iter(n.fuel_input)), n) for n in nodes],
    )
    cav_prev = previous(v["cav_level"])
    tes_prev = previous(v["tes_level"])

    def add(name, terms, sign, rhs=0.0):
        lhs = expression(model.linopy, terms, (DIM, "timestep"))
        rhs = xr.DataArray(
            np.broadcast_to(np.asarray(rhs, dtype=float), tau.shape),
            dims=(DIM, "timestep"),
            coords={d: lhs.coords[d] for d in (DIM, "timestep")},
        )
        model.add_constraints(f"{BLOCK}.{name}", lhs, sign, rhs)

    cmp_max_m, cmp_max_b = param("cmp_p_max_m"), param("cmp_p_max_b")
    exp_max_m, exp_max_b = param("exp_p_max_m"), param("exp_p_max_b")
    cav_level_max = param("cav_level_max")
    cmp_share = param("cmp_q_tes_share")
    exp_share = param("exp_q_tes_share")

    # --- compression ------------------------------------------------------
    add("cmp_p_constr", [(v["cmp_p"], -1.0), (el_in, 1.0)], "=")
    # cmp_p_max(t) == m * cav_level(t-1) + b (t = 0: == b)
    add(
        "cmp_p_max_constr",
        [(v["cmp_p_max"], 1.0), (cav_prev, -cmp_max_m)],
        "=",
        cmp_max_b,
    )
    add(
        "cmp_p_max_area_constr",
        [(v["cmp_p"], 1.0), (v["cmp_p_max"], -1.0)],
        "<=",
    )
    add(
        "cmp_st_p_min_constr",
        [(v["cmp_p"], 1.0), (v["cmp_st"], -param("cmp_p_min"))],
        ">=",
    )
    add(
        "cmp_st_p_max_constr",
        [
            (v["cmp_p"], 1.0),
            (v["cmp_st"], -(cmp_max_m * cav_level_max + cmp_max_b)),
        ],
        "<=",
    )
    add(
        "cmp_q_out_constr",
        [
            (v["cmp_q_out_sum"], 1.0),
            (v["cmp_p"], -param("cmp_q_out_m")),
            (v["cmp_st"], -param("cmp_q_out_b")),
        ],
        "=",
    )
    add(
        "cmp_q_out_sum_constr",
        [
            (v["cmp_q_out_sum"], 1.0),
            (v["cmp_q_waste"], -1.0),
            (v["tes_e_in"], -1.0),
        ],
        "=",
    )
    add(
        "cmp_q_out_shr_constr",
        [(v["cmp_q_waste"], cmp_share), (v["tes_e_in"], -(1 - cmp_share))],
        "=",
    )

    # --- expansion --------------------------------------------------------
    add("exp_p_constr", [(v["exp_p"], -1.0), (el_out, 1.0)], "=")
    add(
        "exp_p_max_constr",
        [(v["exp_p_max"], 1.0), (cav_prev, -exp_max_m)],
        "=",
        exp_max_b,
    )
    add(
        "exp_p_max_area_constr",
        [(v["exp_p"], 1.0), (v["exp_p_max"], -1.0)],
        "<=",
    )
    add(
        "exp_st_p_min_constr",
        [(v["exp_p"], 1.0), (v["exp_st"], -param("exp_p_min"))],
        ">=",
    )
    add(
        "exp_st_p_max_constr",
        [
            (v["exp_p"], 1.0),
            (v["exp_st"], -(exp_max_m * cav_level_max + exp_max_b)),
        ],
        "<=",
    )
    add(
        "exp_q_in_constr",
        [
            (v["exp_q_in_sum"], 1.0),
            (v["exp_p"], -param("exp_q_in_m")),
            (v["exp_st"], -param("exp_q_in_b")),
        ],
        "=",
    )
    add("exp_q_fuel_constr", [(v["exp_q_fuel_in"], -1.0), (fuel_in, 1.0)], "=")
    add(
        "exp_q_in_sum_constr",
        [
            (v["exp_q_in_sum"], 1.0),
            (v["exp_q_fuel_in"], -1.0),
            (v["tes_e_out"], -1.0),
            (v["exp_q_add_in"], -1.0),
        ],
        "=",
    )
    add(
        "exp_q_in_shr_constr",
        [
            (v["exp_q_fuel_in"], exp_share),
            (v["exp_q_add_in"], -(1 - exp_share)),
            (v["tes_e_out"], -(1 - exp_share)),
        ],
        "=",
    )

    # --- cavern -----------------------------------------------------------
    # the y-intersections are constants, not multiplied by the status
    add(
        "cav_e_in_constr",
        [(v["cav_e_in"], 1.0), (v["cmp_p"], -param("cav_e_in_m"))],
        "=",
        param("cav_e_in_b"),
    )
    # the outflow depends on the expansion power
    add(
        "cav_e_out_constr",
        [(v["cav_e_out"], 1.0), (v["exp_p"], -param("cav_e_out_m"))],
        "=",
        param("cav_e_out_b"),
    )
    # eta * level(t) == level(t-1) + tau * (in - out) (t = 0: no level(t-1))
    add(
        "cav_eta_constr",
        [
            (v["cav_level"], param("cav_eta_temp")),
            (cav_prev, -1.0),
            (v["cav_e_in"], -tau),
            (v["cav_e_out"], tau),
        ],
        "=",
    )
    add("cav_ub_constr", [(v["cav_level"], 1.0)], "<=", cav_level_max)

    # --- thermal energy storage (tes_eta_temp is not used) ----------------
    add(
        "tes_eta_constr",
        [
            (v["tes_level"], 1.0),
            (tes_prev, -1.0),
            (v["tes_e_in"], -tau),
            (v["tes_e_out"], tau),
        ],
        "=",
    )
    add(
        "tes_ub_constr",
        [(v["tes_level"], 1.0)],
        "<=",
        param("tes_level_max"),
    )
