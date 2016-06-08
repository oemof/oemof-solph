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

        # save column labels and row values in dict
        row = dict(zip(r.index.values, r.values))

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
        node = eval(row['class'])
        node.label = row['label']
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

        print('\n########################## ROW:', i)
        print('\nDICT BEFORE:')
        for k, v in nodes.items():
            print(k, v.label)

        if node.label in nodes.keys():
            node.inputs.update(inputs)
            node.outputs.update(outputs)
            node.conversion_factors.update(conversion_factors)
            print('\nAPPENDED:', node.label, row['label'])
            print('\nNODE:', node.label, row['label'])
            attrs = dir(node)
            print('--------------------')
            for i in attrs:
                if '_' not in i:
                    print(i, ':', getattr(node, str(i)))
        else:
            node.inputs = inputs
            node.outputs = outputs
            node.conversion_factors = conversion_factors
            nodes[node.label] = node
            print('\nNEW:', node.label, row['label'])
            print('\nNODE:', node.label, row['label'])
            attrs = dir(node)
            print('--------------------')
            for i in attrs:
                if '_' not in i:
                    print(i, ':', getattr(node, str(i)))

        print('\nDICT AFTER:')
        for k, v in nodes.items():
            print(k, v.label)

    for k, v in nodes.items():
        print(k, v.label)

    return nodes
