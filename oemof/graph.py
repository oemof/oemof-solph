# -*- coding: utf-8 -*-

"""Modules for creating and analysing energy system graphs.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/graph.py

SPDX-License-Identifier: MIT
"""

import networkx as nx


def create_nx_graph(energy_system=None, remove_nodes=None, filename=None,
                    remove_nodes_with_substrings=None, remove_edges=None):
    """
    Create a `networkx.DiGraph` for the passed energy system and plot it.
    See http://networkx.readthedocs.io/en/latest/ for more information.

    Parameters
    ----------
    energy_system : `oemof.solph.network.EnergySystem`

    filename : str
        Absolute filename (with path) to write your graph in the graphml
        format. If no filename is given no file will be written.

    remove_nodes: list of strings
        Nodes to be removed e.g. ['node1', node2')]

    remove_nodes_with_substrings: list of strings
        Nodes that contain substrings to be removed e.g. ['elec', 'heat')]

    remove_edges: list of string tuples
        Edges to be removed e.g. [('resource_gas', 'gas_balance')]

    Examples
    --------
    >>> import os
    >>> import pandas as pd
    >>> from oemof.solph import (Bus, Sink, Transformer, Flow, EnergySystem)
    >>> import oemof.graph as grph
    >>> datetimeindex = pd.date_range('1/1/2017', periods=3, freq='H')
    >>> es = EnergySystem(timeindex=datetimeindex)
    >>> b_gas = Bus(label='b_gas', balanced=False)
    >>> bel1 = Bus(label='bel1')
    >>> bel2 = Bus(label='bel2')
    >>> demand_el = Sink(label='demand_el',
    ...                  inputs = {bel1: Flow(nominal_value=85,
    ...                            actual_value=[0.5, 0.25, 0.75],
    ...                            fixed=True)})
    >>> pp_gas = Transformer(label=('pp', 'gas'),
    ...                            inputs={b_gas: Flow()},
    ...                            outputs={bel1: Flow(nominal_value=41,
    ...                                                variable_costs=40)},
    ...                            conversion_factors={bel1: 0.5})
    >>> line_to2 = Transformer(label='line_to2',
    ...                        inputs={bel1: Flow()}, outputs={bel2: Flow()})
    >>> line_from2 = Transformer(label='line_from2',
    ...                          inputs={bel2: Flow()}, outputs={bel1: Flow()})
    >>> es.add(b_gas, bel1, demand_el, pp_gas, bel2, line_to2, line_from2)
    >>> my_graph = grph.create_nx_graph(es)
    >>> # export graph as .graphml for programs like Yed where it can be
    >>> # sorted and customized. this is especially helpful for large graphs
    >>> # grph.create_nx_graph(es, filename="my_graph.graphml")
    >>> [my_graph.has_node(n)
    ...  for n in ['b_gas', 'bel1', "('pp', 'gas')", 'demand_el', 'tester']]
    [True, True, True, True, False]
    >>> list(nx.attracting_components(my_graph))
    [{'demand_el'}]
    >>> sorted(list(nx.strongly_connected_components(my_graph))[1])
    ['bel1', 'bel2', 'line_from2', 'line_to2']
    >>> new_graph = grph.create_nx_graph(energy_system=es,
    ...                                  remove_nodes_with_substrings=['b_'],
    ...                                  remove_nodes=["('pp', 'gas')"],
    ...                                  remove_edges=[('bel2', 'line_from2')],
    ...                                  filename='test_graph')
    >>> [new_graph.has_node(n)
    ...  for n in ['b_gas', 'bel1', "('pp', 'gas')", 'demand_el', 'tester']]
    [False, True, False, True, False]
    >>> my_graph.has_edge("('pp', 'gas')", 'bel1')
    True
    >>> new_graph.has_edge('bel2', 'line_from2')
    False
    >>> os.remove('test_graph.graphml')

    Notes
    -----
    Needs graphviz and networkx (>= v.1.11) to work properly.
    Tested on Ubuntu 16.04 x64 and solydxk (debian 9).
    """
    # construct graph from nodes and flows
    grph = nx.DiGraph()

    # add nodes
    for n in energy_system.nodes:
        grph.add_node(str(n.label), label=str(n.label))

    # add labeled flows on directed edge if an optimization_model has been
    # passed or undirected edge otherwise
    for n in energy_system.nodes:
        for i in n.inputs.keys():
            weight = getattr(energy_system.flows()[(i, n)],
                             'nominal_value', None)
            if weight is None:
                grph.add_edge(str(i.label), str(n.label))
            else:
                grph.add_edge(str(i.label), str(n.label),
                              weigth=format(weight, '.2f'))

    # remove nodes and edges based on precise labels
    if remove_nodes is not None:
        grph.remove_nodes_from(remove_nodes)
    if remove_edges is not None:
        grph.remove_edges_from(remove_edges)

    # remove nodes based on substrings
    if remove_nodes_with_substrings is not None:
        for i in remove_nodes_with_substrings:
            remove_nodes = [str(v.label) for v in energy_system.nodes
                            if i in str(v.label)]
            grph.remove_nodes_from(remove_nodes)

    if filename is not None:
        if filename[-8:] != '.graphml':
            filename = filename + '.graphml'
        nx.write_graphml(grph, filename)

    return grph
