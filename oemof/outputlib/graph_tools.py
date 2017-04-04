# -*- coding: utf-8 -*-
"""Modules for creating and manipulating energy system graphs."""

import logging
try:
    import pylab as plt
except ImportError:
    logging.warning('Pylab could not be imported. Plotting will not work.')
try:
    import networkx as nx
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    logging.warning('Networkx could not be imported. Plotting will not work.')


def graph(energy_system, optimization_model, edge_labels=True,
          remove_nodes=None, remove_nodes_with_substrings=None,
          remove_edges=None, node_color='#AFAFAF', edge_color='#CFCFCF',
          plot=True, node_size=2000):
    """
    Create a `networkx.DiGraph` for the passed energy system and plot it.

    Parameters
    ----------
    energy_system : `oemof.solph.network.EnergySystem`

    optimization_model : `oemof.solph.models.OperationalModel`

    edge_labels: Boolean

    remove_nodes: list of string
        Nodes to be removed e.g. ['node1', node2')]

    remove_nodes_with_substrings: list of strings
        Nodes that contain substrings to be removed e.g. ['elec_', 'heat_')]

    remove_edges: list of string tuples
        Edges to be removed e.g. [('resource_gas', 'gas_balance')]

    node_color : string
        Hex color code oder matplotlib color for node color.

    edge_color
        Hex color code oder matplotlib color for edge color.

    plot : boolean
        Show matplotlib plot.

    node_size : integer
        Size of nodes.

    Notes
    -----
    Needs graphviz and networkx (>= v.1.11) to work properly.
    Tested on Ubuntu 16.04 x64.
    """
    # construct graph from nodes and flows
    G = nx.DiGraph()
    for n in energy_system.nodes:
        G.add_node(n.label)
    for s, t in optimization_model.flows:
        if optimization_model.flows[s, t].nominal_value is None:
            G.add_edge(s.label, t.label)
        else:
            G.add_edge(s.label, t.label,
                       weight=optimization_model.flows[s, t].nominal_value)

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

    # set drawing options
    options = {
     'prog': 'dot',
     'with_labels': True,
     'node_color': node_color,
     'edge_color': edge_color,
     'node_size': node_size
    }

    # draw graph
    pos = graphviz_layout(G)
    nx.draw(G, pos=pos, **options)

    # add edge labels for all edges
    if edge_labels is True:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)

    # show output
    if plot is True:
        plt.show()

    return G
