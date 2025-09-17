# -*- coding: utf-8 -*-

"""
General description
-------------------

You should have grasped the result_object example to understand this one.

This is an example to show how the label attribute can be used with tuples to
manage the results of large energy system. Even though, the feature is
introduced in a small example it is made for large system.

In small energy system you normally address the node, you want your results
from, directly. In large systems you may want to group your results and collect
all power plants of a specific region or pv feed-in of all regions.

Therefore you can use named tuples as label. In a named tuple you need to
specify the fields:

>>> label = namedtuple('solph_label', ['region', 'tag1', 'tag2'])

>>> pv_label = label('region_1', 'renewable_source', 'pv')
>>> pp_gas_label = label('region_2', 'power_plant', 'natural_gas')
>>> demand_label = label('region_3', 'electricity', 'demand')

You always have to address all fields but you can use empty strings or None as
place holders.

>>> elec_bus = label('region_4', 'electricity', '')
>>> print(elec_bus)
solph_label(region='region_4', tag1='electricity', tag2='')

>>> elec_bus = label('region_4', 'electricity', None)
>>> print(elec_bus)
solph_label(region='region_4', tag1='electricity', tag2=None)

Now you can filter the results using the label or the instance:

>>> for key, value in results.items():  # Loop results (keys are tuples!)
...     if isinstance(key[0], comp.Sink) & (key[0].label.tag2 == 'demand'):
...         print("elec demand {0}: {1}".format(key[0].label.region,
...                                             value['sequences'].sum()))

elec demand region_1: 3456
elec demand region_2: 2467
...

In the example below a subclass is created to define ones own string output.
By default the output of a namedtuple is `field1=value1, field2=value2,...`:

>>> print(str(pv_label))
solph_label(region='region_1', tag1='renewable_source', tag2='pv')

With the subclass we created below the output is different, because we defined
our own string representation:

>>> new_pv_label = Label('region_1', 'renewable_source', 'pv')
>>> print(str(new_pv_label))
region_1_renewable_source_pv

You still will be able to get the original string using `repr`:

>>> print(repr(new_pv_label))
Label(tag1='region_1', tag2='renewable_source', tag3='pv')

This a helpful adaption for automatic plots etc..

Afterwards you can use `format` to define your own custom string.:

>>> print('{0}+{1}-{2}'.format(pv_label.region, pv_label.tag2, pv_label.tag1))
region_1+pv-renewable_source

Code
----
Download source code: :download:`tuple_as_label.py </../examples/tuple_as_labels/tuple_as_label.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/tuple_as_labels/tuple_as_label.py
        :language: python
        :lines: 106-

Data
----
Download data: :download:`tuple_as_label.csv </../examples/tuple_as_labels/tuple_as_label.csv>`

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_

"""

# ****************************************************************************
# ********** PART 1 - Define and optimise the energy system ******************
# ****************************************************************************

import logging
import os
import warnings
from collections import namedtuple

import pandas as pd
from oemof.tools import logger

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as comp
from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import helpers
from oemof.solph import processing


# Subclass of the named tuple with its own __str__ method.
# You can add as many tags as you like
# For tag1, tag2 you can define your own fields like region, fuel, type...
class Label(namedtuple("solph_label", ["tag1", "tag2", "tag3"])):
    __slots__ = ()

    def __str__(self):
        """The string is used within solph as an ID, so it hast to be unique"""
        return "_".join(map(str, self._asdict().values()))


