#!/usr/bin/python
# -*- coding: utf-8

import os
import logging
import pandas as pd
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    logging.warning('Matplotlib could not be imported. Plotting will not work.')


class ResultsDataFrame(pd.DataFrame):
    r"""Creates a multi-indexed pandas dataframe from a solph result object
    and holds methods to create subsets of the data.

    Note
    ----
    This is so far only a rough sketch and serves as a base for discussion.

    Parameters
    ----------
    result_object : dictionary
        solph result objects
    bus_labels : list if strings
        List of strings with buses that should be contained in dataframe.
        If not set, all buses are contained.

    Attributes
    ----------
    result_object : dictionary
        solph result objects
    bus_labels : list if strings
        List of strings with buses that should be contained in dataframe.
        If not set, all buses are contained.
    bus_types : list if strings
        List of strings with bus types that should be contained in dataframe.
        If not set, all bus types are contained.
    data_frame : pandas dataframe
        Multi-indexed pandas dataframe holding the data from the result object.
        For more information on advanced dataframe indexing see:
        http://pandas.pydata.org/pandas-docs/stable/advanced.html

    """
    def __init__(self, **kwargs):
        # default values if not arguments are passed
        es = kwargs.get('energy_system')

        rows_list = []
        for k, v in es.results.items():
            if 'Bus' in str(k.__class__):
                for kk, vv in v.items():
                    row = dict()
                    row['bus_label'] = k.label
                    if k is kk:
                        row['type'] = 'other'
                    else:
                        row['type'] = 'from_bus'
                    if k is kk:
                        row['obj_label'] = 'duals'
                    elif isinstance(kk, str):
                        row['obj_label'] = 'kk'
                    else:
                        row['obj_label'] = kk.label
                    row['datetime'] = es.timeindex
                    row['val'] = vv
                    rows_list.append(row)
            else:
                if k in v.keys():
                    # self ref. components (results[component][component])
                    for kk, vv in v.items():
                        if k is kk:
                            # self ref. comp. (results[component][component])
                            row = dict()
                            row['bus_label'] = list(k.outputs.keys())[0].label
                            row['type'] = 'other'
                            row['obj_label'] = k.label
                            row['datetime'] = es.timeindex
                            row['val'] = vv
                            rows_list.append(row)
                        else:
                            # bus inputs (only self ref. components)
                            row = dict()
                            row['bus_label'] = list(k.outputs.keys())[0].label
                            row['type'] = 'to_bus'
                            row['obj_label'] = k.label
                            row['datetime'] = es.timeindex
                            row['val'] = v.get(list(k.outputs.keys())[0])
                            rows_list.append(row)
                else:
                    for kk, vv in v.items():
                        # bus inputs (results[component][bus])
                        row = dict()
                        row['bus_label'] = kk.label
                        row['type'] = 'to_bus'
                        row['obj_label'] = k.label
                        row['datetime'] = es.timeindex
                        row['val'] = vv
                        rows_list.append(row)

        # split date and value lists to tuples
        tuples = [
            (item['bus_label'], item['type'], item['obj_label'],
             date, val)
            for item in rows_list for date, val in zip(item['datetime'],
                                                       item['val'])]

        # create MultiIndex DataFrame
        index = ['bus_label', 'type', 'obj_label', 'datetime']

        columns = index + ['val']

        super().__init__(tuples, columns=columns)
        self.set_index(index, inplace=True)
        self.sort_index(inplace=True)

    def slice_by(self, **kwargs):
        r""" Method for slicing the ResultsDataFrame. A subset is returned.

        Other Parameters
        ----------------
        bus_label : string
        type : string (to_bus/from_bus/other)
        obj_label: string
        date_from : string
            Start date selection e.g. "2016-01-01 00:00:00". If not set, the
            whole time range will be plotted.
        date_to : string
            End date selection e.g. "2016-03-01 00:00:00". If not set, the
            whole time range will be plotted.

        """
        kwargs.setdefault('bus_label', slice(None))
        kwargs.setdefault('type', slice(None))
        kwargs.setdefault('obj_label', slice(None))
        kwargs.setdefault(
            'date_from', self.index.get_level_values('datetime')[0])
        kwargs.setdefault(
            'date_to', self.index.get_level_values('datetime')[-1])

        # slicing
        idx = pd.IndexSlice

        subset = self.loc[idx[
            kwargs['bus_label'],
            kwargs['type'],
            kwargs['obj_label'],
            slice(pd.Timestamp(kwargs['date_from']),
                  pd.Timestamp(kwargs['date_to']))], :]

        return subset

    def slice_unstacked(self, unstacklevel='obj_label',
                        formatted=False, **kwargs):
        r"""Method for slicing the ResultsDataFrame. An unstacked
        subset is returned.

        Parameters
        ----------
        unstacklevel : string (default: 'obj_label')
            Level to unstack the subset of the DataFrame.
        formatted : boolean

        """
        subset = self.slice_by(**kwargs)
        subset = subset.unstack(level=unstacklevel)
        if formatted is True:
            subset.reset_index(level=['bus_label', 'type'], drop=True,
                               inplace=True)
        # use standard instead of multi-indexed columns
        subset.columns = subset.columns.get_level_values(1).unique()
        return subset

    def slice_bus_balance(self, bus_label):
        r"""Method for slicing the ResultsDataFrame. An balance around a bus
        with inputs, outputs and other values is returned.

        Parameters
        ----------
        bus_label : string

        """
        dfs = []
        for l in self.index.levels[1]:
            df = self.slice_unstacked(bus_label=bus_label, type=l,
                                      formatted=True)
            dfs.append(df)
        subset = pd.concat(dfs, axis=1)
        # use standard instead of multi-indexed columns
        subset.columns = [v for v in subset.columns]
        return subset

    def bus_balance_to_csv(self, bus_labels=None, output_path=''):
        r"""Method for saving bus balances of the ResultsDataFrame as single
        csv files. A balance around each bus with inputs, outputs and other
        values is saved for a passed list of bus labels. If no labels are
        passed, all busses are saved. Additionally, an output path for the
        files can be specified.

        Parameters
        ----------
        bus_labels : list of strings
        output_path : string

        """
        if bus_labels is None:
            bus_labels = self.index.levels[0]
        for bus in bus_labels:
            self.slice_bus_balance(bus).to_csv(
                    os.path.join(output_path, bus + '.csv'))


