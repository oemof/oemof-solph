"""
This module can be used to check the installation.
This is not an illustrated example.
"""

import oemof.solph as solph
import pandas as pd


def run_test_example():
    date_time_index = pd.date_range('1/1/2012', periods=5, freq='H')

    energysystem = solph.EnergySystem(timeindex=date_time_index)

    bgas = solph.Bus(label="natural_gas")
    bel = solph.Bus(label="electricity")
    solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})
    solph.Source(label='rgas', outputs={bgas: solph.Flow()})
    solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=[10, 20, 30, 40, 50], fixed=True, nominal_value=1)})
    solph.LinearTransformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
        conversion_factors={bel: 0.58})
    om = solph.OperationalModel(energysystem)

    # check solvers
    solver = dict()
    for s in ['cbc', 'glpk', 'gurobi', 'cplex']:
        try:
            om.solve(solver=s)
            solver[s] = "working"
        except Exception:
            solver[s] = "not working"
    print("*********")
    print('Solver installed with oemof:')
    for s, t in solver.items():
        print("{0}: {1}".format(s, t))
    print("*********")
    print("oemof successfully installed.")

if __name__ == "__main__":
    run_test_example()
