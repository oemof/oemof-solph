#!/usr/bin/python
# -*- coding: utf-8
#
# BaseMap example based on by tutorial 10 by geophysique.be
# You need the following toolboxes installed:
# numpy, matplotlib, basemap and psycopg2

import sys
import os
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection


def connect2db(dic):
    '''
    Open database connection using the values of a dictionary.
    The dictionary must contain at least the following values:
        ip: the ip of the database server
        db: the name of the database
        user: the name of the database user
        password: the password of the database user
    '''
    conn = psycopg2.connect('''host=%s dbname=%s user=%s password=%s
    ''' % (dic['ip'], dic['db'], dic['user'], dic['password']))
    return conn


def close_db(cur, conn, commit=False):
    '''
    Close open database connection while "cur" and "conn" are connection objects
    Use "commit=True" if you want to write the changes to the database
    '''
    if commit:
        conn.commit()
    cur.close()
    conn.close()


def convert_coordinates(m, polygon):
    seg = []
    for coord in polygon.split(","):
        seg.append(m(float(coord.split()[0]), float(coord.split()[1])))
    return seg


def fetch_data(dico, name_geo_column, name_data_column, schema, table,
        base_column=None):
    conn = connect2db(dico)
    cur = conn.cursor()
    cur.execute('''
    select ST_AsText(%s) from %s.%s order by "ID";
    ''' % (name_geo_column, schema, table))
    geo_data = cur.fetchall()
    if base_column is None:
        cur.execute('''
        select %s from %s.%s order by "ID";
        ''' % (name_data_column, schema, table))
        out_data = np.array(cur.fetchall())[:, 0]
    else:
        cur.execute('''
        select %s,"%s" from %s.%s order by "ID";
        ''' % (name_data_column, base_column, schema, table))
        tmp_data = np.array(cur.fetchall())
        out_data = tmp_data[:, 0] / tmp_data[:, 1]
    close_db(cur, conn)
    return geo_data, out_data


def create_figure(plottitle, fsize):
    mpl.rcParams['font.size'] = fsize - 3
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['axes.labelsize'] = 8.
    mpl.rcParams['xtick.labelsize'] = 6.
    mpl.rcParams['ytick.labelsize'] = 6.
    fig = plt.figure(figsize=(11.7, 8.3))
    plt.subplots_adjust(left=0.0, right=1.0, top=0.90, bottom=0.10,
        wspace=0.1, hspace=0.05)
    ax = plt.subplot(111)
    ax.set_title(replace_umlaute(plottitle), size=fsize)
    return fig, ax


def create_basemap(map_res, proj, coord):
    '''
    coord = [[x1,y2],[x2,y2]]
    '''
    m = Basemap(resolution=map_res, projection=proj, llcrnrlat=coord[0, 1],
        urcrnrlat=coord[1, 1], llcrnrlon=coord[0, 0], urcrnrlon=coord[1, 0],
        lat_ts=(coord[0, 0] + coord[1, 0]) / 2)
    m.drawcountries(linewidth=0.5)
    m.drawcoastlines(linewidth=0.5)
    #m.fillcontinents()
    #m.drawmapboundary(fill_color='white')
    #m.fillcontinents(color='lightgrey',lake_color='aqua')
    #m.shadedrelief()
    #m.etopo()
    #m.bluemarble()
    return m


def draw_grid(m, grid_parts, coord):
    m.drawparallels(np.arange(coord[0, 1], coord[1, 1], grid_parts),
        labels=[1, 0, 0, 0], color='black', dashes=[1, 0.1], labelstyle='+/-',
        linewidth=0.2)
    m.drawmeridians(np.arange(coord[0, 0], coord[0, 1], grid_parts),
        labels=[0, 0, 0, 1], color='black', dashes=[1, 0.1], labelstyle='+/-',
        linewidth=0.2)
    return m


def draw_polygons(m, ax, geo_data, out_data, color_map, maxvalue,
        unit_adaptation, plot_values, l_width, text_coord):
    cmap = plt.get_cmap(color_map)
    nr = 0
    for mp in geo_data:
        multipolygon = []
        if (mp[0].find('POLYGON', 0, 30) > -1
                and mp[0].find('MULTIPOLYGON', 0, 30) < 0):
            mp = mp[0].replace("POLYGON", "")
            mp = mp.replace("((", "")
            mp = mp.replace("))", "")
            multipolygon.append(np.asarray(convert_coordinates(m, mp)))
        elif mp[0].find('MULTIPOLYGON', 0, 30) > -1:
            mp = mp[0].replace("MULTIPOLYGON", "")
            mp = mp.replace("(((", "(")
            mp = mp.replace(")))", ")")
            for polygon in mp.split("),("):
                polygon = polygon.replace("(", "")
                polygon = polygon.replace(")", "")
                multipolygon.append(np.asarray(convert_coordinates(m, polygon)))
        else:
            print ((mp[0][0:30] + '...'))
            sys.exit('''ERROR: So far only polygons and multipolygons
                are supported''')
        lines = LineCollection(multipolygon, antialiaseds=(1, ))
        out_value = out_data[nr]
        #print out_value
        if out_value is None:
            out_value = 0
        else:
            out_value = out_value * unit_adaptation
        lines.set_facecolors(cmap(float(out_value) / float(maxvalue)))
        lines.set_edgecolors('k')
        lines.set_linewidth(l_width)
        ax.add_collection(lines)
        if plot_values:
            x, y = m(text_coord[nr, 0], text_coord[nr, 1])
            text = str(round(out_value, 1))
            plt.text(x, y, text, fontsize=14, fontweight='bold', ha='center',
                va='center', color='black', backgroundcolor='w')
        nr = nr + 1
    return m, ax


