import pandas as pd
from helpers import LCOH, epc

import oemof.solph as solph

# %%[sec_1_start]
data = pd.read_csv("input_data.csv", sep=";", index_col=0, parse_dates=True)
# %%[sec_1_end]

district_heating_system = solph.EnergySystem(
    timeindex=data.index, infer_last_interval=False
)

heat_bus = solph.Bus(label="heat network")
gas_bus = solph.Bus(label="gas network")

district_heating_system.add(heat_bus, gas_bus)
# %%[sec_2_start]
waste_heat_bus = solph.Bus(label="waste heat network")
electricity_bus = solph.Bus(label="electricity network")

district_heating_system.add(waste_heat_bus, electricity_bus)
# %%[sec_2_end]

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

# %%[sec_3_start]
# ist die waste heat source fix oder unendlich?
waste_heat_source = solph.components.Source(
    label="waste heat source", outputs={waste_heat_bus: solph.flows.Flow()}
)

electricity_source = solph.components.Source(
    label="electricity source",
    outputs={
        electricity_bus: solph.flows.Flow(variable_costs=data["el_spot_price"])
    },
)

district_heating_system.add(waste_heat_source, electricity_source)
# %%[sec_3_end]
spec_inv_gas_boiler = 60000
var_cost_gas_boiler = 1.10

gas_boiler = solph.components.Converter(
    label="gas boiler",
    inputs={gas_bus: solph.flows.Flow()},
    outputs={
        heat_bus: solph.flows.Flow(
            nominal_value=solph.Investment(
                ep_costs=epc(spec_inv_gas_boiler), maximum=50
            ),
            variable_costs=var_cost_gas_boiler,
        )
    },
    conversion_factors={gas_bus: 0.95},
)

district_heating_system.add(gas_boiler)

# %%[sec_4_start]
cop = 3.5
spec_inv_heat_pump = 500000
var_cost_heat_pump = 1.2

heat_pump = solph.components.Converter(
    label="heat pump",
    inputs={
        electricity_bus: solph.flows.Flow(),
        waste_heat_bus: solph.flows.Flow(),
    },
    outputs={
        heat_bus: solph.flows.Flow(
            nominal_value=solph.Investment(ep_costs=epc(spec_inv_heat_pump)),
            variable_costs=1.2,
        )
    },
    conversion_factors={
        electricity_bus: 1 / cop,
        waste_heat_bus: (cop - 1) / cop,
    },
)
district_heating_system.add(heat_pump)
# %%[sec_4_end]

# %%[sec_5_start]
spec_inv_storage = 1060
var_cost_storage = 0.1

heat_storage = solph.components.GenericStorage(
    label="heat storage",
    nominal_capacity=solph.Investment(ep_costs=epc(spec_inv_storage)),
    inputs={heat_bus: solph.flows.Flow(variable_costs=var_cost_storage)},
    outputs={heat_bus: solph.flows.Flow(variable_costs=var_cost_storage)},
    invest_relation_input_capacity=1 / 24,
    invest_relation_output_capacity=1 / 24,
    balanced=True,
    loss_rate=0.001,
)

district_heating_system.add(heat_storage)
# %%[sec_5_end]

# solve model
model = solph.Model(district_heating_system)
model.solve(solver="cbc", solve_kwargs={"tee": True})

# results
results = solph.processing.results(model)

data_gas_bus = solph.views.node(results, "gas network")["sequences"]
data_heat_bus = solph.views.node(results, "heat network")["sequences"]

# %%[sec_6_start]
data_el_bus = solph.views.node(results, "electricity network")["sequences"]
data_caps = solph.views.node(results, "heat network")["scalars"]

cap_gas_boiler = data_caps[("gas boiler", "heat network"), "invest"]
cap_heat_pump = data_caps[("heat pump", "heat network"), "invest"]
cap_storage = solph.views.node(results, "heat storage")["scalars"][
    (("heat storage", "None"), "invest")
]
cap_storage_out = data_caps[("heat storage", "heat network"), "invest"]

print(f"capacity gas boiler: {cap_gas_boiler:.1f} MW")
print(f"capacity heat pump: {cap_heat_pump:.1f} MW")
print(f"capacity heat storage: {cap_storage:.1f} MWh")
print(f"capacity heat storage (out): {cap_storage_out:.1f} MW")
# %%[sec_6_end]

# %%[sec_7_start]
invest_cost = (
    spec_inv_gas_boiler * cap_gas_boiler
    + spec_inv_heat_pump * cap_heat_pump
    + spec_inv_storage * cap_storage
)
operation_cost = (
    var_cost_gas_boiler
    * data_heat_bus[(("gas boiler", "heat network"), "flow")].sum()
    + (
        data["gas price"]
        * data_gas_bus[(("gas network", "gas boiler"), "flow")]
    ).sum()
    + var_cost_heat_pump
    * data_heat_bus[(("heat pump", "heat network"), "flow")].sum()
    + (
        data["el_spot_price"]
        * data_el_bus[(("electricity network", "heat pump"), "flow")]
    ).sum()
    + var_cost_storage
    * data_heat_bus[(("heat storage", "heat network"), "flow")].sum()
    + var_cost_storage
    * data_heat_bus[(("heat network", "heat storage"), "flow")].sum()
)
heat_produced = data_heat_bus[(("heat network", "heat sink"), "flow")].sum()

lcoh = LCOH(invest_cost, operation_cost, heat_produced)
print(f"LCOH: {lcoh:.2f} €/MWh")
# %%[sec_7_end]

import matplotlib.pyplot as plt

# plt.style.use('dark_background')

# %%[sec_8_start]
unit_colors = {
    "gas boiler": "#EC6707",
    "heat pump": "#B54036",
    "heat storage (discharge)": "#BFBFBF",
    "heat storage (charge)": "#696969",
}

fig, ax = plt.subplots(figsize=[10, 6])

bottom = 0
for unit in ["heat pump", "gas boiler", "heat storage"]:
    unit_label = f"{unit} (discharge)" if "storage" in unit else unit
    ax.bar(
        data_heat_bus.index,
        data_heat_bus[((unit, "heat network"), "flow")],
        label=unit_label,
        color=unit_colors[unit_label],
        bottom=bottom,
    )
    bottom += data_heat_bus[((unit, "heat network"), "flow")]

unit_label = "heat storage (charge)"
ax.bar(
    data_heat_bus.index,
    -1 * data_heat_bus[(("heat network", "heat storage"), "flow")],
    label=unit_label,
    color=unit_colors[unit_label],
)

ax.legend(loc="upper center", ncol=2)
ax.grid(axis="y")
ax.set_ylabel("Hourly heat production in MWh")

# plt.tight_layout()
# plt.savefig('intro_tut_dhs_2_hourly_heat_production.svg')


fig, ax = plt.subplots(figsize=[10, 6])

data_heat_storage = solph.views.node(results, "heat storage")["sequences"]

ax.plot(
    data_heat_storage[(("heat storage", "None"), "storage_content")],
    color="#00395B",
)

ax.grid(axis="y")
ax.set_ylabel("Hourly heat storage content in MWh")

# plt.tight_layout()
# plt.savefig('intro_tut_dhs_2_hourly_storage_content.svg')

plt.show()
# %%[sec_8_end]
