#!/usr/bin/python
# -*- coding: utf-8

'''
BaseMap example based on by tutorial 10 by geophysique.be
You need the following toolboxes installed:
numpy, matplotlib, basemap and psycopg2
'''

import sys
import dblib as db
import numpy as np
import matplotlib.pyplot as plt
from os.path import expanduser
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap


def set_default_values(main_dt):
    'Set default values.'
    home = expanduser("~")
    for key in main_dt['plot_region_list']:
        main_dt['geo_tables'][key].setdefault('facecolor', '#badd69')
        main_dt['geo_tables'][key].setdefault('edgecolor', '#ffffff')
        main_dt['geo_tables'][key].setdefault('linewidth', '1')
        main_dt['geo_tables'][key].setdefault('geo_col', 'geom')
        main_dt['geo_tables'][key].setdefault('id_col', 'gid')
        main_dt.setdefault('plotname', home + '/geoplot.svg')
        main_dt.setdefault('plottitle', 'Plottitel')
        main_dt.setdefault('legendlable', 'Lable of legend')
        main_dt.setdefault('color_map', 'seismic')
        main_dt.setdefault('fsize', '15')
        main_dt.setdefault('proj', 'merc')
        main_dt.setdefault('nodata', '#000000')
        main_dt.setdefault('save', True)
        main_dt.setdefault('show', True)


def convert_coordinates(m, polygon):
    'Converts the coordinates to the given projection.'
    seg = []
    for coord in polygon.split(","):
        seg.append(m(float(coord.split()[0]), float(coord.split()[1])))
    return seg


def fetch_geometries(main_dt):
    '''
    Reads the geometry and the id of all given tables and writes it to the
    'geom'-key of each branch.
    '''
    select_str = 'SELECT {id_col}, ST_AsText('
    simp_true = '''
        ST_SIMPLIFY({geo_col},{simp_tolerance})) FROM {schema}.{table} '''
    simp_false = '''
        {geo_col}) FROM {schema}.{table} '''
    where_str = '''
        WHERE "{where_col}" {where_cond} '''
    order_str = 'ORDER BY {id_col} DESC;'

    for key in main_dt['plot_region_list']:
        sql = select_str

        # Adds st_simplify if simp_tolerance is defined in the datatree
        if 'simp_tolerance' in main_dt['geo_tables'][key]:
            sql += simp_true
        else:
            sql += simp_false

        # Adds the where condition if a where column is defined in the datatree
        if 'where_col' in main_dt['geo_tables'][key]:
            sql += where_str

        # Adds ORDER BY to order the output by id
        sql += order_str

        # Reads the geometry and the id and writes it to the 'geom'-key
        main_dt['geo_tables'][key]['geom'] = db.execute_read_db(
            main_dt['db'], sql.format(**main_dt['geo_tables'][key]))


def create_vectors_multipolygon(main_dt, mp):
    ''
    vectors = []
    mp = mp[1].replace("MULTIPOLYGON", "")
    mp = mp.replace("(((", "(")
    mp = mp.replace(")))", ")")
    for polygon in mp.split("),("):
        polygon = polygon.replace("(", "")
        polygon = polygon.replace(")", "")
        vectors.append(np.asarray(convert_coordinates(main_dt['m'], polygon)))
    return vectors


def create_vectors_polygon(main_dt, mp):
    ''
    vectors = []
    mp = mp[1].replace("POLYGON", "")
    mp = mp.replace("((", "")
    mp = mp.replace("))", "")
    vectors.append(np.asarray(convert_coordinates(main_dt['m'], mp)))
    return vectors


def create_vectors_lines(main_dt, mp):
    ''
    vectors = []
    mp = mp[1].replace("LINESTRING", "")
    mp = mp.replace("(", "")
    mp = mp.replace(")", "")
    vectors.append(np.asarray(convert_coordinates(main_dt['m'], mp)))
    return vectors


def get_maximum_and_minimum_value(main_dt, key):
    '''
    Gets the maximum and minimum value of the whole data dictionary branch,
    if not set.
    '''
    if 'minvalue' in main_dt['geo_tables'][key]:
        minvalue = main_dt['geo_tables'][key]['minvalue']
    else:
        minvalue = float("inf")
        for c in list(main_dt['geo_tables'][key]['data'].keys()):
            if minvalue > main_dt['geo_tables'][key]['data'][c]:
                minvalue = main_dt['geo_tables'][key]['data'][c]
        main_dt['geo_tables'][key]['minvalue'] = minvalue
    if 'maxvalue' in main_dt['geo_tables'][key]:
        maxvalue = main_dt['geo_tables'][key]['maxvalue']
    else:
        maxvalue = 0
        for c in list(main_dt['geo_tables'][key]['data'].keys()):
            if maxvalue < main_dt['geo_tables'][key]['data'][c]:
                maxvalue = main_dt['geo_tables'][key]['data'][c]
        main_dt['geo_tables'][key]['maxvalue'] = maxvalue


