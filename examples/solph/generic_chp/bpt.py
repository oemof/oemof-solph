# -*- coding: utf-8 -*-
"""
Example that illustrates how to use custom component `GenericCHP` can be used.

In this case it is used to model a back pressure turbine.
"""

import pandas as pd
import oemof.solph as solph
from oemof.outputlib import processing, views
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# maximum timesteps are 200 in this case, everything above creates the same
# lp-files and thus results
def run_example(file_name='generic_chp', timesteps=200,
                plot=False, silent=True):
    """
    Function for `GenericCHP` example that generates test results.

    --------
    >>> import numpy as np
    >>> results_original = [6203.3011879818987, 13796.698812010998, 20000.0]
    >>> results_actual = run_example()
    >>> np.isclose(results_original, results_actual,
    ...            rtol=1e-4, atol=1e-07).tolist()
    [True, True, True]
    """
    #
    data = pd.read_csv(file_name + '.csv', sep=",")

    # select periods
    periods = len(data[0:timesteps])-1

    # create an energy system
    idx = pd.date_range('1/1/2017', periods=periods, freq='H')
    es = solph.EnergySystem(timeindex=idx)

    # resources
    bgas = solph.Bus(label='bgas')

    rgas = solph.Source(label='rgas', outputs={bgas: solph.Flow()})

    # heat
    bth = solph.Bus(label='bth')

    # dummy source at high costs that serves the residual load
    source_th = solph.Source(label='source_th',
                             outputs={bth: solph.Flow(variable_costs=1000)})

    demand_th = solph.Sink(label='demand_th', inputs={
                            bth: solph.Flow(fixed=True,
                                            actual_value=data['demand_th'],
                                            nominal_value=200)})

    # power
    bel = solph.Bus(label='bel')

    demand_el = solph.Sink(label='demand_el', inputs={bel: solph.Flow(
                           variable_costs=data['price_el'])})

    # back pressure turbine with same parameters as ccet
    # (for back pressure characteristics Q_CW_min=0 and back_pressure=True)
    bpt = solph.components.GenericCHP(
        label='back_pressure_turbine',
        fuel_input={bgas: solph.Flow(
            H_L_FG_share_max=[0.19 for p in range(0, periods)])},
        electrical_output={bel: solph.Flow(
            P_max_woDH=[200 for p in range(0, periods)],
            P_min_woDH=[80 for p in range(0, periods)],
            Eta_el_max_woDH=[0.53 for p in range(0, periods)],
            Eta_el_min_woDH=[0.43 for p in range(0, periods)])},
        heat_output={bth: solph.Flow(
            Q_CW_min=[0 for p in range(0, periods)])},
        Beta=[0.19 for p in range(0, periods)],
        fixed_costs=0, back_pressure=True)

    # create an optimization problem and solve it
    om = solph.OperationalModel(es)

    # debugging
    om.write('bpt.lp', io_options={'symbolic_solver_labels': True})

    # solve model
    if silent is not True:
        om.solve(solver='gurobi', solve_kwargs={'tee': True})
    else:
        om.solve(solver='gurobi', solve_kwargs={'tee': False})

    # create result object
    results = processing.results(om)

    # store as csv
    # data = results[(bpt,)]['sequences'].to_csv('results_ccet_' + file_name)

    # plot data
    if plt is not None and plot is True:
        # plot PQ diagram from component results
        data = results[(bpt,)]['sequences']
        ax = data.plot(kind='scatter', x='Q', y='P', grid=True)
        ax.set_xlabel('Q (MW)')
        ax.set_ylabel('P (MW)')
        plt.show()

        # plot thermal bus
        data = views.node(results, 'bth')['sequences']
        ax = data.plot(kind='line', drawstyle='steps-post', grid=True)
        ax.set_xlabel('Time (h)')
        ax.set_ylabel('Q (MW)')
        plt.show()

    # generate test results
    data = views.node(results, 'bth')
    testresults = list(data['sequences'].sum(axis=0).to_dict().values())
    testresults = sorted(testresults)

    return testresults


if __name__ == '__main__':
    import doctest
    import filecmp

    # run doctests
    doctest.testmod()

    # check lp files (constraints)
    if not filecmp.cmp('bpt_original.lp', 'bpt.lp'):
        print('LP files are not identical!')

    # run example
    run_example(plot=True, silent=False)
