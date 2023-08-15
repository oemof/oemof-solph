"""
General description
-------------------

Cellular energy systems are proposed by the VDE-ETG. They are, as the name
implies, energy systems that consist of cells. Each cell can contain
multiple other cells. So there is a hierarchy between them.

However, the hierarchical levels are abstracted here and the structure is flat.

The connections between the cells are modelled as Links. Each connector Link
has two inputs (buses of the parent and child cell) and two outputs (buses of
the parent and child cell). Losses can be modelled by using the
`conversion_factors` of the Link class.

Code
----
Download source code: :download:`cellular.py </../examples/cellular/cellular.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/cellular/cellular.py
        :language: python
        :lines: 45-346

Installation requirements
-------------------------

This example requires at least oemof.solph (v0.5.1), install by:

.. code:: bash

    pip install oemof.solph[examples]

Licence
-------

Lennart Schürmann <lennart.schuermann@umsicht.fraunhofer.de>

`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_

"""


from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import processing
from oemof.solph import views


def main():
    ###########################################################################
    # define the cells of the cellular energy system
    ###########################################################################
    # define necessary parameters

    n_periods = 3

    daterange = create_time_index(year=2020, interval=1, number=n_periods)

    mysolver = "cbc"

    # create the energy cells
    es = EnergySystem(
        label="es", timeindex=daterange, infer_last_interval=False
    )
    ec_1 = EnergySystem(
        label="ec1", timeindex=daterange, infer_last_interval=False
    )
    ec_2 = EnergySystem(
        label="ec2", timeindex=daterange, infer_last_interval=False
    )
    ec_1_1 = EnergySystem(
        label="ec1_1", timeindex=daterange, infer_last_interval=False
    )
    ec_1_2 = EnergySystem(
        label="ec1_2", timeindex=daterange, infer_last_interval=False
    )
    ec_2_1 = EnergySystem(
        label="ec2_1", timeindex=daterange, infer_last_interval=False
    )
    ec_2_2 = EnergySystem(
        label="ec2_2", timeindex=daterange, infer_last_interval=False
    )

    demand_1 = [10] * n_periods
    demand_2 = [10] * n_periods
    demand_1_1 = [10] * n_periods
    demand_1_2 = [10] * n_periods
    demand_2_1 = [10] * n_periods
    demand_2_2 = [80] * n_periods

    pv_1 = [10] * n_periods
    pv_2 = [10] * n_periods
    pv_1_1 = [80] * n_periods
    pv_1_2 = [40] * n_periods
    pv_2_1 = [10] * n_periods
    pv_2_2 = [10] * n_periods

    bus_el_es = buses.Bus(label="bus_el_es")
    bus_el_ec_1 = buses.Bus(label="bus_el_ec_1")
    bus_el_ec_2 = buses.Bus(label="bus_el_ec_2")
    bus_el_ec_1_1 = buses.Bus(label="bus_el_ec_1_1")
    bus_el_ec_1_2 = buses.Bus(label="bus_el_ec_1_2")
    bus_el_ec_2_1 = buses.Bus(label="bus_el_ec_2_1")
    bus_el_ec_2_2 = buses.Bus(label="bus_el_ec_2_2")

    es.add(bus_el_es)
    ec_1.add(bus_el_ec_1)
    ec_2.add(bus_el_ec_2)
    ec_1_1.add(bus_el_ec_1_1)
    ec_1_2.add(bus_el_ec_1_2)
    ec_2_1.add(bus_el_ec_2_1)
    ec_2_2.add(bus_el_ec_2_2)

    sink_el_ec_1 = cmp.Sink(
        label="sink_el_ec_1",
        inputs={bus_el_ec_1: flows.Flow(fix=demand_1, nominal_value=1)},
    )
    sink_el_ec_2 = cmp.Sink(
        label="sink_el_ec_2",
        inputs={bus_el_ec_2: flows.Flow(fix=demand_2, nominal_value=1)},
    )
    sink_el_ec_1_1 = cmp.Sink(
        label="sink_el_ec_1_1",
        inputs={bus_el_ec_1_1: flows.Flow(fix=demand_1_1, nominal_value=1)},
    )
    sink_el_ec_1_2 = cmp.Sink(
        label="sink_el_ec_1_2",
        inputs={bus_el_ec_1_2: flows.Flow(fix=demand_1_2, nominal_value=1)},
    )
    sink_el_ec_2_1 = cmp.Sink(
        label="sink_el_ec_2_1",
        inputs={bus_el_ec_2_1: flows.Flow(fix=demand_2_1, nominal_value=1)},
    )
    sink_el_ec_2_2 = cmp.Sink(
        label="sink_el_ec_2_2",
        inputs={bus_el_ec_2_2: flows.Flow(fix=demand_2_2, nominal_value=1)},
    )

    ec_1.add(sink_el_ec_1)
    ec_2.add(sink_el_ec_2)
    ec_1_1.add(sink_el_ec_1_1)
    ec_1_2.add(sink_el_ec_1_2)
    ec_2_1.add(sink_el_ec_2_1)
    ec_2_2.add(sink_el_ec_2_2)

    source_el_ec_1 = cmp.Source(
        label="source_el_ec_1",
        outputs={
            bus_el_ec_1: flows.Flow(
                max=pv_1, nominal_value=1, variable_costs=5
            )
        },
    )
    source_el_ec_2 = cmp.Source(
        label="source_el_ec_2",
        outputs={
            bus_el_ec_2: flows.Flow(
                max=pv_2, nominal_value=1, variable_costs=5
            )
        },
    )
    source_el_ec_1_1 = cmp.Source(
        label="source_el_ec_1_1",
        outputs={
            bus_el_ec_1_1: flows.Flow(
                max=pv_1_1, nominal_value=1, variable_costs=10
            )
        },
    )
    source_el_ec_1_2 = cmp.Source(
        label="source_el_ec_1_2",
        outputs={
            bus_el_ec_1_2: flows.Flow(
                max=pv_1_2, nominal_value=1, variable_costs=1
            )
        },
    )
    source_el_ec_2_1 = cmp.Source(
        label="source_el_ec_2_1",
        outputs={
            bus_el_ec_2_1: flows.Flow(
                max=pv_2_1, nominal_value=1, variable_costs=5
            )
        },
    )
    source_el_ec_2_2 = cmp.Source(
        label="source_el_ec_2_2",
        outputs={
            bus_el_ec_2_2: flows.Flow(
                max=pv_2_2, nominal_value=1, variable_costs=5
            )
        },
    )

    ec_1.add(source_el_ec_1)
    ec_2.add(source_el_ec_2)
    ec_1_1.add(source_el_ec_1_1)
    ec_1_2.add(source_el_ec_1_2)
    ec_2_1.add(source_el_ec_2_1)
    ec_2_2.add(source_el_ec_2_2)

    connector_el_ec_1 = cmp.Link(
        label="connector_el_ec_1",
        inputs={
            bus_el_es: flows.Flow(),
            bus_el_ec_1: flows.Flow(),
        },
        outputs={
            bus_el_es: flows.Flow(),
            bus_el_ec_1: flows.Flow(),
        },
        conversion_factors={
            (bus_el_es, bus_el_ec_1): 1,
            (bus_el_ec_1, bus_el_es): 1,
        },
    )

    connector_el_ec_2 = cmp.Link(
        label="connector_el_ec_2",
        inputs={
            bus_el_es: flows.Flow(),
            bus_el_ec_2: flows.Flow(),
        },
        outputs={
            bus_el_es: flows.Flow(),
            bus_el_ec_2: flows.Flow(),
        },
        conversion_factors={
            (bus_el_es, bus_el_ec_2): 1,
            (bus_el_ec_2, bus_el_es): 1,
        },
    )

    connector_el_ec_1_1 = cmp.Link(
        label="connector_el_ec_1_1",
        inputs={
            bus_el_ec_1: flows.Flow(),
            bus_el_ec_1_1: flows.Flow(),
        },
        outputs={
            bus_el_ec_1: flows.Flow(),
            bus_el_ec_1_1: flows.Flow(),
        },
        conversion_factors={
            (bus_el_ec_1, bus_el_ec_1_1): 0.85,
            (bus_el_ec_1_1, bus_el_ec_1): 0.85,
        },
    )

    connector_el_ec_1_2 = cmp.Link(
        label="connector_el_ec_1_2",
        inputs={
            bus_el_ec_1: flows.Flow(),
            bus_el_ec_1_2: flows.Flow(),
        },
        outputs={
            bus_el_ec_1: flows.Flow(),
            bus_el_ec_1_2: flows.Flow(),
        },
        conversion_factors={
            (bus_el_ec_1, bus_el_ec_1_2): 1,
            (bus_el_ec_1_2, bus_el_ec_1): 1,
        },
    )

    connector_el_ec_2_1 = cmp.Link(
        label="connector_el_ec_2_1",
        inputs={
            bus_el_ec_2: flows.Flow(),
            bus_el_ec_2_1: flows.Flow(),
        },
        outputs={
            bus_el_ec_2: flows.Flow(),
            bus_el_ec_2_1: flows.Flow(),
        },
        conversion_factors={
            (bus_el_ec_2, bus_el_ec_2_1): 1,
            (bus_el_ec_2_1, bus_el_ec_2): 1,
        },
    )

    connector_el_ec_2_2 = cmp.Link(
        label="connector_el_ec_2_2",
        inputs={
            bus_el_ec_2: flows.Flow(),
            bus_el_ec_2_2: flows.Flow(),
        },
        outputs={
            bus_el_ec_2: flows.Flow(),
            bus_el_ec_2_2: flows.Flow(),
        },
        conversion_factors={
            (bus_el_ec_2, bus_el_ec_2_2): 1,
            (bus_el_ec_2_2, bus_el_ec_2): 1,
        },
    )

    # the connectors are all part of the overarching, the upmost es
    es.add(
        connector_el_ec_1,
        connector_el_ec_2,
        connector_el_ec_1_1,
        connector_el_ec_1_2,
        connector_el_ec_2_1,
        connector_el_ec_2_2,
    )

    cmodel = Model(
        energysystem=[es, ec_1, ec_2, ec_1_1, ec_1_2, ec_2_1, ec_2_2]
    )

    cmodel.solve(solver=mysolver)

    # evaluate and plot the results
    results = processing.results(cmodel)

    print(views.node(results, "bus_el_ec_1")["sequences"].iloc[0, :])
    msg = (
        "\nAs we can see, a flow of 70 kW is going from the bus_el_ec_1 "
        "to the connector_el_ec_1. It is composed of 30 kW from "
        "connector_el_ec_1_2 (and therefore ec_1_2) and 40 kW from "
        "connector_el_ec_1_1 (and therefore ec_1_1). Where does it go?\n"
    )
    print(msg)
    print(views.node(results, "bus_el_ec_2_2")["sequences"].iloc[0, :])
    msg = (
        "\nIt is going into bus_el_ec_2_2 (and therefore ec_2_2), to "
        "supply the demand.\n"
    )
    print(msg)

    msg = (
        "Here we can see that the conversion factors are in fact considered:\n"
    )
    print(msg)
    print(views.node(results, "connector_el_ec_1_1")["sequences"].iloc[0, :])


if __name__ == "__main__":
    main()
