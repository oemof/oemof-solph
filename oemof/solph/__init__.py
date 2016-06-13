"""


"""
from oemof.solph.network import (Sink, Source, LinearTransformer, Storage, Bus,
                                 Flow)
from oemof.solph.plumbing import OperationalModel
from oemof.solph.groupings import GROUPINGS


if __name__ == "__main__":
    import pandas as pd
    from oemof.core import energy_system as oces
    from oemof.solph.options import Investment, Discrete

    es = oces.EnergySystem(groupings=GROUPINGS,
                           time_idx=[1,2,3])

    lt = len(es.time_idx)

    bel = Bus(label="el_balance")
    bcoal = Bus(label="coalbus")

    so = Source(label="coalsource",
                outputs={bcoal: Flow()})

    wind = Source(label="wind", outputs={
        bel:Flow(actual_value=[1, 1, 2],
                 nominal_value=2,
                 fixed_costs=25,
                 investment=Investment(maximum=100, ep_costs=200))
        }
    )

    si = Sink(label="sink", inputs={bel: Flow(max=[0.1, 0.2, 0.9],
                                              nominal_value=10, fixed=True,
                                              negative_gradient = 0.5,
                                              actual_value=[1, 2, 3])})

    trsf = LinearTransformer(label='trsf', inputs={bcoal:Flow()},
                             outputs={bel:Flow(nominal_value=10,
                                               min= 0.5, fixed_costs=5,
                                               variable_costs=10, summed_max=4,
                                               positive_gradient=0.5,
                                               negative_gradient=0.5,
                                               summed_min=2,
                                               discrete=Discrete(startup_costs=104,
                                                                 shutdown_costs=99, initial_status=0))},
                             conversion_factors={bel: 0.4})
    stor = Storage(label="stor", inputs={bel: Flow()}, outputs={bel:Flow()},
                   nominal_capacity=50, inflow_conversion_factor=0.9,
                   outflow_conversion_factor=0.8, initial_capacity=0.5,
                   capacity_loss=0.001)

    date_time_index = pd.date_range('1/1/2011', periods=3, freq='60min')
    om = OperationalModel(es, timeindex=date_time_index)
    om.solve(solve_kwargs={'tee': True})
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})
    #om.pprint()
