# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `PiecewiseLinearTransformer`
can be used.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
oemof/tests/test_scripts/test_solph/test_generic_chp/test_generic_chp.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import pandas as pd
from oemof.solph import (Sink, Bus, Flow, Model, EnergySystem)
import oemof.outputlib as outputlib
import oemof.solph as solph
import numpy as np


def test_pwltf():
    # Set timeindex and create data
    periods = 20
    datetimeindex = pd.date_range('1/1/2019', periods=periods, freq='H')
    step = 5
    demand = np.arange(0, step*periods, step)

    # Set up EnergySystem, buses and sink
    energysystem = EnergySystem(timeindex=datetimeindex)
    b_gas = Bus(label='gas', balanced=False)
    b_el = Bus(label='electricity')
    demand_el = Sink(label='demand',
                     inputs={b_el: Flow(nominal_value=1,
                                        actual_value=demand,
                                        fixed=True)})

    energysystem.add(b_gas, b_el, demand_el)

    # Define conversion function and breakpoints
    conv_func = lambda x: 0.01 * x**2
    in_breakpoints = np.arange(0, 110, 25)
    out_breakpoints = conv_func(in_breakpoints)

    # Create and add PiecewiseLinearTransformer
    pwltf = solph.custom.PiecewiseLinearTransformer(
        label='pwltf',
        inputs={b_gas: solph.Flow(
        nominal_value=100,
        variable_costs=1)},
        outputs={b_el: solph.Flow()},
        in_breakpoints=in_breakpoints,
        out_breakpoints=out_breakpoints,
        conversion_function=conv_func,
        pw_repn='CC')

    energysystem.add(pwltf)

    # Create and solve the optimization model
    optimization_model = Model(energysystem)
    optimization_model.solve(solver='cbc')

    # Get results
    results = outputlib.processing.results(optimization_model)
    string_results = outputlib.processing.convert_keys_to_strings(results)
    sequences = {k:v['sequences'] for k, v in string_results.items()}
    df = pd.concat(sequences, axis=1)
    df[('efficiency', None, None)] = df[('pwltf', 'electricity')].divide(df[('gas', 'pwltf')])

    # Test: Compare results with piecewise linearized function
    def linearized_func(func, x_break, x):
        y_break=func(x_break)
        condlist = [(x_l <= x)&(x < x_u) for x_l, x_u in zip(x_break[:-1], x_break[1:])]
        funclist = []
        for i in range(len(x_break)-1):
            b = y_break[i]
            a = (y_break[i+1] - y_break[i]) * 1/((x_break[i+1] - x_break[i]))
            funclist.append(lambda x, b=b, a=a, i=i: b + a*(x-x_break[i]))
        return np.piecewise(x, condlist, funclist)

    production_expected = linearized_func(conv_func, in_breakpoints, df[('gas', 'pwltf')]['flow'].values)
    production_modeled = df[('pwltf', 'electricity')]['flow'].values

    assert np.allclose(production_modeled, production_expected)
