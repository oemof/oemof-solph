# %%

from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import EnergySystem

from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import processing, views

###########################################################################
# define the cells of the cellular energy system
###########################################################################

n_periods = 3

daterange = create_time_index(year=2020, interval=1, number=n_periods)

mysolver = "gurobi"

# create the energy cells
es = EnergySystem(label="es", timeindex=daterange, infer_last_interval=False)
ec_1 = EnergySystem(
    label="ec1", timeindex=daterange, infer_last_interval=False
)
ec_2 = EnergySystem(
    label="ec2", timeindex=daterange, infer_last_interval=False
)
ec_1_1 = EnergySystem(
    label="ec1_1", timeindex=daterange, infer_last_interval=False
)
ec_1_2 = EnergySystem(
    label="ec1_2", timeindex=daterange, infer_last_interval=False
)
ec_2_1 = EnergySystem(
    label="ec2_1", timeindex=daterange, infer_last_interval=False
)
ec_2_2 = EnergySystem(
    label="ec2_2", timeindex=daterange, infer_last_interval=False
)

demand_1 = [10] * n_periods
demand_2 = [10] * n_periods
demand_1_1 = [10] * n_periods
demand_1_2 = [10] * n_periods
demand_2_1 = [10] * n_periods
demand_2_2 = [10] * n_periods

pv_1 = [100] * n_periods
pv_2 = [100] * n_periods
pv_1_1 = [100] * n_periods
pv_1_2 = [100] * n_periods
pv_2_1 = [100] * n_periods
pv_2_2 = [100] * n_periods

bus_el_es = buses.Bus(label="bus_el_es")
bus_el_ec_1 = buses.Bus(label="bus_el_ec_1")
bus_el_ec_2 = buses.Bus(label="bus_el_ec_2")
bus_el_ec_1_1 = buses.Bus(label="bus_el_ec_1_1")
bus_el_ec_1_2 = buses.Bus(label="bus_el_ec_1_2")
bus_el_ec_2_1 = buses.Bus(label="bus_el_ec_2_1")
bus_el_ec_2_2 = buses.Bus(label="bus_el_ec_2_2")

es.add(bus_el_es)
ec_1.add(bus_el_ec_1)
ec_2.add(bus_el_ec_2)
ec_1_1.add(bus_el_ec_1_1)
ec_1_2.add(bus_el_ec_1_2)
ec_2_1.add(bus_el_ec_2_1)
ec_2_2.add(bus_el_ec_2_2)

sink_el_ec_1 = cmp.Sink(
    label="sink_el_ec_1",
    inputs={bus_el_ec_1: flows.Flow(fix=demand_1, nominal_value=1)},
)
sink_el_ec_2 = cmp.Sink(
    label="sink_el_ec_2",
    inputs={bus_el_ec_2: flows.Flow(fix=demand_2, nominal_value=1)},
)
sink_el_ec_1_1 = cmp.Sink(
    label="sink_el_ec_1_1",
    inputs={bus_el_ec_1_1: flows.Flow(fix=demand_1_1, nominal_value=1)},
)
sink_el_ec_1_2 = cmp.Sink(
    label="sink_el_ec_1_2",
    inputs={bus_el_ec_1_2: flows.Flow(fix=demand_1_2, nominal_value=1)},
)
sink_el_ec_2_1 = cmp.Sink(
    label="sink_el_ec_2_1",
    inputs={bus_el_ec_2_1: flows.Flow(fix=demand_2_1, nominal_value=1)},
)
sink_el_ec_2_2 = cmp.Sink(
    label="sink_el_ec_2_2",
    inputs={bus_el_ec_2_2: flows.Flow(fix=demand_2_2, nominal_value=1)},
)

ec_1.add(sink_el_ec_1)
ec_2.add(sink_el_ec_2)
ec_1_1.add(sink_el_ec_1_1)
ec_1_2.add(sink_el_ec_1_2)
ec_2_1.add(sink_el_ec_2_1)
ec_2_2.add(sink_el_ec_2_2)

