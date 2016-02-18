# -*- coding: utf-8 -*-
"""

@author: Simon Hilpert simon.hilpert@fh-flensburg.de
"""
import pandas as pd
import logging
from ..core.network.entities import Bus
from ..core.network.entities.components import sources as source
from ..core.network.entities.components import sinks as sink
from ..core.network.entities.components import transformers as transformer
from ..core.network.entities.components import transports as transport


def add_bus(row, **kwargs):
    r""" Adds bus object ot list of busses. The function is used
    by apply() method of pandas data frames.

    Parameters
    ----------
    row : row of pandas.DataFrame()
    busses : list
        list of existing busses
    busprices : pandas.DataFrame()
       data frame containting the values for the busprices. Column index is
       the uid of bus to create.
    """
    busprices = kwargs.get('busprices', None)
    busses = kwargs.get('busses', [])

    # check for prices
    if row['timeseries']:
        price = busprices[row['uid']]
    # if price is constant
    else:
        price = row['price']

    if row.get('sum_out_limit', False) == False or 'FALSE':
        sum_out_limit = float('+inf')
    else:
        sum_out_limit = float(row['sum_out_limit'])
    # set kwargs from row items
    kwargs = {}
    for k in row.keys():
        kwargs.update({k: row[k]})
    kwargs['price'] = price
    kwargs['sum_out_limit'] = sum_out_limit
    obj = Bus(**kwargs)
    busses.append(obj)


def add_source(row, **kwargs):
    r""" Adds source object ot list of source. The function is used
    by apply() method of pandas data frames.

    Parameters
    ----------
    row : row of pandas.DataFrame()
    busses : list
        list of existing busses
    sink : list
        list of sources where object are appended
    sourcevalues : pandas.DataFrame()
       data frame containting the values for the source column index is uid of
       source to create.
    """
    sourcevalues = kwargs.get('sourcevalues', None)
    busses = kwargs.get('busses', None)
    sources = kwargs.get('sources', None)

    cls = getattr(source, row['class'])

    # set kwargs from row
    kwargs = {}
    for k in row.keys():
        kwargs.update({k: row[k]})

    # set special kwargs (conversion to list etc. )
    kwargs['out_max'] = [row.get('out_max', None)]
    kwargs['outputs'] = [b for b in busses if b.uid == row['output']]
    kwargs['val'] = sourcevalues[row['uid']]

    obj = cls(**kwargs)
    sources.append(obj)


def add_sink(row, **kwargs):
    r""" Adds sink object ot list of transformers. The function is used
    by apply() method of pandas data frames.

    Parameters
    ----------
    row : row of pandas.DataFrame()
    busses : list
        list of existing busses
    sink : list
        list of sinks where object are appended
    sinkvalues : pandas.DataFrame()
       data frame containting the values for the sink column index is uid of
       sink
    """
    sinkvalues = kwargs.get('sinkvalues', None)
    busses = kwargs.get('busses', None)
    sinks = kwargs.get('sinks', [])

    cls = getattr(sink, row['class'])

    # set special kwargs (conversion to list etc. )
    inputs = [b for b in busses if b.uid == row['input']]

    # instantiate sink object
    obj = cls(uid=row['uid'],
              inputs=inputs,
              val=sinkvalues[row['uid']])
    sinks.append(obj)


def add_transformer(row, **kwargs):
    r""" Adds transformer objects ot list of transformers. The function is used
    by apply() method of pandas data frames.

    Parameters
    ----------
    row : row of pandas.DataFrame()
    busses : list
        list of existing busses
    transformers : list
        list of transformers where object are appended
    """
    if not row['skip']:
        busses = kwargs.get('busses', None)
        transformers = kwargs.get('transformers', [])
        # get transformer class

        cls = getattr(transformer, row['class'])

        # set kwargs from row
        kwargs = {}
        for k in row.keys():
            kwargs.update({k: row[k]})
        # set special kwargs (conversion to list etc. )
        kwargs['eta'] = [row['eta']]
        kwargs['out_max'] = [row['out_max']]
        kwargs['output_price'] = [row.get('output_price')]
        kwargs['outputs'] = [bus for bus in busses if bus.uid == row["output"]]
        kwargs['inputs'] = [b for b in busses if b.uid == row['input']]
        opex_var = kwargs['inputs'][0].price / kwargs['eta'][0]
        kwargs['opex_var'] = opex_var
        kwargs['out_min'] = [row['out_max']*row.get('out_min', 0)]

        # instantiate storage object from class
        obj = cls(**kwargs)
        transformers.append(obj)


def add_storage(row, **kwargs):
    r""" Adds storage objects ot list of storages. The function is used by
    apply() method of pandas data frames.

    Parameters
    ----------
    row : row of pandas.DataFrame()
    busses : list
        list of existing busses
    transformers : list
        list of transformers where object are appended
    """
    if not row['skip']:
        busses = kwargs.get('busses', None)
        transformers = kwargs.get('transformers', [])
        # get storage class
        cls = getattr(transformer, row['class'])
        # set kwargs from row
        kwargs = {}
        for k in row.keys():
            kwargs.update({k: row[k]})
        # set special kwargs (conversion to list etc. )
        kwargs['out_max'] = [row.get('out_max')]
        kwargs['in_max'] = [row.get('in_max')]
        kwargs['outputs'] = [bus for bus in busses if bus.uid == row["output"]]
        kwargs['inputs'] = [b for b in busses if b.uid == row['input']]

        # instantiate storage object from class
        obj = cls(**kwargs)
        transformers.append(obj)


