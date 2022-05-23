"""
General description
-------------------
The gradient constraint can restrict a component to change the output within
one time step. In this example a storage will buffer this restriction, so the
more flexible the power plant can be run the less the storage will be used.

Change the GRADIENT variable in the example to see the effect on the usage of
the storage.


Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""

import matplotlib.pyplot as plt
import pandas as pd

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import flows
from oemof.solph import processing

# The gradient for the output of the natural gas power plant.
# Change the gradient between 0.1 and 0.0001 and check the results. The
# more flexible the power plant can be run the less the storage will be used.
GRADIENT = 0.001

date_time_index = pd.date_range("1/1/2012", periods=48, freq="H")
print(date_time_index)
energysystem = EnergySystem(timeindex=date_time_index, timemode="explicit")

demand = [
    209643, 207497, 200108, 191892, 185717, 180672, 172683, 170048, 171132,
    179532, 189155, 201026, 208466, 207718, 205443, 206255, 217240, 232798,
    237321, 232387, 224306, 219280, 223701, 213926, 201834, 192215, 187152,
    184355, 184438, 182786, 180105, 191509, 207104, 222501, 231127, 238410,
    241184, 237413, 234469, 235193, 242730, 264196, 265950, 260283, 245578,
    238849, 241553, 231372
]

# create natural gas bus
bgas = buses.Bus(label="natural_gas")

# create electricity bus
bel = buses.Bus(label="electricity")

# adding the buses to the energy system
energysystem.add(bgas, bel)

# create excess component for the electricity bus to allow overproduction
energysystem.add(cmp.Sink(label="excess_bel", inputs={bel: flows.Flow()}))

# create source object representing the natural gas commodity (annual limit)
energysystem.add(
    cmp.Source(
        label="rgas",
        outputs={bgas: flows.Flow(variable_costs=5)},
    )
)

# create simple sink object representing the electrical demand
energysystem.add(
    cmp.Sink(
        label="demand",
        inputs={bel: flows.Flow(fix=demand, nominal_value=1)},
    )
)

# create simple transformer object representing a gas power plant
energysystem.add(
    cmp.Transformer(
        label="pp_gas",
        inputs={bgas: flows.Flow()},
        outputs={
            bel: flows.Flow(
                nominal_value=10e5,
                negative_gradient={"ub": GRADIENT},
                positive_gradient={"ub": GRADIENT},
            )
        },
        conversion_factors={bel: 0.58},
    )
)

# create storage object representing a battery
storage = cmp.GenericStorage(
    nominal_storage_capacity=999999999,
    label="storage",
    inputs={bel: flows.Flow()},
    outputs={bel: flows.Flow()},
    loss_rate=0.0,
    initial_storage_level=None,
    inflow_conversion_factor=1,
    outflow_conversion_factor=0.8,
)

energysystem.add(storage)

# initialise the operational model
model = Model(energysystem)

# solve
model.solve(solver="cbc")

# processing the results
results = processing.results(model)

print("C", results[(storage, None)]["sequences"])
print("f", results[(storage, bel)]["sequences"])
ax = results[(storage, None)]["sequences"].diff().plot()
ax = results[(storage, bel)]["sequences"].mul(-1).plot(ax=ax)
ax = results[(storage, None)]["sequences"].plot(ax=ax)
results[(bel, storage)]["sequences"].plot(ax=ax)
plt.show()
exit(0)
# get all variables of a specific component/bus
custom_storage = solph.views.node(results, "storage")
electricity_bus = solph.views.node(results, "electricity")

# plotting
fig, ax = plt.subplots(figsize=(10, 5))
custom_storage["sequences"].plot(ax=ax, kind="line", drawstyle="steps-post")
plt.legend(
    loc="upper center",
    prop={"size": 8},
    bbox_to_anchor=(0.5, 1.25),
    ncol=2,
)
fig.subplots_adjust(top=0.8)
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
electricity_bus["sequences"].plot(ax=ax, kind="line", drawstyle="steps-post")
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.show()
