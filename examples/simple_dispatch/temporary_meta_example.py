import os
import pprint

import matplotlib.pyplot as plt
import pandas as pd

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph import create_time_index
from oemof.solph.components import Converter
from oemof.solph.components import Sink
from oemof.solph.components import Source


def main(solver="cbc"):
    # Read data file
    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input_data.csv"
    )
    data = pd.read_csv(filename)
    data = data.iloc[:24]

    # Create an energy system and optimize the dispatch at least costs.
    # ####################### initialize and provide data #####################
    datetimeindex = create_time_index(2016, number=len(data))
    energysystem = EnergySystem(
        timeindex=datetimeindex, infer_last_interval=False
    )

    # ######################### create energysystem components ################

    # resource buses
    bcoal = Bus(label="coal", balanced=False)
    bgas = Bus(label="gas", balanced=False)
    boil = Bus(label="oil", balanced=False)
    blig = Bus(label="lignite", balanced=False)

    # electricity and heat
    bel = Bus(label="bel")
    bth = Bus(label="bth")

    energysystem.add(bcoal, bgas, boil, blig, bel, bth)

    # an excess and a shortage variable can help to avoid infeasible problems
    energysystem.add(Sink(label="excess_el", inputs={bel: Flow()}))
    # shortage_el = Source(label='shortage_el',
    #                      outputs={bel: Flow(variable_costs=200)})

    # sources
    energysystem.add(
        Source(
            label="wind",
            outputs={bel: Flow(fix=data["wind"], nominal_capacity=66.3)},
        )
    )

    energysystem.add(
        Source(
            label="pv",
            outputs={bel: Flow(fix=data["pv"], nominal_capacity=65.3)},
        )
    )

    # demands (electricity/heat)
    energysystem.add(
        Sink(
            label="demand_el",
            inputs={bel: Flow(nominal_capacity=85, fix=data["demand_el"])},
        )
    )

    energysystem.add(
        Sink(
            label="demand_th",
            inputs={bth: Flow(nominal_capacity=40, fix=data["demand_th"])},
        )
    )

    # power plants
    energysystem.add(
        Converter(
            label="pp_coal",
            inputs={bcoal: Flow()},
            outputs={bel: Flow(nominal_capacity=20.2, variable_costs=25)},
            conversion_factors={bel: 0.39},
        )
    )

    energysystem.add(
        Converter(
            label="pp_lig",
            inputs={blig: Flow()},
            outputs={bel: Flow(nominal_capacity=11.8, variable_costs=19)},
            conversion_factors={bel: 0.41},
        )
    )

    energysystem.add(
        Converter(
            label="pp_gas",
            inputs={bgas: Flow()},
            outputs={bel: Flow(nominal_capacity=41, variable_costs=40)},
            conversion_factors={bel: 0.50},
        )
    )

    energysystem.add(
        Converter(
            label="pp_oil",
            inputs={boil: Flow()},
            outputs={bel: Flow(nominal_capacity=5, variable_costs=50)},
            conversion_factors={bel: 0.28},
        )
    )

    # combined heat and power plant (chp)
    energysystem.add(
        Converter(
            label="pp_chp",
            inputs={bgas: Flow()},
            outputs={
                bel: Flow(nominal_capacity=30, variable_costs=42),
                bth: Flow(nominal_capacity=40),
            },
            conversion_factors={bel: 0.3, bth: 0.4},
        )
    )

    # heat pump with a coefficient of performance (COP) of 3
    b_heat_source = Bus(label="b_heat_source")
    energysystem.add(b_heat_source)

    energysystem.add(
        Source(label="heat_source", outputs={b_heat_source: Flow()})
    )

    cop = 3
    energysystem.add(
        Converter(
            label="heat_pump",
            inputs={bel: Flow(), b_heat_source: Flow()},
            outputs={bth: Flow(nominal_capacity=10)},
            conversion_factors={bel: 1 / cop, b_heat_source: (cop - 1) / cop},
        )
    )

    # create optimization model based on energy_system
    optimization_model = Model(energysystem=energysystem)

    # solve problem
    results = optimization_model.solve(
        solver=solver, solve_kwargs={"tee": False, "keepfiles": False}
    )

    pprint.pprint(results.keys())


if __name__ == "__main__":
    for solver_name in ["highs", "cbc", "scip"]:
        print(solver_name)
        main(solver=solver_name)
