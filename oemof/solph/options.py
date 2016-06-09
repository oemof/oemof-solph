# -*- coding: utf-8 -*-
"""

"""
from collections import abc, UserList


def Sequence(sequence_or_scalar):
    """ Tests if an object is sequence (except string) or scalar and returns
    a the original sequence if object is a sequence and a 'emulated' sequence
    object of class _Sequence if object is a scalar or string.

    Parameters
    ----------
    sequence_or_scalar : array-like or scalar (None, int, etc.)

    Examples
    --------
    >>> Sequence([1,2])
    [1, 2]

    >>> x = Sequence(10)
    >>> x[0]
    10

    >>> x[10]
    10
    >>> print(x)
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    """
    if (isinstance(sequence_or_scalar, abc.Iterable) and not
            isinstance(sequence_or_scalar, str)):
        return sequence_or_scalar
    else:
        return _Sequence(default=sequence_or_scalar)


class _Sequence(UserList):
    """ Emulates a list whose length is not known in advance.

    Parameters
    ----------
    source:
    default:


    Examples
    --------
    >>> s = _Sequence(default=42)
    >>> len(s)
    0
    >>> s[2]
    42
    >>> len(s)
    3
    >>> s[0] = 23
    >>> s
    [23, 42, 42]

    """
    def __init__(self, *args, **kwargs):
        self.default = kwargs["default"]
        super().__init__(*args)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            return self.data[key]

    def __setitem__(self, key, value):
        try:
            self.data[key] = value
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            self.data[key] = value


class Investment:
    """
    Parameters
    ----------
    maximum : float
        Maximum of the additional invested capacity
    ep_costs : float
        Equivalent periodical costs for the investment, if period is one
        year these costs are equal to the equivalent annual costs.

    """
    def __init__(self, maximum=float('+inf'), ep_costs=0):
        self.maximum = maximum
        self.ep_costs = ep_costs


class Discrete:
    """
    """
    def __init__(self, **kwargs):
        # super().__init__(self, **kwargs)
        self.start_costs = kwargs.get('start_costs')
        self.minimum_uptime = kwargs.get('minimum_uptime')
        self.minimum_downtime = kwargs.get('minimum_downtime')


def NodesFromCSV(file_nodes_flows, file_nodes_flows_sequences,
                 delimiter=','):
    """ Creates nodes with their respective flows and sequences from
    a pre-defined CSV structure. An example has been provided in the
    development examples

    Parameters
    ----------
    file_nodes_flows : string with name of CSV file of nodes and flows
    file_nodes_flows_sequences : string with name of CSV file of sequences
    delimiter : delimiter of CSV file

    """

    import math
    import pandas as pd
    from oemof.solph.network import (Bus, Source, Sink, Flow,
                                     LinearTransformer, Storage)
    from oemof.solph.options import Sequence

    nodes_flows = pd.read_csv(file_nodes_flows, sep=delimiter)
    nodes_flows_seq = pd.read_csv(file_nodes_flows_sequences, sep=delimiter,
                                  header=None)
    nodes_flows_seq.drop(0, axis=1, inplace=True)
    nodes_flows_seq = nodes_flows_seq.transpose()
    nodes_flows_seq.set_index([0, 1, 2, 3, 4], inplace=True)
    nodes_flows_seq.columns = range(0, len(nodes_flows_seq.columns))

    # iterate over dataframe rows and create objects
    nodes = {}
    for i, r in nodes_flows.iterrows():

        print('\n########################## ROW:', i)

        # save column labels and row values in dict
        row = dict(zip(r.index.values, r.values))


        ############################################## one flow per line
        # create flow and set flow attributes
        flow = Flow()
        flow_attrs = vars(Flow()).keys()
        for attr in flow_attrs:
            if attr in row.keys() and row[attr]:
                if row[attr] != 'seq':
                    setattr(flow, attr, Sequence(row[attr]))
                else:
                    seq = nodes_flows_seq.loc[row['class'],
                                              row['label'],
                                              row['source'],
                                              row['target'],
                                              attr]
                    seq = [i for i in seq.values]
                    setattr(flow, attr, seq)
        # create node and set node attributes
        # (attributes must be placed either in the first line or in all lines
        #  of multiple node entries (flows) in csv file)

        print('\nDICT BEFORE INSTANCE CREATION:')
        for k, v in nodes.items():
            print(k, v.label)

        ######################################### more than one node per line
        ############# thats why inputs and outputs  and conversion factors, ...
        ############# have to be appended and accessible attributes

        # to be filled dynamically from dataframe
        classes = {'Source': Source, 'Sink': Sink,
                   'LinearTransformer': LinearTransformer,
                   'Storage': Storage}
        if row['class'] in classes.keys():
            node = nodes.get(row['label'])
            if node is None:
                node = classes[row['class']](label=row['label'])

        print('\n node.label:', node.label)

        # delete node at start of iteration!?
        print('\nDICT AFTER LABEL ASSIGNMENT:')
        for k, v in nodes.items():
            print(k, v.label)

        for attr in row.keys():
            if (attr not in flow_attrs and
               attr not in ('class', 'label', 'source', 'target',
                            'conversion_factors')):
                    if row[attr] != 'seq':
                        setattr(node, attr, Sequence(row[attr]))
                    else:
                        seq = nodes_flows_seq.loc[row['class'],
                                                  row['label'],
                                                  row['source'],
                                                  row['target'],
                                                  attr]
                        seq = [i for i in seq.values]
                        setattr(node, attr, seq)

        # create an input entry for the current line
        if row['label'] == row['target']:
            if row['source'] not in nodes.keys():
                nodes[row['source']] = Bus(label=row['source'])
            inputs = {nodes[row['source']]: flow}
        else:
            inputs = {}

        # create an output entry for the current line
        if row['label'] == row['source']:
            if row['target'] not in nodes.keys():
                nodes[row['target']] = Bus(label=row['target'])
            outputs = {nodes[row['target']]: flow}
        else:
            outputs = {}

        # create a conversion_factor entry for the current line
        if row['target'] and not math.isnan(row['conversion_factors']):
            conversion_factors = {nodes[row['target']]:
                                  row['conversion_factors']}
        else:
            conversion_factors = {}

        # add node to dict and assign attributes depending on
        # if there are multiple lines per node or not
        for source, f in inputs.items():
            source.outputs[node] = f
        node.outputs.update(outputs)
        if node.label in nodes.keys():
            node.conversion_factors.update(conversion_factors)
        else:
            node.conversion_factors = conversion_factors
            nodes[node.label] = node
    for k, v in nodes.items():
        print(k, v.label)

    return nodes