class DataFramePlot(ResultsDataFrame):
    r"""Creates plots based on the subset of a multi-indexed pandas dataframe
    of the :class:`ResultsDataFrame class
    <oemof.outputlib.to_pandas.ResultsDataFrame>`.

    Parameters
    ----------
    subset : pandas.DataFrame
        A subset of the results DataFrame.
    ax : matplotlib axis object
        Axis object of the last plot.

    Attributes
    ----------
    subset : pandas.DataFrame
        A subset of the results DataFrame.
    ax : matplotlib axis object
        Axis object of the last plot.
    """

    def __init__(self, **kwargs):
        super(DataFramePlot, self).__init__(**kwargs)
        self.subset = kwargs.get('subset')
        self.ax = kwargs.get('ax')

    def slice_unstacked(self, unstacklevel='obj_label', **kwargs):
        r"""Method for slicing the ResultsDataFrame. The subset attribute
        will set to an unstacked subset. The self-attribute is returned to
        allow chaining. This method is an extension of the
        :class:`slice_unstacked <ResultsDataFrame.slice_unstacked>` method
        of the `ResultsDataFrame` class (parent class).

        Parameters
        ----------
        unstacklevel : string (default: 'obj_label')
            Level to unstack the subset of the DataFrame.
        """
        self.subset = super(
            DataFramePlot, self).slice_unstacked(
                unstacklevel='obj_label', **kwargs)
        return self

    def rearrange_subset(self, order):
        r"""
        Change the order of the subset DataFrame

        Parameters
        ----------
        order : list
            New order of columns

        Returns
        -------
        self
        """
        cols = list(self.subset.columns.values)
        neworder = [x for x in list(order) if x in set(cols)]
        missing = [x for x in list(cols) if x not in set(order)]
        if len(missing) > 0:
            logging.warning(
                "Columns that are not part of the order list are removed: " +
                str(missing))
        self.subset = self.subset[neworder]

    def color_from_dict(self, colordict):
        r""" Method to convert a dictionary containing the components and its
        colors to a color list that can be directly used with the color
        parameter of the pandas plotting method.

        Parameters
        ----------
        colordict : dictionary
            A dictionary that has all possible components as keys and its
            colors as items.

        Returns
        -------
        list
            Containing the colors of all components of the subset attribute
        """
        tmplist = list(
            map(colordict.get, list(self.subset.columns)))
        tmplist = ['#ff00f0' if v is None else v for v in tmplist]
        if len(tmplist) == 1:
            colorlist = tmplist[0]
        else:
            colorlist = tmplist
        return colorlist

    def set_datetime_ticks(self, tick_distance=None, number_autoticks=3,
                           date_format='%d-%m-%Y %H:%M'):
        r""" Set configurable ticks for the time axis. One can choose the
        number of ticks or the distance between ticks and the format.

        Parameters
        ----------
        tick_distance : real
            The distance between to ticks in hours. If not set autoticks are
            set (see number_autoticks).
        number_autoticks : int (default: 3)
            The number of ticks on the time axis, independent of the time
            range. The higher the number of ticks is, the shorter should be the
            date_format string.
        date_format : string (default: '%d-%m-%Y %H:%M')
            The string to define the format of the date and time. See
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
            for more information.
        """
        dates = self.subset.index.get_level_values('datetime').unique()
        if tick_distance is None:
            tick_distance = int(len(dates) / number_autoticks) - 1
        self.ax.set_xticks(range(0, len(dates), tick_distance),
                           minor=False)
        self.ax.set_xticklabels(
            [item.strftime(date_format)
             for item in dates.tolist()[0::tick_distance]],
            rotation=0, minor=False)

    def outside_legend(self, reverse=False, plotshare=0.9, **kwargs):
        r""" Move the legend outside the plot. Bases on the ideas of Joe
        Kington. See
        http://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        for more information.

        Parameters
        ----------
        reverse : boolean (default: False)
            Print out the legend in reverse order. This is interesting for
            stack-plots to have the legend in the same order as the stacks.
        plotshare : real (default: 0.9)
            Share of the plot area to create space for the legend (0 to 1).

        Other Parameters
        ----------------
        loc : string (default: 'center left')
            Location of the plot.
        bbox_to_anchor : tuple (default: (1, 0.5))
            Set the anchor for the legend.
        ncol : integer (default: 1)
            Number of columns of the legend.
        handles : list of handles
            A list of handels if they are already modified by another function
            or method. Normally these handles will be automatically taken from
            the artist object.
        lables : list of labels
            A list of labels if they are already modified by another function
            or method. Normally these handles will be automatically taken from
            the artist object.
        Note
        ----
        All keyword arguments (kwargs) will be directly passed to the
        matplotlib legend class. See
        http://matplotlib.org/api/legend_api.html#matplotlib.legend.Legend
        for more parameters.
        """
        kwargs.setdefault('loc', 'center left')
        kwargs.setdefault('bbox_to_anchor', (1, 0.5))
        kwargs.setdefault('ncol', 1)
        handles = kwargs.pop('handles', self.ax.get_legend_handles_labels()[0])
        labels = kwargs.pop('labels', self.ax.get_legend_handles_labels()[1])

        if reverse:
            handles.reverse()
            labels.reverse()

        box = self.ax.get_position()
        self.ax.set_position([box.x0, box.y0, box.width * plotshare,
                              box.height])

        self.ax.legend(handles, labels, **kwargs)

    def plot(self, **kwargs):
        r""" Passing the subset attribute to the pandas plotting method. All
        parameters will be directly passed to pandas.DataFrame.plot(). See
        http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html
        for more information.

        Returns
        -------
        self
        """
        self.ax = self.subset.plot(**kwargs)
        return self

    def io_plot(self, bus_label, cdict, line_kwa=None, lineorder=None,
                bar_kwa=None, barorder=None, **kwargs):
        r""" Plotting a combined bar and line plot to see the fitting of in-
        and out-coming flows of a bus balance.

        Parameters
        ----------
        bus_label : string
            Uid of the bus to plot the balance.
        cdict : dictionary
            A dictionary that has all possible components as keys and its
            colors as items.
        line_kwa : dictionary
            Keyword arguments to be passed to the pandas line plot.
        bar_kwa : dictionary
            Keyword arguments to be passed to the pandas bar plot.
        lineorder : list
            Order of columns to plot the line plot
        barorder : list
            Order of columns to plot the bar plot

        Note
        ----
        Further keyword arguments will be passed to the
        :class:`slice_unstacked method <DataFramePlot.slice_unstacked>`.

        Returns
        -------
        handles, labels
            Manipulated labels to correct the unusual construction of the
            stack line plot. You can use them for further manipulations.
        """
        self.ax = kwargs.get('ax', self.ax)

        if bar_kwa is None:
            bar_kwa = dict()
        if line_kwa is None:
            line_kwa = dict()

        if self.ax is None:
            fig = plt.figure()
            self.ax = fig.add_subplot(1, 1, 1)

        # Create a bar plot for all input flows
        self.slice_unstacked(bus_label=bus_label, type='to_bus', **kwargs)
        if barorder is not None:
            self.rearrange_subset(barorder)
        self.subset.plot(kind='bar', linewidth=0, stacked=True, width=1,
                         ax=self.ax, color=self.color_from_dict(cdict),
                         **bar_kwa)

        # Create a line plot for all output flows
        self.slice_unstacked(bus_label=bus_label, type='from_bus', **kwargs)
        if lineorder is not None:
            self.rearrange_subset(lineorder)
        # The following changes are made to have the bottom line on top layer
        # of all lines. Normally the bottom line is the first line that is
        # plotted and will be on the lowest layer. This is difficult to read.
        new_df = pd.DataFrame(index=self.subset.index)
        n = 0
        tmp = 0
        for col in self.subset.columns:
            if n < 1:
                new_df[col] = self.subset[col]
            else:
                new_df[col] = self.subset[col] + tmp
            tmp = new_df[col]
            n += 1
        if lineorder is None:
            new_df.sort_index(axis=1, ascending=False, inplace=True)
        else:
            lineorder = list(lineorder)
            lineorder.reverse()
            new_df = new_df[lineorder]
        colorlist = self.color_from_dict(cdict)
        if isinstance(colorlist, list):
            colorlist.reverse()
        separator = len(colorlist)
        new_df.plot(kind='line', ax=self.ax, color=colorlist,
                    drawstyle='steps-mid', **line_kwa)

        # Adapt the legend to the new order
        handles, labels = self.ax.get_legend_handles_labels()
        tmp_lab = [x for x in reversed(labels[0:separator])]
        tmp_hand = [x for x in reversed(handles[0:separator])]
        handles = tmp_hand + handles[separator:]
        labels = tmp_lab + labels[separator:]
        labels.reverse()
        handles.reverse()

        self.ax.legend(handles, labels)
        return handles, labels
