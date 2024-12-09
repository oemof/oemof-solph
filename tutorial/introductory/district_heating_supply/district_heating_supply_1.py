# %%[sec_1_start]
import pandas as pd

data = pd.read_csv('input_data.csv', sep=';', index_col=0, parse_dates=True)
# %%[sec_1_end]

# %%[sec_2_start]
import oemof.solph as solph

district_heating_system = solph.EnergySystem(timeindex=data.index)
# %%[sec_2_end]

# %%[sec_3_start]
# Question: How to name the variables?
hnw = solph.Bus(label='heat network')
gnw = solph.Bus(label='gas network')

district_heating_system.add(hnw, gnw)
# %%[sec_3_end]

# %%[sec_4_start]
gas_source = solph.components.Source(
    label='gas source',
    outputs={gnw: solph.flows.Flow(variable_costs=data['gas price'])}
)

# nominal_value -> nominal_capacity
heat_sink = solph.components.Sink(
    label='heat sink',
    inputs={
        hnw: solph.flows.Flow(
            nominal_value=data['heat demand'].max(),
            fix=data['heat demand']/data['heat demand'].max()
        )
    }
)

district_heating_system.add(heat_sink, gas_source)

# %%[sec_4_end]

# %%[sec_5_start]
gas_boiler = solph.components.Converter(
    label='gas boiler',
    inputs={gnw: solph.flows.Flow()},
    outputs={
        hnw: solph.flows.Flow(
            nominal_value=20,
            variable_costs=0.50
        )
    },
    conversion_factors={gnw: 0.95}
)

district_heating_system.add(gas_boiler)
# %%[sec_5_end]

# %%[sec_6_start]
model = solph.Model(district_heating_system)
model.solve(solver="cbc", solve_kwargs={"tee": True})
# %%[sec_6_end]

# %%[sec_7_start]
results = solph.processing.results(model)

data_gnw = solph.views.node(results, 'gas network')['sequences']
data_hnw = solph.views.node(results, 'heat network')['sequences']
# %%[sec_7_end]

# %%[sec_8_start]
i = 0.05
n = 20
spec_inv_gas_boiler = 50000
cap_gas_boiler = 20
var_cost_gas_boiler = 0.50

q = 1 + i
# pvf = present value factor
pvf = (q**n - 1)/(q**n * (q - 1))
invest = spec_inv_gas_boiler * cap_gas_boiler
cost = (
    var_cost_gas_boiler * data_hnw[(('gas boiler', 'heat network'), 'flow')].sum()
    + (data['gas price'] * data_gnw[(('gas network', 'gas boiler'), 'flow')]).sum()
)
Q = data_hnw[(('heat network', 'heat sink'), 'flow')].sum()

LCOH = (invest + pvf * cost)/(pvf * Q)
# %%[sec_8_end]

# %%[sec_9_start]
co2 = 
# %%[sec_9_end]

# %%[sec_10_start]
import matplotlib.pyplot as plt

fig, ax = plt.subplot(figsize=[10, 6])
# %%[sec_10_end]