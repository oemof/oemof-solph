#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import logging
import os
import dblib as db
from . import config as config


def stackplot_core(main_dc, reg, energy_type, ax_dc, ax):
    '''
    Returns an artist container with the stackplot
    '''
    # set start value for stackplot to zero to start at y=0
    bottom_val = 0

    # create artist container for stack plot (sp)
    sp = list(range(len(main_dc['res']['info'][energy_type]['generation'])))
    components = db.cut_lists(main_dc['order']['generation'],
        main_dc['res']['info'][energy_type]['generation'])

    # Summing up the data from all components for the upper bar
    tmp_res_dc = {}
    for c in components:
        tmp_res_dc[c] = main_dc['res'][energy_type]['generation'][c][reg][
            main_dc['res']['info']['vector_start']:
                main_dc['res']['info']['vector_end'] + 1]
        bottom_val += tmp_res_dc[c]

    # loop to create stackbars for the plot
    for i, c in zip(list(range(len(sp))), reversed(components)):
        bottom_val = bottom_val - tmp_res_dc[c]
        sp[i] = ax_dc[ax].bar(
            np.arange(float(main_dc['res']['info']['plotstart']),
                float(main_dc['res']['info']['plotend'] + 1)),     # counter
            tmp_res_dc[c],
            width=1,
            linewidth=0,
            color=main_dc['res']['color'][c],
            label=c,
            bottom=bottom_val)
        main_dc['res']['legend']['generation'][energy_type].append(
            main_dc['res']['name'][c][0])
    return sp


def lineplot_core(main_dc, reg, energy_type, ax_dc, ax):
    '''
    Returns an artist container with the lineplot
    '''
    # set start value for stackplot to zero to start at y=0
    plot_val = 0

    # creates an empty artist container for line plot (lp)
    lp = list(range(len(main_dc['res']['info'][energy_type]['demand'])))
    components = db.cut_lists(main_dc['order']['demand'],
        main_dc['res']['info'][energy_type]['demand'])

    # Summing up the data from all components for the upper line
    tmp_res_dc = {}
    for c in components:
        tmp_res_dc[c] = main_dc['res'][energy_type]['demand'][c][reg][
            main_dc['res']['info']['vector_start']:
                main_dc['res']['info']['vector_end'] + 1]
        plot_val += tmp_res_dc[c]

    # Filling the artist container
    for i, c in zip(list(range(len(lp))), reversed(components)):
        lp[i], = ax_dc[ax].plot(np.arange(float(
                main_dc['res']['info']['plotstart']),
                float(main_dc['res']['info']['plotend'] + 1)) + 0.5,
            plot_val,
            lw=2,
            color=main_dc['res']['color'][c][0])
        plot_val = plot_val - tmp_res_dc[c]
        main_dc['res']['legend']['demand'][energy_type].append(
            main_dc['res']['name'][c][0])
    return lp


def plot_plot(fig, main_dc):
    '''
    Plots a  combined plot from two artist container (bars and lines).
    '''

    # Saves plot
    if main_dc['res']['save']:
        fig.savefig(os.path.join(main_dc['res']['save_path'],
            main_dc['res']['save_name'] + '.pdf'))

    # shows plot
    if main_dc['res']['show']:
        plt.show(fig)
    plt.close(fig)


def get_name_and_color(main_dc, u_type, energy_type):
    '''
    Fetch name and color from the database for all components used.
    '''
    name_col = 'name_eng'
    components = (list(main_dc['res'][energy_type][u_type].keys()) +
        [energy_type])
    for comp in components:
        db_tmp = db.fetch_columns(main_dc['basic'], 'a_rli_corporate',
            'technologie_definition', columns=['farbcode_hex', name_col],
            where_column='char4_code', where_condition=comp)
        if not db_tmp['farbcode_hex']:
            db_tmp.setdefault('farbcode_hex', [])
            db_tmp['farbcode_hex'] = ['#ff00c8']
            logging.warning('Color for {0} is not defined'.format(comp))
        if not db_tmp[name_col]:
            db_tmp.setdefault(name_col, [])
            db_tmp[name_col] = ['no name']
            logging.warning('Name for {0} is not defined'.format(comp))
        main_dc['res']['color'][comp] = db_tmp['farbcode_hex']
        main_dc['res']['name'][comp] = db_tmp[name_col]


