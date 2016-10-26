# -*- coding: utf-8 -*-
"""

"""
from collections import abc, UserList

from .. import network
from .options import BinaryFlow, Investment


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


def NodesFromCSV(file_nodes_flows, file_nodes_flows_sequences,
                 delimiter=',', additional_classes={},
                 additional_seq_attributes=[]):
    """ Creates nodes with their respective flows and sequences from
    a pre-defined CSV structure. An example has been provided in the
    development examples

    Parameters
    ----------
    file_nodes_flows : string with name of CSV file of nodes and flows
    file_nodes_flows_sequences : string with name of CSV file of sequences
    delimiter : delimiter of CSV file
    additional_classes : dictionary with additional classes to be used in csv
                         of type {'MyClass1': MyClass1, ...}
    additional_seq_attributes : list of strings with attributes that have to be
                                of type 'solph sequence'

    """

    import pandas as pd
    from .network import (Bus, Source, Sink, Flow, LinearTransformer, Storage)

    # dataframe creation and manipulation
    nodes_flows = pd.read_csv(file_nodes_flows, sep=delimiter)
    nodes_flows_seq = pd.read_csv(file_nodes_flows_sequences, sep=delimiter,
                                  header=None)
    nodes_flows_seq.dropna(axis=0, how='all', inplace=True)
    nodes_flows_seq.drop(0, axis=1, inplace=True)
    nodes_flows_seq = nodes_flows_seq.transpose()
    nodes_flows_seq.set_index([0, 1, 2, 3, 4], inplace=True)
    nodes_flows_seq.columns = range(0, len(nodes_flows_seq.columns))
    nodes_flows_seq = nodes_flows_seq.astype(float)

    # class dictionary for dynamic instantiation
    classes = {'Source': Source, 'Sink': Sink,
               'LinearTransformer': LinearTransformer,
               'Storage': Storage, 'Bus': Bus}
    classes.update(additional_classes)

    # attributes that have to be converted into a solph sequence
    seq_attributes = ['actual_value', 'min', 'max', 'positive_gradient',
                      'negative_gradient', 'variable_costs',
                      'capacity_loss', 'inflow_conversion_factor',
                      'outflow_conversion_factor', 'capacity_max',
                      'capacity_min'] + additional_seq_attributes

    # attributes of different classes
    flow_attrs = vars(Flow()).keys()
    bus_attrs = vars(Bus()).keys()

    # iteration over dataframe rows to create objects
    nodes = {}
    for i, r in nodes_flows.iterrows():

        # check if current line holds valid data or is just for visual purposes
        # e.g. a blank line or a line that contains data explanations
        if isinstance(r['class'], str) and r['class'] in classes.keys():

            # drop NaN values from series
            r = r.dropna()
            # save column labels and row values in dict
            row = dict(zip(r.index.values, r.values))

            # create node if not existent and set attributes
            # (attributes must be placed either in the first line or in all
            #  lines of multiple node entries (flows) in csv file)
            try:
                if row['class'] in classes.keys():
                    node = nodes.get(row['label'])
                    if node is None:
                        node = classes[row['class']](label=row['label'])
                # for the if check below we use all flow_attrs except
                # investment
                # because for storages investment needs to be set as a node
                # attribute (and a flow attribute)
                flow_attrs_ = [i for i in flow_attrs if i != 'investment']
                for attr in row.keys():
                    if (attr not in flow_attrs_ and
                       attr not in ('class', 'label', 'source', 'target',
                                    'conversion_factors')):
                            if row[attr] != 'seq':
                                if attr in seq_attributes:
                                    row[attr] = Sequence(float(row[attr]))
                                # again from investment storage the next lines
                                # are a little hacky as we need to create an
                                # solph.options.Investment() object
                                if (isinstance(node, Storage) and
                                        attr == 'investment'):
                                    setattr(node, attr, Investment())
                                    invest_attrs = vars(Investment()).keys()
                                    for iattr in invest_attrs:
                                        if iattr in row.keys() and row[attr]:
                                            setattr(node.investment,
                                                    iattr, row[iattr])
                                # for all 'normal' attributes
                                else:
                                    setattr(node, attr, row[attr])

                            else:
                                seq = nodes_flows_seq.loc[row['class'],
                                                          row['label'],
                                                          row['source'],
                                                          row['target'],
                                                          attr]
                                if attr in seq_attributes:
                                    seq = [i for i in seq]
                                    seq = Sequence(seq)
                                else:
                                    seq = [i for i in seq.values]
                                setattr(node, attr, seq)
            except:
                print('Error with node creation in line', i+2, 'in csv file.')
                print('Label:', row['label'])
                raise

            # create flow and set attributes
            try:
                flow = Flow()
                for attr in flow_attrs:
                    if attr in row.keys() and row[attr]:
                        if row[attr] != 'seq':
                            if attr in seq_attributes:
                                row[attr] = Sequence(float(row[attr]))
                            setattr(flow, attr, row[attr])
                        if row[attr] == 'seq':
                            seq = nodes_flows_seq.loc[row['class'],
                                                      row['label'],
                                                      row['source'],
                                                      row['target'],
                                                      attr]
                            if attr in seq_attributes:
                                seq = [i for i in seq]
                                seq = Sequence(seq)
                            else:
                                seq = [i for i in seq.values]
                            setattr(flow, attr, seq)
                        # this block is only for binary flows!
                        if attr == 'binary' and row[attr] is True:
                            # create binary object for flow
                            setattr(flow, attr, BinaryFlow())
                            binary_attrs = vars(BinaryFlow()).keys()
                            for battr in binary_attrs:
                                if battr in row.keys() and row[attr]:
                                    setattr(flow.binary, battr, row[battr])
                        # this block is only for investment flows!
                        if attr == 'investment' and row[attr] is True:
                            if isinstance(node, Storage):
                                # set the flows of the storage to Investment as
                                # without attributes, as costs etc are set at
                                # the node
                                setattr(flow, attr, Investment())
                            else:
                                # create binary object for flow
                                setattr(flow, attr, Investment())
                                invest_attrs = vars(Investment()).keys()
                                for iattr in invest_attrs:
                                    if iattr in row.keys() and row[attr]:
                                        setattr(flow.investment, iattr,
                                                row[iattr])
            except:
                print('Error with flow creation in line', i+2, 'in csv file.')
                print('Label:', row['label'])
                raise

            # create an input entry for the current line
            try:
                if row['label'] == row['target']:
                    if row['source'] not in nodes.keys():
                        nodes[row['source']] = Bus(label=row['source'])
                        for attr in bus_attrs:
                            if attr in row.keys() and row[attr] is not None:
                                setattr(nodes[row['source']], attr, row[attr])
                    inputs = {nodes[row['source']]: flow}
                else:
                    inputs = {}
            except:
                print('Error with input creation in line', i+2, 'in csv file.')
                print('Label:', row['label'])
                raise

            # create an output entry for the current line
            try:
                if row['label'] == row['source']:
                    if row['target'] not in nodes.keys():
                        nodes[row['target']] = Bus(label=row['target'])
                        for attr in bus_attrs:
                            if attr in row.keys() and row[attr] is not None:
                                setattr(nodes[row['target']], attr, row[attr])
                    outputs = {nodes[row['target']]: flow}
                else:
                    outputs = {}
            except:
                print('Error with output creation in line', i+2,
                      'in csv file.')
                print('Label:', row['label'])
                raise

            # create a conversion_factor entry for the current line
            try:
                if row['target'] and 'conversion_factors' in row:
                    conversion_factors = {nodes[row['target']]:
                                          Sequence(row['conversion_factors'])}
                else:
                    conversion_factors = {}
            except:
                print('Error with conversion factor creation in line', i+2,
                      'in csv file.')
                print('Label:', row['label'])
                raise

            # add node to dict and assign attributes depending on
            # if there are multiple lines per node or not
            try:
                for source, f in inputs.items():
                    network.flow[source, node] = f
                for target, f in outputs.items():
                    network.flow[node, target] = f
                if node.label in nodes.keys():
                    if not isinstance(node, Bus):
                        node.conversion_factors.update(conversion_factors)
                else:
                    if not isinstance(node, Bus):
                        node.conversion_factors = conversion_factors
                        nodes[node.label] = node
            except:
                print('Error adding node to dict in line', i+2, 'in csv file.')
                print('Label:', row['label'])
                raise

    return nodes
