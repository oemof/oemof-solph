# -*- coding: utf-8 -*-

"""
General description
-------------------
This example shows how to create an energysystem with oemof objects and
solve it with the solph module. Results are plotted with solph.

Dispatch modelling is a typical thing to do with solph. However cost does not
have to be monetary but can be emissions etc. In this example a least cost
dispatch of different generators that meet an inelastic demand is undertaken.
Some of the generators are renewable energies with marginal costs of zero.
Additionally, it shows how combined heat and power units may be easily modelled
as well.

Code
----
Download source code: :download:`simple_dispatch.py </../examples/simple_dispatch/simple_dispatch.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/simple_dispatch/simple_dispatch.py
        :language: python
        :lines: 45-

Data
----
Download data: :download:`input_data.csv </../examples/simple_dispatch/input_data.csv>`

Installation requirements
-------------------------

This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph import create_time_index
from oemof.solph import views
from oemof.solph.components import Converter
from oemof.solph.components import Sink
from oemof.solph.components import Source


def main(optimize=True):
    # Read data file
    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input_data.csv"
    )
    data = pd.read_csv(filename)

    solver = "cbc"

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
            conversion_factors={bel: 1 / 3, b_heat_source: (cop - 1) / cop},
        )
    )

    # ################################ optimization ###########################

    if optimize is False:
        return energysystem

    # create optimization model based on energy_system
    optimization_model = Model(energysystem=energysystem)

    # solve problem
    optimization_model.solve(
        solver=solver, solve_kwargs={"tee": True, "keepfiles": False}
    )

    # write back results from optimization object to energysystem
    optimization_model.results()

    # ################################ results ################################

    # subset of results that includes all flows into and from electrical bus
    # sequences are stored within a pandas.DataFrames and scalars e.g.
    # investment values within a pandas.Series object.
    # in this case the entry data['scalars'] does not exist since no investment
    # variables are used
    data = views.node(optimization_model.results(), "bel")
    data["sequences"].info()
    print("Optimization successful. Showing some results:")

    # see: https://pandas.pydata.org/pandas-docs/stable/visualization.html
    node_results_bel = views.node(optimization_model.results(), "bel")
    node_results_flows = node_results_bel["sequences"]

    fig, ax = plt.subplots(figsize=(10, 5))
    node_results_flows.plot(
        ax=ax, kind="bar", stacked=True, linewidth=0, width=1
    )
    ax.set_title("Sums for optimization period")
    ax.legend(loc="upper right", bbox_to_anchor=(1, 1))
    ax.set_xlabel("Energy (MWh)")
    ax.set_ylabel("Flow")
    plt.legend(loc="center left", prop={"size": 8}, bbox_to_anchor=(1, 0.5))
    fig.subplots_adjust(right=0.8)

    dates = node_results_flows.index
    tick_distance = int(len(dates) / 7) - 1
    ax.set_xticks(range(0, len(dates), tick_distance), minor=False)
    if tick_distance > 0:
        ax.set_xticklabels(
            [
                item.strftime("%d-%m-%Y")
                for item in dates.tolist()[0::tick_distance]
            ],
            rotation=90,
            minor=False,
        )

    plt.show()

    node_results_bth = views.node(optimization_model.results(), "bth")
    node_results_flows = node_results_bth["sequences"]

    fig, ax = plt.subplots(figsize=(10, 5))
    node_results_flows.plot(
        ax=ax, kind="bar", stacked=True, linewidth=0, width=1
    )
    ax.set_title("Sums for optimization period")
    ax.legend(loc="upper right", bbox_to_anchor=(1, 1))
    ax.set_xlabel("Energy (MWh)")
    ax.set_ylabel("Flow")
    plt.legend(loc="center left", prop={"size": 8}, bbox_to_anchor=(1, 0.5))
    fig.subplots_adjust(right=0.8)

    dates = node_results_flows.index
    tick_distance = int(len(dates) / 7) - 1
    ax.set_xticks(range(0, len(dates), tick_distance), minor=False)
    if tick_distance > 0:
        ax.set_xticklabels(
            [
                item.strftime("%d-%m-%Y")
                for item in dates.tolist()[0::tick_distance]
            ],
            rotation=90,
            minor=False,
        )

    plt.show()


if __name__ == "__main__":
    main()
