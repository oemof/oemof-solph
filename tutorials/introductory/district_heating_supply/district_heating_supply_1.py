from helpers import LCOH

# %%[sec_1_start]
import pandas as pd

data = pd.read_csv("input_data.csv", sep=";", index_col=0, parse_dates=True)
# %%[sec_1_end]

# %%[sec_2_start]
import oemof.solph as solph

district_heating_system = solph.EnergySystem(
    timeindex=data.index, infer_last_interval=False
)
# %%[sec_2_end]

# %%[sec_3_start]
heat_bus = solph.Bus(label="heat network")
gas_bus = solph.Bus(label="gas network")

district_heating_system.add(heat_bus, gas_bus)
# %%[sec_3_end]

# %%[sec_4_start]
gas_source = solph.components.Source(
    label="gas source",
    outputs={gas_bus: solph.flows.Flow(variable_costs=data["gas price"])},
)

# nominal_value -> nominal_capacity
heat_sink = solph.components.Sink(
    label="heat sink",
    inputs={
        heat_bus: solph.flows.Flow(
            nominal_value=data["heat demand"].max(),
            fix=data["heat demand"] / data["heat demand"].max(),
        )
    },
)

district_heating_system.add(heat_sink, gas_source)
# %%[sec_4_end]

# %%[sec_5_start]
gas_boiler = solph.components.Converter(
    label="gas boiler",
    inputs={gas_bus: solph.flows.Flow()},
    outputs={
        heat_bus: solph.flows.Flow(
            nominal_value=data["heat demand"].max(), variable_costs=1.10
        )
    },
    conversion_factors={gas_bus: 0.95},
)

district_heating_system.add(gas_boiler)
# %%[sec_5_end]

# %%[sec_6_start]
model = solph.Model(district_heating_system)
model.solve(solver="cbc", solve_kwargs={"tee": True})
# %%[sec_6_end]

# %%[sec_7_start]
results = solph.processing.results(model)

data_gas_bus = solph.views.node(results, "gas network")["sequences"]
data_heat_bus = solph.views.node(results, "heat network")["sequences"]
# %%[sec_7_end]


# %%[sec_8_start]
import matplotlib.pyplot as plt

# plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=[10, 6])

ax.bar(
    data_heat_bus.index,
    data_heat_bus[(("gas boiler", "heat network"), "flow")],
    label="gas boiler",
    color="#EC6707",
)

ax.legend(loc="upper right")
ax.grid(axis="y")
ax.set_ylabel("Hourly heat production in MWh")

# plt.tight_layout()
# plt.savefig('intro_tut_dhs_1_hourly_heat_production.svg')
plt.show()
# %%[sec_8_end]

# %%[sec_9_start]
spec_inv_gas_boiler = 50000
cap_gas_boiler = 20
var_cost_gas_boiler = 1.10

invest_cost = spec_inv_gas_boiler * cap_gas_boiler
operation_cost = (
    var_cost_gas_boiler
    * data_heat_bus[(("gas boiler", "heat network"), "flow")].sum()
    + (
        data["gas price"]
        * data_gas_bus[(("gas network", "gas boiler"), "flow")]
    ).sum()
)
heat_produced = data_heat_bus[(("heat network", "heat sink"), "flow")].sum()

lcoh = LCOH(invest_cost, operation_cost, heat_produced)
print(f"LCOH: {lcoh:.2f} €/MWh")
# %%[sec_9_end]
