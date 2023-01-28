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

from oemof.solph import create_time_index
from oemof.solph import flows

from oemof.solph.components.experimental import CellConnector, EnergyCell

import itertools

###########################################################################
# define the cells of the cellular energy system
###########################################################################

n_periods = 1

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

pv_1 = [10] * n_periods
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

# TODO: one CellConnector isn't enough. If ec1 is connected to ec2 and ec3,
# than ec1 doesn't know which share goes to ec2 and which to ec3. The model
# becomes infeasible. Look for another solution. This is the problems with
# necessary subgraphs, Günni talked about.

cc_es = CellConnector(
    label="cc_es",
    inputs={bus_el: flows.Flow()},
    outputs={bus_el: flows.Flow()},
    max_flow=10000,
)
es.add(cc_es)

cc_ec1 = CellConnector(
    label="cc_ec1",
    inputs={bus_el_1: flows.Flow()},
    outputs={bus_el_1: flows.Flow()},
    max_flow=10000,
)
ec1.add(cc_ec1)

cc_ec2 = CellConnector(
    label="cc_ec2",
    inputs={bus_el_2: flows.Flow()},
    outputs={bus_el_2: flows.Flow()},
    max_flow=10000,
)
ec2.add(cc_ec2)

cc_ec3 = CellConnector(
    label="cc_ec3",
    inputs={bus_el_3: flows.Flow()},
    outputs={bus_el_3: flows.Flow()},
    max_flow=10000,
)
ec3.add(cc_ec3)

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
def link_connectors(model, connections, factor=1):
    """
    Connects the CellConnectors of multiple cells with each other, such that
    the inputs and outputs are interlinked.
    Return value does not need to be catched.

    Parameters:
    -----------
    model: CellularModel
        Model containing all GridConnector instances
    connections: set
        A set of subsets, where each subset contains (at least) a pair of two
        CellConnector objects which shall be linked with each other.
    factor: numerical (optional) DEPRECATED
        Factor to account for transmission losses. Defaults to 1. Loss would be
        1-`factor`. Is used as gc1.outflow * factor = gc2.inflow.
    """
    # TODO: enable usage of `factor` argument

    connection_block = po.Block()

    simple_connections = []
    # for every connection pair
    for c in connections:
        # create a list of tuples with simple connections (cell1, cell2)
        pairs = [x for x in itertools.product(c, c) if not x[0] == x[1]]
        for pair in pairs:
            if pair not in simple_connections:
                simple_connections.append(pair)
            else:
                msg = "Connection between {0} and {1} is established twice.".format(
                    pair[0], pair[1]
                )
                raise debugging.SuspiciousUsageWarning(msg)

    # add these connections as a pyomo Set
    connection_block.CONNECTIONS = po.Set(initialize=simple_connections)

    model.add_component("ConnectionBlock", connection_block)

    def link_cells_rule(model, cc1, cc2, t):
        lhs = model.CellConnectorBlock.output_flow[cc1, t]
        rhs = model.CellConnectorBlock.input_flow[cc2, t]
        return lhs == rhs

    model.connections = po.Constraint(
        connection_block.CONNECTIONS, model.TIMESTEPS, rule=link_cells_rule
    )


pairings = {
    (cc_es, cc_ec1),
    (cc_ec1, cc_ec2),
    (cc_ec1, cc_ec3),
}
link_connectors(cmodel, pairings, factor=1)
# link_connectors(cmodel, cc_es, cc_ec1)
# link_connectors(cmodel, cc_ec1, cc_ec2)
# link_connectors(cmodel, cc_ec1, cc_ec3)

###########################################################################
# Solve the model
###########################################################################

res = cmodel.solve(solver=mysolver)
cmodel.write(
    "D:\solph-cellular\cmodel.lp", io_options={"symbolic_solver_labels": True}
)

# %%
