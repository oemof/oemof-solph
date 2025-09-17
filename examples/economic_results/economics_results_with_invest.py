# -*- coding: utf-8 -*-

"""
General description
-------------------

A basic example to show how to model a simple energy system with oemof.solph.
and use the Results class to calculate the variable costs as well as the
investment costs.

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
Download source code: :download:`economic_results.py </../examples/economic_results/economics_results_with_invest.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/economic_results/economics_results_with_invest.py
        :language: python
        :lines: 61-

Data
----
Download data: :download:`time_series.csv </../examples/economic_results/time_series.csv>`

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

import matplotlib.pyplot as plt
import pandas as pd
from oemof.tools import logger

from oemof.solph import EnergySystem
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import Results
from oemof.solph import buses
from oemof.solph import components
from oemof.solph import create_time_index
from oemof.solph import flows


def get_data_from_file_path(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        dir = os.path.dirname(os.path.abspath(__file__))
        data = pd.read_csv(dir + "/" + file_path)
    return data


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
                    nominal_capacity=Investment(
                        ep_costs=300, nonconvex=True, offset=400, maximum=10e10
                    ),
                    variable_costs=50,
                )
            },
            conversion_factors={bus_electricity: 0.58},
        )
    )

    # create storage object representing a battery
    nominal_capacity = 10077997
    nominal_capacity = Investment(ep_costs=80, maximum=nominal_capacity / 6)

    battery_storage = components.GenericStorage(
        nominal_capacity=nominal_capacity,
        label="battery_storage",
        inputs={bus_electricity: flows.Flow(nominal_capacity=10077997 / 6)},
        outputs={
            bus_electricity: flows.Flow(
                nominal_capacity=10077997 / 6, variable_costs=10
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

    # *************************************************************************
    # ********** PART 2 - Processing the results ******************************
    # *************************************************************************

    # These are the keys to access information from the Results()
    keys = results.keys()
    print("\n********* Keys to access information from Results() *********")
    for key in keys:
        print("Key: {}".format(key))

    # Evaluating the economics of the solution

    print("\n********* Evaluating economics *********")

    # -------------- variable costs ---------------------------
    variable_costs = results.to_df("variable_costs")
    values = results.to_df("flow")

    var_costs_dict = {}
    for i, o in energysystem_model.FLOWS:
        var_costs_dict["({}, {})".format(i, o)] = energysystem_model.flows[
            i, o
        ].variable_costs

    df_var_costs = pd.DataFrame.from_dict(var_costs_dict)
    df_var_costs.index = create_time_index(
        2012, number=number_of_time_steps - 1
    )

    start_date = "2012-04-07 00:00:00"
    end_date = "2012-04-21 23:00:00"

    # Create figure and subplots
    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    # First subplot for flow values
    values.loc[start_date:end_date, :].plot(ax=axs[0])
    axs[0].set_title("Flow Values")
    axs[0].set_ylabel("Power in kW")

    # Second subplot for variable costs
    df_var_costs.loc[start_date:end_date, :].plot(ax=axs[1])
    axs[1].set_title("Variable costs")
    axs[1].set_ylabel("specific variable costs in €/kWh")

    # Third subplot for variable opex
    variable_costs.loc[start_date:end_date, :].plot(ax=axs[2])
    axs[2].set_title("Variable OPEX")
    axs[2].set_ylabel("variable costs in €")

    # plt.show()

    # -------------- Investment Costs ---------------------------

    invest = results.to_df("invest")
    print(invest)

    investment_costs = results.to_df("investment_costs")

    annual_costs_dict = {}
    for i, o in energysystem_model.FLOWS:
        if hasattr(energysystem_model.flows[i, o].investment, "ep_costs"):
            annual_costs_dict["({}, {})".format(i, o)] = {
                "ep_costs": (
                    energysystem_model.flows[i, o].investment.ep_costs[0]
                ),
                "offset": (
                    energysystem_model.flows[i, o].investment.offset[0]
                ),
            }
    for node in energysystem_model.nodes:
        if isinstance(
            node,
            components._generic_storage.GenericStorage,
        ):
            annual_costs_dict[node.label] = {
                "ep_costs": (node.investment.ep_costs[0]),
                "offset": (node.investment.offset[0]),
            }

    df_annual_costs = pd.DataFrame.from_dict(annual_costs_dict)

    # Create figure and subplots
    fig2, axs2 = plt.subplots(1, 3, figsize=(10, 6))

    # First subplot for invest decisions
    results.to_df("invest").plot(ax=axs2[0], kind="bar")
    axs2[0].set_title("Yearly Investment Installation")
    axs2[0].set_ylabel("installed capacity in kW")

    # Second subplot for ep_costs and offset
    df_annual_costs.plot(ax=axs2[1], kind="bar")
    axs2[1].set_title("ep_costs and offset")
    axs2[1].set_ylabel("specific investment costs in €/kWh and €")

    # Third subplot for yearly investment costs
    investment_costs.plot(ax=axs2[2], kind="bar")
    axs2[2].set_title("Yearly Investment Costs")
    axs2[2].set_ylabel("investment costs in €")

    plt.show()


if __name__ == "__main__":
    main()
