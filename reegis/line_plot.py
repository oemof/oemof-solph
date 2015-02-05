#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import matplotlib.pyplot as mpl
import os


def get_p_set():

    line_plot_data = ('/home/likewise-open/RL-INSTITUT/rli-server/' +
            '04_Projekte/026_Berechnungstool/04-Projektinhalte/reegis/Plots/' +
            'line_data.csv')
    p_set = {
        # Allgemeines
        'show': 'yes',  # Soll der Plot angezeigt werden?
        'save': True,  # Soll der Plot gespeichert werden?
        'save_file_type': 'pdf',  # in welchem Format soll der Plot
                                  # gespeichert werden
        'plot_name': 'test_plot',  # Unter welchem Namen soll der Plot
                                   # gespeichert werden
        # Daten
        'datafile': line_plot_data,  # File, das die zu plottenden Daten enthält
        'data_x': None,  # Matrix mit x-Werten
        'data_y': None,  # Matrix mit y-Werten
        'y_axes_number': 2,  # Anzahl der y-Achsen
        # Parameter
        'plot_parameters': {1: {'y_axes': 1,
                                'label': 'plot_1',
                                'marker_type': '-x',
                                'color': 'red',
                                'marker_size': 12,
                                'marker_edge_width': 5},
                            2: {'y_axes': 2,
                                'label': 'plot_2',
                                'marker_type': 'x',
                                'color': 'blue',
                                'marker_size': 12,
                                'marker_edge_width': 5}
                           },
        'figsize': None,  # Größe des Plots
        # Achsenbeschriftung
        'x_label': 'hallo',
        'y1_label': 'ciao',
        'y2_label': 'ciao',
        # Achsenlimits und -einteilung
        'x_limit': [0, 20],
        'y1_limit': [0, 100],
        'y2_limit': [0, 100],
        'x_ticks': [0, 20, 40],
        'y1_ticks': [0, 20, 40],
        'y2_ticks': [0, 20, 40],
        # Beschriftung
        'title': 'Titel',
        'font': 'sans-serif',
        'fontsize': 34,
        'legend_fontsize': 30,
        'loc': 1,  # Legendenposition
        # Gitternetz
        'x_grid': 'yes',
        'y_grid': 'yes'
        }
    return p_set


def read_data_from_file(datafile, column_heading=None):
    '''
    Liest Daten aus einer Datei und gibt sie als Matrix zurück.
    Keyword arguments:
        datafile -- Name des Files mit Pfad (z.B. 'home/test.txt')
        column_heading -- Spaltenüberschrift
    Wie das File beschaffen sein muss:
        - Daten müssen als Spalten vorliegen in der Form [x1, y1, x2, y2...]
        - Zeichentrenner müssen ' ' (Leerzeichen) sein
        - Dezimaltrennzeichen muss ein '.' sein
    '''
    # Öffnen des Files
    data_file = open(datafile, "r")

    # Anzahl der Zeilen und Spalten bestimmen
    if column_heading:
        rows = 1
    else:
        rows = 0
    for line in data_file:
        rows += 1
    columns = len(line.split())
    data = np.zeros((rows, columns))

    # Erneutes Öffnen
    data_file.close()
    data_file = open(datafile, "r")

    # Auslesen der Daten
    counter = 0
    for line in data_file:
        if column_heading:
            if counter > 0:
                values = line.split()
                for i in range(len(values)):
                    data[counter - 1, i] = \
                    float(values[i].replace(";", "", 1))
            counter += 1
        else:
            values = line.split()
            for i in range(len(values)):
                data[counter, i] = float(values[i].replace(";", "", 1))
            counter += 1

    # Schließen des Files
    data_file.close()

    # Aufteilen in x- und y-Werte
    data_x = np.zeros((data.shape[0], data.shape[1] / 2))
    data_y = np.zeros((data.shape[0], data.shape[1] / 2))
    for i in range(data.shape[1]):
        if i % 2 == 0:
            data_x[:, i / 2] = data[:, i]
        else:
            data_y[:, (i - 1) / 2] = data[:, i]

    return data_x, data_y


