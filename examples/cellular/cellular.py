#%%
###########################################################################
# imports
###########################################################################

import pandas as pd

import pyomo.environ as po

from oemof.solph import CellularModel
from oemof.solph import buses
from oemof.solph import components as cmp

from oemof.tools import debugging
from warnings import warn

from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import processing, views

from oemof.solph.components.experimental import CellConnector, EnergyCell

import itertools

###########################################################################
# define the cells of the cellular energy system
###########################################################################

n_periods = 3

# daterange = pd.date_range(
#    start="01-01-2022 00:00:00", periods=n_periods, freq="1H"
# )

daterange = create_time_index(year=2020, interval=1, number=n_periods)

mysolver = "gurobi"

# create the energy cells
es = EnergyCell(label="es", timeindex=daterange, infer_last_interval=False)
ec1 = EnergyCell(label="ec1", timeindex=daterange, infer_last_interval=False)
ec2 = EnergyCell(label="ec2", timeindex=daterange, infer_last_interval=False)
ec3 = EnergyCell(label="ec3", timeindex=daterange, infer_last_interval=False)

demand_1 = [10] * n_periods
demand_2 = [10] * n_periods
demand_3 = [80] * n_periods

pv_1 = [100] * n_periods
pv_2 = [10] * n_periods
pv_3 = [10] * n_periods

bus_el = buses.Bus(label="bus_el")
bus_el_1 = buses.Bus(label="bus_el_1")
bus_el_2 = buses.Bus(label="bus_el_2")
bus_el_3 = buses.Bus(label="bus_el_3")

es.add(bus_el)
ec1.add(bus_el_1)
ec2.add(bus_el_2)
ec3.add(bus_el_3)

dem_1 = cmp.Sink(
    label="dem_1", inputs={bus_el_1: flows.Flow(fix=demand_1, nominal_value=1)}
)
dem_2 = cmp.Sink(
    label="dem_2", inputs={bus_el_2: flows.Flow(fix=demand_2, nominal_value=1)}
)
dem_3 = cmp.Sink(
    label="dem_3", inputs={bus_el_3: flows.Flow(fix=demand_3, nominal_value=1)}
)
ec1.add(dem_1)
ec2.add(dem_2)
ec3.add(dem_3)

pv_source_1 = cmp.Source(
    label="pv_source_1",
    outputs={
        bus_el_1: flows.Flow(variable_costs=0, max=pv_1, nominal_value=1)
    },
)
pv_source_2 = cmp.Source(
    label="pv_source_2",
    outputs={
        bus_el_2: flows.Flow(variable_costs=0, max=pv_2, nominal_value=1)
    },
)
pv_source_3 = cmp.Source(
    label="pv_source_3",
    outputs={
        bus_el_3: flows.Flow(variable_costs=0, max=pv_3, nominal_value=1)
    },
)
ec1.add(pv_source_1)
ec2.add(pv_source_2)
ec3.add(pv_source_3)

###########################################################################
# add the grid connectors to the cells
###########################################################################

# Each cell needs a CellConnector object for each connection with another cell.
# So if Cell1 and Cell2 should be connected, each one of them needs one
# CellConnector object.

# CellConnector for es
cc_es_ec1 = CellConnector(
    label="cc_es_ec1",
    inputs={bus_el: flows.Flow()},
    outputs={bus_el: flows.Flow()},
    max_power=10000,
)
es.add(cc_es_ec1)

# CellConnectors for ec1
cc_ec1_es = CellConnector(
    label="cc_ec1_es",
    inputs={bus_el_1: flows.Flow()},
    outputs={bus_el_1: flows.Flow()},
    max_power=10000,
)

cc_ec1_ec2 = CellConnector(
    label="cc_ec1_ec2",
    inputs={bus_el_1: flows.Flow()},
    outputs={bus_el_1: flows.Flow()},
    max_power=10000,
)

cc_ec1_ec3 = CellConnector(
    label="cc_ec1_ec3",
    inputs={bus_el_1: flows.Flow()},
    outputs={bus_el_1: flows.Flow()},
    max_power=10000,
)
ec1.add(cc_ec1_es, cc_ec1_ec2, cc_ec1_ec3)

# CellConnector for ec2
cc_ec2_ec1 = CellConnector(
    label="cc_ec2_ec1",
    inputs={bus_el_2: flows.Flow()},
    outputs={bus_el_2: flows.Flow()},
    max_power=10000,
)
ec2.add(cc_ec2_ec1)

# CellConnector for ec_3
cc_ec3_ec1 = CellConnector(
    label="cc_ec3_ec1",
    inputs={bus_el_3: flows.Flow()},
    outputs={bus_el_3: flows.Flow()},
    max_power=10000,
)
ec3.add(cc_ec3_ec1)

###########################################################################
# create the cellular model
###########################################################################
#%%
pairings = {
    (cc_es_ec1, cc_ec1_es, 0),
    (cc_ec1_ec2, cc_ec2_ec1, 0),
    (cc_ec1_ec3, cc_ec3_ec1, 0),
}
cmodel = CellularModel(EnergyCells={es: [ec1, ec2, ec3]}, Connections=pairings)

###########################################################################
# link the grid connectors to each other
###########################################################################

#%%

# cmodel.receive_duals()
res = cmodel.solve(solver=mysolver)
cmodel.write(
    "D:\solph-cellular\examples\cellular\cmodel.lp",
    io_options={"symbolic_solver_labels": True},
)
results = processing.results(cmodel)
views.node(results, "cc_ec1_ec3")["sequences"]

# %%
