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

import matplotlib.pyplot as plt
import pandas as pd

# import solph module to create/process optimization model instance
from oemof.solph.optimization_model import OptimizationModel
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

data = pd.read_csv("example_data_sc160.csv", sep=",")
timesteps = [t for t in range(8760)]


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
                              c_rate_in = 1/6,
                              c_rate_out = 1/6)

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

simulation = es.Simulation(solver='glpk', timesteps=timesteps,
                           stream_solver_output=True)
energysystem = es.EnergySystem(entities=entities, simulation=simulation)

energysystem.optimize()

# write results back to objects
pp.results_to_objects(energysystem.optimization_model)


# group specific components for result analysis
#components = transformers + renewable_sources


if __name__ == "__main__":
    def plot_dispatch(bus_to_plot):
        # plotting: later as multiple pdf with pie-charts and topology?
        import numpy as np
        import matplotlib as mpl
        import matplotlib.cm as cm

        plot_data = renewable_sources+transformers+storages

        # data preparation
        x = np.arange(len(timesteps))
        y = []
        labels = []
        for c in plot_data:
            if bus_to_plot in c.results['out']:
                y.append(c.results['out'][bus_to_plot])
                labels.append(c.uid)

        # plot production
        fig, ax = plt.subplots()
        sp = ax.stackplot(x, y,
                          colors=('yellow', 'blue', 'grey', 'red'),
                          linewidth=0)

        proxy = [mpl.patches.Rectangle((0, 0), 0, 0,
                                       facecolor=
                                       pol.get_facecolor()[0]) for pol in sp]
        # plot demand
        ax.step(x, demand.results['in'][demand.inputs[0].uid],
                c="black", lw=2)

        # storage soc (capacity at every timestep)
#        ax.step(x, sto_simple.results['cap'], c='green', lw=2.4)

        # plot storage input
        ax.step(x, (np.asarray(
            storage.results['in'][storage.inputs[0].uid])
            + np.asarray(
                demand.results['in'][demand.inputs[0].uid])),
            c='red', ls='-', lw=1)

        ax.legend(proxy, labels)
        ax.grid()

        ax.set_xlabel('Timesteps in h')
        ax.set_ylabel('Power in kW')
        ax.set_title('Dispatch')

    def print_results(bus_to_print):
        import numpy as np

        # demand results
        print('sum elec demand: ',
              np.asarray(demand.results['in'][bus_to_print]).sum())

        # production results
        print_data = renewable_sources+transformers+storages
        sum_production = np.array([])
        for c in print_data:
            print(c)
            res = np.asarray(c.results['out'][bus_to_print])
            sum_production = np.append(sum_production, res)
            print('sum: ', res.sum())
            print('maximum value: ', res.max())

        # only non renewable production results
        transf = np.array([])
        for t in transformers:
            res = np.asarray(t.results['out'][bus_to_print])
            transf = np.append(transf, res)
            print('sum non renewable: ', transf.sum())

        # storage state and capacity
        storage_soc = np.asarray(storage.results['cap'])
        print('sum storage content: ', storage_soc.sum())
        print('storage capacity: ', storage_soc.max())

        # storage load
        storage_load = np.asarray(
            storage.results['in'][storage.inputs[0].uid])
        print('sum storage load: ', storage_load.sum())
        print('maximum storage load: ', storage_load.max())

        # excess
        excess = list()
        for t in energysystem.simulation.timesteps:
            excess.append(
              energysystem.optimization_model.bus.excess_slack['bel', t].value)

        print('sum excess: ', np.asarray(excess).sum())

        # autarky degree
        print('autarky degree: ', (sum_production.sum()  # production
                                   - transf.sum()  # minus non renewable prod.
                                   - np.asarray(excess).sum() # minus excess
                                   - storage_load.sum()) /  # minus stor. load
                                   np.asarray(demand.results['in']
                                              [bus_to_print]).sum())  #  in
                                              # proportion to the demand

    plot_dispatch('bel')
    plt.show()

    print_results('bel')
