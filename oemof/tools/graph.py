# -*- coding: utf-8 -*-

"""Modules for creating and manipulating energy system graphs."""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

import warnings
import networkx as nx

try:
    from matplotlib import pyplot as plt
except ImportError:
    plt = None

try:
    import pygraphviz
except ImportError:
    pygraphviz = None


def create_graph(energy_system=None, optimization_model=None, remove_nodes=None,
                 remove_nodes_with_substrings=None, remove_edges=None):
    """
    Create a `networkx.DiGraph` for the passed energy system and plot it.
    See http://networkx.readthedocs.io/en/latest/ for more information.

    Parameters
    ----------
    energy_system : `oemof.solph.network.EnergySystem`

    optimization_model : `oemof.solph.models.Model`

    remove_nodes: list of strings
        Nodes to be removed e.g. ['node1', node2')]

    remove_nodes_with_substrings: list of strings
        Nodes that contain substrings to be removed e.g. ['elec_', 'heat_')]

    remove_edges: list of string tuples
        Edges to be removed e.g. [('resource_gas', 'gas_balance')]

    Examples
    --------
    >>> import pandas as pd
    >>> from oemof.solph import (Bus, Sink, Transformer, Flow,
    ...                          Model, EnergySystem)
    >>> from oemof.tools import graph as grph
    >>> datetimeindex = pd.date_range('1/1/2017', periods=3, freq='H')
    >>> es = EnergySystem(timeindex=datetimeindex)
    >>> b_gas = Bus(label='b_gas', balanced=False)
    >>> bel1 = Bus(label='bel1')
    >>> bel2 = Bus(label='bel2')
    >>> demand_el = Sink(label='demand_el',
    ...                  inputs = {bel1: Flow(nominal_value=85,
    ...                            actual_value=[0.5, 0.25, 0.75],
    ...                            fixed=True)})
    >>> pp_gas = Transformer(label='pp_gas',
    ...                            inputs={b_gas: Flow()},
    ...                            outputs={bel1: Flow(nominal_value=41,
    ...                                                variable_costs=40)},
    ...                            conversion_factors={bel1: 0.5})
    >>> line_to2 = Transformer(label='line_to2',
    ...                        inputs={bel1: Flow()}, outputs={bel2: Flow()})
    >>> line_from2 = Transformer(label='line_from2',
    ...                          inputs={bel2: Flow()}, outputs={bel1: Flow()})
    >>> es.add(b_gas, bel1, demand_el, pp_gas, bel2, line_to2, line_from2)
    >>> om = Model(energysystem=es)
    >>> my_graph = grph.create_graph(optimization_model=om)
    >>> # export graph as .graphml for programs like Yed where it can be
    >>> # sorted and customized. this is especially helpful for large graphs
    >>> # import networkx as nx
    >>> # nx.write_graphml(my_graph, "my_graph.graphml")
    >>> [my_graph.has_node(n)
    ...  for n in ['b_gas', 'bel1', 'pp_gas', 'demand_el', 'tester']]
    [True, True, True, True, False]
    >>> list(nx.attracting_components(my_graph))
    [{'demand_el'}]
    >>> sorted(list(nx.strongly_connected_components(my_graph))[1])
    ['bel1', 'bel2', 'line_from2', 'line_to2']

    Notes
    -----
    Needs graphviz and networkx (>= v.1.11) to work properly.
    Tested on Ubuntu 16.04 x64 and solydxk (debian 9).
    """
    # construct graph from nodes and flows
    grph = nx.DiGraph()

    # Get energy_system from Model
    if energy_system is None:
        energy_system = optimization_model.es

    # add nodes
    for n in energy_system.nodes:
        grph.add_node(n.label)

    # add labeled flows on directed edge if an optimization_model has been
    # passed or undirected edge otherwise
    if optimization_model:
        for s, t in optimization_model.flows:
            if optimization_model.flows[s, t].nominal_value is None:
                grph.add_edge(s.label, t.label)
            else:
                weight = format(
                    optimization_model.flows[s, t].nominal_value, '.2f')
                grph.add_edge(s.label, t.label, weight=weight)
    else:
        for n in energy_system.nodes:
            for i in n.inputs.keys():
                grph.add_edge(n.label, i.label)

    # remove nodes and edges based on precise labels
    if remove_nodes is not None:
        grph.remove_nodes_from(remove_nodes)
    if remove_edges is not None:
        grph.remove_edges_from(remove_edges)

    # remove nodes based on substrings
    if remove_nodes_with_substrings is not None:
        for i in remove_nodes_with_substrings:
            remove_nodes = [v.label for v in energy_system.nodes
                            if i in v.label]
            grph.remove_nodes_from(remove_nodes)
    return grph


def draw_graph(grph, edge_labels=True, node_color='#AFAFAF',
               edge_color='#CFCFCF', plot=True, node_size=2000,
               with_labels=True, arrows=True, layout='neato'):
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
    warnings.warn(
        "\nThe function to plot the graph is deprecated and will be removed "
        "in oemof >= 0.3.0.")

    if plt is not None or pygraphviz is not None:

        if type(node_color) is dict:
            node_color = [node_color.get(g, '#AFAFAF') for g in grph.nodes()]

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
        pos = nx.drawing.nx_agraph.graphviz_layout(grph, prog=layout)

        nx.draw(grph, pos=pos, **options)

        # add edge labels for all edges
        if edge_labels is True and plt:
            labels = nx.get_edge_attributes(grph, 'weight')
            nx.draw_networkx_edge_labels(grph, pos=pos, edge_labels=labels)

        # show output
        if plot is True:
            plt.show()

    else:
        if plt is None:
            warnings.warn(
                "Graph cannot be drawn due to the missing matplotlib package.")
        if pygraphviz is None:
            warnings.warn(
                "Graph cannot be drawn due to the missing pygraphviz package.")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
