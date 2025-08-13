import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
from oemof.tools import logger
from oemof.network import SubNetwork
from oemof import solph

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components
from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import helpers
from oemof.solph import Results

STORAGE_LABEL = "battery_storage"


def get_data_from_file_path(file_path: str) -> pd.DataFrame:
    file_dir = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(file_dir + "/" + file_path)
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


class Volatile(solph.Facade):

    def __init__(
        self,
        label: str,
        output_bus: solph.Bus,
        timeseries: float | list[float],
        nominal_capacity: float,
    ):
        self.output_bus = output_bus
        self.timeseries = timeseries
        self.nominal_capacity = nominal_capacity

        super().__init__(label=label, facade_type=type(self))

    def define_subnetwork(self):
        self.subnode(
            solph.components.Source,
            label="source",
            outputs={
                self.output_bus: solph.Flow(
                    max=self.timeseries, nominal_capacity=self.nominal_capacity
                ),
            },
        )


def main():
    # For models that need a long time to optimise, saving and loading the
    # EnergySystem might be advised. By default, we do not do this here. Feel
    # free to experiment with this once you understood the rest of the code.

    # *************************************************************************
    # ********** PART 1 - Define and optimise the energy system ***************
    # *************************************************************************

    # Read data file
    file_name = "subnetwork_example.csv"
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

    # *** SUB-NETWORK ***************************
    # Add a subnetwork for Renewable Energies. This not a Facade it just meant
    # to group components
    renewables = SubNetwork("renewables")
    re_bus = renewables.subnode(buses.Bus, "re_elec")

    # create fixed source object representing wind power plants
    renewables.subnode(
        Volatile,
        label="wind",
        output_bus=re_bus,
        timeseries=data["wind"],
        nominal_capacity=1000000,
    )
    # create fixed source object representing pv power plants
    renewables.subnode(
        Volatile,
        label="pv",
        output_bus=re_bus,
        timeseries=data["pv"],
        nominal_capacity=582000,
    )
    renewables.subnode(
        components.Converter,
        label="connection",
        outputs={bus_electricity: flows.Flow()},
        inputs={re_bus: flows.Flow()},
    )
    energysystem.add(renewables)  # Subnetwork to Energysystem
    # *************************************************************

    # create simple sink object representing the electrical demand
    # nominal_value is set to 1 because demand_el is not a normalised series
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
    nominal_value = nominal_capacity / 6

    battery_storage = components.GenericStorage(
        nominal_capacity=nominal_capacity,
        label=STORAGE_LABEL,
        inputs={bus_electricity: flows.Flow(nominal_capacity=nominal_value)},
        outputs={
            bus_electricity: flows.Flow(
                nominal_capacity=nominal_value, variable_costs=0.001
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

    logging.info("Optimise the energy system")

    # initialise the operational model
    energysystem_model = Model(energysystem)

    # This is for debugging only. It is not(!) necessary to solve the problem
    # and should be set to False to save time and disc space in normal use. For
    # debugging the timesteps should be set to 3, to increase the readability
    # of the lp-file.
    if debug:
        file_path = os.path.join(
            helpers.extend_basic_path("lp_files"), "basic_example.lp"
        )
        logging.info(f"Store lp-file in {file_path}.")
        io_option = {"symbolic_solver_labels": True}
        energysystem_model.write(file_path, io_options=io_option)

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    energysystem_model.solve(
        solver=solver, solve_kwargs={"tee": solver_verbose}
    )

    results = Results(energysystem_model)

    # ToDO Implement a filter methode for the Result object to exclude
    #  subcomponents of a facade/sub-network
    # The following lines are meant to show how the result should look like
    # in case the subcomponents should be exclude. There should not be a
    # postprocessing it is better to filter the nodes directly

    # Filter columns that are internal only
    keep_columns = [
        c
        for c in results.flow.columns
        if getattr(c[1].label, "parent", None)
        != getattr(c[0].label, "parent", None)
        or (
            getattr(c[0].label, "parent", True) is True
            and getattr(c[1].label, "parent", True) is True
        )
    ]
    flow_results_filtered = results.flow[keep_columns].copy()

    # Replace subcomponent with facade object
    for level in [0, 1]:
        flow_results_filtered.rename(
            columns={
                c[level]: getattr(c[level].label, "parent", c[level])
                for c in flow_results_filtered.columns
            },
            level=level,
            inplace=True,
        )

    print("**** All results ****")
    print(results.flow.sum())

    print("**** Filtered results ****")
    print(flow_results_filtered.sum())


if __name__ == "__main__":
    main()
