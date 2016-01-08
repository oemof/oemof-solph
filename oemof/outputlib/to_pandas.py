#!/usr/bin/python
# -*- coding: utf-8

import pandas as pd
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt

# TODO:
# - Add storages to column "other".
#   But only the state of charge? I think it is good to have load/unload
#   as output/input (uwe)
#   Yes! (Cord)
#
# - Create some "standard-slices" for plots e.g. all inputs of a specific bus
# - Add option to use a real datetime-index as x-values and proper labeled
#   y-values (e. g. not (wind,val) but wind) for subsets of the multiindex-df
# - Make dataframe creation and plotting configurable with as less code as
#   possible via **kwargs
# - Add possibility to define that dataframe is only created for spefific busses
#   e.g. only for electrical busses or a given list of busses. This might be
#   helpful for very big problems like renpass-gis, etc.


class EnergySystemDataFrame:
    r"""Creates a multi-indexed pandas dataframe from a solph result object
    and holds methods to plot subsets of the data

    Note
    ----
    This is so far only a rough sketch and serves as a base for discussion.

    Parameters
    ----------
    result_object : dictionary
        solph result objects
    idx_start_date : string
        Start date of the dataframe date index e.g. "2016-01-01 00:00:00"
    ixd_date_freq : string
        Frequency for the dataframe date index e.g. "H" for hours

    Attributes
    ----------
    result_object : dictionary
        solph result objects
    idx_start_date : string
        Start date of the dataframe date index e.g. "2016-01-01 00:00:00"
    ixd_date_freq : string
        Frequency for the dataframe date index e.g. "H" for hours
    data_frame : pandas dataframe
        Multi-indexed pandas dataframe holding the data from the result object
    """
    def __init__(self, **kwargs):
        # default values if not arguments are passed
        kwargs.setdefault('ixd_date_freq', 'H')

        self.result_object = kwargs.get('result_object')
        self.energy_system = kwargs.get('energy_system')
        self.idx_start_date = kwargs.get('idx_start_date')
        self.ixd_date_freq = kwargs.get('ixd_date_freq')
        self.data_frame = None
        if not self.result_object:
            self.result_object = self.energy_system.results
        if not (self.data_frame):
            self.data_frame = self.create()

    def create(self):
        r""" Method for creating a multi-index pandas dataframe of
        the result object

        Parameters
        ----------
        self : EnergySystemDataFrame() instance
        """
        df = pd.DataFrame(columns=['bus_uid', 'bus_type', 'type',
                                   'obj_uid', 'datetime', 'val'])
        for e, o in self.result_object.items():
            if 'Bus' in str(e.__class__):
                row = pd.DataFrame()
                # inputs
                for i in e.inputs:
                    if i in self.result_object:
                        row['bus_uid'] = [e.uid]
                        row['bus_type'] = [e.type]
                        row['type'] = ['input']
                        row['obj_uid'] = [i.uid]
                        row['datetime'] = \
                            [pd.date_range(self.idx_start_date,
                             periods=len(self.result_object[i].get(e)),
                             freq=self.ixd_date_freq)]
                        row['val'] = [self.result_object[i].get(e)]
                        df = df.append(row)
                # outputs
                for k, v in o.items():
                    # skip self referenced entries (duals, etc.) and
                    # string keys to put them into "other"
                    if k is not e and not (isinstance(k, str)):
                        row['bus_uid'] = [e.uid]
                        row['bus_type'] = [e.type]
                        row['type'] = ['output']
                        row['obj_uid'] = [k.uid]
                        row['datetime'] = \
                            [pd.date_range(self.idx_start_date,
                             periods=len(v), freq=self.ixd_date_freq)]
                        row['val'] = [v]
                        df = df.append(row)
                # other
                for k, v in o.items():
                    row['bus_uid'] = [e.uid]
                    row['bus_type'] = [e.type]
                    row['type'] = ['other']
                    # self referenced entries (duals, etc.) in else block
                    if k is not e and isinstance(k, str):
                        row['obj_uid'] = [k]
                        row['datetime'] = \
                            [pd.date_range(self.idx_start_date,
                             periods=len(v), freq=self.ixd_date_freq)]
                        row['val'] = [v]
                        df = df.append(row)
                    else:
                        row['obj_uid'] = ['duals']
                        row['datetime'] = \
                            [pd.date_range(self.idx_start_date,
                             periods=len(v), freq=self.ixd_date_freq)]
                        row['val'] = [v]
                        df = df.append(row)

        # split date and value lists columns into rows (long format)
        df_long = pd.DataFrame()
        for index, cols in df.iterrows():
            df_extract = pd.DataFrame.from_dict(
                {'datetime': cols.ix['datetime'],
                 'val': cols.ix['val']})
            df_extract = pd.concat(
                [df_extract, cols.drop(['datetime', 'val']).to_frame().T],
                axis=1).fillna(method='ffill').fillna(method='bfill')
            df_long = pd.concat([df_long, df_extract], ignore_index=True)

        # create multiindexed dataframe
        arrays = [df_long['bus_uid'], df_long['bus_type'], df_long['type'],
                  df_long['obj_uid'], df_long['datetime']]
        tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['bus_uid', 'bus_type', 'type',
                                                 'obj_uid', 'datetime'])
        df_multiindex = pd.DataFrame(df_long['val'].values,
                                     columns=['val'], index=index)

        # sort MultiIndex to work correctly
        df_multiindex.sort_index(inplace=True)

        return df_multiindex

    def plot_bus(self, **kwargs):
        r""" Method for plotting all inputs/outputs of a bus

        Parameters
        ----------
        bus_uid : string
        bus_type : string (e.g. "el" or "gas")
        type : string (input/output/other)
        date_from : string (Start date selection e.g. "2016-01-01 00:00:00")
        date_to : string (End date selection e.g. "2016-03-01 00:00:00")
        """
        kwargs.setdefault('bus_uid', None)
        kwargs.setdefault('bus_type', None)
        kwargs.setdefault('type', None)
        kwargs.setdefault('date_from', None)
        kwargs.setdefault('date_to', None)
        kwargs.setdefault('kind', 'line')
        kwargs.setdefault('title', 'Connected components')
        kwargs.setdefault('xlabel', 'Date')
        kwargs.setdefault('ylabel', 'Power in MW')
        kwargs.setdefault('date_format', '%d-%m-%Y')
        kwargs.setdefault('tick_distance', 24)
        kwargs.setdefault('subplots', False)
        kwargs.setdefault('colormap', 'Spectral')
        kwargs.setdefault('df_plot_kwargs', {})
        kwargs.setdefault('linewidth', 2)

        # slicing
        idx = pd.IndexSlice
        subset = self.data_frame.loc[idx[
            [kwargs.get('bus_uid')],
            :,
            [kwargs.get('type')],
            :,
            slice(
                pd.Timestamp(kwargs.get('date_from')),
                pd.Timestamp(kwargs.get('date_to')))]]
        # extracting levels to use them in plot
        obj_uids = subset.index.get_level_values('obj_uid').unique()
        dates = subset.index.get_level_values('datetime').unique()
        # unstacking object/component level to get columns
        subset = subset.unstack(level='obj_uid')

        # plotting: set matplotlib style
        if kwargs.get('mpl_style'):
            mpl.style.use(kwargs.get('mpl_style'))

        # plotting: basic pandas plot
        ax = subset.plot(
            kind=kwargs.get('kind'), colormap=kwargs.get('colormap'),
            title=kwargs.get('title'), linewidth=kwargs.get('linewidth'),
            subplots=kwargs.get('subplots'), **kwargs['df_plot_kwargs'])

        # plotting: adjustments
        ax.set_ylabel(kwargs.get('ylabel')),
        ax.set_xlabel(kwargs.get('xlabel')),
        # ax.set_xticks(range(0,len(dates),1), minor=True),
        ax.set_xticks(range(0, len(dates), kwargs.get('tick_distance')),
                      minor=False),
        ax.set_xticklabels(
            [item.strftime('%d-%m-%Y')
             for item in dates.tolist()[0::kwargs.get('tick_distance')]],
            rotation=0, minor=False),
        ax.legend(obj_uids, loc='upper right')
        return ax

    def stackplot(self, **kwargs):
        r"""Creating a matplotlib figure object.

        Parameters
        ----------
        """

        # Define default values
        kwargs.setdefault('bus_uid', None)
        kwargs.setdefault('bus_type', None)
        kwargs.setdefault('ax', None)
        kwargs.setdefault('date_from', None)
        kwargs.setdefault('date_to', None)
        kwargs.setdefault('width', 1)
        kwargs.setdefault('title', 'Connected components')
        kwargs.setdefault('xlabel', 'Date')
        kwargs.setdefault('ylabel', 'Power in MW')
        kwargs.setdefault('date_format', '%d-%m-%Y')
        kwargs.setdefault('tick_distance', 24)
        kwargs.setdefault('subplots', False)
        kwargs.setdefault('colormap_bar', 'Spectral')
        kwargs.setdefault('colormap_line', 'jet')
        kwargs.setdefault('df_plot_kwargs', {})
        kwargs.setdefault('linewidth', 2)
        kwargs.setdefault('loc', 'center left')
        kwargs.setdefault('bbox_to_anchor', (1, 0.5))
        kwargs.setdefault('ncol', 1)
        kwargs.setdefault('fancybox', True)
        kwargs.setdefault('shadow', True)
        kwargs.setdefault('drawstyle', 'steps-mid')

        my_kwargs = {
            'ax': kwargs['ax'],
            'width': kwargs['width'],
            'stacked': True}

        ax = self.plot_bus(
            bus_uid=kwargs['bus_uid'], bus_type=kwargs['bus_type'],
            type="input", kind='bar', linewidth=0,
            date_from=kwargs['date_from'],
            date_to=kwargs['date_to'],
            colormap=kwargs['colormap_bar'], title=kwargs['title'],
            xlabel=kwargs['xlabel'], ylabel=kwargs['ylabel'],
            tick_distance=kwargs['tick_distance'], df_plot_kwargs=my_kwargs)

        my_kwargs = {
            'ax': kwargs['ax'],
            'stacked': True,
            'drawstyle': kwargs['drawstyle']}

        ax = self.plot_bus(
            bus_uid=kwargs['bus_uid'], bus_type=kwargs['bus_type'],
            type="output", kind='line', linewidth=kwargs['linewidth'],
            date_from=kwargs['date_from'],
            date_to=kwargs['date_to'],
            colormap=kwargs['colormap_line'], title=kwargs['title'],
            xlabel=kwargs['xlabel'], ylabel=kwargs['ylabel'],
            tick_distance=kwargs['tick_distance'], df_plot_kwargs=my_kwargs)

        # Put a legend to the right of the current axis
        handles, labels = ax.get_legend_handles_labels()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

        # Put a legend to the right of the current axis
        ax.legend(reversed(handles), reversed(labels), loc=kwargs['loc'],
                  bbox_to_anchor=kwargs['bbox_to_anchor'],
                  ncol=kwargs['ncol'], fancybox=kwargs['fancybox'],
                  shadow=kwargs['shadow'])