def get_vectors_from_postgis_map(main_dt, mp):
    ''
    if (mp[1].find('POLYGON', 0, 30) > -1
            and mp[1].find('MULTIPOLYGON', 0, 30) < 0):
        vectors = create_vectors_polygon(main_dt, mp)
    elif (mp[1].find('LINESTRING', 0, 30) > -1):
        vectors = create_vectors_lines(main_dt, mp)
    elif mp[1].find('MULTIPOLYGON', 0, 30) > -1:
        vectors = create_vectors_multipolygon(main_dt, mp)
    else:
        print ((mp[1][0:30] + '...'))
        sys.exit(
            "ERROR: So far only (multi-)polygons and lines are supported.")
    return vectors


def create_geoplot(main_dt, key):
    ''
    if main_dt['geo_tables'][key]['facecolor'] == 'data':
        cmap = plt.get_cmap(main_dt['color_map'])
        get_maximum_and_minimum_value(main_dt, key)

    for mp in main_dt['geo_tables'][key]['geom']:
        vectors = get_vectors_from_postgis_map(main_dt, mp)
        lines = LineCollection(vectors, antialiaseds=(1, ))
        if main_dt['geo_tables'][key]['facecolor'] == 'data':
            if mp[0] in main_dt['geo_tables'][key]['data']:
                lines.set_facecolors(cmap(
                    (float(main_dt['geo_tables'][key]['data'][mp[0]]) - (
                        float(main_dt['geo_tables'][key]['minvalue']))) / (
                        float(main_dt['geo_tables'][key]['maxvalue']) - (
                            float(main_dt['geo_tables'][key]['minvalue'])))))
            else:
                lines.set_facecolors(main_dt['nodata'])
        elif main_dt['geo_tables'][key]['facecolor'] is not None:
            lines.set_facecolors(main_dt['geo_tables'][key]['facecolor'])
        if 'alpha' in main_dt['geo_tables'][key]:
            lines.set_alpha(main_dt['geo_tables'][key]['alpha'])
        lines.set_edgecolors(main_dt['geo_tables'][key]['edgecolor'])
        lines.set_linewidth(main_dt['geo_tables'][key]['linewidth'])
        main_dt['ax'].add_collection(lines)


def create_plot(main_dt):
    'Creates the basic plot object.'
    main_dt['ax'] = plt.subplot(111)
    plt.box(on=None)
    main_dt['ax'].set_title(main_dt['plottitle'], size=main_dt['fsize'])


def create_basemap(main_dt):
    'Creates the basemap.'
    main_dt['m'] = Basemap(
        resolution='i', projection=main_dt['proj'],
        llcrnrlat=main_dt['y1'], urcrnrlat=main_dt['y2'],
        llcrnrlon=main_dt['x1'], urcrnrlon=main_dt['x2'],
        lat_ts=(main_dt['x1'] + main_dt['x2']) / 2)
    main_dt['m'].drawcountries(linewidth=0.5, color='white')
    main_dt['m'].drawcoastlines(linewidth=0.5, color='white')
    #main_dt['m'].fillcontinents()
    #main_dt['m'].drawmapboundary(fill_color='white')
    #main_dt['m'].fillcontinents(color='lightgrey', lake_color='aqua')
    #main_dt['m'].shadedrelief()
    #main_dt['m'].etopo()
    #main_dt['m'].bluemarble()


