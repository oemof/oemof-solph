# -*- coding: utf-8 -*-
"""
Simple example for updating objective after first solve

Tested with oemof version 0.0.5

Info:
simon.hilpert@fh-flensburg.de
"""

import matplotlib.pyplot as plt

from oemof.core import energy_system as es
# solph imports
from oemof.solph.optimization_model import OptimizationModel
from oemof.solph import predefined_objectives as predefined_objectives
# base classes import
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import transformers as transformer

from oemof.outputlib import to_pandas as tpd
import pandas as pd
from oemof.tools import logger
logger.define_logging()


time_index = pd.date_range('1/1/2012', periods=10, freq='H')
simulation = es.Simulation(solver='glpk', timesteps=range(len(time_index)),
                           verbose=False, duals=False,
                           objective_options={
                             'function': predefined_objectives.minimize_cost})
#
energy_system = es.EnergySystem(simulation=simulation, time_idx=time_index)

# resources
bcoal = Bus(uid="coal", type="coal", price=20, balanced=False, excess=False)
bgas = Bus(uid="gas", type="gas", price=35, balanced=False, excess=False)


# electricity and heat
b_el = Bus(uid="b_el", type="el", excess=False)

# demand
demand_el = sink.Simple(uid="demand_el", inputs=[b_el],
                        val=[30, 10, 20, 40, 45, 50, 35, 25, 5, 12])

# Simple Transformer for b_el
pp_coal = transformer.Simple(uid='pp_lig', inputs=[bcoal], outputs=[b_el],
                            in_max=[None],
                            out_max=[10], eta=[0.41],
                            opex_fix=2, opex_var=40)
pp_gas = transformer.Simple(uid='pp_gas', inputs=[bgas], outputs=[b_el],
                            in_max=[None], out_max=[41], eta=[0.45],
                            opex_var=40)

# create optimization model
om = OptimizationModel(energysystem=energy_system)

#
energy_system.optimize(om)

#
# use outputlib to plot
esplot = tpd.DataFramePlot(energy_system=energy_system)
esplot.slice_unstacked(bus_uid="b_el", type="input")
esplot.plot(title="January 2016 Low coal costs",
            stacked=True,
            width=1, lw=0.1,
            kind='bar')
plt.show()

# update variable costs and objective, solve again!
pp_coal.opex_var = 100
om.update_objective()

# solve again
energy_system.optimize(om)

# use outputlib to plot
esplot = tpd.DataFramePlot(energy_system=energy_system)
esplot.slice_unstacked(bus_uid="b_el", type="input")
esplot.plot(title="January 2016: High coal costs",
            stacked=True, width=1, lw=0.1,
            kind='bar')
esplot.ax.set_ylabel('Power in MW')
esplot.ax.set_xlabel('Date')
plt.show()