def add_chp(row, **kwargs):
    r""" Adds chps objects ot list of transformers. The function is used by
    apply() method of pandas data frames.

    Parameters
    ----------
    row : row of pandas.DataFrame()
    busses : list
        list of existing busses
    transformers : list
        list of transformers where object are appended
    """
    if not row['skip']:
        busses = kwargs.get('busses', None)
        transformers = kwargs.get('transformers', None)
        cls = getattr(transformer, row['class'])

        # set kwargs from row
        kwargs = {}
        for k in row.keys():
            kwargs.update({k: row[k]})

        # special kwargs where transformation of type is necessary (e.g. list)
        kwargs['inputs'] = [b for b in busses if b.uid == row['input']]
        kwargs['outputs'] = [bus for bus in busses if
                             any([bus.uid == row["output_el"],
                                  bus.uid == row["output_th"]])]
        kwargs['out_max'] = [row['out_max_el'], row.get('out_max_th', None)]
        kwargs['out_min'] = [row['out_min']]
        kwargs['eta_min'] = [row['eta_el_min'], row.get('eta_th_min', None)]
        kwargs['output_price'] = [row.get('output_price_el'),
                                  row.get('output_price_th')]
        kwargs['eta'] = [row['eta_el'], row['eta_th']]
        # instantiate object with kwargs
        obj = cls(**kwargs)
        transformers.append(obj)


def add_transport(row, **kwargs):
    r""" Adds transpport objects ot list of transports. The function is used by
    apply() method of pandas data frames.

    """
    if not row['skip']:
        busses = kwargs.get('busses', None)
        transports = kwargs.get('transports', None)
        cls = getattr(transport, row['class'])

        # set kwargs from row
        kwargs = {}
        for k in row.keys():
            kwargs.update({k: row[k]})

        kwargs['eta'] = [row['eta']]
        kwargs['out_max'] = [row['out_max']]
        kwargs['in_max'] = [row.get('in_max')]
        kwargs['inputs'] = [b for b in busses if b.uid == row['input']]

        kwargs['outputs'] = [b for b in busses if b.uid == row['output']]

        # instantiate object with kwargs
        obj = cls(**kwargs)
        transports.append(obj)


def entities_from_csv(files, entities_dict=None):
    r""" Creates 'oemof-objects' from csv files by the use of pandas dataframes

    Parameters
    ----------
    files : dict
        dictionary containing the paths to files for object creation. Keys are:
        'transformers','busses','storages','chps', 'sources', 'sourcevalues',
        'sinks', 'sinkvalues', 'busprices'
    entities_dict : dict
        dictionary containing lists of oemof base class objects
    """
    if entities_dict is None:
        entities_dict = {'busses': [],
                         'transformers': [],
                         'sinks': [],
                         'sources': [],
                         'transports': []}
    # first create busses
    file = files.get('busses')
    if file is not None:
        bus_df = pd.read_csv(file)
        file = files.get('busprices')
        if file is not None:
            busprices = pd.read_csv(file)
        else:
            logging.info('No csv data for bus prices!')
            busprices = pd.DataFrame()
        bus_df.apply(add_bus, axis=1, busprices=busprices,
                     busses=entities_dict['busses'])
    # transformers
    file = files.get('transformers')
    if file is not None:
        df = pd.read_csv(file)
        df.apply(add_transformer, axis=1, busses=entities_dict['busses'],
                 transformers=entities_dict['transformers'])

    file = files.get('transports')
    if file is not None:
        df = pd.read_csv(file)
        df.apply(add_transport, axis=1, busses=entities_dict['busses'],
                 transports=entities_dict['transports'])

    file = files.get('storages')
    if file is not None:
        df = pd.read_csv(file)
        df.apply(add_storage, axis=1, busses=entities_dict['busses'],
                 transformers=entities_dict['transformers'])

    file = files.get('sources')
    if file is not None:
        df = pd.read_csv(file)
        values_csv = files.get('sourcevalues')
        if values_csv is not None:
            sourcevalues = pd.read_csv(values_csv)
        else:
            raise ValueError('No csv data found for source values!')
        df.apply(add_source, axis=1, busses=entities_dict['busses'],
                 sources=entities_dict['sources'], sourcevalues=sourcevalues)

    file = files.get('sinks')
    if file is not None:
        df = pd.read_csv(file)
        values_csv = files.get('sinkvalues')
        if values_csv is not None:
            sinkvalues = pd.read_csv(values_csv)
        else:
            raise ValueError('No csv data found for sink values!')
        df.apply(add_sink, axis=1, busses=entities_dict['busses'],
                 sinks=entities_dict['sinks'], sinkvalues=sinkvalues)

    file = files.get('chps', None)
    if file is not None:
        chp_df = pd.read_csv(file)
        chp_df.apply(add_chp, axis=1, busses=entities_dict['busses'],
                     transformers=entities_dict['transformers'])

    entities = sum([entities_dict[k] for k in entities_dict.keys()], [])
    entities_dict['entities'] = entities
    return(entities_dict)
