# -*- coding: utf-8 -*-

"""Modules for creating and manipulating energy system graphs."""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

import logging
import warnings

try:
    from matplotlib import pyplot as plt
except ImportError:
    plt = None

try:
    import networkx as nx
except ImportError:
    nx = None

try:
    import pygraphviz
except ImportError:
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

    optimization_model : `oemof.solph.models.Model`

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
        networkx graph layout, one of: neato, dot, twopi, circo, fdp, sfdp.

    Examples
    --------
    >>> import pandas as pd
    >>> from oemof.solph import (Bus, Sink, Transformer, Flow,
    ...                          Model, EnergySystem)
    >>> from oemof.outputlib import graph_tools as gt
    >>> datetimeindex = pd.date_range('1/1/2017', periods=3, freq='H')
    >>> es = EnergySystem(timeindex=datetimeindex)
    >>> b_gas = Bus(label='b_gas', balanced=False)
    >>> b_el = Bus(label='b_el')
    >>> demand_el = Sink(label='demand_el',
    ...                  inputs = {b_el: Flow(nominal_value=85,
    ...                            actual_value=[0.5, 0.25, 0.75],
    ...                            fixed=True)})
    >>> pp_gas = Transformer(label='pp_gas',
    ...                            inputs={b_gas: Flow()},
    ...                            outputs={b_el: Flow(nominal_value=41,
    ...                                                variable_costs=40)},
    ...                            conversion_factors={b_el: 0.5})
    >>> es.add(b_gas, b_el, demand_el, pp_gas)
    >>> om = Model(energysystem=es)
    >>> my_graph = gt.graph(energy_system=es, optimization_model=om,
    ...                     node_color={demand_el: 'r'}, plot=False)
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
    Tested on Ubuntu 16.04 x64 and solydxk (debian 9).
    """
    # construct graph from nodes and flows
    if nx is not None and pygraphviz is not None:
        grph = nx.DiGraph()

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
            arrows = False
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
        if plt:
            nx.draw(grph, pos=pos, **options)
        else:
            logging.error("Matplotlib could not be imported. "
                          "Plotting will not work. "
                          "Try 'pip install matplotlib'.")
            plot = False

        # add edge labels for all edges
        if edge_labels is True and plt:
            labels = nx.get_edge_attributes(grph, 'weight')
            nx.draw_networkx_edge_labels(grph, pos=pos, edge_labels=labels)

        # show output
        if plot is True:
            plt.show()

    else:
        if nx is None:
            logging.error(
                "Graph cannot be drawn due to the missing networkx package.")
        if pygraphviz is None:
            logging.error(
                "Graph cannot be drawn due to the missing pygraphviz package.")
        grph = None

    return grph


if __name__ == '__main__':
    import doctest
    doctest.testmod()
