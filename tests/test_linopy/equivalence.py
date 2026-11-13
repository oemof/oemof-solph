# -*- coding: utf-8 -*-

"""Equivalence harness: build one energy system with both backends.

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd

from oemof import solph
from oemof.solph._linopy import LinopyModel
from oemof.solph._models import Model as PyomoModel


def solve_both(build_energy_system, solver="highs", duals=False, **kwargs):
    """Solve the energy system from `build_energy_system()` twice.

    The energy system is built anew for each backend, so that neither
    model sees state left by the other.

    Returns
    -------
    (pyomo_model, pyomo_results, linopy_model, linopy_results)
    """
    pyomo_model = PyomoModel(build_energy_system(), **kwargs)
    pyomo_results = pyomo_model.solve(solver=solver, duals=duals)
    linopy_model = LinopyModel(build_energy_system(), **kwargs)
    linopy_results = linopy_model.solve(solver=solver, duals=duals)
    return pyomo_model, pyomo_results, linopy_model, linopy_results


def _by_label(frame):
    """Columns keyed by labels instead of node objects, so that frames of
    two separately built energy systems can be compared."""

    def key(column):
        if isinstance(column, tuple):
            return tuple(str(getattr(c, "label", c)) for c in column)
        return str(getattr(column, "label", column))

    frame = frame.copy()
    frame.columns = [key(c) for c in frame.columns]
    return frame.reindex(sorted(frame.columns), axis=1)


def assert_frames_agree(pyomo_frame, linopy_frame, rtol=1e-6, atol=1e-6):
    """Compare two result tables by label, column by column."""
    left = _by_label(pyomo_frame)
    right = _by_label(linopy_frame)
    assert list(left.columns) == list(right.columns), (
        f"different columns:\n  pyomo:  {list(left.columns)}\n"
        f"  linopy: {list(right.columns)}"
    )
    assert left.shape == right.shape, (left.shape, right.shape)
    np.testing.assert_allclose(
        left.to_numpy(dtype=float),
        right.to_numpy(dtype=float),
        rtol=rtol,
        atol=atol,
    )
    pd.testing.assert_index_equal(left.index, right.index)


def assert_backends_agree(
    build_energy_system,
    solver="highs",
    compare=("flow",),
    duals=False,
    rtol=1e-6,
    atol=1e-6,
    **kwargs,
):
    """Solve with both backends; compare objective and result tables.

    Parameters
    ----------
    build_energy_system : callable
        Returns a fresh :class:`~oemof.solph.EnergySystem` on every call.
    compare : iterable of str
        Result keys (as in :meth:`oemof.solph.Results.get`) to compare
        value by value. For degenerate problems with alternative optima,
        compare the objective only (``compare=()``).
    duals : bool
        Also compare bus duals and reduced costs.
    """
    pyomo_model, pyomo_results, linopy_model, linopy_results = solve_both(
        build_energy_system, solver=solver, duals=duals, **kwargs
    )
    assert linopy_results.solver["optimal"]
    np.testing.assert_allclose(
        linopy_results.solver["objective"],
        pyomo_results.solver["objective"],
        rtol=rtol,
        atol=atol,
    )
    for key in compare:
        assert_frames_agree(
            pyomo_results.get(key),
            linopy_results.get(key),
            rtol=rtol,
            atol=atol,
        )
    if duals:
        for key in ("duals", "reduced_costs"):
            assert_frames_agree(
                pyomo_results.get(key),
                linopy_results.get(key),
                rtol=rtol,
                atol=atol,
            )
    return pyomo_results, linopy_results


__all__ = [
    "assert_backends_agree",
    "assert_frames_agree",
    "solph",
    "solve_both",
]
