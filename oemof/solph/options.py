# -*- coding: utf-8 -*-
"""Optional classes to be added to a network class.
"""


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
    Parameters
    ----------
    startup_costs : numeric
        Costs associated with a start of the flow (representing a unit).
    shutdown_costs : numeric
        Costs associated with the shutdown of the flow (representing a unti).
    minimum_uptime : numeric
        Minimum time that a flow must be greate then its minimum flow after
        startup.
    minimum_downtime : numeric
        Minimum time a flow is forced to zero after shutting down.
    initial_status : numeric (0 or 1)
        Integer value indicating the status of the flow in the first timestep
        (0 = off, 1 = on).
    """
    def __init__(self, **kwargs):
        # super().__init__(self, **kwargs)
        self.startup_costs = kwargs.get('startup_costs')
        self.shutdown_costs = kwargs.get('shutdown_costs')
        self.minimum_uptime = kwargs.get('minimum_uptime')
        self.minimum_downtime = kwargs.get('minimum_downtime')
        self.initial_status = kwargs.get('initial_status', 0)


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
    # TODO : Find a nice way how to add 'additional' arguments for extension
    #        e.g. additional_seq_attributes, additional_classes

    import pandas as pd
    from oemof.solph.network import (Bus, Source, Sink, Flow,
                                     LinearTransformer, Storage)
    from oemof.solph.options import Sequence

    # dataframe creation and manipulation
    nodes_flows = pd.read_csv(file_nodes_flows, sep=delimiter)
    nodes_flows_seq = pd.read_csv(file_nodes_flows_sequences, sep=delimiter,
                                  header=None)
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
                node = nodes.get(row['label'])
                if node is None:
                    node = classes[row['class']](label=row['label'])
                for attr in row.keys():
                    if (attr not in flow_attrs and
                       attr not in ('class', 'label', 'source', 'target',
                                    'conversion_factors')):
                            if row[attr] != 'seq':
                                if attr in seq_attributes:
                                    row[attr] = Sequence(float(row[attr]))
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
                        # this block is only for discrete flows!
                        if attr == 'discrete' and row[attr] is True:
                            # create Discrete object for flow
                            setattr(flow, attr, Discrete())
                            discrete_attrs = vars(Discrete()).keys()
                            for dattr in discrete_attrs:
                                if dattr in row.keys() and row[attr]:
                                    setattr(flow.discrete, dattr, row[dattr])
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
