# -*- coding: utf-8 -*-

"""
General description
-------------------
This Code generates the picture of an energysystem used for the grid icons in
the docs

License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""
###########################################################################
# imports
###########################################################################

import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import plotly.io as pio
from oemof.tools import logger
from oemof.visio import ESGraphRenderer

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components
from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import processing


def plot_figures_for(element: dict) -> None:
    figure, axes = plt.subplots(figsize=(10, 5))
    element["sequences"].plot(ax=axes, kind="line", drawstyle="steps-post")
    plt.legend(
        loc="upper center",
        prop={"size": 8},
        bbox_to_anchor=(0.5, 1.25),
        ncol=2,
    )
    figure.subplots_adjust(top=0.8)
    plt.show()


# uses data from the basic example
def main():

    # *************************************************************************
    # ********** PART 1 - Define and optimise the energy system ***************
    # *************************************************************************

    # Read data file
    file_name = os.path.realpath(
        os.path.join(
            __file__,
            "..",
            "..",
            "..",
            "..",
            r"examples\result_object\time_series.csv",
        )
    )
    data = pd.read_csv(file_name)

    solver = "cbc"  # 'glpk', 'gurobi',....
    number_of_time_steps = len(data)
    solver_verbose = False  # show/hide solver output

    # initiate the logger (see the API docs for more information)
    logger.define_logging(
        logfile="oemof_example.log",
        screen_level=logging.INFO,
        file_level=logging.INFO,
    )

    logging.info("Initialize the energy system")
    date_time_index = create_time_index(2012, number=number_of_time_steps)

    # create the energysystem and assign the time index
    energysystem = EnergySystem(
        timeindex=date_time_index, infer_last_interval=False
    )

    ##########################################################################
    # Create oemof objects
    ##########################################################################

    logging.info("Create oemof objects")

    # The bus objects were assigned to variables which makes it easier to
    # connect components to these buses (see below).

    # create natural gas bus
    bus_gas = buses.Bus(label="natural gas")

    # create electricity bus
    bus_electricity = buses.Bus(label="electricity")

    # create heat bus
    bus_heat = buses.Bus(label="heat")

    # adding the buses to the energy system
    energysystem.add(bus_gas, bus_electricity, bus_heat)

    # create sink for heat demand
    energysystem.add(
        components.Sink(
            label="Heat Demand",
            inputs={
                bus_heat: flows.Flow(fix=data["demand_el"], nominal_value=2)
            },
        )
    )

    # create source object representing the gas commodity
    energysystem.add(
        components.Source(
            label="Gas Grid",
            outputs={bus_gas: flows.Flow()},
        )
    )

    # create fixed source object representing power grid
    energysystem.add(
        components.Source(
            label="Power Grid",
            outputs={bus_electricity: flows.Flow()},
        )
    )

    # create fixed source object representing pv power plants
    energysystem.add(
        components.Source(
            label="Pv Plant",
            outputs={
                bus_electricity: flows.Flow(
                    fix=data["pv"], nominal_value=582000
                )
            },
        )
    )

    # create simple sink object representing the electrical demand
    # nominal_capacity is set to 1 because demand_el is not a normalised series
    energysystem.add(
        components.Sink(
            label="Electricity Demand",
            inputs={
                bus_electricity: flows.Flow(
                    fix=data["demand_el"], nominal_value=1
                )
            },
        )
    )

    # create simple converter object representing a gas boiler
    energysystem.add(
        components.Converter(
            label="Gas boiler",
            inputs={bus_gas: flows.Flow()},
            outputs={bus_heat: flows.Flow(variable_costs=50)},
            conversion_factors={bus_electricity: 0.58},
        )
    )

    # create simple converter object representing a heatpump
    energysystem.add(
        components.Converter(
            label="Heatpump",
            inputs={bus_electricity: flows.Flow()},
            outputs={bus_heat: flows.Flow(variable_costs=50)},
            conversion_factors={bus_electricity: 0.58},
        )
    )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info("Optimise the energy system")

    # initialise the operational model
    energysystem_model = Model(energysystem)

    esgr = ESGraphRenderer(
        energysystem_model,
        legend=False,
        filepath=os.path.realpath(
            os.path.join(__file__, "..", "..", "ES.svg")
        ),
        img_format="svg",
    )
    esgr.render()

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    energysystem_model.solve(
        solver=solver, solve_kwargs={"tee": solver_verbose}
    )

    # after the solve method of the model has been called
    results = processing.results(energysystem_model)
    fig_dict = esgr.sankey(results)
    pio.show(fig_dict)


main()