def draw_legend(m, ax, color_map, maxvalue, legendlable, fsize):
    dataarray = np.clip(np.random.randn(250, 250), -1, 1)
    cax = ax.imshow(dataarray, interpolation='nearest',
        vmin=0, vmax=maxvalue, cmap=plt.get_cmap(color_map))
    cbar = m.colorbar(cax, location='bottom', pad="5%", extend='max')
    cbar.set_label(replace_umlaute(legendlable), size=fsize)
    cbar.ax.tick_params(labelsize=fsize)
    m0 = 0  # colorbar min value
    m4 = maxvalue  # colorbar max value
    m1 = int(1 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 1
    m2 = int(2 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 2
    m3 = int(3 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 3
    cbar.set_ticks([m0, m1, m2, m3, m4])
    cbar.set_ticklabels([m0, m1, m2, m3, m4])
    return m, ax, cbar


def create_map_plot(db_p, p):
    geo_data, out_data = fetch_data(db_p, p['db_geo_column'],
        p['data_column'], p['db_schema'], p['db_view'], p['db_base_column'])
    fig, ax = create_figure(p['title'], p['plot_fontsize'])
    m = create_basemap(p['map_resolution'], p['map_projection'],
            p['map_coordinates'])
    m = draw_grid(m, p['map_grid_parts'], p['map_coordinates'])
    m, ax = draw_polygons(m, ax, geo_data, out_data, p['color_map'],
            p['maxvalue'], p['unit_adaptation'], p['plot_values'],
            p['plot_line_width'], p['plot_text_coord'])
    m, ax, cbar = draw_legend(m, ax, p['color_map'], p['maxvalue'],
            p['legendlable'], p['plot_fontsize'])
    if p['plot_values']:
        plotname = (p['save_file_name'] + '_plot_with_values.' +
            p['save_file_type'])
    else:
        plotname = (p['save_file_name'] + '_plot.' + p['save_file_type'])
    plotname = replace_umlaute(plotname)
    plotname = os.path.join(p['save_file_folder'], plotname)
    if p['save_file']:
        plt.savefig(plotname, dpi=p['save_file_res'])
    if p['show_plot']:
        plt.show()


def replace_umlaute(string):
    string = string.replace('ä', 'ae')
    string = string.replace('ü', 'ue')
    string = string.replace('ö', 'oe')
    string = string.replace('Ä', 'Ae')
    string = string.replace('Ü', 'Ue')
    string = string.replace('Ö', 'Oe')
    string = string.replace('ß', 'ss')
    return string


def exists_column(dic, schema, table_name, column_name):
    '''
    Checks if table exists and returns true or false
    '''
    conn = connect2db(dic)
    cur = conn.cursor()
    cur.execute('''
    select column_name from information_schema.columns
    where table_schema = '%s'
    and table_name = '%s';
    ''' % (schema, table_name))
    column_names = np.array(cur.fetchall())
    close_db(cur, conn)
    return column_name in column_names


def unique_values(dic, schema, table, column_value,
        column_where=None, where_name=None):
    conn = connect2db(dic)
    cur = conn.cursor()
    if column_where is None:
        cur.execute('''
            SELECT %s FROM %s.%s;
            ''' % (column_value, schema, table))
    else:
        cur.execute('''
            SELECT %s FROM %s.%s where %s = '%s';
            ''' % (column_value, schema, table, column_where, where_name))
    return list({}.fromkeys(cur.fetchall()).keys())


def determine_colum_names_from_values(dic, p):
    '''
    Reads values from a table (table_from) with a special condition
    (where_column, where_name) and create columns named by this values in
    a second table (table_to)
    '''
    categories = []
    columns = []
    for col in unique_values(dic, p['db_schema'], p['table_from'],
                    p['value_column'], p['where_column'], p['where_name']):
        categories.append(col[0])
        col = col[0]
        col = col.replace(' ', '_')
        col = col.replace('.', '')
        col = col.replace(',', '')
        columns.append('area_' + col.lower())
    return columns, categories