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
from linopy.solvers import Solver

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


# solve_kwargs of the Pyomo backend: their linopy keyword or solver option
_SOLVE_KWARGS = {
    "keepfiles": ("linopy", "keep_files"),
    "timelimit": ("option", {"highs": "time_limit", "gurobi": "TimeLimit"}),
    "symbolic_solver_labels": ("ignore", None),
}


def _translate(solver, solve_kwargs, options):
    linopy_kwargs = {}
    for key, value in solve_kwargs.items():
        kind, target = _SOLVE_KWARGS.get(key, ("unknown", None))
        if kind == "linopy":
            linopy_kwargs[target] = value
        elif kind == "option" and solver in target:
            options.setdefault(target[solver], value)
        elif kind == "ignore":
            continue
        else:
            warnings.warn(
                f"solve_kwargs '{key}' has no equivalent for '{solver}' in "
                "the linopy backend and is passed to linopy unchanged.",
                UserWarning,
            )
            linopy_kwargs[key] = value
    return linopy_kwargs


def solve(
    model,
    solver="cbc",
    solver_io=None,
    allow_nonoptimal=False,
    duals=False,
    solve_kwargs=None,
    cmdline_options=None,
    persistent=False,
):
    """Solve `model` with linopy; see :meth:`LinopyModel.solve`."""
    solve_kwargs = dict(solve_kwargs or {})
    options = dict(cmdline_options or {})
    tee = bool(solve_kwargs.pop("tee", False))
    linopy_kwargs = _translate(solver, solve_kwargs, options)
    if not tee:
        for key, value in _QUIET_OPTIONS.get(solver, {}).items():
            options.setdefault(key, value)
    if duals:
        model.dual = True
        model.rc = True
    model._solve_settings = {
        "solver": solver,
        "allow_nonoptimal": allow_nonoptimal,
    }

    start = time.perf_counter()
    if persistent:
        solver_object = Solver.from_name(
            solver,
            model.linopy,
            io_api="direct",
            options=options,
            track_updates=True,
        )
        solver_object.solve(model.linopy, assign=True, **linopy_kwargs)
        status, condition = (
            model.linopy.status,
            model.linopy.termination_condition,
        )
        model._persistent = solver_object
    else:
        io_api = solver_io
        if io_api is None or io_api == "python":
            io_api = "direct" if solver in DIRECT_SOLVERS else "lp"
        _add_dummy_constraint_for_files(model, io_api)
        status, condition = model.linopy.solve(
            solver_name=solver, io_api=io_api, **linopy_kwargs, **options
        )
        model._persistent = None
    return _finish(model, status, condition, time.perf_counter() - start)


def resolve(model, require_in_place=False):
    """Solve again with the persistent solver of the last solve; the
    solver applies the changes since then in place where it can."""
    if getattr(model, "_persistent", None) is None:
        msg = "resolve() needs a previous solve(..., persistent=True)."
        raise RuntimeError(msg)
    start = time.perf_counter()
    model._persistent.solve(
        model.linopy, assign=True, disallow_rebuild=require_in_place
    )
    return _finish(
        model,
        model.linopy.status,
        model.linopy.termination_condition,
        time.perf_counter() - start,
    )


def _add_dummy_constraint_for_files(model, io_api):
    if io_api != "direct" and model.linopy.ncons == 0:
        # an LP file without constraints is rejected by e.g. CBC; Pyomo
        # writes the same dummy constraint (ONE_VAR_CONSTANT = 1)
        if "ONE_VAR_CONSTANT" not in model.linopy.variables:
            one = model.linopy.add_variables(
                lower=1, upper=1, name="ONE_VAR_CONSTANT"
            )
            model.linopy.add_constraints(one == 1, name="ONE_VAR_CONSTANT")


def _finish(model, status, condition, wallclock):
    """SolverResults, deprecated attributes and the Results object."""
    settings = model._solve_settings
    solver = settings["solver"]
    status = str(getattr(status, "value", status))
    condition = str(getattr(condition, "value", condition))
    optimal = status == "ok" and condition == "optimal"
    objective = (
        model.linopy.objective.value + model._objective_constant
        if optimal
        else None
    )
    is_mip = bool(len(model.linopy.integers) or len(model.linopy.binaries))
    model.solver_return = LinopySolverReturn(
        status=status,
        termination_condition=condition,
        best_feasible_objective=objective,
        # an optimal LP has no gap; linopy reports no bound for MIPs
        best_objective_bound=None if is_mip else objective,
        wallclock_time=wallclock,
    )
    info = SolverResults(
        optimal=optimal,
        solver=solver,
        objective=objective,
        termination_condition=condition,
        status=status,
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
                "Status": status,
                "Termination condition": condition,
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
        if settings["allow_nonoptimal"]:
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
