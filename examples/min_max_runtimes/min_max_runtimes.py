# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that illustrates how to model min and max runtimes.

Code
----
Download source code: :download:`min_max_runtimes.py </../examples/min_max_runtimes/min_max_runtimes.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/min_max_runtimes/min_max_runtimes.py
        :language: python
        :lines: 33-

Installation requirements
-------------------------

This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_

"""
from matplotlib import pyplot as plt

from oemof import solph


def main(optimize=True):
    # Create demand data
    demand_el = [0] * 24
    for n in [10, 15, 19]:
        demand_el[n] = 1

    # create an energy system
    idx = solph.create_time_index(2017, number=24)
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=False)

    # power bus and components
    bel = solph.Bus(label="bel")

    demand_el = solph.components.Sink(
        label="demand_el",
        inputs={bel: solph.Flow(fix=demand_el, nominal_capacity=10)},
    )

    dummy_el = solph.components.Sink(
        label="dummy_el", inputs={bel: solph.Flow(variable_costs=10)}
    )

    pp1 = solph.components.Source(
        label="plant_min_down_constraints",
        outputs={
            bel: solph.Flow(
                nominal_capacity=10,
                min=0.5,
                max=1.0,
                variable_costs=10,
                nonconvex=solph.NonConvex(
                    minimum_downtime=4, initial_status=0
                ),
            )
        },
    )

    pp2 = solph.components.Source(
        label="plant_min_up_constraints",
        outputs={
            bel: solph.Flow(
                nominal_capacity=10,
                min=0.5,
                max=1.0,
                variable_costs=10,
                nonconvex=solph.NonConvex(minimum_uptime=2, initial_status=1),
            )
        },
    )

    es.add(bel, dummy_el, demand_el, pp1, pp2)

    if optimize is False:
        return es

    # create an optimization problem and solve it
    om = solph.Model(es)

    # debugging
    # om.write('problem.lp', io_options={'symbolic_solver_labels': True})

    # solve model
    om.solve(solver="cbc", solve_kwargs={"tee": True})

    # create result object
    results = solph.processing.results(om)

    # plot data
    data = solph.views.node(results, "bel")["sequences"]
    data[[(("bel", "demand_el"), "flow"), (("bel", "dummy_el"), "flow")]] *= -1
    exclude = ["dummy_el", "status"]
    columns = [
        c
        for c in data.columns
        if not any(s in c[0] or s in c[1] for s in exclude)
    ]
    data = data[columns]
    fig, ax = plt.subplots(figsize=(10, 5))
    data.plot(ax=ax, kind="line", drawstyle="steps-post", grid=True, rot=0)
    ax.set_xlabel("Hour")
    ax.set_ylabel("P [MW]")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=1)
    fig.subplots_adjust(top=0.8)
    plt.show()


if __name__ == "__main__":
    main()
