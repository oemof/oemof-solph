# -*- coding: utf-8 -*-

"""Solving a LinopyModel.

SPDX-License-Identifier: MIT
"""

import logging
import time
import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd

from oemof.solph._models import SolverResults


@dataclass
class LinopySolverReturn:
    """What :attr:`LinopyModel.solver_return` holds after a solve.

    The attribute names follow Pyomo's appsi results, which
    :func:`oemof.solph.processing.meta_results` reads.
    """

    status: str
    termination_condition: str
    best_feasible_objective: float | None
    best_objective_bound: float | None
    wallclock_time: float


# solvers linopy talks to in memory; all others go through LP/MPS files
DIRECT_SOLVERS = {"highs", "gurobi", "mosek", "xpress", "cplex", "copt"}

# solve_kwargs of the Pyomo backend and their linopy/solver equivalent
_QUIET_OPTIONS = {
    "highs": {"output_flag": False},
    "gurobi": {"OutputFlag": 0},
}


def solve(
    model,
    solver="cbc",
    solver_io=None,
    allow_nonoptimal=False,
    duals=False,
    solve_kwargs=None,
    cmdline_options=None,
):
    """Solve `model` with linopy; see :meth:`LinopyModel.solve`."""
    solve_kwargs = dict(solve_kwargs or {})
    options = dict(cmdline_options or {})
    tee = bool(solve_kwargs.pop("tee", False))
    for unknown in list(solve_kwargs):
        warnings.warn(
            f"solve_kwargs '{unknown}' is passed to linopy's solve() "
            "unchanged.",
            UserWarning,
        )
    if not tee:
        for key, value in _QUIET_OPTIONS.get(solver, {}).items():
            options.setdefault(key, value)
    if duals:
        model.dual = True
        model.rc = True

    io_api = solver_io
    if io_api is None or io_api == "python":
        io_api = "direct" if solver in DIRECT_SOLVERS else "lp"
    if io_api != "direct" and model.linopy.ncons == 0:
        # an LP file without constraints is rejected by e.g. CBC; Pyomo
        # writes the same dummy constraint (ONE_VAR_CONSTANT = 1)
        if "ONE_VAR_CONSTANT" not in model.linopy.variables:
            one = model.linopy.add_variables(
                lower=1, upper=1, name="ONE_VAR_CONSTANT"
            )
            model.linopy.add_constraints(one == 1, name="ONE_VAR_CONSTANT")

    start = time.perf_counter()
    status, condition = model.linopy.solve(
        solver_name=solver, io_api=io_api, **solve_kwargs, **options
    )
    wallclock = time.perf_counter() - start

    optimal = status == "ok" and str(condition) == "optimal"
    objective = model.linopy.objective.value if optimal else None
    is_mip = bool(len(model.linopy.integers) or len(model.linopy.binaries))
    model.solver_return = LinopySolverReturn(
        status=str(status),
        termination_condition=str(condition),
        best_feasible_objective=objective,
        # an optimal LP has no gap; linopy reports no bound for MIPs
        best_objective_bound=None if is_mip else objective,
        wallclock_time=wallclock,
    )
    info = SolverResults(
        optimal=optimal,
        solver=solver,
        objective=objective,
        termination_condition=str(condition),
        status=str(status),
        wallclock_time=wallclock,
        best_feasible_objective=objective,
        best_objective_bound=None,
        gap=None,
        message=f"Problem solved using '{solver}' with linopy",
    )
    # the shape of Pyomo's results, for the deprecated
    # Model.solver_results["Solver"][0][...] access
    model._solver_results = {
        "Solver": [
            {
                "Status": str(status),
                "Termination condition": str(condition),
                "Time": wallclock,
            }
        ]
    }

    # --- BEGIN: To be removed together with Model's version (v0.7) ---
    _set_deprecated_energy_system_results(model)
    # --- END ---

    if optimal:
        logging.info("Optimisation successful.")
    else:
        msg = (
            f"The solver did not return an optimal solution. "
            f"Instead the optimisation ended with\n"
            f"       - status: {status}\n"
            f"       - termination condition: {condition}"
        )
        if allow_nonoptimal:
            warnings.warn(msg, UserWarning)
            return model.solver_return
        raise RuntimeError(msg)

    from oemof.solph._results import Results

    return Results(model, solver_info=pd.Series(info.__dict__))


def reduced_costs(model):
    """Reduced costs of all variables, c - A'y, keyed by variable label.

    linopy returns primal values and row duals only; the reduced costs
    follow from them for any solver.
    """
    m = model.linopy
    matrices = m.matrices
    duals = np.nan_to_num(np.asarray(matrices.dual, dtype=float))
    rc = np.asarray(matrices.c, dtype=float) - matrices.A.T @ duals
    return dict(zip(np.asarray(matrices.vlabels), rc))


def _set_deprecated_energy_system_results(model):
    """EnergySystem.results, deprecated, as set by Model.solve()."""
    from oemof.solph import EnergySystem

    model.es._results = model._solver_results

    def results(self):
        warnings.warn(
            "EnergySystem.results is deprecated and will be removed in a"
            " future version. Use solph.Results instead.",
            FutureWarning,
        )
        return self._results

    EnergySystem.results = property(results)
