# -*- coding: utf-8 -*-

"""
General description:
---------------------
This script shows how use the custom component `solph.custom.Link` to build
a simple transshipment model.

Code
----
Download source code: :download:`transshipment.py </../examples/electrical/transshipment.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/electrical/transshipment.py
        :language: python
        :lines: 39-211

Installation requirements
-------------------------
This example requires oemof.solph (v0.5.x), install by:

.. code:: bash

    pip install oemof.solph[examples]

To draw the graph pygraphviz is required, installed by:

.. code:: bash

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

# oemof imports
from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import components as cmp
from oemof.solph import processing
from oemof.solph import views
from oemof.solph.components import Link

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
        Use nominal capacities of flow as edge label
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
        "prog": "dot",
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


def main(optimize=True):
    datetimeindex = pd.date_range("1/1/2017", periods=3, freq="h")

    es = EnergySystem(timeindex=datetimeindex, infer_last_interval=False)

    b_0 = Bus(label="b_0")

    b_1 = Bus(label="b_1")

    es.add(b_0, b_1)

    es.add(
        Link(
            label="line_0",
            inputs={b_0: Flow(), b_1: Flow()},
            outputs={
                b_1: Flow(nominal_capacity=Investment()),
                b_0: Flow(nominal_capacity=Investment()),
            },
            conversion_factors={(b_0, b_1): 0.95, (b_1, b_0): 0.9},
        )
    )

    es.add(
        cmp.Source(
            label="gen_0",
            outputs={b_0: Flow(nominal_capacity=100, variable_costs=50)},
        )
    )

    es.add(
        cmp.Source(
            label="gen_1",
            outputs={b_1: Flow(nominal_capacity=100, variable_costs=50)},
        )
    )

    es.add(
        cmp.Sink(
            label="load_0",
            inputs={b_0: Flow(nominal_capacity=150, fix=[0, 1])},
        )
    )

    es.add(
        cmp.Sink(
            label="load_1",
            inputs={b_1: Flow(nominal_capacity=150, fix=[1, 0])},
        )
    )

    if optimize is False:
        return es

    m = Model(energysystem=es)

    # m.write('transshipment.lp', io_options={'symbolic_solver_labels': True})

    m.solve(solver="cbc", solve_kwargs={"tee": True, "keepfiles": False})

    m.results()

    graph = create_nx_graph(es, m)

    if pygz is not None:
        draw_graph(
            graph,
            plot=True,
            layout="neato",
            node_size=3000,
            node_color={"b_0": "#cd3333", "b_1": "#7EC0EE", "b_2": "#eeac7e"},
        )

    results = processing.results(m)

    print(views.node(results, "gen_0"))
    print(views.node(results, "gen_1"))

    views.node(results, "line_0")["sequences"].plot(kind="bar")

    # look at constraints of Links in the pyomo model LinkBlock
    m.LinkBlock.pprint()


if __name__ == "__main__":
    main()