source_el_ec_1 = cmp.Source(
    label="source_el_ec_1",
    outputs={
        bus_el_ec_1: flows.Flow(max=pv_1, nominal_value=1, variable_costs=5)
    },
)
source_el_ec_2 = cmp.Source(
    label="source_el_ec_2",
    outputs={
        bus_el_ec_2: flows.Flow(max=pv_2, nominal_value=1, variable_costs=5)
    },
)
source_el_ec_1_1 = cmp.Source(
    label="source_el_ec_1_1",
    outputs={
        bus_el_ec_1_1: flows.Flow(
            max=pv_1_1, nominal_value=1, variable_costs=0
        )
    },
)
source_el_ec_1_2 = cmp.Source(
    label="source_el_ec_1_2",
    outputs={
        bus_el_ec_1_2: flows.Flow(
            max=pv_1_2, nominal_value=1, variable_costs=5
        )
    },
)
source_el_ec_2_1 = cmp.Source(
    label="source_el_ec_2_1",
    outputs={
        bus_el_ec_2_1: flows.Flow(
            max=pv_2_1, nominal_value=1, variable_costs=10
        )
    },
)
source_el_ec_2_2 = cmp.Source(
    label="source_el_ec_2_2",
    outputs={
        bus_el_ec_2_2: flows.Flow(
            max=pv_2_2, nominal_value=1, variable_costs=10
        )
    },
)

ec_1.add(source_el_ec_1)
ec_2.add(source_el_ec_2)
ec_1_1.add(source_el_ec_1_1)
ec_1_2.add(source_el_ec_1_2)
ec_2_1.add(source_el_ec_2_1)
ec_2_2.add(source_el_ec_2_2)

connector_el_ec_1 = buses.Bus(
    label="connector_el_ec_1",
    inputs={
        bus_el_es: flows.Flow(),
        bus_el_ec_1: flows.Flow(),
    },
    outputs={
        bus_el_es: flows.Flow(),
        bus_el_ec_1: flows.Flow(),
    },
)

connector_el_ec_2 = buses.Bus(
    label="connector_el_ec_2",
    inputs={
        bus_el_es: flows.Flow(),
        bus_el_ec_2: flows.Flow(),
    },
    outputs={
        bus_el_es: flows.Flow(),
        bus_el_ec_2: flows.Flow(),
    },
)

# relax the max constraint to see different results
connector_el_ec_1_1 = buses.Bus(
    label="connector_el_ec_1_1",
    inputs={
        bus_el_ec_1: flows.Flow(),
        bus_el_ec_1_1: flows.Flow(),
    },
    outputs={
        bus_el_ec_1: flows.Flow(max=20, nominal_value=1),
        bus_el_ec_1_1: flows.Flow(),
    },
)

connector_el_ec_1_2 = buses.Bus(
    label="connector_el_ec_1_2",
    inputs={
        bus_el_ec_1: flows.Flow(),
        bus_el_ec_1_2: flows.Flow(),
    },
    outputs={
        bus_el_ec_1: flows.Flow(),
        bus_el_ec_1_2: flows.Flow(),
    },
)

connector_el_ec_2_1 = buses.Bus(
    label="connector_el_ec_2_1",
    inputs={
        bus_el_ec_2: flows.Flow(),
        bus_el_ec_2_1: flows.Flow(),
    },
    outputs={
        bus_el_ec_2: flows.Flow(),
        bus_el_ec_2_1: flows.Flow(),
    },
)

connector_el_ec_2_2 = buses.Bus(
    label="connector_el_ec_2_2",
    inputs={
        bus_el_ec_2: flows.Flow(),
        bus_el_ec_2_2: flows.Flow(),
    },
    outputs={
        bus_el_ec_2: flows.Flow(),
        bus_el_ec_2_2: flows.Flow(),
    },
)

# the connectors are all part of the overarching es
es.add(
    connector_el_ec_1,
    connector_el_ec_2,
    connector_el_ec_1_1,
    connector_el_ec_1_2,
    connector_el_ec_2_1,
    connector_el_ec_2_2,
)

# %%
cmodel = Model(energysystem=[es, ec_1, ec_2, ec_1_1, ec_1_2, ec_2_1, ec_2_2])
# %%
cmodel.write(
    "D:/solph-cellular/examples/cellular/cmodel.lp",
    io_options={"symbolic_solver_labels": True},
)
# %%
cmodel.solve()

# %%
results = processing.results(cmodel)
views.node(results, "connector_el_ec_1_1")["sequences"]
# %%
