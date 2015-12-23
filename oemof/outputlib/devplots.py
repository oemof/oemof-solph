#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

import matplotlib.pyplot as plt
import pandas as pd
import logging


class stackplot:
    r''' Creates a plot around a bus with all inputs as bar plots and all
    outputs as lineplots.

    TODO: Check if EnergySystem contains a results dictionary!
    TODO: Option to remove empty time series from legend (e.g. unused storage)
    TODO: Combine legends in a combined plot and keep only the lowest x-axis.
    TODO: Default naming for title, axis...
    TODO: Passing kwargs to 'bar' or 'line' plot but not both (e.g. lw=4).
    TODO: Set order of columns to plot
    TODO: Sink has to be the lowest line but plotted on top.

    Parameters
    ----------
    plot_dc : dictionary of pandas.DataFrame
        A dictionary with the keys 'in' and 'out' containing a DataFrame with
        all input time series ('in') and all output time series 'out'.
    es : oemof.core.EnergySystem object
        An EnergySystem object containing a results dictionary.

    Attributes
    ----------
    plot_dc : dictionary of pandas.DataFrame
        A dictionary with the keys 'in' and 'out' containing a DataFrame with
        all input time series ('in') and all output time series 'out'.
    es : oemof.core.EnergySystem object
        An EnergySystem object containing a results dictionary.

    Note
    ----
    The EnergySystem object needs to have a results dictionary.

    '''
    def __init__(self, **kwargs):
        self.plot_dc = kwargs.get('plot_dc', {})
        self.es = kwargs.get('es')

    def create_io_df(self, uid):
        r'''Create a dictionary of DataFrames containing all time series around
        a bus.

        The returned dictionary has two keys ('in', 'out') that contain the
        DataFrame of the incoming and outgonig flows of the bus.

        Parameters
        ----------
        uid : string or tuple
            The uid of the bus, that should be plotted

        Returns
        -------
        dictionary : Dicionary of DataFrames
        '''
        logging.debug('Getting bus for uid: {0}'.format(uid))
        bus = [obj for obj in self.es.entities if obj.uid == uid][0]
        index = pd.date_range(pd.datetime(self.es.year, 1, 1, 0, 0),
                              pd.datetime(self.es.year, 12, 31, 23, 0),
                              freq='H')
        tmp_dc = {}
        tmp_dc['in'] = pd.DataFrame()
        tmp_dc['out'] = pd.DataFrame()
        logging.debug(
            'Creating DataFrame for all inputs of bus: {0}'.format(bus))
        for entity in bus.inputs:
            tmp_dc['in'][entity.uid] = pd.Series(self.es.results[entity][bus],
                                                 index=index)
        logging.debug(
            'Creating DataFrame for all outputs of bus: {0}'.format(bus))
        for entity in bus.outputs:
            tmp_dc['out'][entity.uid] = pd.Series(self.es.results[bus][entity],
                                                  index=index)
        return tmp_dc

    def create_fig(self, figw=24, figh=14, fontl=14, fontg=19):
        r'''Creating a matplotlib figure object.

        Parameters
        ----------
        figw : float or int
            Width of the figure object (default: 24).
        figh : float or int
            Height of the figure object (default: 14).
        fontg : float or int
            General font size within the plot (default: 19).
        fontl : float or int
            Font size of the legend (default: 14).
        '''
        fig = plt.figure(figsize=(figw, figh))
        plt.rcParams.update({'font.size': fontg})
        plt.rc('legend', **{'fontsize': fontl})
        return fig

    def core(self, eid, ax, kind, prange, **kwargs):
        r'''Plotting a DataFrame of the dictionary.
        eid : str
            The key of the plot_dc dictionary.
        ax : matplotlib artist object
            If an artist object is passed the plot will be added to this artist
            object.
        kind : string
            The type of the plot ('bar', 'line', ...). See the pandas plot
            documentation for more information.
        prange : range of the pandas index
            The range of the pandas.DataFrame to be plotted. The range should
            be of the same time a the DataFrame index.

        Returns
        -------
        matplotlib artis object
        '''
        logging.debug('Plotting from {0} to {1}.'.format(prange[0],
                                                         prange[-1]))
        df_slice = self.plot_dc[eid].loc[prange].reset_index(
            drop=True)
        logging.debug('Creating a {0}-plot.'.format(kind))
        return df_slice.plot(kind=kind, stacked=True, ax=ax, **kwargs)

    def full(self, prange, **kwargs):
        r'''Create a full plot of a valid plot_dc dictionary

        Parameters
        ----------
        prange : range of the pandas index
            The range of the pandas.DataFrame to be plotted. The range should
            be of the same time a the DataFrame index. The DataFrames are part
            of the plot_dc dictionary with the keys 'in' and 'out'.
        \**kwargs : keyword arguments
            Additional arguments to be passed to the plotting command.
        '''
        fig = self.create_fig()
        ax = fig.add_subplot(1, 1, 1)

        self.part(prange, ax, **kwargs)

    def part(self, prange, ax, **kwargs):
        r'''Create a part of plot within an existing artist object using a
        valid plot_dc dictionary.

        Parameters
        ----------
        prange : range of the pandas index
            The range of the pandas.DataFrame to be plotted. The range should
            be of the same time a the DataFrame index. The DataFrames are part
            of the plot_dc dictionary with the keys 'in' and 'out'.
        ax : matplotlib artist object
            The new plot will be added to this artist object.
        \**kwargs : keyword arguments
            Additional arguments to be passed to the plotting command.
        '''
        in_color = None
        if kwargs.get('out_color') is not None:
            logging.debug('Using an own color set for "out": {0}'.format(
                kwargs.get('out_color')))
            kwargs['color'] = kwargs.pop('out_color')
            logging.debug('Using an own color set for "in": {0}'.format(
                kwargs.get('in_color')))
            in_color = kwargs.pop('in_color')
        ax = self.core('out', ax, 'line', prange, linewidth=2, **kwargs)

        if in_color is not None:
            kwargs['color'] = in_color
        ax = self.core('in', ax, 'bar', prange, width=1, linewidth=0, **kwargs)

        # Shrink current axis by 20%
        handles, labels = ax.get_legend_handles_labels()

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(reversed(handles), reversed(labels), loc='center left',
                  bbox_to_anchor=(1, 0.5), ncol=1, fancybox=True,
                  shadow=True)

        fg = pd.date_range(pd.datetime(2010, 6, 1, 0, 0),
                           periods=168, freq='H')

        labels = fg[0::24].format(formatter=lambda x: x.strftime(
            '%d.%m.-%H:%M'))
        ticks = list(range(len(fg)))[0::24]
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels, rotation=10)
