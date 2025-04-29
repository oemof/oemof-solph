# %%[sec_1_start]
import pandas as pd

data = pd.read_csv("input_data.csv", sep=";", index_col=0, parse_dates=True)
# %%[sec_1_end]

# %%[sec_2_start]
import oemof.solph as solph

district_heating_system = solph.EnergySystem(timeindex=data.index)
# %%[sec_2_end]

# %%[sec_3_start]
# Question: How to name the variables?
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
        heat_bus: solph.flows.Flow(nominal_value=20, variable_costs=0.50)
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
def LCOH(invest_cost, operation_cost, heat_produced, revenue=0, i=0.05, n=20):
    q = 1 + i
    pvf = (q**n - 1) / (q**n * (q - 1))

    return (invest_cost + pvf * (operation_cost - revenue)) / (
        pvf * heat_produced
    )


# %%[sec_8_end]

# %%[sec_9_start]
spec_inv_gas_boiler = 50000
cap_gas_boiler = 20
var_cost_gas_boiler = 0.50

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
# %%[sec_9_end]
print(f"LCOH: {lcoh:.2f} €/MWh")

# %%[sec_10_start]
co2 = data_gas_bus[(("gas network", "gas boiler"), "flow")].sum() * 201.2
# %%[sec_10_end]
print(f"CO2-emissions: {co2:.0f} kg")

# %%[sec_11_start]
import matplotlib.pyplot as plt

fig, ax = plt.subplot(figsize=[10, 6])
# %%[sec_11_end]

# %%[sec_12_start]
import matplotlib.pyplot as plt

fig, ax = plt.subplot(figsize=[10, 6])
# %%[sec_12_end]
