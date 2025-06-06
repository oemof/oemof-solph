# -*- coding: utf-8 -*-

"""
General description
-------------------

Example that shows how to use "flow_count_limit".

This example shows a case where only one out of two Flows can be
active at a time. Another typical usage might be a connection to a
grid where energy can only flow into one direction or a storage that
cannot be charged and discharged at the same time.

Note that binary variables are computationally expensive. Thus, you
might want to avoid using this constraint if you do not really need it.

Code
----
Download source code: :download:`flow_count_limit.py </../examples/flow_count_limit/flow_count_limit.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/flow_count_limit/flow_count_limit.py
        :language: python
        :lines: 39-159

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]

License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""
import pandas as pd

import oemof.solph as solph
from oemof.solph import processing
from oemof.solph import views

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def main(optimize=True):
    energy_system = solph.EnergySystem(
        timeindex=pd.date_range("1/1/2012", periods=4, freq="h")
    )

    bel = solph.Bus(label="bel")
    energy_system.add(bel)

    # There are a sink and a source, both creating a revenue (negative cost),
    # so it would be optimal to use both at the same time. To suppress this,
    # the constraint "limit_active_flow_count" is used.
    # You might define any keyword (here "my_keyword") like:
    # > Flow(nonconvex=solph.NonConvex(),
    # >      my_keyword=True,
    #        ...)
    # But also any existing one (e.g. "emission_factor") can be used.

    energy_system.add(
        solph.components.Source(
            label="source1",
            outputs={
                bel: solph.Flow(
                    nonconvex=solph.NonConvex(),
                    nominal_capacity=210,
                    variable_costs=[-1, -5, -1, -1],
                    max=[1, 1, 1, 0],
                    custom_attributes={"my_keyword": True},
                )
            },
        )
    )

    # Note: The keyword is also defined when set to False.
    energy_system.add(
        solph.components.Sink(
            label="sink1",
            inputs={
                bel: solph.Flow(
                    nonconvex=solph.NonConvex(),
                    variable_costs=[-2, -1, -2, -2],
                    nominal_capacity=250,
                    max=[1, 1, 1, 0],
                    custom_attributes={"my_keyword": False},
                )
            },
        )
    )

    # Should be ignored because my_keyword is not defined.
    energy_system.add(
        solph.components.Source(
            label="source2",
            outputs={
                bel: solph.Flow(
                    variable_costs=1,
                    nonconvex=solph.NonConvex(),
                    max=[1, 1, 1, 0],
                    nominal_capacity=145,
                )
            },
        )
    )

    # Should be ignored because it is not NonConvex.
    energy_system.add(
        solph.components.Sink(
            label="sink2",
            inputs={
                bel: solph.Flow(
                    custom_attributes={"my_keyword": True},
                    fix=[0, 1, 1, 0],
                    nominal_capacity=130,
                )
            },
        )
    )

    if optimize is False:
        return energy_system

    model = solph.Model(energy_system)

    # only one of the two flows may be active at a time
    solph.constraints.limit_active_flow_count_by_keyword(
        model, "my_keyword", lower_limit=0, upper_limit=1
    )

    model.solve()

    results = processing.results(model)

    if plt is not None:
        data = views.node(results, "bel")["sequences"]
        ax = data.plot(kind="line", grid=True)
        ax.set_xlabel("Time (h)")
        ax.set_ylabel("P (MW)")

        plt.figure()
        ax = plt.gca()
        plt.plot(
            results[("my_keyword", "my_keyword")]["sequences"],
            label="my_keyword_count",
        )
        ax.set_xlabel("Time (h)")
        ax.set_ylabel("Count (1)")
        plt.grid()
        plt.legend()
        plt.show()


if __name__ == "__main__":
    main()