def remove_empty_arrays(main_dc, u_type, energy_type):
    '''
    Remove empty arrays from the result dictionaryan from the plot.
    '''
    if main_dc['res']['remove_empty_arrays']:
        for comp in list(main_dc['res'][energy_type][u_type].keys()):
            sum_comp = 0
            for reg in list(main_dc['res'][energy_type][u_type][comp].keys()):
                sum_comp += sum(main_dc['res'][energy_type][u_type][comp][reg])
            if sum_comp == 0:
                main_dc['res'][energy_type][u_type].pop(comp)
                main_dc['res']['info'][energy_type][u_type].remove(comp)


def define_test_plot_dc(main_dc):
    '''
    Defines a dictionary to test the plot function
    without reading real data sets.
    '''
    main_dc.setdefault('res', {})
    main_dc['res']['elec'] = {}
    main_dc['res']['elec']['generation'] = {}
    main_dc['res']['elec']['generation']['tccg'] = {}
    main_dc['res']['elec']['generation']['tocg'] = {}
    main_dc['res']['elec']['generation']['rpvo'] = {}

    main_dc['res']['elec']['demand'] = {}
    main_dc['res']['elec']['demand']['lele'] = {}
    main_dc['res']['elec']['demand']['sbat'] = {}
    main_dc['res']['elec']['demand']['lele']['deu'] = (
        np.array([1, 3, 5, 8, 4, 6, 9]) + np.array([2, 9, 3, 2, 1, 8, 3]))
    main_dc['res']['elec']['demand']['sbat']['deu'] = np.array(
        [3, 6, 7, 9, 2, 1, 4])

    main_dc['res']['elec']['generation']['tccg']['deu'] = np.array(
        [1, 3, 5, 8, 4, 6, 9])
    main_dc['res']['elec']['generation']['tocg']['deu'] = np.array(
        [3, 6, 7, 9, 2, 1, 4])
    main_dc['res']['elec']['generation']['rpvo']['deu'] = np.array(
        [2, 9, 3, 2, 1, 8, 3])

    main_dc['res']['info'] = {}
    main_dc['res']['info']['elec'] = {}
    main_dc['res']['info']['elec']['generation'] = ['tccg', 'tocg', 'rpvo']
    main_dc['res']['info']['elec']['demand'] = ['lele', 'sbat']

    main_dc['res']['info']['timestart'] = 1
    main_dc['res']['info']['timeend'] = 7
    main_dc['res']['info']['timesteps'] = 7
    main_dc['res']['info']['energy_types'] = ['elec']
    reg = 'deu'
    energy_type = 'elec'

    main_dc['res']['show'] = True
    main_dc['res']['save'] = False
    main_dc['res']['print'] = {}
    main_dc['res']['print']['ylabel'] = True
    main_dc['res']['print']['title'] = True
    main_dc['res']['print']['legend'] = True
    main_dc['res']['print']['last_legend'] = False
    main_dc['res']['print']['xlabel'] = False
    main_dc['res']['print']['last_xlabel'] = True
    main_dc['res']['xlabel'] = 'Test x-axis'
    return main_dc, reg, energy_type


def create_test_plot(main_dc):
    '''
    Creates a test plot with data from 'define_test_plot_dc'.
    '''
    logging.info('Test Plot')
    ax_dc = {}
    [main_dc, region, energy_type] = define_test_plot_dc(main_dc)
    prepare_plot_dict(main_dc)
    fig = create_default_figure(main_dc)
    multi_stacked_time_plot(main_dc, ax_dc, fig, [energy_type], [region])


def check_for_missing_components(main_dc, comp_type, energy_type):
    '''
    Checks the component list for components that are not in the "order"-list.
    If a component is not in the "order"-list, it will not be plotted!
    '''
    missing_comp = list(set(main_dc['res']['info'][energy_type][comp_type]).
        difference(set(main_dc['order'][comp_type])))
    if missing_comp:
        logging.error('Missing "{0}"-component in "order"-list: {1}'.format(
            comp_type, missing_comp))


