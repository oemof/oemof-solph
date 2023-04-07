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
pv_2 = [10] * n_periods
pv_3 = [60] * n_periods

bus_el = buses.Bus(label="bus_el")
bus_el_1 = buses.Bus(label="bus_el_1")
bus_el_2 = buses.Bus(label="bus_el_2")
bus_el_3 = buses.Bus(label="bus_el_3")

es.add(bus_el)
ec1.add(bus_el_1)
ec2.add(bus_el_2)
ec3.add(bus_el_3)

source_es = cmp.Source(
    label="source_es",
    outputs={bus_el: flows.Flow(variable_costs=100, nominal_value=1, max=50)},
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
# TODO: include the `link_connectors` in the CellularModel class and use
# the hierarchy to create the model
cmodel = CellularModel(EnergyCells={es: [ec1, ec2, ec3]})

###########################################################################
# link the grid connectors to each other
###########################################################################


#%%
def link_connectors(model, linkages):
    """
    Connects the CellConnectors of multiple cells with each other, such that
    the inputs and outputs are interlinked.
    Return value does not need to be catched.

    Parameters:
    -----------
    model: CellularModel
        Model of the energy system. Must already contain all CellConnectors
        used in the `linkages` set.
    linkages: set
        A set of tuples, where each tuple is created as (CellConnector1,
        CellConnector2, loss_factor).
        Links are established symmetrically, so loss_factor is applied in
        both directions. See equation (x) for usage of loss_factor.
    """
    # TODO: maybe move this into the CellularModel class to hide it from the user

    # block for new connections
    connection_block = po.Block()

    # Set with all CellConnector instances in linkages
    cell_connectors = set(
        [
            x
            for x in itertools.chain.from_iterable(linkages)
            if isinstance(x, CellConnector)
        ]
    )
    # check for orphaned CellConnector instances
    # TODO: make this a separate function?
    all_cell_connectors = set(model.CellConnectorBlock.CELLCONNECTORS)
    orphaned_cell_connectors = all_cell_connectors - cell_connectors

    if orphaned_cell_connectors:  # True if there are orphaned cc's
        msg = (
            "A CellConnector is designed to always be connected to one other "
            "CellConnector. The following CellConnector(s) are not connected "
            "to a counterpart: {0}. If this is intended and you know what you "
            "are doing, you can ignore or disable the SuspiciousUsageWarning."
        )
        warn(
            msg.format(orphaned_cell_connectors),
            debugging.SuspiciousUsageWarning,
        )

    # Check if max_power is the same in all pairs of CellConnectors
    # TODO: make this a separate function?
    for pair in linkages:
        if not pair[0].max_power == pair[1].max_power:
            msg = (
                "Two connected CellConnectors need to have the same max_power "
                "value. The following values where set:\n"
                "{0}: {1}\n"
                "{2}: {3}"
            )
            raise ValueError(
                msg.format(
                    pair[0].label,
                    pair[0].max_power,
                    pair[1].label,
                    pair[1].max_power,
                )
            )

    # mirror all linkages
    connection_block.LINKAGES = set()
    for link in linkages:
        # add the original link
        connection_block.LINKAGES.add(link)
        # add the mirrored link
        connection_block.LINKAGES.add((link[1], link[0], link[2]))

    model.add_component("ConnectionBlock", connection_block)

    def _equate_CellConnector_flows_rule(m):
        for (cc1, cc2, lf) in linkages:
            for t in m.TIMESTEPS:
                lhs = model.flow[cc1, cc1.input_bus, t]
                rhs = (1 - lf) * model.flow[cc2.output_bus, cc2, t]
                return lhs == rhs

    setattr(
        model,
        "equate_CellConnector_flows",
        po.Constraint(model.TIMESTEPS, noruleinit=True),
    )
    setattr(
        model,
        "equate_CellConnector_flows_build",
        po.BuildAction(rule=_equate_CellConnector_flows_rule),
    )


pairings = {
    (cc_es_ec1, cc_ec1_es, 0.5),
    (cc_ec1_ec2, cc_ec2_ec1, 0.2),
    (cc_ec1_ec3, cc_ec3_ec1, 0.1),
}
link_connectors(cmodel, pairings)
# link_connectors(cmodel, cc_es, cc_ec1)
# link_connectors(cmodel, cc_ec1, cc_ec2)
# link_connectors(cmodel, cc_ec1, cc_ec3)

###########################################################################
# Solve the model
###########################################################################
cmodel.receive_duals()
res = cmodel.solve(solver=mysolver)
cmodel.write(
    "D:\solph-cellular\cmodel.lp", io_options={"symbolic_solver_labels": True}
)
results = processing.results(cmodel)
views.node(results, "cc_ec1_ec3")["sequences"]

# %%
