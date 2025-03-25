# -*- coding: utf-8 -*-

"""
General description
-------------------

A basic example to show how to get the dual variables from the system. Try
to understand the plot.

Code
----
Download source code: :download:`dual_variable_example.py </../examples/dual_variable_example/dual_variable_example.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/dual_variable_example/dual_variable_example.py
        :language: python
        :lines: 34-297


Installation requirements
-------------------------

This example requires the version v0.5.x of oemof.solph:

.. code:: bash

    pip install 'oemof.solph[examples]>=0.5,<0.6'

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>

SPDX-License-Identifier: MIT
"""
###########################################################################
# imports
###########################################################################

import pandas as pd
from matplotlib import pyplot as plt
from oemof.tools import logger

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import flows
from oemof.solph import processing


def main(optimize=True):
    # *************************************************************************
    # ********** PART 1 - Define and optimise the energy system ***************
    # *************************************************************************

    solver = "cbc"  # 'glpk', 'gurobi',....
    number_of_time_steps = 48
    solver_verbose = False  # show/hide solver output

    # initiate the logger (see the API docs for more information)
    logger.define_logging()

    date_time_index = pd.date_range(
        "1/1/2012", periods=number_of_time_steps, freq="h"
    )

    energysystem = EnergySystem(
        timeindex=date_time_index, infer_last_interval=True
    )

    demand = [
        209,
        207,
        200,
        191,
        185,
        180,
        172,
        170,
        171,
        179,
        189,
        201,
        208,
        207,
        205,
        206,
        217,
        232,
        237,
        232,
        224,
        219,
        223,
        213,
        201,
        192,
        187,
        184,
        184,
        182,
        180,
        191,
        207,
        222,
        231,
        238,
        241,
        237,
        234,
        235,
        242,
        264,
        265,
        260,
        245,
        238,
        241,
        231,
    ]
    pv = [
        0.18,
        0.11,
        0.05,
        0.05,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.05,
        0.07,
        0.11,
        0.13,
        0.15,
        0.22,
        0.28,
        0.33,
        0.25,
        0.17,
        0.09,
        0.09,
        0.07,
        0.05,
        0.05,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.09,
        0.21,
        0.33,
        0.44,
        0.54,
        0.61,
        0.65,
        0.67,
        0.64,
        0.59,
        0.52,
    ]

    ##########################################################################
    # Create oemof object
    ##########################################################################

    # create natural gas bus
    bus_gas = buses.Bus(label="natural_gas")

    # create electricity bus
    bus_elec = buses.Bus(label="electricity")

    # adding the buses to the energy system
    energysystem.add(bus_gas, bus_elec)

    # create excess component for the electricity bus to allow overproduction
    energysystem.add(
        cmp.Sink(label="excess_bel", inputs={bus_elec: flows.Flow()})
    )

    # create source object representing the gas commodity (annual limit)
    energysystem.add(
        cmp.Source(
            label="rgas",
            outputs={bus_gas: flows.Flow(variable_costs=38)},
        )
    )

    # create fixed source object representing pv power plants
    energysystem.add(
        cmp.Source(
            label="pv",
            outputs={bus_elec: flows.Flow(fix=pv, nominal_capacity=700)},
        )
    )

    # create simple sink object representing the electrical demand
    energysystem.add(
        cmp.Sink(
            label="demand",
            inputs={bus_elec: flows.Flow(fix=demand, nominal_capacity=1)},
        )
    )

    # create simple converter object representing a gas power plant
    energysystem.add(
        cmp.Converter(
            label="pp_gas",
            inputs={bus_gas: flows.Flow()},
            outputs={bus_elec: flows.Flow(nominal_capacity=400)},
            conversion_factors={bus_elec: 0.5},
        )
    )

    # create storage object representing a battery
    cap = 400
    storage = cmp.GenericStorage(
        nominal_capacity=cap,
        label="storage",
        inputs={bus_elec: flows.Flow(nominal_capacity=cap / 6)},
        outputs={
            bus_elec: flows.Flow(
                nominal_capacity=cap / 6, variable_costs=0.001
            )
        },
        loss_rate=0.00,
        initial_storage_level=0,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )

    energysystem.add(storage)

    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    if optimize is False:
        return energysystem

    # initialise the operational model
    model = Model(energysystem)

    model.receive_duals()

    # if tee_switch is true solver messages will be displayed
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    # add results to the energy system to make it possible to store them.
    results = processing.results(model)

    flows_to_bus = pd.DataFrame(
        {
            str(k[0].label): v["sequences"]["flow"]
            for k, v in results.items()
            if k[1] is not None and k[1] == bus_elec
        }
    )
    flows_from_bus = pd.DataFrame(
        {
            str(k[1].label): v["sequences"]["flow"]
            for k, v in results.items()
            if k[1] is not None and k[0] == bus_elec
        }
    )

    storage = pd.DataFrame(
        {
            str(k[0].label): v["sequences"]["storage_content"]
            for k, v in results.items()
            if k[1] is None and k[0] == storage
        }
    )

    duals = pd.DataFrame(
        {
            str(k[0].label): v["sequences"]["duals"]
            for k, v in results.items()
            if k[1] is None and isinstance(k[0], buses.Bus)
        }
    )

    my_flows = pd.concat(
        [flows_to_bus, flows_from_bus, storage, duals],
        keys=["to_bus", "from_bus", "content", "duals"],
        axis=1,
    )

    my_flows.plot()
    plt.show()


if __name__ == "__main__":
    main()