def prepare_plot_dict(main_dc, region=None):
    '''
    Set needed keys and lists for the plot dictionary and
    checks for needed keys, lists and elements.
    '''
    if region is None:
        region = 'undefined region'

    # Types of components for the plot
    main_dc['res']['usage_type'] = ['generation', 'demand']

    #Set your own parameter
    main_dc['res'].setdefault('print', {})

    main_dc['res']['print'].setdefault('ylabel', True)
    main_dc['res']['print'].setdefault('title', True)

    # Use this parameters, if you want to save the plots to you disk
    main_dc['res'].setdefault('save', True)
    main_dc['res'].setdefault('save_path', os.environ['HOME'])
    main_dc['res'].setdefault('save_name', 'plot__' + region[0])

    # Showing the plot directly on the screen
    main_dc['res'].setdefault('show', True)

    # If you plot a multiplot with the same x-axis, only the x-label of the
    # lowermost subplot ist printed.
    main_dc['res']['print'].setdefault('xlabel', False)
    main_dc['res']['print'].setdefault('last_xlabel', True)

    # If you have a multiplot with the same legends, only one legend is
    # plotted.
    main_dc['res']['print'].setdefault('legend', True)
    main_dc['res']['print'].setdefault('last_legend', False)

    #Defines the full name of the region:
    # If you have more than one region you should use the database
    # to resolve the full name from the region code.
    main_dc['res'].setdefault('name', {})
    if not type(region) is list:
        region = list([region, ])
    for r in region:
        main_dc['res']['name'].setdefault(r, "'{0}'".format(r))

    # Set keys for the plot dictionary
    main_dc['res'].setdefault('legend', {})
    main_dc['res'].setdefault('color', {})
    main_dc['res'].setdefault('name', {})
    main_dc['res'].setdefault('artist', {})
    main_dc['res'].setdefault('remove_empty_arrays', False)

    # everything inside the loop is done for 'generation' and 'demand'.
    for u_type in main_dc['res']['usage_type']:
        #Creating an empty list for legend entries
        main_dc['res']['legend'].setdefault(u_type, {})
        for energy_type in list(main_dc['res']['info']['energy_types']):
            main_dc['res']['legend'][u_type][energy_type] = []
            remove_empty_arrays(main_dc, u_type, energy_type)
            get_name_and_color(main_dc, u_type, energy_type)
            check_for_missing_components(main_dc, u_type, energy_type)

    # Will set default values if they don't(!) exist.
    # User defined values can be defined before or after this definition.
    main_dc['res'].setdefault('title', 'Titel des Plots')
    main_dc['res'].setdefault('ylabel', 'Beschriftung der y-Achse')
    main_dc['res'].setdefault('xlabel', 'Beschriftung der x-Achse')
    main_dc['res']['legend']['generation'].setdefault('loc', 4)
    main_dc['res']['legend']['generation'].setdefault('title',
        'Generation')
    main_dc['res']['legend']['demand'].setdefault('loc', 1)
    main_dc['res']['legend']['demand'].setdefault('title', 'Demand')
    main_dc['res'].setdefault('font', {})
    main_dc['res']['font'].setdefault('general', 19)
    main_dc['res']['font'].setdefault('legend', 14)
    main_dc['res'].setdefault('figsize', {})
    main_dc['res']['figsize'].setdefault('width', 24.0)
    main_dc['res']['figsize'].setdefault('height', 14.0)
    main_dc['res'].setdefault('plotpath', os.environ['HOME'])
    main_dc['res']['info'].setdefault('plotstart',
        main_dc['res']['info']['timestart'])
    main_dc['res']['info'].setdefault('plotend',
        main_dc['res']['info']['timeend'])


def multiplot(main_dc, region, element_list):
    '''
    Creates a multiplot for chp in the region 'lk_wittenberg'.
    '''

    config.plot(main_dc)

    logging.info('Creates a multiplot.')

    # Creates the dictionary for the artist container
    ax_dc = {}

    main_dc['res']['remove_empty_arrays'] = True

    # Creates the default keys for the plot
    # use: print((res_dc.keys())) to see the keys.
    # All default values and a lot more can be changed
    # See the matplotlib documentation for more details.
    prepare_plot_dict(main_dc, region)

    # Creates a default figure
    fig = create_default_figure(main_dc)

    # Plots the stacked_time_plot.
    multi_stacked_time_plot(main_dc, ax_dc, fig, element_list, region)


