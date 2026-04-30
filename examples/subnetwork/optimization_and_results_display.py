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
                         |          |        |
     DSO(DSO)            |<------------------|
                         |------------------>|

Code
----
Download source code: :download:`optimization_and_results_display.py </../examples/subnetwork/optimization_and_results_display.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/subnetwork/optimization_and_results_display.py
        :language: python
        :lines: 61-

Data
----
Download data: :download:`time_series.csv </../examples/subnetwork/time_series.csv>`

Installation requirements
-------------------------
This example requires oemof.solph (at least v0.6.3), install by:

.. code:: bash

    pip install oemof.solph>=0.6.3

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

from oemof.network import Node
from oemof.solph import EnergySystem
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import Results
from oemof.solph import Bus
from oemof.solph import Flow
from oemof.solph import components
from oemof.solph import create_time_index


def get_data_from_file_path(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        dir = os.path.dirname(os.path.abspath(__file__))
        data = pd.read_csv(dir + "/" + file_path)
    return data


class DSO(Node):
    def __init__(
        self,
        name,
        bus,
        energy_price,
        feedin_tariff,
        peak_demand_pricing=0,
        peak_demand_pricing_period=1,
        renewable_share=0.44,
        feedin_cap=None,
    ):
        """
        Energy provider for electricity distribution.

        This class represents a distribution system operator (DSO) that
        provides electricity from the utility grid with pricing and
        feedin capabilities.

        .. important ::
            The renewable share affects the overall system renewable
            factor calculation.

        :Structure:
          *input* & *output*
            bus : Electricity

        Parameters
        ----------
        name : str
            |name|
        energy_price : float, default=0.3
            |energy_prics|
        feedin_tariff : float, default=0.1
            |feedin_tariff|
        peak_demand_pricing : float, default=0
            |peak_demand_pricing|
        peak_demand_pricing_period : int, default=1
            |peak_demand_period|
        renewable_share : float, default=0.44
            |renewable_share|
        feedin_cap : float or None, default=None
            |feedin_cap|

        Examples
        --------
        >>> from oemof.solph import Bus
        >>> ebus = Bus(label="any_bus")
        >>> my_dso = DSO(
        ...     name="any_network",
        ...     bus=ebus,
        ...     energy_price=0.25,
        ...     feedin_tariff=0.08,
        ... )

        """
        self.name = name
        self.bus = bus
        self.energy_price = energy_price
        self.feedin_tariff = feedin_tariff
        self.peak_demand_pricing = peak_demand_pricing
        self.peak_demand_pricing_period = peak_demand_pricing_period
        self.renewable_share = renewable_share  # Specific emission
        self.feedin_cap = feedin_cap

        super().__init__(label=self.name)

        internal_bus = self.subnode(Bus, local_name="internal_bus")

        self.subnode(
            components.Converter,
            inputs={self.bus: Flow(variable_costs=self.feedin_tariff * -1)},
            outputs={internal_bus: Flow()},
            local_name="feedin_converter",
        )

        self.subnode(
            components.Sink,
            inputs={internal_bus: Flow()},
            local_name="feedin_sink",
        )

        self.subnode(
            components.Converter,
            inputs={internal_bus: Flow()},
            outputs={self.bus: Flow(variable_costs=self.energy_price)},
            local_name="consumption_converter",
        )

        self.subnode(
            components.Source,
            outputs={internal_bus: Flow()},
            local_name="consumption_source",
        )


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
    bus_gas = Bus(label="natural_gas")

    # create electricity bus
    bus_electricity = Bus(label="electricity")

    # adding the buses to the energy system
    energysystem.add(bus_gas, bus_electricity)

    energysystem.add(
        DSO(
            name="My_DSO",
            bus=bus_electricity,
            energy_price=100,
            feedin_tariff=0.001,
        )
    )

    # create excess component for the electricity bus to allow overproduction
    energysystem.add(
        components.Sink(
            label="excess_bus_electricity",
            inputs={bus_electricity: Flow()},
        )
    )

    # create source object representing the gas commodity
    energysystem.add(
        components.Source(
            label="rgas",
            outputs={bus_gas: Flow()},
        )
    )

    # create fixed source object representing wind power plants
    energysystem.add(
        components.Source(
            label="wind",
            outputs={
                bus_electricity: Flow(
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
                bus_electricity: Flow(fix=data["pv"], nominal_capacity=582000)
            },
        )
    )

    # create simple sink object representing the electrical demand
    # nominal_capacity is set to 1 because demand_el is not a normalised series
    energysystem.add(
        components.Sink(
            label="demand",
            inputs={
                bus_electricity: Flow(
                    fix=data["demand_el"], nominal_capacity=1
                )
            },
        )
    )

    # create simple converter object representing a gas power plant
    energysystem.add(
        components.Converter(
            label="pp_gas",
            inputs={bus_gas: Flow()},
            outputs={
                bus_electricity: Flow(
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
        inputs={bus_electricity: Flow(nominal_capacity=10077997 / 6)},
        outputs={
            bus_electricity: Flow(
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

    logging.info("Extract the results energy system with the results.")

    results = Results(energysystem_model)

    # *************************************************************************
    # ********** PART 2 - Processing the results ******************************
    # *************************************************************************

    # These are the keys to access information from the Results()
    keys = results.keys()
    print("\n********* Keys to access information from Results() *********")
    for key in keys:
        print("Key: {}".format(key))

    print("\n********* Summary of flows *********")
    print(results["flow"].sum())
    # TODO @gnn:
    #   here I would like to only see "electricity My_DSO" instead of
    #   "electricity ('feedin_converter', 'My_DSO')" for feedin and "DSO
    #   electricity" for consumption, but none of the internal flows
    #   (like "('internal_bus', 'My_DSO') ('feedin_sink', 'My_DSO')")
    print("\n********* Summary of investments *********")
    print(results["invest"])
    # TODO @gnn:
    #   here I would like to not have the "(pp_gas, electricity)" column
    #   label for the investment of the pp_gas but rather simply
    #   "pp_gas"

    # Evaluating the economics of the solution
    print("\n********* Evaluating economics *********")

    # -------------- variable costs ---------------------------
    variable_costs = results.get("variable_costs")
    values = results.get("flow")

    var_costs_dict = {}
    for i, o in energysystem_model.FLOWS:
        var_costs_dict["({}, {})".format(i, o)] = energysystem_model.flows[
            i, o
        ].variable_costs

    df_var_costs = pd.DataFrame.from_dict(var_costs_dict)
    df_var_costs.index = create_time_index(
        2012, number=number_of_time_steps - 1
    )

    start_date = "2012-01-07 00:00:00"
    end_date = "2012-01-14 23:00:00"

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

    invest = results.get("invest")

    investment_costs = results.get("investment_costs")

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
    results.get("invest").plot(ax=axs2[0], kind="bar")
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
