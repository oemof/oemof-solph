# -*- coding: utf-8 -*-

"""Example for solph model with mutiple capacity periods.

SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import numpy as np

from oemof import solph

def main():
    es = solph.EnergySystem(
        timeindex=np.linspace(start=0, stop=12, num=13),
        investment_times=[0, 4, 12],
    )

    bus = solph.Bus(label="bus")

    source = solph.components.Source(
        label="source",
        outputs={
            bus: solph.Flow(
                nominal_capacity=solph.Investment(maximum=4, ep_costs=0.1),
            ),
        },
    )
    sink = solph.components.Sink(
        label="sink",
        inputs={
            bus: solph.Flow(
                nominal_capacity=[4, 3],
                variable_costs=-2,
            ),
        },
    )
    es.add(bus, sink, source)

    model = solph.Model(es)

    results = model.solve()

    print(results["flow"])
    print(results["nominal_capacity"])
    print(results["objective"])


if __name__ == "__main__":
    main()
