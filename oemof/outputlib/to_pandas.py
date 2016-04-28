#!/usr/bin/python
# -*- coding: utf-8

import logging
import pandas as pd
try:
    import matplotlib.pyplot as plt
except:
    logging.warning('Matplotlib does not work.')


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
    bus_uids : list if strings
        List of strings with busses that should be contained in dataframe.
        If not set, all busses are contained.
    bus_types : list if strings
        List of strings with bus types that should be contained in dataframe.
        If not set, all bus types are contained.

    Attributes
    ----------
    result_object : dictionary
        solph result objects
    bus_uids : list if strings
        List of strings with busses that should be contained in dataframe.
        If not set, all busses are contained.
    bus_types : list if strings
        List of strings with bus types that should be contained in dataframe.
        If not set, all bus types are contained.
    data_frame : pandas dataframe
        Multi-indexed pandas dataframe holding the data from the result object.
        For more information on advanced dataframe indexing see:
        http://pandas.pydata.org/pandas-docs/stable/advanced.html
    bus_uids : list if strings
        List of strings with busses that should be contained in dataframe
    bus_types : list if strings
        List of strings with bus types that should be contained in dataframe.
    """

    def __init__(self, **kwargs):
        # default values if not arguments are passed
        es = kwargs.get('energy_system')

        rows_list = []
        for k, v in es.results.items():
            if ('Bus' in str(k.__class__)):
                for kk, vv in v.items():
                    row = {}
                    row['bus_uid'] = k.uid
                    row['bus_type'] = k.type
                    row['type'] = ('output' if not (isinstance(kk, str)) else
                                   'other')
                    row['obj_uid'] = 'duals' if (k is kk) else (
                                      kk     if (isinstance(kk, str)) else
                                      kk.uid)
                    row['datetime'] = es.time_idx
                    row['val'] = vv
                    rows_list.append(row)
            else:
                if k in v.keys():
                    # self ref. components (results[component][component])
                    for kk, vv in v.items():
                        if(k is kk):
                            # self ref. comp. (results[component][component])
                            row = {}
                            row['bus_uid'] = k.outputs[0].uid
                            row['bus_type'] = k.outputs[0].type
                            row['type'] = 'other'
                            row['obj_uid'] = k.uid
                            row['datetime'] = es.time_idx
                            row['val'] = vv
                            rows_list.append(row)
                        else:
                            # bus inputs (only self ref. components)
                            row = {}
                            row['bus_uid'] = k.outputs[0].uid
                            row['bus_type'] = k.outputs[0].type
                            row['type'] = 'input'
                            row['obj_uid'] = k.uid
                            row['datetime'] = es.time_idx
                            row['val'] = v.get(k.outputs[0])
                            rows_list.append(row)
                else:
                    for kk, vv in v.items():
                        # bus inputs (results[component][bus])
                        row = {}
                        row['bus_uid'] = kk.uid
                        row['bus_type'] = kk.type
                        row['type'] = 'input'
                        row['obj_uid'] = k.uid
                        row['datetime'] = es.time_idx
                        row['val'] = vv
                        rows_list.append(row)

        # split date and value lists to tuples
        tuples = [
            (item['bus_uid'], item['bus_type'], item['type'], item['obj_uid'],
             date, val)
            for item in rows_list for date, val in zip(item['datetime'],
                                                       item['val'])]

        # create multiindexed dataframe
        index = ['bus_uid', 'bus_type', 'type',
                 'obj_uid', 'datetime']

        columns = index + ['val']

        super().__init__(tuples, columns=columns)
        self.set_index(index, inplace=True)
        self.sort_index(inplace=True)

    def slice_by(self, **kwargs):
        r""" Method for slicing the ResultsDataFrame. A subset is returned.

        Parameters
        ----------
        bus_uid : string
        bus_type : string (e.g. "el" or "gas")
        type : string (input/output/other)
        obj_uid: string
        date_from : string
            Start date selection e.g. "2016-01-01 00:00:00". If not set, the
            whole time range will be plotted.
        date_to : string
            End date selection e.g. "2016-03-01 00:00:00". If not set, the
            whole time range will be plotted.

        """
        kwargs.setdefault('bus_uid', slice(None))
        kwargs.setdefault('bus_type', slice(None))
        kwargs.setdefault('type', slice(None))
        kwargs.setdefault('obj_uid', slice(None))
        kwargs.setdefault(
            'date_from', self.index.get_level_values('datetime')[0])
        kwargs.setdefault(
            'date_to', self.index.get_level_values('datetime')[-1])

        # slicing
        idx = pd.IndexSlice

        subset = self.loc[idx[
            kwargs['bus_uid'],
            kwargs['bus_type'],
            kwargs['type'],
            kwargs['obj_uid'],
            slice(pd.Timestamp(kwargs['date_from']),
                  pd.Timestamp(kwargs['date_to']))], :]

        return subset

    def slice_unstacked(self, unstacklevel='obj_uid', **kwargs):
        r"""Method for slicing the ResultsDataFrame. A unstacked
        subset is returned.

        Parameters
        ----------
        unstacklevel : string (default: 'obj_uid')
            Level to unstack the subset of the DataFrame.
        """
        subset = self.slice_by(**kwargs)
        subset = subset.unstack(level=unstacklevel)
        subset.columns = subset.columns.droplevel()
        return subset


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

    def slice_unstacked(self, unstacklevel='obj_uid', **kwargs):
        r"""Method for slicing the ResultsDataFrame. The subset attribute
        will set to an unstacked subset. The self-attribute is returned to
        allow chaining. This method is an extension of the
        :class:`slice_unstacked <ResultsDataFrame.slice_unstacked>` method
        of the `ResultsDataFrame` class (parent class).

        Parameters
        ----------
        unstacklevel : string (default: 'obj_uid')
            Level to unstack the subset of the DataFrame.
        """
        self.subset = super(
            DataFramePlot, self).slice_unstacked(
                unstacklevel='obj_uid', **kwargs)
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
        print(neworder)
        self.subset = self.subset[neworder]

    def color_from_dict(self, colordict):
        r""" Method to convert a dictionary containing the components and its
        colors to a color list that can be directly useed with the color
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
            The disctance between to ticks in hours. If not set autoticks are
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
        loc : string (default: 'center left')
            Location of the plot.
        bbox_to_anchor : tuple (default: (1, 0.5))
            Set the anchor for the legend.
        ncol : integer (default: 1)
            Number of columns of the legend.
        handles : list of handles
            A list of handels if they are already modified by another function
            or method. Normally these handles will be automatically taken from
            the artis object.
        lables : list of labels
            A list of labels if they are already modified by another function
            or method. Normally these handles will be automatically taken from
            the artis object.
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

    def io_plot(self, bus_uid, cdict, line_kwa={}, lineorder=None, bar_kwa={},
                barorder=None, **kwargs):
        r""" Plotting a combined bar and line plot to see the fitting of in-
        and outcomming flows of a bus balance.

        Parameters
        ----------
        bus_uid : string
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
            Manipulated labels to correct the unsual construction of the
            stack line plot. You can use them for further maipulations.
        """
        self.ax = kwargs.get('ax', self.ax)

        if self.ax is None:
            fig = plt.figure()
            self.ax = fig.add_subplot(1, 1, 1)

        # Create a bar plot for all input flows
        self.slice_unstacked(bus_uid=bus_uid, type='input', **kwargs)
        if barorder is not None:
            self.rearrange_subset(barorder)
        self.subset.plot(kind='bar', linewidth=0, stacked=True, width=1,
                         ax=self.ax, color=self.color_from_dict(cdict),
                         **bar_kwa)

        # Create a line plot for all output flows
        self.slice_unstacked(bus_uid=bus_uid, type='output', **kwargs)
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
            lineorder.reverse()
            new_df = new_df[lineorder]
        colorlist = self.color_from_dict(cdict)
        if isinstance(colorlist, list):
            colorlist.reverse()
        separator = len(colorlist)
        new_df.plot(kind='line', ax=self.ax, color=colorlist,
                    drawstyle='steps-mid', **line_kwa)

        # Adapt the legend to the new oder
        handles, labels = self.ax.get_legend_handles_labels()
        tmp_lab = [x for x in reversed(labels[0:separator])]
        tmp_hand = [x for x in reversed(handles[0:separator])]
        handles = tmp_hand + handles[separator:]
        labels = tmp_lab + labels[separator:]
        labels.reverse()
        handles.reverse()

        self.ax.legend(handles, labels)
        return handles, labels
