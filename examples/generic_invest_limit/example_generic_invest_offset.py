# -*- coding: utf-8 -*-
r"""
General description
-------------------
Example that shows how to use "Generic Investment Limit With Offset".

There are two supply chains. The energy systems looks like that:

.. code-block:: text

                  bus_a_0          bus_a_1
                   |                 |
    source_a_0 --->|---> trafo_a --->|--->demand_a
                                     |
                       source_a_1--->|
                                     |

                  bus_b_0          bus_b_1
                   |                 |
    source_b_0 --->|---> trafo_b --->|--->demand_b
                                     |
                       source_b_1--->|
                                     |
                                     v
                              generic_storage_b
                               /            \
                              |              |
                              v              v
                            bus_b_1        bus_b_1


Everything is identical - the costs for the sources, the demand, the efficiency
of the Converter. And both Converter have an investment at the output.
The source '\*_1' is in both cases very expensive, so that
a investment is probably done in the converter. The demand and the
maximum investment in Converter b1 is so set, that an investment in a generic
storage is beneficial to not use source b0.
Now, all investments share a third resource, which is called "space" in this
example. (This could be anything, and you could use as many additional
resources as you want.) And this resource is limited. In this case, every
converter and storage capacity unit, which might be installed, needs 2 space
for each installed capacity as well as an offset.
See what happens, have fun ;)

Code
----
Download source code: :download:`example_generic_invest.py </../examples/generic_invest_limit/example_generic_invest_offset.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/generic_invest_limit/example_generic_invest_offset.py
        :language: python
        :lines: 62-

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]

License
-------
Maximilian Hillen <maximilian.hillen@dlr.de>

`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""

import logging
import os

from PIL.ImageChops import offset

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

from oemof import solph


def main(optimize=True):

    data = [2, 2, 12, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    # create an energy system
    idx = solph.create_time_index(2020, number=len(data))
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=False)

    # Parameter: costs for the sources
    c_0 = 10
    c_1 = 100

    epc_invest = 50

    # commodity a
    bus_a_0 = solph.Bus(label="bus_a_0")
    bus_a_1 = solph.Bus(label="bus_a_1")
    es.add(bus_a_0, bus_a_1)

    es.add(
        solph.components.Source(
            label="source_a_0",
            outputs={bus_a_0: solph.Flow(variable_costs=c_0)},
        )
    )

    es.add(
        solph.components.Source(
            label="source_a_1",
            outputs={bus_a_1: solph.Flow(variable_costs=c_1 * 10000)},
        )
    )

    es.add(
        solph.components.Sink(
            label="demand_a",
            inputs={bus_a_1: solph.Flow(fix=data, nominal_capacity=1)},
        )
    )

    # commodity b
    bus_b_0 = solph.Bus(label="bus_b_0")
    bus_b_1 = solph.Bus(label="bus_b_1")
    es.add(bus_b_0, bus_b_1)
    es.add(
        solph.components.Source(
            label="source_b_0",
            outputs={bus_b_0: solph.Flow(variable_costs=c_0)},
        )
    )

    es.add(
        solph.components.Source(
            label="source_b_1",
            outputs={bus_b_1: solph.Flow(variable_costs=c_1 * 10000)},
        )
    )

    es.add(
        solph.components.Sink(
            label="demand_b",
            inputs={bus_b_1: solph.Flow(fix=data, nominal_capacity=1)},
        )
    )

    # Converter a
    es.add(
        solph.components.Converter(
            label="trafo_a",
            inputs={bus_a_0: solph.Flow()},
            outputs={
                bus_a_1: solph.Flow(
                    nominal_capacity=solph.Investment(
                        ep_costs=epc_invest,
                        custom_attributes={"space": {"cost": 1, "offset": 20}},
                        nonconvex=True,
                        maximum=20,
                    ),
                    custom_attributes={"space": 0.1},
                )
            },
            conversion_factors={bus_a_1: 1},
        )
    )

    # Converter b
    es.add(
        solph.components.Converter(
            label="trafo_b",
            inputs={bus_b_0: solph.Flow()},
            outputs={
                bus_b_1: solph.Flow(
                    nominal_capacity=solph.Investment(
                        ep_costs=epc_invest,
                        custom_attributes={"space": {"cost": 1}},
                        nonconvex=True,
                        maximum=10,
                    ),
                    custom_attributes={"space": 0.1},
                )
            },
        )
    )
    # Generic Storage b_0
    generic_storage_b_0 = solph.components.GenericStorage(
        label="generic_storage_b_0",
        inputs={bus_b_1: solph.Flow()},
        outputs={bus_b_1: solph.Flow()},
        inflow_conversion_factor=1,
        nominal_capacity = solph.Investment(
            ep_costs=epc_invest ,
            nonconvex=True,
            maximum=1,
            custom_attributes={"space": {"cost": 0.5, "offset":1 }},
        ),
        invest_relation_input_capacity = 0.5,
        invest_relation_output_capacity = 0.5,
    )

    es.add(generic_storage_b_0)

    # Generic Storage b_1
    generic_storage_b_1 = solph.components.GenericStorage(
            label="generic_storage_b_1",
            inputs={bus_b_1: solph.Flow()},
            outputs={bus_b_1: solph.Flow()},
            inflow_conversion_factor=1,
            nominal_capacity = solph.Investment(
                ep_costs=epc_invest *100,
                nonconvex=True,
                maximum=2,
                custom_attributes={"space": {"cost": 1, "offset":5 }},
                )
            ,
        )

    es.add(generic_storage_b_1)
    if optimize is False:
        return es

    # create an optimization problem and solve it
    om = solph.Model(es)

    # add constraint for generic investment limit
    om = solph.constraints.additional_total_limit(om, "space", limit=100)
    # export lp file
    filename = os.path.join(
        solph.helpers.extend_basic_path("lp_files"), "GenericInvest.lp"
    )
    logging.info("Store lp-file in {0}.".format(filename))
    om.write(filename, io_options={"symbolic_solver_labels": True})

    # solve model
    om.solve(solver="gurobi", solve_kwargs={"tee": True})

    # create result object
    results = solph.processing.results(om)

    bus1 = solph.views.node(results, "bus_a_1")["sequences"]
    bus2 = solph.views.node(results, "bus_b_1")["sequences"]

    # plot the time series (sequences) of a specific component/bus
    if plt is not None:
        bus1.plot(kind="line", drawstyle="steps-mid")
        plt.legend()
        plt.show()
        bus2.plot(kind="line", drawstyle="steps-mid")
        plt.legend()
        plt.show()

    space_used = om.total_limit_space()
    print("Space value: ", space_used)
    print(
        "Investment trafo_a: ",
        solph.views.node(results, "trafo_a")["scalars"][0],
    )
    print(
        "Investment trafo_b: ",
        solph.views.node(results, "trafo_b")["scalars"][0],
    )

    print(
        "Investment generic_storage_b_0: ",
        results[generic_storage_b_0, None]["scalars"]["total"],
    )

    print(
        "Investment generic_storage_b_1: ",
        results[generic_storage_b_1, None]["scalars"]["total"],
    )

if __name__ == "__main__":
    main()
