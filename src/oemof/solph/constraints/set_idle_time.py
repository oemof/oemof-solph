# -*- coding: utf-8 -*-

"""Constraints to relate variables in an existing model.

SPDX-FileCopyrightText: Jann Launer

SPDX-License-Identifier: MIT
"""
from pyomo import environ as po
from pyomo.core.util import prod


def set_idle_time(model, f1, f2, n, name_constraint="constraint_idle_time"):
    r"""
    Enforces f1 to be inactive for n timesteps before f2 can be active.

    For each timestep status of f2 can only be "on" if f1 has been off the previous n timesteps.

    **Constraint:**

    .. math:: X_2(t) \cdot \sum_{s=0}^t X_1(s) = 0 \forall t < n
    .. math:: X_2(t) \cdot \sum_{s=t-n}^t X_1(s) = 0 \forall t \le n

    """
    # make sure that idle time is not longer than number of timesteps
    n_timesteps = len(model.TIMESTEPS)
    assert (
        n_timesteps > n
    ), f"Selected idle time {n} is longer than total number of timesteps {n_timesteps}"

    def _idle_rule(m):
        # In the first n steps, the status of f1 has to be inactive for f2 to be active
        for ts in list(m.TIMESTEPS)[:n]:
            expr = (
                m.NonConvexFlowBlock.status[f2[0], f2[1], ts]
                * sum(
                    m.NonConvexFlowBlock.status[f1[0], f1[1], t]
                    for t in range(ts+1)
                )
                == 0
            )
            if expr is not True:
                getattr(m, name_constraint).add(ts, expr)

        # for all following timesteps, f1 has to be inactive in the preceding window of n timesteps for f2 to be active
        for ts in list(m.TIMESTEPS)[n:]:
            expr = (
                m.NonConvexFlowBlock.status[f2[0], f2[1], ts]
                * sum(
                    m.NonConvexFlowBlock.status[f1[0], f1[1], t]
                    for t in range(ts - n, ts+1)
                )
                == 0
            )
            if expr is not True:
                getattr(m, name_constraint).add(ts, expr)

    setattr(
        model,
        name_constraint,
        po.Constraint(model.TIMESTEPS, noruleinit=True),
    )
    setattr(
        model,
        name_constraint + "_build",
        po.BuildAction(rule=_idle_rule),
    )

    return model
