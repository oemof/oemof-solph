# -*- coding: utf-8 -*-

import pandas as pd
import os
import os.path as path
import logging
from oemof import network
from ..options import BinaryFlow, Investment
from ..plumbing import sequence
from ..network import (Bus, Source, Sink, Flow, LinearTransformer, Storage,
                       EnergySystem)


PARAMETER = (
    'conversion_factors', 'nominal_value',
    'min', 'max', 'summed_max', 'actual_value', 'fixed_costs', 'variable_costs',
    'fixed', 'nominal_capacity', 'capacity_loss', 'inflow_conversion_factor',
    'outflow_conversion_factor', 'initial_capacity', 'capacity_min',
    'capacity_max', 'balanced', 'sort_index')
INDEX = ('class', 'label', 'source', 'target')


class SolphScenario(EnergySystem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p = kwargs.get('parameters')
        self.s = kwargs.get('sequences')
        self.path = kwargs.get('path', path.dirname(path.realpath(__file__)))
        self.name = kwargs.get('name')

    def create_parameter_table(self, additional_parameter=None):
        """Create an empty parameter table."""
        if additional_parameter is None:
            additional_parameter = tuple()

        my_index = pd.MultiIndex(levels=[[], [], [], []],
                                 labels=[[], [], [], []],
                                 names=INDEX)
        self.p = pd.DataFrame(columns=PARAMETER + tuple(additional_parameter),
                              index=my_index)

    def create_sequence_table(self, datetime_index=None):
        """Create an empty sequence table."""
        if datetime_index is None:
            datetime_index = self.timeindex

        my_index = pd.MultiIndex(
            levels=[[1], [2], [3], [4], [5]], labels=[[0], [0], [0], [0], [0]],
            names=INDEX + ('attributes',))

        df = pd.DataFrame(index=datetime_index, columns=my_index)
        del df[1, 2, 3, 4, 5]
        self.s = df

    def create_tables(self, **kwargs):
        """Create empty scenario tables (sequence and parameter)."""
        self.create_parameter_table(
            additional_parameter=kwargs.get('additional_parameter'))
        self.create_sequence_table(datetime_index=kwargs.get('datetime_index'))

    def read_parameter_table(self, filename=None):
        """Read existing parameter table from file."""
        if filename is None:
            filename = path.join(self.path, self.name + '.csv')
        self.p = pd.read_csv(filename, index_col=[0, 1, 2, 3])

    def read_sequence_table(self, filename=None):
        """Read existing parameter table from file."""
        if filename is None:
            filename = path.join(self.path, self.name + '_seq.csv')
        self.s = pd.read_csv(filename, header=[0, 1, 2, 3, 4], parse_dates=True,
                             index_col=0)

    def read_tables(self, parameterfile=None, sequencefile=None):
        """Read existing scenario tables (parameter and sequence)"""
        self.read_parameter_table(parameterfile)
        self.read_sequence_table(sequencefile)

    def write_parameter_table(self, filename=None):
        """Write parameter table to file."""
        if filename is None:
            filename = path.join(self.path, self.name + '.csv')
        self.p.sort_values('sort_index', inplace=True)
        self.p.fillna('').to_csv(filename)

    def write_sequence_table(self, filename=None):
        """Write sequence table to file."""
        if filename is None:
            filename = path.join(self.path, self.name + '_seq.csv')
        self.s.to_csv(filename)

    def write_tables(self, parameterfile=None, sequencefile=None):
        """Write scenario tables into two separate files."""
        self.write_parameter_table(parameterfile)
        self.write_sequence_table(sequencefile)

    def create_nodes(self):
        """
        Create nodes for a solph.energysystem

        Notes
        -----
        At the moment the nodes_from_csv function does not accept Multiindex
        DataFrames therefore the DataFrames need to be reshaped.
        """
        tmp1 = pd.DataFrame(
            index=self.s.columns).reset_index().transpose().reset_index()
        tmp2 = self.s.reset_index()
        for n in range(len(tmp2.columns.levels) - 1):
            tmp2.columns = tmp2.columns.droplevel(0)
        length = len(tmp1.columns)
        tmp1.columns = list(range(length))
        tmp2.columns = list(range(length))

        # noinspection PyTypeChecker
        return nodes_from_csv(
            nodes_flows=self.p.reset_index(),
            nodes_flows_seq=pd.concat([tmp1, tmp2], ignore_index=True))

    def add_parameters(self, idx, columns, values):
        self.p.loc[idx, columns] = values
        self.p = self.p.sortlevel()

    def add_sequences(self, idx, seq):
        self.s[idx[0], idx[1], idx[2], idx[3], idx[4]] = seq

    def add_comment_line(self, comment, sort_entry):
        self.p.loc[('### {0}'.format(comment), '', '', ''),
                   'sort_index'] = sort_entry
        self.p = self.p.sortlevel()


def create_node(row, nodes, classes, flow_attrs, seq_attributes,
                nodes_flows_seq, i):
    """
    Create node if not existent and set attributes for the current line
    (attributes must be placed either in the first line or in all
    lines of multiple node entries (flows) in csv file and be unique
    to assign them either to a node or flow object)
    """
    try:
        if row['class'] in classes.keys():
            node = nodes.get(row['label'])
            if node is None:
                node = classes[row['class']](label=row['label'])
        # for the if check below we use all flow_attrs except
        # investment because for storages investment needs to be set as a node
        # attribute (and a flow attribute)
        flow_attrs_ = [i for i in flow_attrs if i != 'investment']
        for attr in row.keys():
            if (attr not in flow_attrs_ and
               attr not in ('class', 'label', 'source', 'target',
                            'conversion_factors')):
                    if row[attr] != 'seq':
                        if attr in seq_attributes:
                            row[attr] = sequence(float(row[attr]))
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
                            seq = sequence(seq)
                        else:
                            seq = [i for i in seq.values]
                        setattr(node, attr, seq)
    except:
        print('Error with node creation in line', i+2, 'in csv file.')
        print('Label:', row['label'])
        raise
    return node


def create_flow(row, node, flow_attrs, seq_attributes, nodes_flows_seq, i):
    """
    Create flow and set attributes for the current line
    (based on attributes that only belong to the flow object)
    """
    try:
        flow = Flow()
        for attr in flow_attrs:
            if attr in row.keys() and row[attr]:
                if row[attr] != 'seq':
                    if attr in seq_attributes:
                        row[attr] = sequence(float(row[attr]))
                    setattr(flow, attr, row[attr])
                if row[attr] == 'seq':
                    seq = nodes_flows_seq.loc[row['class'],
                                              row['label'],
                                              row['source'],
                                              row['target'],
                                              attr]
                    if attr in seq_attributes:
                        seq = [i for i in seq]
                        seq = sequence(seq)
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
        print('Error with flow creation in line', i + 2, 'in csv file.')
        print('Label:', row['label'])
        raise
    return flow


def create_output_entry(row, nodes, flow, bus_attrs, type1, type2, i):
    """
    Create an output entry for the current line
    (a dict for the nodes outputs of type {node1: flow1, node2: flow2})
    """
    try:
        if row['label'] == row[type1]:
            if row[type2] not in nodes.keys():
                nodes[row[type2]] = Bus(label=row[type2])
                for attr in bus_attrs:
                    if attr in row.keys() and row[attr] is not None:
                        setattr(nodes[row[type2]], attr, row[attr])
            tmp = {nodes[row[type2]]: flow}
        else:
            tmp = {}
    except:
        print('Error with output creation in line', i + 2,
              'in csv file.')
        print('Label:', row['label'])
        raise
    return tmp


def create_conversion_factors(row, nodes, nodes_flows_seq, i):
    """
    Create a conversion_factor entry for the current line
    (a dict for the conversion factors of type {node1: eta1, node2: eta2})
    """
    try:
        if row['target'] and 'conversion_factors' in row:
            if row['conversion_factors'] == 'seq':
                seq = nodes_flows_seq.loc[row['class'],
                                          row['label'],
                                          row['source'],
                                          row['target'],
                                          'conversion_factors']
                seq = [i for i in seq]
                seq = sequence(seq)
                conversion_factors = {nodes[row['target']]: seq}
            else:
                conversion_factors = {
                    nodes[row['target']]:
                        sequence(float(row['conversion_factors']))}
        else:
            conversion_factors = {}
    except:
        print('Error with conversion factor creation in line', i + 2,
              'in csv file.')
        print('Label:', row['label'])
        raise
    return conversion_factors


def NodesFromCSV(file_nodes_flows, file_nodes_flows_sequences, **kwargs):
    """Keep old name to keep the API."""
    nodes_from_csv(file_nodes_flows, file_nodes_flows_sequences, **kwargs)


def nodes_from_csv(file_nodes_flows=None, file_nodes_flows_sequences=None,
                   nodes_flows=None, nodes_flows_seq=None, delimiter=',',
                   additional_classes=None, additional_seq_attributes=None,
                   additional_flow_attributes=None):
    """ Creates nodes with their respective flows and sequences from
    a pre-defined CSV structure. An example has been provided in the
    development examples

    Parameters
    ----------
    nodes_flows_seq : pandas.DataFrame
    nodes_flows : pandas.DataFrame
    file_nodes_flows : string
        Name of CSV file with nodes and flows
    file_nodes_flows_sequences : string
        Name of of CSV file containing sequences
    delimiter : str
        Delimiter of CSV file
    additional_classes : dict
        Dictionary containing additional classes to be recognized inside the
        csv reader. Looks like: {'MyClass1': MyClass1, ...}
    additional_seq_attributes : iterable
        List of string with attributes that have to be of type 'solph sequence'
        and that shall be recognized inside the csv file.
    additional_flow_attributes : iterable
        List of string with attributes that shall be recognized inside the
        csv file and set as flow attribute

    """
    # Check attributes for None values
    if additional_classes is None:
        additional_classes = dict()
    if additional_seq_attributes is None:
        additional_seq_attributes = list()
    if additional_flow_attributes is None:
        additional_flow_attributes = list()

    # DataFrame creation and manipulation
    if nodes_flows is None:
        nodes_flows = pd.read_csv(file_nodes_flows, sep=delimiter)

    if nodes_flows_seq is None:
        nodes_flows_seq = pd.read_csv(file_nodes_flows_sequences,
                                      sep=delimiter, header=None)
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
    flow_attrs = list(vars(Flow()).keys()) + additional_flow_attributes
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

            # create node and set attributes
            node = create_node(row, nodes, classes, flow_attrs, seq_attributes,
                               nodes_flows_seq, i)

            # create flow and set attributes
            flow = create_flow(row, node, flow_attrs, seq_attributes,
                               nodes_flows_seq, i)

            # create inputs, outputs
            inputs = create_output_entry(row, nodes, flow, bus_attrs,
                                         'target', 'source', i)

            outputs = create_output_entry(row, nodes, flow, bus_attrs,
                                          'source', 'target', i)

            # create conversion factors
            conversion_factors = create_conversion_factors(row, nodes,
                                                           nodes_flows_seq, i)

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


def merge_csv_files(path=None, output_path=None, write=True):
    """
    Merge csv files from a specified directory. All files with 'seq' will be
    merged and all other files. Make sure that no other csv-files than the ones
    to be merged are inside the specified directory.

    Parameters
    ----------
    path: str
        Path to the directory where csv files are stored
    output_path : str
        Path where the merged files are written to (default is `path` above)
    write : boolean
        Indicating if new, merged dataframes should be written to csv

    Returns
    -------
    Tuple of dataframes (nodes_flows, nodes_flows_seq)
    """
    if output_path is None:
        output_path = path

    files = [f for f in os.listdir(path) if f.endswith('.csv')]

    nodes_flows = pd.DataFrame()
    nodes_flows_seq = pd.DataFrame()

    for f in files:
        if 'seq' in f:
            tmp_df = pd.read_csv(os.path.join(path, f), index_col=[0],
                                 header=[0, 1, 2, 3, 4])
            nodes_flows_seq = pd.concat([nodes_flows_seq, tmp_df], axis=1)
        else:
            tmp_df = pd.read_csv(os.path.join(path, f))
            nodes_flows = pd.concat([nodes_flows, tmp_df])

    if write is True:
        nodes_flows.to_csv(os.path.join(output_path,
                                        'merged_nodes_flows.csv'), index=False)
        if isinstance(nodes_flows_seq.columns, pd.MultiIndex):
            nodes_flows_seq.to_csv(os.path.join(output_path,
                                   'merged_nodes_flows_seq.csv'))
        else:
            raise ValueError('Columns of merge seq-csvfile is not Multiindex.'
                             'Did you use unique column-headers across all '
                             'files?')

    return nodes_flows, nodes_flows_seq


def resample_sequence(seq_base_file=None, output_path=None,
                      samples=None, file_prefix=None, file_suffix='_seq',
                      header=[0, 1, 2, 3, 4]):
    """
    This function can be used for resampling the sequence csv-data file.
    The file is read  from the specified path: `seq_base_file`, resampled and,
    written back to the a specified directory. Note that the sequence files
    are expected to have a timeindex column that can be parsed by
    pandas, with entries like: '2014-01-01 00:00:00+00:00'


    Parameters
    ----------
    seq_base_file : string
        File that contains data to be resampled.
    output_path : string
        Path for resampled seq-files. If no path is specified,
        attr:`seq_base_file` path will be used.
    samples : list
        List of strings with the resampling rate e.g. ['4H', '2H']. See
        `pandas.DataFrame.resample` method for more information on format.
    file_prefix : string
        String that is put as prefix of the file name, i.e. filename is created
        by: `file_prefix+s+file_suffix+'.csv'`
    file_suffix : string
        Sring that is put as suffix (before .csv), default is '_seq'. See also
        file_prefix.
    header : list
        List of integers to specifiy the header lines
    """
    if samples is None:
        raise ValueError('Missing sample attribute. Please specifiy!')
    if output_path is None:
        logging.info('No output_path specified' +
                     ', setting output_path to seq_path!')
        output_path = seq_base_file

    if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)

    seq_path, seq_file = os.path.split(seq_base_file)

    # read the file and parse the dates from the first column (index 0)
    seq = pd.read_csv(os.path.join(seq_path, seq_file),
                      header=header, parse_dates=[0])

    # store the first column name for reuse
    first_col = seq.columns[0]
    # set the index as datetimeindex from column with parsed dates
    seq.index = seq[first_col]
    # set timeindex

    # convert columns to numeric values, except the datetimecolumn, but!
    # which we keep for reuse
    for col in seq:
        if col == first_col:
            seq[col] = -999999
        else:
            seq[col] = seq[col].astype(float)

    for s in samples:
        # resample dataframes
        seq_sampled = seq.resample(s).mean()
        # assign the resampled datetimeindex values to the first columns,
        # replacing the -999999
        seq_sampled[first_col] = seq_sampled.index
        if file_prefix is None:
            file_prefix = seq_file.split('seq')[0]
            logging.info('Setting filename prefix to: {}'.format(file_prefix))

        filename = os.path.join(output_path, file_prefix+s+file_suffix+'.csv')
        logging.info('Writing sample file to {0}.'.format(filename))
        seq_sampled.to_csv(filename, index=False)
    return seq_sampled
