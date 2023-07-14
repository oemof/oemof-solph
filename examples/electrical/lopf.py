# -*- coding: utf-8 -*-

"""
General description
-------------------
This script shows how to do a linear optimal powerflow (lopf) calculation
based on custom oemof components. The example is based on the PyPSA
simple lopf example.

Note: As oemof currently does not support models with one timesteps, therefore
there are two.

Code
----
Download source code: :download:`lopf.py </../examples/electrical/lopf.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/electrical/lopf.py
        :language: python
        :lines: 40-217

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

    pip install oemof.solph[examples]

To draw the graph pygraphviz is required, installed by:

    pip install pygraphviz

License
-------
Simon Hilpert - 12.12.2017 - simon.hilpert@uni-flensburg.de

`MIT license <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_

"""
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from oemof.network.graph import create_nx_graph
from oemof.solph import EnergySystem, Investment, Model, processing, views
from oemof.solph.components import Sink, Source
from oemof.solph.buses.experimental import ElectricalBus
from oemof.solph.flows.experimental import ElectricalLine
from oemof.solph.flows import Flow

try:
    import pygraphviz as pygz
except ModuleNotFoundError:
    pygz = None


def draw_graph(
    grph,
    edge_labels=True,
    node_color="#AFAFAF",
    edge_color="#CFCFCF",
    plot=True,
    node_size=2000,
    with_labels=True,
    arrows=True,
    layout="neato",
):
    """
    Draw a graph. This function will be removed in future versions.

    Parameters
    ----------
    grph : networkxGraph
        A graph to draw.
    edge_labels : boolean
        Use nominal values of flow as edge label
    node_color : dict or string
        Hex color code oder matplotlib color for each node. If string, all
        colors are the same.

    edge_color : string
        Hex color code oder matplotlib color for edge color.

    plot : boolean
        Show matplotlib plot.

    node_size : integer
        Size of nodes.

    with_labels : boolean
        Draw node labels.

    arrows : boolean
        Draw arrows on directed edges. Works only if an optimization_model has
        been passed.
    layout : string
        networkx graph layout, one of: neato, dot, twopi, circo, fdp, sfdp.
    """
    if isinstance(node_color, dict):
        node_color = [node_color.get(g, "#AFAFAF") for g in grph.nodes()]

    # set drawing options
    options = {
        # "prog": "dot",
        "with_labels": with_labels,
        "node_color": node_color,
        "edge_color": edge_color,
        "node_size": node_size,
        "arrows": arrows,
    }

    # draw graph
    pos = nx.drawing.nx_agraph.graphviz_layout(grph, prog=layout)

    nx.draw(grph, pos=pos, **options)

    # add edge labels for all edges
    if edge_labels is True and plt:
        labels = nx.get_edge_attributes(grph, "weight")
        nx.draw_networkx_edge_labels(grph, pos=pos, edge_labels=labels)

    # show output
    if plot is True:
        plt.show()


def main():
    datetimeindex = pd.date_range("1/1/2017", periods=2, freq="H")

    es = EnergySystem(timeindex=datetimeindex)

    b_el0 = ElectricalBus(label="b_0", v_min=-1, v_max=1)

    b_el1 = ElectricalBus(label="b_1", v_min=-1, v_max=1)

    b_el2 = ElectricalBus(label="b_2", v_min=-1, v_max=1)

    es.add(b_el0, b_el1, b_el2)

    es.add(
        ElectricalLine(
            input=b_el0,
            output=b_el1,
            reactance=0.0001,
            investment=Investment(ep_costs=10),
            min=-1,
            max=1,
        )
    )

    es.add(
        ElectricalLine(
            input=b_el1,
            output=b_el2,
            reactance=0.0001,
            nominal_value=60,
            min=-1,
            max=1,
        )
    )

    es.add(
        ElectricalLine(
            input=b_el2,
            output=b_el0,
            reactance=0.0001,
            nominal_value=60,
            min=-1,
            max=1,
        )
    )

    es.add(
        Source(
            label="gen_0",
            outputs={b_el0: Flow(nominal_value=100, variable_costs=50)},
        )
    )

    es.add(
        Source(
            label="gen_1",
            outputs={b_el1: Flow(nominal_value=100, variable_costs=25)},
        )
    )

    es.add(
        Sink(label="load", inputs={b_el2: Flow(nominal_value=100, fix=[1, 1])})
    )

    m = Model(energysystem=es)

    # m.write('lopf.lp', io_options={'symbolic_solver_labels': True})

    m.solve(solver="cbc", solve_kwargs={"tee": True, "keepfiles": False})

    m.results()

    graph = create_nx_graph(es)

    if pygz is not None:
        draw_graph(
            graph,
            plot=True,
            layout="neato",
            node_size=3000,
            node_color={"b_0": "#cd3333", "b_1": "#7EC0EE", "b_2": "#eeac7e"},
        )

    results = processing.results(m)

    print(views.node(results, "gen_0")["sequences"])
    print(views.node(results, "gen_1")["sequences"])
    print(views.node(results, "load")["sequences"])


if __name__ == "__main__":
    main()
