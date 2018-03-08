
import os
import pandas as pd
from oemof.solph import (
    Bus, Sink, Source, Flow, Transformer, Model, EnergySystem)

filename = os.path.join(os.path.dirname(__file__), 'input_data.csv')
data = pd.read_csv(filename, sep=",")

bcoal = Bus(label='coal', balanced=False)
bgas = Bus(label='gas', balanced=False)
boil = Bus(label='oil', balanced=False)
blig = Bus(label='lignite', balanced=False)

# electricity and heat
bel = Bus(label='b_el')
bth = Bus(label='b_th')

# an excess and a shortage variable can help to avoid infeasible problems
excess_el = Sink(label='excess_el', inputs={bel: Flow()})
# shortage_el = Source(label='shortage_el',
#                      outputs={bel: Flow(variable_costs=200)})

# sources
wind = Source(
    label='wind',
    outputs={
        bel: Flow(
            actual_value=data['wind'],
            nominal_value=66.3,
            fixed=True
        )
    }
)

pv = Source(
    label='pv',
    outputs={
        bel: Flow(
            actual_value=data['pv'],
            nominal_value=65.3,
            fixed=True
        )
    }
)

# demands (electricity/heat)
demand_el = Sink(
    label='demand_elec',
    inputs={
        bel: Flow(
            nominal_value=85,
            actual_value=data['demand_el'],
            fixed=True
        )
    }
)

demand_th = Sink(
    label='demand_therm',
    inputs={
        bth: Flow(
            nominal_value=40,
            actual_value=data['demand_th'],
            fixed=True
        )
    }
)

# power plants
pp_coal = Transformer(
    label='pp_coal',
    inputs={bcoal: Flow()},
    outputs={
        bel: Flow(
            nominal_value=20.2,
            variable_costs=25
        )
    },
    conversion_factors={bel: 0.39}
)

pp_lig = Transformer(
    label='pp_lig',
    inputs={blig: Flow()},
    outputs={
        bel: Flow(
            nominal_value=11.8,
            variable_costs=19
        )
    },
    conversion_factors={bel: 0.41}
)

pp_gas = Transformer(
    label='pp_gas',
    inputs={bgas: Flow()},
    outputs={
        bel: Flow(
            nominal_value=41,
            variable_costs=40
        )
    },
    conversion_factors={bel: 0.50}
)

pp_oil = Transformer(
    label='pp_oil',
    inputs={boil: Flow()},
    outputs={
     bel: Flow(
         nominal_value=5,
         variable_costs=50
     )
    },
    conversion_factors={bel: 0.28}
)

# combined heat and power plant (chp)
pp_chp = Transformer(
    label='pp_chp',
    inputs={bgas: Flow()},
    outputs={
     bel: Flow(
         nominal_value=30,
         variable_costs=42
     ),
     bth: Flow(nominal_value=40)
    },
    conversion_factors={bel: 0.3, bth: 0.4}
)

# heatpump with a coefficient of performance (COP) of 3
b_heat_source = Bus(label='b_heat_source')

heat_source = Source(label='heat_source', outputs={b_heat_source: Flow()})

cop = 3
heat_pump = Transformer(
    label='heat_pump',
    inputs={bel: Flow(), b_heat_source: Flow()},
    outputs={bth: Flow(nominal_value=10)},
    conversion_factors={bel: 1 / 3, b_heat_source: (cop - 1) / cop}
)

datetimeindex = pd.date_range('1/1/2012', periods=24, freq='H')
energysystem = EnergySystem(timeindex=datetimeindex)
energysystem.add(
    bcoal, bgas, boil, bel, bth, blig, excess_el, wind, pv, demand_el,
    demand_th, pp_coal, pp_lig, pp_oil, pp_gas, pp_chp, b_heat_source,
    heat_source, heat_pump
)

# ################################ optimization ###########################

# create optimization model based on energy_system
optimization_model = Model(energysystem=energysystem)

# solve problem
optimization_model.solve()
