# -*- coding: utf-8 -*-
"""Modules for creating and manipulating energy system graphs."""

import logging
import re
import warnings

try:
    from matplotlib import pyplot as plt
except ImportError:
    logging.warning('Matplotlib could not be imported.',
                    ' Plotting will not work.')
try:
    import networkx as nx
    from networkx.drawing.nx_agraph import graphviz_layout
    import pygraphviz
except ImportError:
    nx = None
    graphviz_layout = None
    pygraphviz = None


warnings.filterwarnings("ignore")  # deactivate matplotlib warnings in networkx


def graph(energy_system, optimization_model=None, edge_labels=True,
          remove_nodes=None, remove_nodes_with_substrings=None,
          remove_edges=None, node_color='#AFAFAF', edge_color='#CFCFCF',
          plot=True, node_size=2000, with_labels=True, arrows=True,
          layout='neato'):
    """
    Create a `networkx.DiGraph` for the passed energy system and plot it.
    See http://networkx.readthedocs.io/en/latest/ for more information.

    Parameters
    ----------
    energy_system : `oemof.solph.network.EnergySystem`

    optimization_model : `oemof.solph.models.OperationalModel`

    edge_labels: boolean
        Use nominal values of flow as edge label

    remove_nodes: list of strings
        Nodes to be removed e.g. ['node1', node2')]

    remove_nodes_with_substrings: list of strings
        Nodes that contain substrings to be removed e.g. ['elec_', 'heat_')]

    remove_edges: list of string tuples
        Edges to be removed e.g. [('resource_gas', 'gas_balance')]

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
        networkx graph layout, one of: neato, dot, twopi, circo, fdp, nop, wc,
        acyclic, gvpr, gvcolor, ccomps, sccmap, tred, sfdp.

    Examples
    --------
    >>> import pandas as pd
    >>> from oemof.solph import (Bus, Sink, LinearTransformer, Flow,
    ...                          OperationalModel, EnergySystem)
    >>> datetimeindex = pd.date_range('1/1/2017', periods=3, freq='H')
    >>> es = EnergySystem(timeindex=datetimeindex)
    >>> b_gas = Bus(label='b_gas', balanced=False)
    >>> b_el = Bus(label='b_el')
    >>> demand = Sink(label='demand_el',
    ...               inputs = {b_el: Flow(nominal_value=85,
    ...                         actual_value=[0.5, 0.25, 0.75],
    ...                         fixed=True)})
    >>> pp_gas = LinearTransformer(label='pp_gas',
    ...                            inputs={b_gas: Flow()},
    ...                            outputs={b_el: Flow(nominal_value=41,
    ...                                                variable_costs=40)},
    ...                            conversion_factors={b_el: 0.5})
    >>> om = OperationalModel(es=es)
    >>> my_graph = graph(energy_system=es, optimization_model=om,
                         node_color={demand: 'r'}, plot=False)
    >>> # export graph as .graphml for programs like Yed where it can be
    >>> # sorted and customized. this is especially helpful for large graphs
    >>> # import networkx as nx
    >>> # nx.write_graphml(my_graph, "my_graph.graphml")
    >>> [my_graph.has_node(n)
    ...  for n in ['b_gas', 'b_el', 'pp_gas', 'demand_el']]
    [True, True, True, True]

    Notes
    -----
    Needs graphviz and networkx (>= v.1.11) to work properly.
    Tested on Ubuntu 16.04 x64.
    """
    # construct graph from nodes and flows
    if nx:
        G = nx.DiGraph()

        # add nodes
        for n in energy_system.nodes:
            G.add_node(n.label)

        # add labeled flows on directed edge if an optimization_model has been
        # passed or undirected edge otherwise
        if optimization_model:
            for s, t in optimization_model.flows:
                if optimization_model.flows[s, t].nominal_value is None:
                    G.add_edge(s.label, t.label)
                else:
                    weight = optimization_model.flows[s, t].nominal_value
                    G.add_edge(s.label, t.label, weight=weight)
        else:
            arrows = False
            for n in energy_system.nodes:
                for i in n.inputs.keys():
                    G.add_edge(n.label, i.label)

        # remove nodes and edges based on precise labels
        if remove_nodes is not None:
            G.remove_nodes_from(remove_nodes)
        if remove_edges is not None:
            G.remove_edges_from(remove_edges)

        # remove nodes based on substrings
        if remove_nodes_with_substrings is not None:
            for i in remove_nodes_with_substrings:
                remove_nodes = [v.label for v in energy_system.nodes
                                if i in v.label]
                G.remove_nodes_from(remove_nodes)

        if type(node_color) is dict:
            node_color = [node_color.get(g, '#AFAFAF') for g in G.nodes()]

        # set drawing options
        options = {
         'prog': 'dot',
         'with_labels': with_labels,
         'node_color': node_color,
         'edge_color': edge_color,
         'node_size': node_size,
         'arrows': arrows
        }

        # draw graph
        pos = graphviz_layout(G, prog=layout)
        nx.draw(G, pos=pos, **options)

        # add edge labels for all edges
        if edge_labels is True:
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)

        # show output
        if plot is True:
            plt.show()

    else:
        logging.warning("Graph cannot be drawn due to missing packages.")
        G = None

    return G


for o in [graph]:
    if (((nx is None) or (graphviz_layout is None) or (pygraphviz is None)) and
            (getattr(o, "__doc__") is not None)):
        o.__doc__ = re.sub(r"((^|\n)\s*)>>>", r"\1>>",
                           re.sub(r"((^|\n)\s*)\.\.\.", r"\1..", o.__doc__))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
