# -*- coding: utf-8 -*-

"""
General description
-------------------

A basic example to show how to model a simple energy system with oemof.solph.

The following energy system is modeled:

.. code-block:: text

                     input/output  bgas     bel
                         |          |        |
                         |          |        |
     wind(FixedSource)   |------------------>|
                         |          |        |
     pv(FixedSource)     |------------------>|
                         |          |        |
     rgas(Commodity)     |--------->|        |
                         |          |        |
     demand(Sink)        |<------------------|
                         |          |        |
                         |          |        |
     pp_gas(Converter)   |<---------|        |
                         |------------------>|
                         |          |        |
     storage(Storage)    |<------------------|
                         |------------------>|

Code
----
Download source code: :download:`basic_example.py </../examples/basic_example/basic_example.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/basic_example/basic_example.py
        :language: python
        :lines: 61-

Data
----
Download data: :download:`basic_example.csv </../examples/basic_example/basic_example.csv>`

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]

License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""
###########################################################################
# imports
###########################################################################

import logging
import os
import pprint as pp
from datetime import datetime

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
from oemof.solph import helpers
from oemof.solph import processing
from oemof.solph import views

STORAGE_LABEL = "battery_storage"


def get_data_from_file_path(file_path: str) -> pd.DataFrame:
    dir = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(dir + "/" + file_path)
    return data


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
def main(dump_and_restore=False):
    # For models that need a long time to optimise, saving and loading the
    # EnergySystem might be advised. By default, we do not do this here. Feel
    # free to experiment with this once you understood the rest of the code.
    dump_results = restore_results = dump_and_restore

    # *************************************************************************
    # ********** PART 1 - Define and optimise the energy system ***************
    # *************************************************************************

    # Read data file
    file_name = "basic_example.csv"
    data = get_data_from_file_path(file_name)

    solver = "cbc"  # 'glpk', 'gurobi',....
    debug = False  # Set number_of_timesteps to 3 to get a readable lp-file.
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

    bus_heat = buses.Bus(label="heat")

    # adding the buses to the energy system
    energysystem.add(bus_gas, bus_electricity, bus_heat)

    # create excess component for the electricity bus to allow overproduction
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

    # create fixed source object representing wind power plants
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

    # create simple converter object representing a gas power plant
    energysystem.add(
        components.Converter(
            label="Gas boiler",
            inputs={bus_gas: flows.Flow()},
            outputs={bus_heat: flows.Flow(variable_costs=50)},
            conversion_factors={bus_electricity: 0.58},
        )
    )

    energysystem.add(
        components.Converter(
            label="Heatpump",
            inputs={bus_electricity: flows.Flow()},
            outputs={bus_heat: flows.Flow(variable_costs=50)},
            conversion_factors={bus_electricity: 0.58},
        )
    )

    # create storage object representing a battery
    nominal_capacity = 10077997
    nominal_capacity = nominal_capacity / 6

    # battery_storage = components.GenericStorage(
    #     label=STORAGE_LABEL,
    #     inputs={bus_electricity: flows.Flow()},
    #     outputs={bus_electricity: flows.Flow(variable_costs=0.001)},
    #     loss_rate=0.00,
    #     initial_storage_level=None,
    #     inflow_conversion_factor=1,
    #     outflow_conversion_factor=0.8,
    # )

    # energysystem.add(battery_storage)

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info("Optimise the energy system")

    # initialise the operational model
    energysystem_model = Model(energysystem)

    esgr = ESGraphRenderer(
        energysystem_model,
        legend=False,
        filepath="D:/ES.svg",
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