def draw_legend(main_dt, minvalue, maxvalue):
    ''
    legendlable = main_dt['legendlable']
    dataarray = np.clip(np.random.randn(250, 250), -1, 1)
    cax = main_dt['ax'].imshow(
        dataarray, interpolation='nearest',
        vmin=minvalue, vmax=maxvalue, cmap=plt.get_cmap(main_dt['color_map']))
    cbar = main_dt['m'].colorbar(
        cax, location='bottom', pad="5%", extend='max')
    cbar.set_label(legendlable, size=main_dt['fsize'])
    cbar.ax.tick_params(labelsize=main_dt['fsize'])
    cbar.set_clim(minvalue, maxvalue)

    m0 = int(minvalue + 1)  # colorbar min value
    m4 = int(maxvalue)  # colorbar max value
    m1 = int(1 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 1
    m2 = int(2 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 2
    m3 = int(3 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 3
    cbar.set_ticks([m0, m1, m2, m3, m4])
    cbar.set_ticklabels([m0, m1, m2, m3, m4])


def draw_coordinate_system(main_dt):
    'Draws parallels and meridians.'
    # Draw parallels and meridians
    main_dt['m'].drawparallels(
        np.arange(main_dt['y1'], main_dt['y2'], main_dt['grid_parts']),
        labels=[1, 0, 0, 0], color='black', dashes=[1, 0.1], labelstyle='+/-',
        linewidth=0.2)
    main_dt['m'].drawmeridians(
        np.arange(main_dt['x1'], main_dt['x2'], main_dt['grid_parts']),
        labels=[0, 0, 0, 1], color='black', dashes=[1, 0.1], labelstyle='+/-',
        linewidth=0.2)


def gplot(main_dt):
    r"""Plots geographic tables from a postgis database. The table needs an id
    column and a geographic column in the postgis wkb format.

    The function is base on the tutorial 10 by geophysique.be. [1]_

    Parameters
    ----------
    main_dt : dictionary
        Main dictionary as described below.

    Other Parameters
    ----------------
    main_dt['geo_tables'] : dictionary
        Dictionary with a least the definition of the tabel and the schema.
        All the other values will get the default value. This will not work for
        all tables. Default id colum: 'gid', default geometry column: 'geom'.
    main_dt['x1'/'x2'] : float
        longitude for the left (x1) and right (x2) corner (east = positiv).
    main_dt['y1'/'y2'] : float
        latitude for the lower (y1) and upper (y2) corner (north = positiv).
    main_dt['grid_parts'] : integer
        parts to devide the coordinate system grid
    main_dt['plot_region_list'] : list
        list of keys of the ['geo_tables'] branch to be plotted


    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    dblib.basic_pg.get_db_dict

    Notes
    -----
    Please note that there must be a file named init_local.py in the folder
    named: '[$HOME].python_local/'.
    See :py:func:`definition of init_local.py <dblib.basic_pg.get_db_dict>`.

    References
    ----------
    .. [1] `Géophysique.be <http://www.geophysique.be/tutorials/>`_

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    .. code:: python

        import outputlib as out

        main_dt = {}
        main_dt['geo_tables'] = {}

        # Germany off-shore regions (ZNES)
        main_dt['geo_tables']['de_offshore'] = {
            'table': 'deu3_21',
            'geo_col': 'geom',
            'id_col': 'region_id',
            'schema': 'deutschland',
            'simp_tolerance': '0.01',
            'where_col': 'region_id',
            'where_cond': '> 11018',
            'facecolor': '#a5bfdd'
            }

        # Germany dena_18 regions (ZNES)
        main_dt['geo_tables']['de_onshore'] = {
            'table': 'deu3_21',
            'geo_col': 'geom',
            'id_col': 'region_id',
            'schema': 'deutschland',
            'simp_tolerance': '0.01',
            'where_col': 'region_id',
            'where_cond': '< 11019'
            }

        # Landkreis Wittenberg
        main_dt['geo_tables']['lk_wtb'] = {
            'table': 'gemeinden',
            'geo_col': 'the_geom',
            'id_col': 'ogc_fid',
            'schema': 'wittenberg',
            'simp_tolerance': '0.01',
            'where_col': 'admin_leve',
            'where_cond': "= '6'",
            'facecolor': '#aa0000'
            }

        # Define the bounding box
        main_dt['x1'] = 3
        main_dt['x2'] = 16.
        main_dt['y1'] = 47.
        main_dt['y2'] = 56
        main_dt['grid_parts'] = 2

        # Write the tables defined above in this list to be plotted.
        # One can define more tables and select the needed ones in this list.
        main_dt['plot_region_list'] = ['de_offshore', 'de_onshore', 'lk_wtb']

        out.gplot(main_dt)
    """
    main_dt['db'] = db.get_db_dict()

    # Define bounding box
    # This should be a result of postgis.

    # Sets the default values
    set_default_values(main_dt)

    #Creates plot figure
    create_plot(main_dt)

    #Creates Basemap
    create_basemap(main_dt)
    draw_coordinate_system(main_dt)

    #Draw geometries
    fetch_geometries(main_dt)
    for key in main_dt['plot_region_list']:
        create_geoplot(main_dt, key)
        if 'maxvalue' in main_dt['geo_tables'][key]:
            maxvalue = main_dt['geo_tables'][key].pop('maxvalue')
            minvalue = main_dt['geo_tables'][key].pop('minvalue')
            if main_dt['cbar']:
                draw_legend(main_dt, minvalue, maxvalue)

    #save and show plot
    plt.tight_layout()
    if main_dt['save']:
        plt.savefig(main_dt['plotname'], dpi=150, format='svg')
    if main_dt['show']:
        plt.show()
    else:
        plt.close()
