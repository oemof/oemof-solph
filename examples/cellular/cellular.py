#%%
###########################################################################
# imports
###########################################################################

import pandas as pd

import pyomo.environ as po

from oemof.solph import CellularModel
from oemof.solph import buses
from oemof.solph import components as cmp

from oemof.solph import create_time_index
from oemof.solph import flows

from oemof.solph.components.experimental import CellConnector, EnergyCell

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

demand_1 = [80] * n_periods
demand_2 = [10] * n_periods
demand_3 = [10] * n_periods

pv_1 = [0] * n_periods
pv_2 = [40] * n_periods
pv_3 = [50] * n_periods

bus_el = buses.Bus(label="bus_el")
bus_el_1 = buses.Bus(label="bus_el_1")
bus_el_2 = buses.Bus(label="bus_el_2")
bus_el_3 = buses.Bus(label="bus_el_3")

es.add(bus_el)
ec1.add(bus_el_1)
ec2.add(bus_el_2)
ec3.add(bus_el_3)

source_es = cmp.Source(
    label="source_es", outputs={bus_el: flows.Flow(variable_costs=100)}
)
es.add(source_es)

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

# TODO: Refactor, such that there's only one CellConnector necessary per
# cell and energy type (ele, gas, heat)
# CC-Bennenung: cc_from_to

cc_es_ec1 = CellConnector(
    label="cc_es_ec1",
    inputs={bus_el: flows.Flow()},
    outputs={bus_el: flows.Flow()},
    max_flow=10000,
)
es.add(cc_es_ec1)

cc_ec1_es = CellConnector(
    label="cc_ec1_es",
    inputs={bus_el_1: flows.Flow()},
    outputs={bus_el_1: flows.Flow()},
    max_flow=10000,
)
cc_ec1_ec2 = CellConnector(
    label="cc_ec1_ec2",
    inputs={bus_el_1: flows.Flow()},
    outputs={bus_el_1: flows.Flow()},
    max_flow=10000,
)
cc_ec1_ec3 = CellConnector(
    label="cc_ec1_ec3",
    inputs={bus_el_1: flows.Flow()},
    outputs={bus_el_1: flows.Flow()},
    max_flow=10000,
)
ec1.add(cc_ec1_es, cc_ec1_ec2, cc_ec1_ec3)

cc_ec2_ec1 = CellConnector(
    label="cc_ec2_ec1",
    inputs={bus_el_2: flows.Flow()},
    outputs={bus_el_2: flows.Flow()},
    max_flow=10000,
)
ec2.add(cc_ec2_ec1)

cc_ec3_ec1 = CellConnector(
    label="cc_ec3_ec1",
    inputs={bus_el_3: flows.Flow()},
    outputs={bus_el_3: flows.Flow()},
    max_flow=10000,
)
ec3.add(cc_ec3_ec1)

###########################################################################
# create the cellular model
###########################################################################
#%%
# TODO: Rework, how the model is created from here on.
# Would be neat to pass the CellularModel a graph-structure
# ALTERNATIVELY: pass a list of all energy cells and make the connections
# afterwards, so the connections determine the hierarchy. Adjustments need to
# be made in the CellularModel __init__ function for that.
cmodel = CellularModel(EnergyCells={es: [ec1, ec2, ec3]})

###########################################################################
# link the grid connectors to each other
###########################################################################

#%%
def link_connectors(model, cc1, cc2, factor=1):
    """
    Connects two CellConnectors with each other, such that the inputs and outputs are interlinked.
    Return value does not need to be catched.

    Parameters:
    -----------
    model: CellularModel
        Model containing all GridConnector instances
    gc1: GridConnector
        One of the two GridConnectors to be linked
    gc2: GridConnector
        The second of the two GridConnectors to be linked
    factor: numerical (optional)
        Factor to account for transmission losses. Defaults to 1. Loss would be 1-`factor`. Is used as gc1.outflow * factor = gc2.inflow.
    """

    def equate_variables_rule(m):
        return var1 == var2 * factor

    for t in model.TIMESTEPS:
        # connect input of cc1 with output of cc2
        var1 = model.CellConnectorBlock.input_flow[cc1, t]
        var2 = model.CellConnectorBlock.output_flow[cc2, t]
        name = "_".join(["equate", var1.name, var2.name])
        setattr(model, name, po.Constraint(rule=equate_variables_rule))
        # connect input of cc2 with output of cc1
        var1 = model.CellConnectorBlock.input_flow[cc2, t]
        var2 = model.CellConnectorBlock.output_flow[cc1, t]
        name = "_".join(["equate", var1.name, var2.name])
        setattr(model, name, po.Constraint(rule=equate_variables_rule))


link_connectors(cmodel, cc_es_ec1, cc_ec1_es)
link_connectors(cmodel, cc_ec1_ec2, cc_ec2_ec1)
link_connectors(cmodel, cc_ec1_ec3, cc_ec3_ec1)

###########################################################################
# Solve the model
###########################################################################

res = cmodel.solve(solver=mysolver)
cmodel.write(
    "D:\solph-cellular\cmodel.lp", io_options={"symbolic_solver_labels": True}
)

# %%