def main(optimize=True):
    # Read data file
    home_path = os.path.dirname(__file__)
    filename = os.path.join(home_path, "tuple_as_label.csv")
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError:
        msg = "Data file not found: {0}. Only one value used!"
        warnings.warn(msg.format(filename), UserWarning)
        data = pd.DataFrame({"pv": [0.3], "wind": [0.6], "demand_el": [500]})

    solver = "cbc"  # 'glpk', 'gurobi',....
    debug = False  # Set number_of_timesteps to 3 to get a readable lp-file.
    number_of_time_steps = len(data)
    solver_verbose = False  # show/hide solver output

    # initiate the logger (see the API docs for more information)
    logger.define_logging(
        logfile="oemof_example.log",
        screen_level=logging.INFO,
        file_level=logging.WARNING,
    )

    logging.info("Initialize the energy system")
    energysystem = EnergySystem(
        timeindex=create_time_index(2012, number=number_of_time_steps),
        infer_last_interval=False,
    )

    ##########################################################################
    # Create oemof object
    ##########################################################################

    logging.info("Create oemof objects")

    # The bus objects were assigned to variables which makes it easier to
    # connect components to these buses (see below).

    # create natural gas bus
    bgas = buses.Bus(label=Label("bus", "gas", None))

    # create electricity bus
    bel = buses.Bus(label=Label("bus", "electricity", None))

    # adding the buses to the energy system
    energysystem.add(bgas, bel)

    # create excess component for the electricity bus to allow overproduction
    energysystem.add(
        comp.Sink(
            label=Label("sink", "electricity", "excess"),
            inputs={bel: flows.Flow()},
        )
    )

    # create source object representing the gas commodity (annual limit)
    energysystem.add(
        comp.Source(
            label=Label("commodity_source", "gas", "commodity"),
            outputs={bgas: flows.Flow()},
        )
    )

    # create fixed source object representing wind pow er plants
    energysystem.add(
        comp.Source(
            label=Label("ee_source", "electricity", "wind"),
            outputs={bel: flows.Flow(fix=data["wind"], nominal_capacity=2000)},
        )
    )

    # create fixed source object representing pv power plants
    energysystem.add(
        comp.Source(
            label=Label("ee_source", "electricity", "pv"),
            outputs={bel: flows.Flow(fix=data["pv"], nominal_capacity=3000)},
        )
    )

    # create simple sink object representing the electrical demand
    energysystem.add(
        comp.Sink(
            label=Label("sink", "electricity", "demand"),
            inputs={
                bel: flows.Flow(
                    fix=data["demand_el"] / 1000, nominal_capacity=1
                )
            },
        )
    )

    # create simple Converter object representing a gas power plant
    energysystem.add(
        comp.Converter(
            label=Label("power plant", "electricity", "gas"),
            inputs={bgas: flows.Flow()},
            outputs={
                bel: flows.Flow(nominal_capacity=10000, variable_costs=50)
            },
            conversion_factors={bel: 0.58},
        )
    )

    # create storage object representing a battery
    nominal_capacity = 5000
    storage = comp.GenericStorage(
        nominal_capacity=nominal_capacity,
        label=Label("storage", "electricity", "battery"),
        inputs={bel: flows.Flow(nominal_capacity=nominal_capacity / 6)},
        outputs={bel: flows.Flow(nominal_capacity=nominal_capacity / 6)},
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )

    energysystem.add(storage)

    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    if optimize is False:
        return energysystem

    logging.info("Optimise the energy system")

    # initialise the operational model
    model = Model(energysystem)

    # This is for debugging only. It is not(!) necessary to solve the problem
    # and should be set to False to save time and disc space in normal use. For
    # debugging the timesteps should be set to 3, to increase the readability
    # of the lp-file.
    if debug:
        filename = os.path.join(
            helpers.extend_basic_path("lp_files"), "tuple_as_label.lp"
        )
        logging.info("Store lp-file in {0}.".format(filename))
        model.write(filename, io_options={"symbolic_solver_labels": True})

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    model.receive_duals()
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    logging.info("Store the energy system with the results.")

    # The processing module of the outputlib can be used to extract the results
    # from the model transfer them into a homogeneous structured dictionary.

    results = processing.results(model)

    # ** Create a table with all sequences and store it into a file (csv/xlsx)
    flows_to_bus = pd.DataFrame(
        {
            str(k[0].label): v["sequences"]["flow"]
            for k, v in results.items()
            if k[1] is not None and k[1] == bel
        }
    )
    flows_from_bus = pd.DataFrame(
        {
            str(k[1].label): v["sequences"]["flow"]
            for k, v in results.items()
            if k[1] is not None and k[0] == bel
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

    # Store the table to csv or excel file:
    my_flows.to_csv(os.path.join(home_path, "my_flows.csv"))
    # my_flows.to_excel(os.path.join(home_path, "my_flows.xlsx"))
    print(my_flows.sum())

    # ********* Use your tuple labels to filter the components
    ee_sources = [
        str(f[0].label)
        for f in results.keys()
        if f[0].label.tag1 == "ee_source"
    ]
    print(ee_sources)

    # It is possible to filter components by the label tags and the class, so
    # the label concepts is a result of the postprocessing. If it is necessary
    # to get all components of a region, "region" should be a field of the
    # label. To filter only by tags you can add a tag named "class" with the
    # name of the class as value.
    electricity_buses = list(
        set(
            [
                str(f[0].label)
                for f in results.keys()
                if f[0].label.tag2 == "electricity"
                and isinstance(f[0], buses.Bus)
            ]
        )
    )
    print(electricity_buses)


if __name__ == "__main__":
    main()
