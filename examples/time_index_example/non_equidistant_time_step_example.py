# -*- coding: utf-8 -*-

"""
General description
-------------------

An example to show how non-equidistant time steps work.
In addition to the comments in the simple example, note that:

- Time steps in the beginning are 15 minutes.
- Time steps in the end are hourly.
- In the middle, there is a very short demand peak of one minute. This, however,
  does barely influence the storage contents.
- Storage losses are defined per hour.
  - storage_fixed looses 1 energy unit per hour
  - storage_relative looses 50 % of its contents per hour
- If possible, energy is transferred from storage with relative losses to the
  one with fixed losses to minimise total losses.

Code
----
Download source code: :download:`non_equidistant_time_step_example.py </../examples/time_index_example/non_equidistant_time_step_example.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/time_index_example/non_equidistant_time_step_example.py
        :language: python
        :lines: 40-

Installation requirements
-------------------------

This example requires oemof.solph, install by:

.. code:: bash

    pip install oemof.solph

"""
import pandas as pd

from oemof import solph

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None


def main(optimize=True):
    solver = "cbc"  # 'glpk', 'gurobi',...
    solver_verbose = False  # show/hide solver output

    date_time_index = pd.DatetimeIndex(
        data=[
            "2000-1-1T00:00:00",
            "2000-1-1T00:15:00",
            "2000-1-1T00:30:00",
            "2000-1-1T00:45:00",
            "2000-1-1T01:00:00",
            "2000-1-1T01:00:01",
            "2000-1-1T02:00:00",
            "2000-1-1T03:00:00",
            "2000-1-1T04:00:00",
            "2000-1-1T05:00:00",
        ]
    )

    energy_system = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=False
    )

    bus = solph.buses.Bus(label="bus")
    source = solph.components.Source(
        label="source",
        outputs={
            bus: solph.flows.Flow(
                nominal_capacity=16,
                variable_costs=0.2,
                max=[0, 0, 0, 0, 0, 0, 0, 1, 1],
            )
        },
    )

    # storage with constant losses
    storage_fixed = solph.components.GenericStorage(
        label="storage_fixed",
        inputs={bus: solph.flows.Flow()},
        outputs={bus: solph.flows.Flow()},
        nominal_capacity=8,
        initial_storage_level=1,
        fixed_losses_absolute=1,  # 1 energy unit loss per hour
    )

    # storage with relative losses, we disallow outflows in the first time
    # steps, so that the content is not transferred to storage_fixed
    storage_relative = solph.components.GenericStorage(
        label="storage_relative",
        inputs={bus: solph.flows.Flow()},
        outputs={
            bus: solph.flows.Flow(
                nominal_capacity=4, max=[0, 0, 0, 0, 0, 0, 0, 1, 1]
            )
        },
        nominal_capacity=8,
        initial_storage_level=1,
        loss_rate=0.5,  # 50 % losses per hour
    )
    sink = solph.components.Sink(
        label="sink",
        inputs={
            bus: solph.flows.Flow(
                nominal_capacity=8,
                variable_costs=0.1,
                fix=[0.75, 0.5, 0, 0, 1, 0, 0, 0, 0],
            )
        },
    )

    energy_system.add(bus, source, sink, storage_relative, storage_fixed)

    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    if optimize is False:
        return energy_system

    model = solph.Model(energy_system)
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    results = solph.processing.results(model)

    results_df = results[(storage_fixed, None)]["sequences"].copy()
    results_df.rename(
        columns={"storage_content": "storage_fixed"}, inplace=True
    )
    results_df["storage_fixed_inflow"] = results[(bus, storage_fixed)][
        "sequences"
    ]["flow"]
    results_df["storage_fixed_outflow"] = results[(storage_fixed, bus)][
        "sequences"
    ]["flow"]
    results_df["storage_relative"] = results[(storage_relative, None)][
        "sequences"
    ]["storage_content"]
    results_df["storage_relative_inflow"] = results[(bus, storage_relative)][
        "sequences"
    ]["flow"]
    results_df["storage_relative_outflow"] = results[(storage_relative, bus)][
        "sequences"
    ]["flow"]

    print(results_df)

    if plt is not None:
        plt.plot(
            results[(bus, storage_fixed)]["sequences"],
            "r-",
            drawstyle="steps-post",
            label="storage_fixed inflow",
        )
        plt.plot(
            results[(storage_fixed, None)]["sequences"],
            "r--",
            label="storage_fixed content",
        )
        plt.plot(results[(storage_fixed, None)]["sequences"], "r+")
        plt.plot(
            results[(storage_fixed, bus)]["sequences"],
            "r:",
            drawstyle="steps-post",
            label="storage_fixed outflow",
        )

        plt.plot(
            results[(bus, storage_relative)]["sequences"],
            "m-",
            drawstyle="steps-post",
            label="storage_relative inflow",
        )
        plt.plot(
            results[(storage_relative, None)]["sequences"],
            "m--",
            label="storage_relative content",
        )
        plt.plot(results[(storage_relative, None)]["sequences"], "m+")
        plt.plot(
            results[(storage_relative, bus)]["sequences"],
            "m:",
            drawstyle="steps-post",
            label="storage_relative outflow",
        )

        plt.legend()
        plt.show()


if __name__ == "__main__":
    main()
