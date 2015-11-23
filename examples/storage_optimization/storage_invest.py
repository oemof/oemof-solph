# -*- coding: utf-8 -*-

"""
General description:
---------------------

The example models the following energy system:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |

Data:
------
The application uses some data from BNetzA scenario 2033 B. Demand-series
are generated randomly.

Notes:
-------
The energy system is build out of objects. It is solved and the results
are written back into the objects.

"""

###############################################################################
# imports
###############################################################################

import pandas as pd

# import solph module to create/process optimization model instance
from oemof.solph import postprocessing as pp

# import oemof base classes to create energy system objects
from oemof.core import energy_system as es
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer


###############################################################################
# read data from csv file
###############################################################################

data = pd.read_csv("storage_invest.csv", sep=",")
timesteps = [t for t in range(192)]


###############################################################################
# set optimzation options for storage components
###############################################################################

transformer.Storage.optimization_options.update({'investment': lambda: True})

###############################################################################
# Create oemof objetc
###############################################################################

# create bus
bgas = Bus(uid="bgas",
           type="gas",
           price=70,
           balanced=True,
           excess=False)

# create electricity bus
bel = Bus(uid="bel",
          type="el",
          excess=True)

# create commodity object for gas resource
rgas = source.Commodity(uid='rgas',
                        outputs=[bgas],
                        sum_out_limit=194397000)

# create fixed source object for wind
wind = source.FixedSource(uid="wind",
                          outputs=[bel],
                          val=data['wind'],
                          out_max=[1000000],
                          add_out_limit=0,
                          capex=1000,
                          opex_fix=20,
                          lifetime=25,
                          crf=0.08)

# create fixed source object for pv
pv = source.FixedSource(uid="pv",
                        outputs=[bel],
                        val=data['pv'],
                        out_max=[582000],
                        add_out_limit=0,
                        capex=900,
                        opex_fix=15,
                        lifetime=25,
                        crf=0.08)

# create simple sink object for demand
demand = sink.Simple(uid="demand", inputs=[bel], val=data['demand_el'])

# create simple transformer object for gas powerplant
pp_gas = transformer.Simple(uid='pp_gas',
                            inputs=[bgas], outputs=[bel],
                            opex_var=50, out_max=[10e10], eta=[0.58])

# create storage transformer object for storage
storage = transformer.Storage(uid='sto_simple',
                              inputs=[bel],
                              outputs=[bel],
                              eta_in=1,
                              eta_out=0.8,
                              cap_loss=0.00,
                              opex_fix=35,
                              opex_var=10e10,
                              capex=1000,
                              cap_max=0,
                              cap_initial=0,
                              c_rate_in=1/6,
                              c_rate_out=1/6)

###############################################################################
# Create, solve and postprocess OptimizationModel instance
###############################################################################

# group busses
buses = [bgas, bel]

# create lists of components
transformers = [pp_gas]
renewable_sources = [pv, wind]
commodities = [rgas]
storages = [storage]
sinks = [demand]

# groupt components
components = transformers + renewable_sources + storages + sinks + commodities

# create list of all entities
entities = components + buses

# TODO: other solver libraries should be passable
simulation = es.Simulation(solver='glpk', timesteps=timesteps,
                           stream_solver_output=True)

energysystem = es.EnergySystem(entities=entities, simulation=simulation)

energysystem.optimize()

# write results back to objects
pp.results_to_objects(energysystem.optimization_model)


if __name__ == "__main__":
    import postprocessing as pp

    data = renewable_sources+transformers+storages

    pp.plot_dispatch('bel', timesteps, data, storage, demand)
#    pp.plot_dispatchplt.show()

    pp.print_results('bel', data, demand, transformers, storage,
                     energysystem)
