import pandas as pd
import oemof.solph as solph
# from helpers import lcoh

# %%[sec_1_start]
data = pd.read_csv('input_data.csv', sep=';', index_col=0, parse_dates=True)
# %%[sec_1_end]

district_heating_system = solph.EnergySystem(
    timeindex=data.index, infer_last_interval=False
)

heat_bus = solph.Bus(label='heat network')
gas_bus = solph.Bus(label='gas network')

district_heating_system.add(heat_bus, gas_bus)
# %%[sec_2_start]
waste_heat_bus = solph.Bus(label='waste heat network')
electricity_bus = solph.Bus(label='electricity network')

district_heating_system.add(waste_heat_bus, electricity_bus)
# %%[sec_2_end]

gas_source = solph.components.Source(
    label='gas source',
    outputs={gas_bus: solph.flows.Flow(variable_costs=data['gas price'])}
)

# nominal_value -> nominal_capacity
heat_sink = solph.components.Sink(
    label='heat sink',
    inputs={
        heat_bus: solph.flows.Flow(
            nominal_value=data['heat demand'].max(),
            fix=data['heat demand']/data['heat demand'].max()
        )
    }
)

district_heating_system.add(heat_sink, gas_source)

# %%[sec_3_start]
# ist die waste heat source fix oder unendlich?
waste_heat_source = solph.components.Source(
    label='waste heat source',
    outputs={waste_heat_bus: solph.flows.Flow()}
)

electricity_source = solph.components.Source(
    label='electricity source',
    outputs={electricity_bus: solph.flows.Flow(
        variable_costs=data['electricity price'])}
)

district_heating_system.add(waste_heat_source, electricity_source)
# %%[sec_3_end]

gas_boiler = solph.components.Converter(
    label='gas boiler',
    inputs={gas_bus: solph.flows.Flow()},
    outputs={
        heat_bus: solph.flows.Flow(
            nominal_value=20,
            variable_costs=0.50
        )
    },
    conversion_factors={gas_bus: 0.95}
)

district_heating_system.add(gas_boiler)

# %%[sec_4_start]
def epc(capex, lifetime=20, wacc=0.05):
    epc = capex * (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)
    return epc

spec_inv_storage=250

# Soll es ein saisonaler oder Pufferspeicher sein?
heat_storage = solph.components.GenericStorage(
    label='heat storage',
    investment=solph.Investment(
        ep_costs=epc(spec_inv_storage)
    )
    inputs={heat_bus: solph.flows.Flow(nominal_capacity=100, variable_costs=10)},
    outputs={heat_bus: solph.flows.Inves(nominal_capacity=100, variable_costs=10)},
    loss_rate=0.001, nominal_capacity=50,
)
# %%[sec_4_end]

# %%[sec_5_start]
cop = 3
spec_inv_heat_pump = 500000

heat_pump = solph.components.Converter(
    label='heat pump',
    inputs={
        electricity_bus: solph.flows.Flow(),
        waste_heat_bus: solph.flows.Flow()
        },
    outputs={
        heat_bus: solph.flows.Flow(
            nominal_value=solph.Investment(
                ep_costs=epc(spec_inv_heat_pump), maximum=50
                ),
        )
    },
    conversion_factors={
        electricity_bus: 1/cop,
        waste_heat_bus: (cop-1)/cop
        }
)
district_heating_system.add(heat_pump)
# %%[sec_5_end]

# solve model
model = solph.Model(district_heating_system)
model.solve(solver="cbc", solve_kwargs={"tee": True})


# results
results = solph.processing.results(model)

data_gas_bus = solph.views.node(results, 'gas network')['sequences']
data_heat_bus = solph.views.node(results, 'heat network')['sequences']

spec_inv_gas_boiler = 50000
cap_gas_boiler = 20
var_cost_gas_boiler = 0.50

invest_cost = spec_inv_gas_boiler * cap_gas_boiler
operation_cost = (
    var_cost_gas_boiler * data_heat_bus[(('gas boiler', 'heat network'), 'flow')].sum()
    + (data['gas price'] * data_gas_bus[(('gas network', 'gas boiler'), 'flow')]).sum()
)
heat_produced = data_heat_bus[(('heat network', 'heat sink'), 'flow')].sum()

lcoh = LCOH(invest_cost, operation_cost, heat_produced)

print(f'LCOH: {lcoh:.2f} €/MWh')


co2 = data_gas_bus[(('gas network', 'gas boiler'), 'flow')].sum() * 201.2

print(f'CO2-emissions: {co2:.0f} kg')


import matplotlib.pyplot as plt

fig, ax = plt.subplot(figsize=[10, 6])



import matplotlib.pyplot as plt

fig, ax = plt.subplot(figsize=[10, 6])