def line_plot(p_set=None):

    # retrieve p_set if no p_set is given
    if not p_set:
        p_set = get_p_set()

    # Daten auslesen (wenn nötig)
    if p_set['datafile']:
        p_set['data_x'], p_set['data_y'] = \
        read_data_from_file(p_set['datafile'])

    # Erstellen von fig, ax1 und evtl. ax2
    if not p_set['figsize']:
        p_set['figsize'] = [22.0, 14.0]
    fig = mpl.figure(figsize=(p_set['figsize'][0], p_set['figsize'][1]))
    ax1 = fig.add_subplot(1, 1, 1)
    if p_set['y_axes_number'] == 2:
        ax2 = ax1.twinx()

    # Plot
    plots = list(range(p_set['data_x'].shape[1]))
    for i in range(p_set['data_x'].shape[1]):
        if p_set['plot_parameters'][i + 1]['y_axes'] == 1:
            plots[i] = ax1.plot(
                p_set['data_x'][:, i],  # x-Werte
                p_set['data_y'][:, i],  # y-Werte
                p_set['plot_parameters'][i + 1]['marker_type'],  # Marker
                label=
                p_set['plot_parameters'][i + 1]['label'],  # Label in Legende
                color=p_set['plot_parameters'][i + 1]['color'],  # Farbe
                markersize=p_set['plot_parameters'][i + 1]['marker_size'],
                markeredgewidth=
                p_set['plot_parameters'][i + 1]['marker_edge_width']
                )
        elif p_set['plot_parameters'][i + 1]['y_axes'] == 2:
            plots[i] = ax2.plot(
                p_set['data_x'][:, i],  # x-Werte
                p_set['data_y'][:, i],  # y-Werte
                p_set['plot_parameters'][i + 1]['marker_type'],  # Marker
                label=
                p_set['plot_parameters'][i + 1]['label'],  # Label in Legende
                color=p_set['plot_parameters'][i + 1]['color'],  # Farbe
                markersize=p_set['plot_parameters'][i + 1]['marker_size'],
                markeredgewidth=
                p_set['plot_parameters'][i + 1]['marker_edge_width']
                )

    # Achsenbeschriftung
    ax1.set_xlabel(p_set['x_label'])
    ax1.set_ylabel(p_set['y1_label'])
    if p_set['y_axes_number'] == 2:
        ax2.set_ylabel(p_set['y2_label'])

    # Limits
    if p_set['x_limit']:
        ax1.set_xlim([p_set['x_limit'][0], p_set['x_limit'][1]])
        if p_set['y_axes_number'] == 2:
            ax2.set_xlim([p_set['x_limit'][0], p_set['x_limit'][1]])
    if p_set['y1_limit']:
        ax1.set_ylim([p_set['y1_limit'][0], p_set['y1_limit'][1]])
    if p_set['y_axes_number'] == 2:
        if p_set['y2_limit']:
            ax2.set_ylim([p_set['y2_limit'][0], p_set['y2_limit'][1]])

    # Achsenticks
    if p_set['x_ticks']:
        ax1.xaxis.set_ticks(p_set['x_ticks'])
        if p_set['y_axes_number'] == 2:
            ax2.xaxis.set_ticks(p_set['x_ticks'])
    if p_set['y1_ticks']:
        ax1.yaxis.set_ticks(p_set['y1_ticks'])
    if p_set['y_axes_number'] == 2:
        if p_set['y2_ticks']:
            ax2.yaxis.set_ticks(p_set['y2_ticks'])

    # Schriftgröße
    mpl.rcParams.update({'font.size': p_set['fontsize']})
    mpl.rc('legend', **{'fontsize': p_set['legend_fontsize']})
    mpl.rc('font', **{'family': p_set['font']})

    # Titel
    if p_set['title']:
        mpl.title(p_set['title'])

    # Legende
    lines = plots[0]
    for i in range(p_set['data_x'].shape[1]):
        if i > 0:
            lines += plots[i]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc=p_set['loc'], numpoints=1)

    # Gitter
    if p_set['x_grid']:
        ax1.xaxis.grid(True)
    if p_set['y_grid']:
        ax1.yaxis.grid(True)

    # Anzeigen
    if p_set['show']:
        mpl.show(fig)

    # Speichern
    if p_set['save']:
        save_file = (str(p_set['plot_name']) + '.' +
            str(p_set['save_file_type']))
        fig.savefig(os.path.join(os.path.expanduser("~"), save_file))

    return