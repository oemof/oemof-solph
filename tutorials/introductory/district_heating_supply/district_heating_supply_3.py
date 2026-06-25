import os

import pandas as pd
from helpers import LCOH
from helpers import epc

import oemof.solph as solph

file_path = os.path.dirname(__file__)
filename = os.path.join(file_path, "input_data.csv")

data = pd.read_csv(filename, sep=";", index_col=0, parse_dates=True)

district_heating_system = solph.EnergySystem(
    timeindex=data.index,
    infer_last_interval=True,
)

heat_bus = solph.Bus(label="heat network")
gas_bus = solph.Bus(label="gas network")
waste_heat_bus = solph.Bus(label="waste heat network")
electricity_bus = solph.Bus(label="electricity network")

district_heating_system.add(heat_bus, gas_bus, waste_heat_bus, electricity_bus)

gas_source = solph.components.Source(
    label="gas source",
    outputs={gas_bus: solph.flows.Flow(variable_costs=data["gas price"])},
)

electricity_source = solph.components.Source(
    label="electricity source",
    outputs={
        electricity_bus: solph.flows.Flow(variable_costs=data["el_spot_price"])
    },
)

heat_sink = solph.components.Sink(
    label="heat sink",
    inputs={
        heat_bus: solph.flows.Flow(
            nominal_capacity=data["heat demand"].max(),
            fix=data["heat demand"] / data["heat demand"].max(),
        )
    },
)

district_heating_system.add(gas_source, electricity_source, heat_sink)


waste_heat_source = solph.components.Source(
    label="waste heat source", outputs={waste_heat_bus: solph.flows.Flow()}
)

district_heating_system.add(waste_heat_source)

spec_inv_gas_boiler = 60000
var_cost_gas_boiler = 1.10

gas_boiler = solph.components.Converter(
    label="gas boiler",
    inputs={gas_bus: solph.flows.Flow()},
    outputs={
        heat_bus: solph.flows.Flow(
            nominal_capacity=solph.Investment(
                ep_costs=epc(spec_inv_gas_boiler), maximum=50
            ),
            variable_costs=var_cost_gas_boiler,
        )
    },
    conversion_factors={gas_bus: 0.95},
)

district_heating_system.add(gas_boiler)

spec_inv_storage = 1060
var_cost_storage = 0.1

heat_storage = solph.components.GenericStorage(
    label="heat storage",
    nominal_capacity=solph.Investment(ep_costs=epc(spec_inv_storage)),
    inputs={
        heat_bus: solph.flows.Flow(
            variable_costs=var_cost_storage,
            nominal_capacity=solph.Investment(),
        )
    },
    outputs={
        heat_bus: solph.flows.Flow(
            variable_costs=var_cost_storage,
            nominal_capacity=solph.Investment(),
        )
    },
    invest_relation_input_capacity=1 / 24,
    invest_relation_output_capacity=1 / 24,
    balanced=True,
    loss_rate=0.001,
)

district_heating_system.add(heat_storage)

cop = 3.5
spec_inv_heat_pump = 500000
var_cost_heat_pump = 1.2

# %%[sec_1_start]
heat_pump = solph.components.Converter(
    label="heat pump",
    inputs={
        electricity_bus: solph.flows.Flow(),
        waste_heat_bus: solph.flows.Flow(),
    },
    outputs={
        heat_bus: solph.flows.Flow(
            nominal_capacity=solph.Investment(
                ep_costs=epc(spec_inv_heat_pump), maximum=999
            ),
            variable_costs=1.2,
            minimum=0.5,
            nonconvex=solph.NonConvex(),
        )
    },
    conversion_factors={
        electricity_bus: 1 / cop,
        waste_heat_bus: (cop - 1) / cop,
    },
)
district_heating_system.add(heat_pump)
# %%[sec_1_end]

# %%[sec_2_start]
# solve model
model = solph.Model(district_heating_system)
results = model.solve(
    solver="cbc",
    solve_kwargs={"tee": True},
    cmdline_options={"ratio": 0.01},
    allow_nonoptimal=True,
)
# %%[sec_2_end]

# results

flows = results["flow"]

cap_gas_boiler = results["invest"][("gas boiler", "heat network")][0]
cap_heat_pump = results["invest"][("heat pump", "heat network")][0]
cap_storage = results["invest"]["heat storage"][0]
cap_storage_out = results["invest"][("heat storage", "heat network")][0]

print(f"capacity gas boiler: {cap_gas_boiler:.1f} MW")
print(f"capacity heat pump: {cap_heat_pump:.1f} MW")
print(f"capacity heat storage: {cap_storage:.1f} MWh")
print(f"capacity heat storage (out): {cap_storage_out:.1f} MW")

invest_cost = (
    spec_inv_gas_boiler * cap_gas_boiler
    + spec_inv_storage * cap_storage
    + spec_inv_heat_pump * cap_heat_pump
)
operation_cost = (
    var_cost_gas_boiler
    * flows[("gas boiler", "heat network")].sum()
    + (
        data["gas price"]
        * flows[("gas network", "gas boiler")]
    ).sum()
    + var_cost_heat_pump
    * flows[("heat pump", "heat network")].sum()
    + (
        data["el_spot_price"]
        * flows[("electricity network", "heat pump")]
    ).sum()
    + var_cost_storage
    * flows[("heat storage", "heat network")].sum()
    + var_cost_storage
    * flows[("heat network", "heat storage")].sum()
)
heat_produced = flows[("heat network", "heat sink")].sum()

lcoh = LCOH(invest_cost, operation_cost, heat_produced)
print(f"LCOH: {lcoh:.2f} €/MWh")

import matplotlib.pyplot as plt

# plt.style.use('dark_background')

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
        flows.index,
        flows[(unit, "heat network")],
        label=unit_label,
        color=unit_colors[unit_label],
        bottom=bottom,
    )
    bottom += flows[(unit, "heat network")]

unit_label = "heat storage (charge)"
ax.bar(
    flows.index,
    -1 * flows[("heat network", "heat storage")],
    label=unit_label,
    color=unit_colors[unit_label],
)

ax.legend(loc="upper center", ncol=2)
ax.grid(axis="y")
ax.set_ylabel("Hourly heat production in MWh")

# plt.tight_layout()
# plt.savefig('intro_tut_dhs_3_hourly_heat_production.svg')


fig, ax = plt.subplots(figsize=[10, 6])

ax.plot(
    results["storage_content"]["heat storage"],
    color="#00395B",
)

ax.grid(axis="y")
ax.set_ylabel("Hourly heat storage content in MWh")

# plt.tight_layout()
# plt.savefig('intro_tut_dhs_3_hourly_storage_content.svg')

plt.show()