def singleplot(main_dc, region, elements):
    '''
    Creates two single plots for heat and power in the region 'lk_wittenberg'.
    '''

    logging.info('Creates single plots for heat and power.')

    config.plot(main_dc)

    # Creates the default keys for the plot
    # use: print((res_dc.keys())) to see the keys.
    # All default values and a lot more can be changed
    # See the matplotlib documentation for more details.
    prepare_plot_dict(main_dc, region)

    # Use a loop to create two plots instead of a multiplot.
    for element_list in elements:
        # Creates the dictionary for the artist container
        ax_dc = {}

        # Creates a default figure
        fig = create_default_figure(main_dc)

        main_dc['res']['save_name'] = element_list[0] + '__' + region[0]

        # Plots the stacked_time_plot.
        multi_stacked_time_plot(main_dc, ax_dc, fig, element_list, region)


def test_plot(main_dc):
    '''
    Plots a test plot
    '''
    config.plot(main_dc)
    create_test_plot(main_dc)


def calculate_time_vectors(main_dc):
    'Calculates the time vectors for the plots.'
    if (main_dc['res']['info']['plotstart'] <
            main_dc['res']['info']['timestart']) or (
            main_dc['res']['info']['plotend'] >
            main_dc['res']['info']['timeend']):
        logging.error('Time intervall is wrong:')

    main_dc['res']['info']['vector_start'] = (
        main_dc['res']['info']['plotstart'] -
        main_dc['res']['info']['timestart'])
    main_dc['res']['info']['vector_end'] = (main_dc['res']['info']['plotend'] -
        main_dc['res']['info']['plotstart'] +
        main_dc['res']['info']['vector_start'])


def create_default_figure(main_dc):
    '''
    Creates a default figure with default font sizes.
    '''
    fig = plt.figure(figsize=(main_dc['res']['figsize']['width'],
        main_dc['res']['figsize']['height']))
    plt.rcParams.update({'font.size': main_dc['res']['font']['general']})
    plt.rc('legend', **{'fontsize': main_dc['res']['font']['legend']})
    return fig


def add_legend(main_dc, etype, ax_dc, i):
    'Adds a legend to the artist container'
    for u_type in main_dc['res']['usage_type']:
        ax_dc[i].add_artist(ax_dc[i].legend(
            main_dc['res']['artist'][u_type],
            main_dc['res']['legend'][u_type][etype],
            loc=main_dc['res']['legend'][u_type]['loc'],
            title=main_dc['res']['legend'][u_type]['title']))


def multi_stacked_time_plot(main_dc, ax_dc, fig, element_list, regions):
    '''
    Creates a stacked bar plot with stacked bars for all components, that
    have an electricity output and a line plot for all components, that have
    an electricity input.

    For testing new features call: stacked_time_plot(basic_dc)
    without res_dc and region.

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters

    Keyword arguments

    Returns
    '''
    calculate_time_vectors(main_dc)
    i = 0
    if type(element_list) is not list:
        element_list = [element_list, ]
    number_of_subplots = len(element_list) * len(regions)
    for etype in element_list:
        for region in regions:
            i += 1
            logging.info('Creating Plot {0} - {1}'.format(region, etype))

            # Define subplots. If the number of subplots is one,
            # the subplot will be the mainplot.
            ax_dc[i] = fig.add_subplot(number_of_subplots, 1, i)

            # print label for the y-axis
            if main_dc['res']['print']['ylabel']:
                ax_dc[i].set_ylabel("{0} energy".format(
                    main_dc['res']['name'][etype][0]))

            # print label for the x-axis
            if main_dc['res']['print']['xlabel']:
                ax_dc[i].set_xlabel("Hour of the Year")

            # create plots
            main_dc['res']['artist']['generation'] = stackplot_core(main_dc,
                region, etype, ax_dc, i)
            main_dc['res']['artist']['demand'] = lineplot_core(main_dc, region,
                etype, ax_dc, i)

            # set axis tight
            ax_dc[i].axis('tight')

            # print title
            if main_dc['res']['print']['title']:
                main_dc['res']['name'].setdefault(region, region)
                ax_dc[i].set_title("{0} energy in {1}".format(
                    main_dc['res']['name'][etype][0],
                    main_dc['res']['name'][region]))

            # print legend
            if main_dc['res']['print']['legend']:
                add_legend(main_dc, etype, ax_dc, i)

    if main_dc['res']['print']['last_legend']:
        add_legend(main_dc, etype, ax_dc, i)
    if main_dc['res']['print']['last_xlabel']:
        ax_dc[i].set_xlabel(main_dc['res']['xlabel'])
    plot_plot(fig, main_dc)