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


def check_oemof_installation(silent=False):
    logging.disable(logging.CRITICAL)

    date_time_index = pd.date_range("1/1/2012", periods=5, freq="H")
    energysystem = solph.EnergySystem(timeindex=date_time_index)

    bgas = solph.Bus(label="natural_gas")
    bel = solph.Bus(label="electricity")
    solph.Sink(label="excess_bel", inputs={bel: solph.Flow()})
    solph.Source(label="rgas", outputs={bgas: solph.Flow()})
    solph.Sink(
        label="demand",
        inputs={bel: solph.Flow(fix=[10, 20, 30, 40, 50], nominal_value=1)},
    )
    solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
        conversion_factors={bel: 0.58},
    )
    om = solph.Model(energysystem)

    # check solvers
    solver = dict()
    for s in ["cbc", "glpk", "gurobi", "cplex"]:
        try:
            om.solve(solver=s)
            solver[s] = "working"
        except Exception:
            solver[s] = "not working"

    if not silent:
        print()
        print("*****************************")
        print("Solver installed with oemof:")
        print()
        for s, t in solver.items():
            print("{0}: {1}".format(s, t))
        print()
        print("*****************************")
        print("oemof successfully installed.")
        print("*****************************")
