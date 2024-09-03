# -*- coding: utf-8 -*-

"""This module can be used to check the installation.

This is not an illustrated example.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: jnnr

SPDX-License-Identifier: MIT

"""

import logging

import pandas as pd

from oemof import solph


def _check_oemof_installation(solvers):
    logging.disable(logging.CRITICAL)

    date_time_index = pd.date_range("1/1/2012", periods=6, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=False,
    )

    bgas = solph.buses.Bus(label="natural_gas")
    bel = solph.buses.Bus(label="electricity")
    solph.components.Sink(label="excess_bel", inputs={bel: solph.flows.Flow()})
    solph.components.Source(label="rgas", outputs={bgas: solph.flows.Flow()})
    solph.components.Sink(
        label="demand",
        inputs={
            bel: solph.flows.Flow(fix=[10, 20, 30, 40, 50], nominal_capacity=1)
        },
    )
    solph.components.Converter(
        label="pp_gas",
        inputs={bgas: solph.flows.Flow()},
        outputs={
            bel: solph.flows.Flow(nominal_capacity=10e10, variable_costs=50)
        },
        conversion_factors={bel: 0.58},
    )
    om = solph.Model(energysystem)

    # check solvers
    solver_status = dict()
    for s in solvers:
        try:
            om.solve(solver=s)
            solver_status[s] = True
        except Exception:
            solver_status[s] = False

    return solver_status


def check_oemof_installation():

    solvers_to_test = ["cbc", "glpk", "gurobi", "cplex"]

    solver_status = _check_oemof_installation(solvers_to_test)

    print_text = (
        "***********************************\n"
        "Solver installed with oemof.solph:\n"
        "\n"
    )
    for solver, works in solver_status.items():
        if works:
            print_text += f"{solver}: installed and working\n"
        else:
            print_text += f"{solver}: not installed/ not working\n"
    print_text += (
        "\n"
        "***********************************\n"
        "oemof.solph successfully installed.\n"
        "***********************************\n"
    )

    print(print_text)
