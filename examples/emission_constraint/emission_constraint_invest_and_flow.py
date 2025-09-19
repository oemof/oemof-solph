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


We individualized the costs for the sources, the demand, the efficiency
of the Converter. And both Converter have an investment at the output.
The source '\*_1' is in both cases very expensive, so that
a investment is probably done in the converter. The demand and the
maximum investment in Converter b1 is so set, that an investment in a generic
storage is beneficial to not use source b0. Two generic storage are set, since
the storage b_0 is cheaper the preferred investment is there and afterward
in storage b_1.
Now, all investments share a third resource, which is called "emission" in this
example. (This could be anything, and you could use as many additional
resources as you want.) And this resource is limited. In this case, every
converter and storage capacity unit, which might be installed, needs emission
for each installed capacity as well as an offset. In addition to that the flow
through a converter has as well emission.
See what happens, have fun ;)

Code
----
Download source code: :download:`emission_constraint_invest.py </../examples/generic_invest_limit/emission_constraint_invest_and_flow.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/generic_invest_limit/emission_constraint_invest_and_flow.py
        :language: python
        :lines: 62-

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]

License
-------
Maximilian Hillen <maximilian.hillen@rwth-aachen.de>

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
    c_0 = 1000
    c_1 = 10000

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
            outputs={bus_a_1: solph.Flow(variable_costs=c_1)},
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
            outputs={bus_b_1: solph.Flow(variable_costs=c_1 )},
        )
    )

    es.add(
        solph.components.Sink(
            label="demand_b",
            inputs={bus_b_1: solph.Flow(fix=data, nominal_capacity=1)},
        )
    )

    # Converter a
    emission_conv_a_linear=1
    emission_conv_a_offset=20
    emission_conv_a_flow=0.1
    converter_a = solph.components.Converter(
            label="trafo_a",
            inputs={bus_a_0: solph.Flow()},
            outputs={
                bus_a_1: solph.Flow(
                    nominal_capacity=solph.Investment(
                        ep_costs=epc_invest,
                        custom_attributes={"emission": {"linear": emission_conv_a_linear, "offset": emission_conv_a_offset}},
                        nonconvex=True,
                        maximum=20,
                    ),
                    custom_attributes={"emission": emission_conv_a_flow},
                )
            },
            conversion_factors={bus_a_1: 1},
        )
    es.add(converter_a)

    # Converter b
    emission_conv_b_linear=1
    emission_conv_b_flow=0.1
    converter_b = solph.components.Converter(
            label="trafo_b",
            inputs={bus_b_0: solph.Flow()},
            outputs={
                bus_b_1: solph.Flow(
                    nominal_capacity=solph.Investment(
                        ep_costs=epc_invest,
                        custom_attributes={"emission": {"linear": emission_conv_b_linear}},
                        nonconvex=True,
                        maximum=10,
                    ),
                    custom_attributes={"emission": emission_conv_b_flow},
                )
            },
        )
    es.add(converter_b)

    # Generic Storage b_0
    emission_storage_b_0_linear=0.5
    emission_storage_b_0_offset=1
    generic_storage_b_0 = solph.components.GenericStorage(
        label="generic_storage_b_0",
        inputs={bus_b_1: solph.Flow()},
        outputs={bus_b_1: solph.Flow()},
        inflow_conversion_factor=1,
        nominal_capacity=solph.Investment(
            ep_costs=epc_invest,
            nonconvex=True,
            maximum=1,
            custom_attributes={"emission": {"linear": emission_storage_b_0_linear, "offset": emission_storage_b_0_offset}},
        ),
        invest_relation_input_capacity=0.5,
        invest_relation_output_capacity=0.5,
    )

    es.add(generic_storage_b_0)

    # Generic Storage b_1
    emission_storage_b_1_linear=1
    emission_storage_b_1_offset=5
    generic_storage_b_1 = solph.components.GenericStorage(
        label="generic_storage_b_1",
        inputs={bus_b_1: solph.Flow()},
        outputs={bus_b_1: solph.Flow()},
        inflow_conversion_factor=1,
        nominal_capacity=solph.Investment(
            ep_costs=epc_invest * 100,
            nonconvex=True,
            maximum=2,
            custom_attributes={"emission": {"linear": emission_storage_b_1_linear, "offset": emission_storage_b_1_offset}},
        ),
    )

    es.add(generic_storage_b_1)
    if optimize is False:
        return es

    # create an optimization problem and solve it
    om = solph.Model(es)

    # add constraint for generic investment limit
    om = solph.constraints.additional_total_limit(om, "emission", limit=100)
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

    emission_used = om.total_limit_emission()
    print("emission value: ", emission_used)
    print(
        "Investment trafo_a: ",
        solph.views.node(results, "trafo_a")["scalars"][0],
    )
    print(
        "Emission investment of trafo_a: ",
        solph.views.node(results, "trafo_a")["scalars"][0] * emission_conv_a_linear + emission_conv_a_offset,
    )
    print(
        "Emission flow through trafo_a: ",
        results[converter_a, bus_a_1]["sequences"]["flow"].sum() * emission_conv_a_flow,
    )

    print(
        "Investment trafo_b: ",
        solph.views.node(results, "trafo_b")["scalars"][0],
    )
    print(
        "Emission investment of trafo_b: ",
        solph.views.node(results, "trafo_b")["scalars"][0] * emission_conv_b_linear,
    )
    print(
        "Emission flow through trafo_b: ",
        results[converter_b, bus_b_1]["sequences"]["flow"].sum() * emission_conv_b_flow,
    )

    print(
        "Investment generic_storage_b_0: ",
        results[generic_storage_b_0, None]["scalars"]["total"],
    )
    print(
        "Emission investment generic_storage_b_0: ",
        results[generic_storage_b_0, None]["scalars"]["total"] * emission_storage_b_0_linear
        + results[generic_storage_b_0, None]["scalars"]["invest_status"] *emission_storage_b_0_offset,
    )

    print(
        "Investment generic_storage_b_1: ",
        results[generic_storage_b_1, None]["scalars"]["total"],
    )
    print(
        "Emission investment generic_storage_b_1: ",
        results[generic_storage_b_1, None]["scalars"]["total"] * emission_storage_b_1_linear
        + results[generic_storage_b_1, None]["scalars"]["invest_status"] *emission_storage_b_1_offset,
    )

if __name__ == "__main__":
    main()
