# -*- coding: utf-8 -*-
"""
Example that shows how to use "Offset-Invest".

Code
----
Download source code: :download:`minimal_invest.py </../examples/investment_with_minimal_invest/minimal_invest.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/investment_with_minimal_invest/minimal_invest.py
        :language: python
        :lines: 31-

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]

License
-------
Johannes Röder <https://www.uni-bremen.de/en/res/team/johannes-roeder-m-sc>

`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_

"""

import logging
import os

import pandas as pd
from matplotlib import pyplot as plt

from oemof import solph


def main(optimize=True):
    data = [0, 15, 30, 35, 20, 25, 27, 10, 5, 2, 15, 40, 20, 0, 0]

    # create an energy system
    idx = solph.create_time_index(2017, number=len(data))
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=False)

    bus_0 = solph.Bus(label="bus_0")
    bus_1 = solph.Bus(label="bus_1")
    es.add(bus_0, bus_1)

    c_0 = 10
    c_1 = 100

    es.add(
        solph.components.Source(
            label="source_0", outputs={bus_0: solph.Flow(variable_costs=c_0)}
        )
    )

    es.add(
        solph.components.Source(
            label="source_1", outputs={bus_1: solph.Flow(variable_costs=c_1)}
        )
    )

    es.add(
        solph.components.Sink(
            label="demand",
            inputs={bus_1: solph.Flow(fix=data, nominal_capacity=1)},
        )
    )

    # solph.Sink(label='excess_1', inputs={
    #     bus_1: solph.Flow()})

    # parameter
    p_install_min = 20
    p_install_max = 35000
    c_fix = 2000
    c_var = 180
    eta = 0.8

    # non offset invest
    trafo = solph.components.Converter(
        label="converter",
        inputs={bus_0: solph.Flow()},
        outputs={
            bus_1: solph.Flow(
                nominal_capacity=solph.Investment(
                    ep_costs=c_var,
                    maximum=p_install_max,
                    minimum=p_install_min,
                    # existing=10,
                    nonconvex=True,
                    offset=c_fix,
                ),
                # min=0.1,
                # fixed=True,
                # actual_value=[0.5, 0.5, 0.5, 0.5, 0.5],
            )
        },
        conversion_factors={bus_1: eta},
    )
    es.add(trafo)

    if optimize is False:
        return es

    # create an optimization problem and solve it
    om = solph.Model(es)

    # export lp file
    filename = os.path.join(
        solph.helpers.extend_basic_path("lp_files"), "OffsetInvestor.lp"
    )
    logging.info("Store lp-file in {0}.".format(filename))
    om.write(filename, io_options={"symbolic_solver_labels": True})

    # solve model
    om.solve(solver="cbc", solve_kwargs={"tee": True})

    # create result object
    results = solph.processing.results(om)

    bus1 = solph.views.node(results, "bus_1")["sequences"]

    # plot the time series (sequences) of a specific component/bus
    if plt is not None:
        bus1.plot(kind="line", drawstyle="steps-mid")
        plt.legend()
        plt.show()

    # Nachvollziehen der Berechnung
    # Kosten Invest
    p_invest = solph.views.node(results, "converter")["scalars"][
        (("converter", "bus_1"), "invest")
    ]
    invest_binary = solph.views.node(results, "converter")["scalars"][
        (("converter", "bus_1"), "invest_status")
    ]
    c_invest = p_invest * c_var + c_fix * invest_binary

    # costs analysis
    e_source_0 = solph.views.node(results, "source_0")["sequences"][
        (("source_0", "bus_0"), "flow")
    ].sum()
    c_source_0 = c_0 * e_source_0
    e_source_1 = solph.views.node(results, "source_1")["sequences"][
        (("source_1", "bus_1"), "flow")
    ].sum()
    c_source_1 = c_1 * e_source_1

    c_total = c_invest + c_source_0 + c_source_1

    es.results["meta"] = solph.processing.meta_results(om)
    objective = pd.DataFrame.from_dict(es.results["meta"]).at[
        "Lower bound", "objective"
    ]

    print("  objective:", objective)
    print("  berechnet:", c_total)

    print("")
    print("Max. zulässige Investleistung", p_install_max)
    print("Erforderlicher Mindest-Invest", p_install_min)
    print("Installierte Leistung:", p_invest)
    print(
        "Maximale Leistung - demand:",
        solph.views.node(results, "bus_1")["sequences"][
            (("bus_1", "demand"), "flow")
        ].max(),
    )
    print(
        "Maximale Leistung im Einsatz",
        solph.views.node(results, "converter")["sequences"][
            (("converter", "bus_1"), "flow")
        ].max(),
    )
    if p_invest > max(data):
        print("Anlage wurde überdimensioniert")


if __name__ == "__main__":
    main()
