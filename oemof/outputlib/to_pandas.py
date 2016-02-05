#!/usr/bin/python
# -*- coding: utf-8

import os
import logging
import pandas as pd
try:
    import matplotlib.pyplot as plt
except:
    logging.warning('Matplotlib does not work.')

# TODO:
# - Make dataframe creation and plotting configurable with as less code as
#   possible via self.result_object.get(i, {} and **kwargs


class ResultsDataFrame(pd.DataFrame):
    r"""Creates a multi-indexed pandas dataframe from a solph result object
    and holds methods to create subsets of the data.

    Note
    ----
    This is so far only a rough sketch and serves as a base for discussion.

    Parameters
    ----------

    energy_system : class:`Entity <oemof.core.EnergySystem>`
        energy supply system
    """

    def __init__(self, **kwargs):
        # default values if not arguments are passed
        es = kwargs.get('energy_system')

        rows_list = []
        for k, v in es.results.items():
            if ('Bus' in str(k.__class__)):
                if k in v.keys():
                    for kk, vv in v.items():
                        if(k is kk):
                            # duals (results[bus][bus])
                            row = {}
                            row['bus_uid'] = k.uid
                            row['bus_type'] = k.type
                            row['type'] = 'other'
                            row['obj_uid'] = 'duals'
                            row['datetime'] = es.time_idx
                            row['val'] = v.get(k)
                            rows_list.append(row)
                else:
                    for kk, vv in v.items():
                        if (isinstance(kk, str)):
                            row = {}
                            # bus variables (results[bus]['some_key'])
                            row['bus_uid'] = k.uid
                            row['bus_type'] = k.type
                            row['type'] = 'other'
                            row['obj_uid'] = kk
                            row['datetime'] = es.time_idx
                            row['val'] = vv
                            rows_list.append(row)
                        else:
                            # bus outputs (results[bus][component])
                            row = {}
                            row['bus_uid'] = k.uid
                            row['bus_type'] = k.type
                            row['type'] = 'output'
                            row['obj_uid'] = kk.uid
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
        tuples = [(item['bus_uid'],
                   item['bus_type'],
                   item['type'],
                   item['obj_uid'],
                   date,
                   val)
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
        kwargs.setdefault('date_from', self.index.get_level_values('datetime')[0])
        kwargs.setdefault('date_to', self.index.get_level_values('datetime')[-1])


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


class DataFramePlot(ResultsDataFrame):
    r"""Creates a multi-indexed pandas dataframe from a solph result object
    and holds methods to plot subsets of the data.

    Parameters
    ----------

    energy_system : class:`Entity <oemof.core.EnergySystem>`
        energy supply system
    """

    def __init__(self, **kwargs):
        super(DataFramePlot, self).__init__(**kwargs)
        self.subset = kwargs.get('subset')
        self.ax = kwargs.get('ax')

    def slice_unstacked(self, **kwargs):
        ""
        unstacklevel = kwargs.get('unstacklevel', 'obj_uid')
        subset = super(DataFramePlot, self).slice_by(**kwargs)
        subset = subset.unstack(level=unstacklevel)
        self.subset = subset
        return self

    def color_from_dict(self, colordict):
        ""
        tmplist = list(
            map(colordict.get, list(self.subset['val'].columns)))
        tmplist = ['#ff00f0' if v is None else v for v in tmplist]
        if len(tmplist) == 1:
            colorlist = tmplist[0]
        else:
            colorlist = tmplist
        return colorlist

    def set_datetime_ticks(self, tick_distance=None, number_autoticks=3,
                           date_format='%d-%m-%Y %H:%M'):
        ""
        dates = self.subset.index.get_level_values('datetime').unique()
        if tick_distance is None:
            tick_distance = int(len(dates) / number_autoticks) - 1
        self.ax.set_xticks(range(0, len(dates), tick_distance),
                           minor=False)
        self.ax.set_xticklabels(
            [item.strftime(date_format)
             for item in dates.tolist()[0::tick_distance]],
            rotation=0, minor=False)
        return self

    def outside_legend(self, **kwargs):
        ""
        kwargs.setdefault('reverse', False)
        kwargs.setdefault('loc', 'center left')
        kwargs.setdefault('bbox_to_anchor', (1, 0.5))
        kwargs.setdefault('ncol', 1)
        kwargs.setdefault('plotshare', 0.9)
        kwargs.setdefault('fancybox', True)
        kwargs.setdefault('shadow', True)
        kwargs.setdefault('handles', self.ax.get_legend_handles_labels()[0])
        kwargs.setdefault('labels', self.ax.get_legend_handles_labels()[1])

        if kwargs['reverse']:
            kwargs['handles'] = reversed(kwargs['handles'])
            kwargs['labels'] = reversed(kwargs['labels'])

        box = self.ax.get_position()
        self.ax.set_position([box.x0, box.y0, box.width * kwargs['plotshare'],
                              box.height])

        self.ax.legend(
            kwargs['handles'], kwargs['labels'], loc=kwargs['loc'],
            bbox_to_anchor=kwargs['bbox_to_anchor'], ncol=kwargs['ncol'],
            fancybox=kwargs['fancybox'], shadow=kwargs['shadow'])

    def plot(self, **kwargs):
        ""
        self.ax = self.subset.plot(**kwargs)
        return self

    def io_plot(self, bus_uid, cdict, line_kwa={}, bar_kwa={}, **kwargs):
        ""
        self.ax = kwargs.get('ax')
        if self.ax is None:
            fig = plt.figure()
            self.ax = fig.add_subplot(1, 1, 1)

        self.slice_unstacked(bus_uid=bus_uid, type='input', **kwargs)
        self.subset.plot(kind='bar', linewidth=0, stacked=True, width=1,
                         ax=self.ax, color=self.color_from_dict(cdict),
                         **bar_kwa)
        self.slice_unstacked(bus_uid=bus_uid, type='output', **kwargs)
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
        new_df.sort_index(axis=1, ascending=False, inplace=True)
        colorlist = self.color_from_dict(cdict)
        colorlist.reverse()
        separator = len(colorlist)
        new_df.plot(kind='line', ax=self.ax, color=colorlist,
                    drawstyle='steps-mid', **line_kwa)

        handles, labels = self.ax.get_legend_handles_labels()

        tmp_lab = [x for x in reversed(labels[0:separator])]
        tmp_hand = [x for x in reversed(handles[0:separator])]
        handles = tmp_hand + handles[separator:]
        labels = tmp_lab + labels[separator:]
        labels.reverse()
        handles.reverse()

        self.ax.legend(handles, labels)
        return handles, labels

    def plot_bus(self, bus_uid, **kwargs):
        r""" Method for plotting all inputs/outputs of a bus

        Parameters
        ----------
        bus_uid : string
        bus_type : string (e.g. "el" or "gas")
        type : string (input/output/other)
        date_from : string, optional
            Start date selection e.g. "2016-01-01 00:00:00". If not set, the
            whole time range will be plotted.
        date_to : string, optional
            End date selection e.g. "2016-03-01 00:00:00". If not set, the
            whole time range will be plotted.
        exclude_obj_uids : list of strings
            List of strings/substrings of obj_uids to be excluded
        """
        kwargs.setdefault('date_from', self.index.get_level_values('datetime')[0])
        kwargs.setdefault('date_to', self.index.get_level_values('datetime')[-1])
        kwargs.setdefault('type', slice(None))
        kwargs.setdefault('kind', 'line')
        kwargs.setdefault('title', 'Connected components')
        kwargs.setdefault('xlabel', 'Date')
        kwargs.setdefault('ylabel', 'Power in MW')
        kwargs.setdefault('date_format', '%d-%m-%Y')
        kwargs.setdefault('subplots', False)
        kwargs.setdefault('colormap', 'Spectral')
        kwargs.setdefault('df_plot_kwargs', {})
        kwargs.setdefault('linewidth', 2)
        kwargs.setdefault('number_autoticks', 3)

        # slicing
        subset = self.slice_by(bus_uid=bus_uid, **kwargs)

        # remove passed obj_uids/substrings of obj_uids (case sensitive)
        if kwargs.get('exclude_obj_uids'):
            for expr in kwargs.get('exclude_obj_uids'):
                subset = subset.iloc[
                    ~subset.index.get_level_values('obj_uid').str
                    .contains(expr)]

        # extract levels to use them in plot
        dates = subset.index.get_level_values('datetime').unique()

        # unstack object/component level to get columns
        subset = subset.unstack(level='obj_uid')

        # Create color list from color dictionary
        if kwargs.get('colordict'):
            kwargs['colormap'] = None
            clist = list(
                map(kwargs.get('colordict').get, list(subset['val'].columns)))
            clist = ['#ff00f0' if v is None else v for v in clist]
            if len(clist) == 1:
                kwargs['df_plot_kwargs']['color'] = clist[0]
            else:
                kwargs['df_plot_kwargs']['color'] = clist

        # if no tick distance is set, it is set automatically
        if not kwargs.get('tick_distance'):
            # if the ticks are set automatically date and time are shown
            kwargs['tick_distance'] = int(len(dates) /
                                          kwargs['number_autoticks']) - 1
            kwargs['date_format'] = '%d-%m-%Y %H:%M'

        # plotting: set matplotlib style
        if kwargs.get('mpl_style'):
            plt.style.use(kwargs.get('mpl_style'))

        # plotting: basic pandas plot
        ax = subset.plot(
            kind=kwargs.get('kind'), colormap=kwargs.get('colormap'),
            title=kwargs.get('title'), linewidth=kwargs.get('linewidth'),
            subplots=kwargs.get('subplots'), **kwargs['df_plot_kwargs'])

        # plotting: adjustments
        ax.set_ylabel(kwargs.get('ylabel')),
        ax.set_xlabel(kwargs.get('xlabel')),
        ax.set_xticks(range(0, len(dates), kwargs.get('tick_distance')),
                      minor=False)
        ax.set_xticklabels(
            [item.strftime(kwargs['date_format'])
             for item in dates.tolist()[0::kwargs.get('tick_distance')]],
            rotation=0, minor=False)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='upper right')
        return ax

    def stackplot(self, bus_uid, **kwargs):
        r"""Creating a stackplot for the given bus.

        Parameters
        ----------
        bus_uid : string
            Uid of the bus to plot.
        autostyle : boolean, optional (default: False)
            Skips the figure_size, tick_distance, style and the legend settings
            and uses the autoformat of the pandas plot function instead.
        date_from : string, optional
            Start date selection e.g. "2016-01-01 00:00:00". If not set, the
            whole time range will be plotted.
        date_to : string, optional
            End date selection e.g. "2016-03-01 00:00:00". If not set, the
            whole time range will be plotted.
        exclude_obj_uids : list of strings
            List of strings/substrings of obj_uids to be excluded
        figheight : int, optional (default: 14)
            Height of the figure. "autostyle=True" will disable this parameter.
        fighwidth : int, optional (default: 24)
            Width of the figure. "autostyle=True" will disable this parameter.
        fontgeneral : int, optional (default: 19)
            General font size. "autostyle=True" will disable this parameter.
        fontlegend : int, optional (default: 19)
            Font size of the legend. "autostyle=True" will disable this
            parameter.
        show : boolean, optional (default: True)
            Show the plot on the screen.
        save : boolean, optional (default: False)
            Save the plot to disc as a pdf file.
        savename : string, optional (default: 'stackplot' + bus_uid)
            Name of the file without the suffix.
        savepath : string, optional (default: '~/.oemof/plots')
            Path for the plots.
        style : string, optional (default: 'grayscale')
            Possible values are 'bmh', 'grayscale', 'fivethirtyeight',
            'dark_background', 'ggplot'. See the `matplotlib documentation
            <http://matplotlib.org/users/style_sheets.html>`_ for more
            information. "autostyle=True" will disable this parameter.
        """
        logging.info('Creating stackplot for Bus: {0}'.format(bus_uid))

        kwargs.setdefault('autostyle', False)
        kwargs.setdefault('figwidth', 24)
        kwargs.setdefault('figheight', 14)
        kwargs.setdefault('fontlegend', 19)
        kwargs.setdefault('fontgeneral', 19)
        kwargs.setdefault('style', 'grayscale')
        kwargs.setdefault('show', True)
        kwargs.setdefault('save', False)
        kwargs.setdefault('savename', 'stackplot_{0}'.format(str(bus_uid)))
        kwargs.setdefault('savepath', os.path.join(
            os.environ['HOME'], '.oemof', 'plots'))

        if not kwargs['autostyle']:
            fig = plt.figure(figsize=(kwargs['figwidth'], kwargs['figheight']))
            plt.rc('legend', **{'fontsize': kwargs['fontlegend']})
            plt.rcParams.update({'font.size': kwargs['fontgeneral']})
            plt.style.use(kwargs['style'])
        else:
            fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1)

        self.stackplot_part(bus_uid, ax, **kwargs)

        if kwargs['save']:
            if not os.path.isdir(kwargs['savepath']):
                os.mkdir(kwargs['savepath'])
            fullpath = os.path.join(kwargs['savepath'],
                                    kwargs['savename'] + '.pdf')
            logging.info('Saving plot to {0}'.format(fullpath))
            fig.savefig(fullpath)
        if kwargs['show']:
            plt.show(fig)
        plt.close(fig)

    def stackplot_part(self, bus_uid, ax, **kwargs):
        r"""Creating a stackplot for the given bus. This is only the core part
        of the plot method to use within a subplot. To plot one bus in one step
        you should use the :meth:`stackplot`.

        Parameters
        ----------
        bus_uid : string
            Uid of the bus to plot.
        autostyle : boolean, optional (default: False)
            Skips the figure_size, tick_distance, style and the legend settings
            and uses the autoformat of the pandas plot function instead.
        date_from : string, optional
            Start date selection e.g. "2016-01-01 00:00:00". If not set, the
            whole time range will be plotted.
        date_to : string, optional
            End date selection e.g. "2016-03-01 00:00:00". If not set, the
            whole time range will be plotted.
        tick_distance : int, optional
            Distance between two ticks of the x-axis in hours.
            "autostyle=True" will disable this parameter.
        date_format : string, optional (default: '%d-%m-%Y')
            Format of the date and time in the x-axis.
            "autostyle=True" will disable this parameter.
        """

        # Define default values
        kwargs.setdefault('bus_uid', None)
        kwargs.setdefault('bus_type', None)
        kwargs.setdefault('ax', None)
        kwargs.setdefault('date_from', self.index.get_level_values('datetime')[0])
        kwargs.setdefault('date_to', self.index.get_level_values('datetime')[-1])
        kwargs.setdefault('autostyle', False)
        kwargs.setdefault('width', 1)
        kwargs.setdefault('title', 'Connected components')
        kwargs.setdefault('xlabel', 'Date')
        kwargs.setdefault('ylabel', 'Power in MW')
        kwargs.setdefault('date_format', '%d-%m-%Y')
        kwargs.setdefault('tick_distance', None)
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

        if kwargs['autostyle']:
            kwargs['tick_distance'] = False

        my_kwargs = {
            'ax': ax,
            'width': kwargs['width'],
            'stacked': True}

        ax = self.plot_bus(
            bus_uid, date_from=kwargs['date_from'], date_to=kwargs['date_to'],
            type="input", kind='bar', linewidth=0,
            colormap=kwargs['colormap_bar'], title=kwargs['title'],
            xlabel=kwargs['xlabel'], ylabel=kwargs['ylabel'],
            colordict=kwargs.get('colordict'),
            tick_distance=kwargs['tick_distance'], df_plot_kwargs=my_kwargs)

        my_kwargs = {
            'ax': ax,
            'stacked': True,
            'drawstyle': kwargs['drawstyle']}

        ax = self.plot_bus(
            bus_uid, date_from=kwargs['date_from'], date_to=kwargs['date_to'],
            type="output", kind='line', linewidth=kwargs['linewidth'],
            colormap=kwargs['colormap_line'], title=kwargs['title'],
            colordict=kwargs.get('colordict'),
            exclude_obj_uids=kwargs.get('exclude_obj_uids'),
            xlabel=kwargs['xlabel'], ylabel=kwargs['ylabel'],
            tick_distance=kwargs['tick_distance'], df_plot_kwargs=my_kwargs)

        handles, labels = ax.get_legend_handles_labels()

        if not kwargs['autostyle']:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

            # Put a legend to the right of the current axis
            ax.legend(reversed(handles), reversed(labels), loc=kwargs['loc'],
                      bbox_to_anchor=kwargs['bbox_to_anchor'],
                      ncol=kwargs['ncol'], fancybox=kwargs['fancybox'],
                      shadow=kwargs['shadow'])
        else:
            ax.legend(reversed(handles), reversed(labels))
