# -*- coding: utf-8 -*-

"""
General description
-------------------

Something...


Installation requirements
-------------------------

This example requires oemof.solph (v0.5.x), install by:

    pip install oemof.solph[examples]


License
-------
`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_
"""
import pandas as pd
from oemof.network.network import Node

import oemof.solph as solph
from oemof.solph import processing
from oemof.solph import views

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

energy_system = solph.EnergySystem(
    timeindex=pd.date_range("1/1/2012", periods=4, freq="H")
)
Node.registry = energy_system

bel = solph.Bus(label="bel")

# There are a sink and a source, both creating a revenue (negative cost),
# so it would be optimal to use both at the same time. To suppress this,
# the constraint "limit_active_flow_count" is used.
# You might define any keyword (here "my_keyword") like:
# > Flow(nonconvex=solph.NonConvex(),
# >      my_keyword=True,
#        ...)
# But also any existing one (e.g. "emission_factor") can be used.

solph.components.Source(
    label="source1",
    outputs={
        bel: solph.Flow(
            nonconvex=solph.NonConvex(),
            nominal_value=210,
            variable_costs=[-1, -5, -1, -1],
            max=[1, 1, 1, 0],
            my_keyword=True,
        )
    },
)

# Note: The keyword is also defined when set to False.
solph.components.Sink(
    label="sink1",
    inputs={
        bel: solph.Flow(
            nonconvex=solph.NonConvex(),
            variable_costs=[-2, -1, -2, -2],
            nominal_value=250,
            max=[1, 1, 1, 0],
            my_keyword=False,
        )
    },
)

# Should be ignored because my_keyword is not defined.
solph.components.Source(
    label="source2",
    outputs={
        bel: solph.Flow(
            variable_costs=1,
            nonconvex=solph.NonConvex(),
            max=[1, 1, 1, 0],
            nominal_value=145,
        )
    },
)

# Should be ignored because it is not NonConvex.
solph.components.Sink(
    label="sink2",
    inputs={
        bel: solph.Flow(my_keyword=True, fix=[0, 1, 1, 0], nominal_value=130)
    },
)

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
