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
Download source code: :download:`result_object.py </../examples/result_object/result_object.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/result_object/result_object.py
        :language: python
        :lines: 61-

Data
----
Download data: :download:`time_series.csv </../examples/result_object/time_series.csv>`

Installation requirements
-------------------------
This example requires oemof.solph (v0.6.x), install by:

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
from oemof.tools import logger

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components
from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import processing
from oemof.solph import Results
from oemof.solph import views


def get_data_from_file_path(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
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


def main(optimize=True):

    # *************************************************************************
    # ********** PART 1 - Define and optimise the energy system ***************
    # *************************************************************************

    # Read data file
    file_name = "time_series.csv"
    data = get_data_from_file_path(file_name)

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
    bus_gas = buses.Bus(label="natural_gas")

    # create electricity bus
    bus_electricity = buses.Bus(label="electricity")

    # adding the buses to the energy system
    energysystem.add(bus_gas, bus_electricity)

    # create excess component for the electricity bus to allow overproduction
    energysystem.add(
        components.Sink(
            label="excess_bus_electricity",
            inputs={bus_electricity: flows.Flow()},
        )
    )

    # create source object representing the gas commodity
    energysystem.add(
        components.Source(
            label="rgas",
            outputs={bus_gas: flows.Flow()},
        )
    )

    # create fixed source object representing wind power plants
    energysystem.add(
        components.Source(
            label="wind",
            outputs={
                bus_electricity: flows.Flow(
                    fix=data["wind"], nominal_capacity=1000000
                )
            },
        )
    )

    # create fixed source object representing pv power plants
    energysystem.add(
        components.Source(
            label="pv",
            outputs={
                bus_electricity: flows.Flow(
                    fix=data["pv"], nominal_capacity=582000
                )
            },
        )
    )

    # create simple sink object representing the electrical demand
    # nominal_capacity is set to 1 because demand_el is not a normalised series
    energysystem.add(
        components.Sink(
            label="demand",
            inputs={
                bus_electricity: flows.Flow(
                    fix=data["demand_el"], nominal_capacity=1
                )
            },
        )
    )

    # create simple converter object representing a gas power plant
    energysystem.add(
        components.Converter(
            label="pp_gas",
            inputs={bus_gas: flows.Flow()},
            outputs={
                bus_electricity: flows.Flow(
                    nominal_capacity=10e10, variable_costs=50
                )
            },
            conversion_factors={bus_electricity: 0.58},
        )
    )

    # create storage object representing a battery
    nominal_capacity = 10077997
    nominal_capacity = nominal_capacity / 6

    battery_storage = components.GenericStorage(
        nominal_capacity=nominal_capacity,
        label="battery_storage",
        inputs={
            bus_electricity: flows.Flow(nominal_capacity=nominal_capacity)
        },
        outputs={
            bus_electricity: flows.Flow(
                nominal_capacity=nominal_capacity, variable_costs=0.001
            )
        },
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )

    energysystem.add(battery_storage)

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    if optimize is False:
        return energysystem

    logging.info("Optimise the energy system")

    # initialise the operational model
    energysystem_model = Model(energysystem)

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    energysystem_model.solve(
        solver=solver, solve_kwargs={"tee": solver_verbose}
    )

    logging.info("Store the energy system with the results.")

    # The processing module of the outputlib can be used to extract the results
    # from the model transfer them into a homogeneous structured dictionary.

    results = Results(energysystem_model)

    result_dict = processing.results(energysystem_model)

    # *************************************************************************
    # ********** PART 2 - Processing the results ******************************
    # *************************************************************************

    # define an alias for shorter calls below (optional)
    storage = energysystem.groups["battery_storage"]

    # print a time slice of the state of charge
    start_time = datetime(2012, 7, 4, 8, 0, 0)
    end_time = datetime(2012, 7, 4, 17, 0, 0)

    print("\n********* State of Charge (slice) *********")
    print(
        f"{result_dict[(storage, None)]['sequences'][start_time : end_time]}\n"
    )
    print(f"{results.storage_content[storage][start_time : end_time]}\n")

    # get all variables of a specific component/bus
    custom_storage = views.node(result_dict, "battery_storage")
    electricity_bus = views.node(result_dict, "electricity")

    # plot the time series (sequences) of a specific component/bus
    plot_figures_for(custom_storage)
    plot_figures_for(electricity_bus)

    # print the sums of the flows around the electricity bus
    print("********* Main results *********")
    print(electricity_bus["sequences"].sum(axis=0))


if __name__ == "__main__":
    main()
