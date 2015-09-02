#!/usr/bin/python
# -*- coding: utf-8

'''
BaseMap example based on by tutorial 10 by geophysique.be
You need the following toolboxes installed:
numpy, matplotlib, basemap and psycopg2
'''
import matplotlib.pyplot as plt
import sys
import numpy as np
from os.path import expanduser
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap
from shapely.wkt import loads as wkt_loads
import math


def get_bounding_box(main_dt):
    '''Get bounding box of given geometry of write it to main_dt'''

    # min/max start values for x*,y*
    x1 = 180
    x2 = -180
    y1 = 90
    y2 = -90

    # get bounding box from database
    for plot_region in main_dt['geo_tables']:
        bb_sel_str = '''select box2d(st_union(st_simplify(
            {geo_col}, {0}))) from {schema}.{table}
            where {where_col} {where_cond};'''.format(
            main_dt['geo_tables'][plot_region]['simp_tolerance_bb'],
            **main_dt['geo_tables'][plot_region])
        bb_str = rdb.execute_read_db(main_dt['db'], bb_sel_str)[0][0]
        bb_list = create_list_box(bb_str)
        if x1 > float(bb_list[0]):
            x1 = float(bb_list[0])
        if x2 < float(bb_list[2]):
            x2 = float(bb_list[2])
        if y1 > float(bb_list[1]):
            y1 = float(bb_list[1])
        if y2 < float(bb_list[3]):
            y2 = float(bb_list[3])

    # write into data tree
    main_dt['x1'] = x1
    main_dt['x2'] = x2
    main_dt['y1'] = y1
    main_dt['y2'] = y2


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
        main_dt.setdefault('colorbar_extend', 'max')
        main_dt.setdefault('fsize', '15')
        main_dt.setdefault('proj', 'merc')
        main_dt.setdefault('nodata', '#000000')
        main_dt.setdefault('save', True)
        main_dt.setdefault('show', True)
        main_dt.setdefault('x1', None)
        main_dt.setdefault('x2', None)
        main_dt.setdefault('y1', None)
        main_dt.setdefault('y2', None)
        main_dt['geo_tables'][key].setdefault('simp_tolerance_bb', 0.2)
        main_dt.setdefault('epsg', None)
        main_dt.setdefault('cbar', True)
        main_dt.setdefault('figure_format', 'svg')
        main_dt.setdefault('floor_coord_labels', False)
        main_dt.setdefault('coord_system_color', 'black')
        main_dt.setdefault('meridians_dashes', [1, 1])
        main_dt.setdefault('parallels_dashes', [1, 1])
        main_dt.setdefault('transmission', False)


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
        main_dt['geo_tables'][key]['geom'] = main_dt['conn'].execute(
            sql.format(**main_dt['geo_tables'][key])).fetchall()


def create_vectors_multipolygon(main_dt, multipolygon):
    'Create the vectors for MultiPolygons'
    vectors = []
    for polygon in multipolygon:
        seg = []
        for coord in list(polygon.exterior.coords):
            seg.append(main_dt['m'](coord[0], coord[1]))
        vectors.append(np.asarray(seg))
    return vectors


def create_vectors_polygon(main_dt, polygon):
    'Create the vectors for Polygons'
    vectors = []
    seg = []
    for coord in list(polygon.exterior.coords):
        seg.append(main_dt['m'](coord[0], coord[1]))
    vectors.append(np.asarray(seg))
    return vectors


def create_vectors_multilinestring(main_dt, multilinestring):
    'Create the vectors for MulitLineStrings'
    vectors = []
    for linestring in multilinestring:
        seg = []
        for coord in list(list(linestring.coords)):
            seg.append(main_dt['m'](coord[0], coord[1]))
        vectors.append(np.asarray(seg))
    return vectors


def create_vectors_linestring(main_dt, linestring):
    'Create the vectors for LineStrings'
    vectors = []
    seg = []
    for coord in list(list(linestring.coords)):
        seg.append(main_dt['m'](coord[0], coord[1]))
    vectors.append(np.asarray(seg))
    return vectors


def create_list_box(box_str):
    '''Converts box representation of geom to list'''

    box_str = box_str.replace("BOX", "")
    tmp_str = box_str.replace("(", "").replace(")", "")
    tmp_str = tmp_str.replace(",", " ").split(" ")
    return tmp_str


def create_list_point(point_str):
    '''Converts box representation of geom to list'''

    point_str = point_str.replace("POINT", "")
    tmp_str = point_str.replace("(", "").replace(")", "")
    tmp_str = tmp_str.replace(",", " ").split(" ")
    return tmp_str


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
    '''
    Check for the geometry type and
    call the appropriate function to create the vectors
    '''
    if mp.geom_type == 'MultiPolygon':
        vectors = create_vectors_multipolygon(main_dt, mp)
    elif mp.geom_type == 'Polygon':
        vectors = create_vectors_polygon(main_dt, mp)
    elif mp.geom_type == 'MultiLineString':
        vectors = create_vectors_multilinestring(main_dt, mp)
    elif mp.geom_type == 'LineString':
        vectors = create_vectors_linestring(main_dt, mp)
    else:
        print (mp.geom_type)
        sys.exit(
            "ERROR: So far only (multi-)polygons and lines are supported.")
    return vectors


def create_geoplot(main_dt, key):
    ''
    if main_dt['geo_tables'][key]['facecolor'] == 'data':
        cmap = plt.get_cmap(main_dt['color_map'])
        get_maximum_and_minimum_value(main_dt, key)

    for mp in main_dt['geo_tables'][key]['geom']:
        vectors = get_vectors_from_postgis_map(main_dt, wkt_loads(mp[1]))
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
        resolution='i', epsg=main_dt['epsg'], projection=main_dt['proj'],
        llcrnrlat=main_dt['y1'], urcrnrlat=main_dt['y2'],
        llcrnrlon=main_dt['x1'], urcrnrlon=main_dt['x2'],
        lat_ts=(main_dt['x1'] + main_dt['x2']) / 2)
    main_dt['m'].drawcountries(linewidth=0.5, color='white')
    main_dt['m'].drawcoastlines(linewidth=0.5, color='white')
    # main_dt['m'].fillcontinents()
    # main_dt['m'].drawmapboundary(fill_color='white')
    # main_dt['m'].fillcontinents(color='lightgrey', lake_color='aqua')
    # main_dt['m'].shadedrelief()
    # main_dt['m'].etopo()
    # main_dt['m'].bluemarble()


def draw_legend(main_dt, minvalue, maxvalue):
    ''
    legendlable = main_dt['legendlable']
    dataarray = np.clip(np.random.randn(250, 250), -1, 1)
    cax = main_dt['ax'].imshow(
        dataarray, interpolation='nearest',
        vmin=minvalue, vmax=maxvalue, cmap=plt.get_cmap(main_dt['color_map']))
    if main_dt['colorbar_extend'] is None:
        cbar = main_dt['m'].colorbar(
            cax, location='bottom', pad="5%")
    else:
        cbar = main_dt['m'].colorbar(
            cax, location='bottom', pad="5%",
            extend=main_dt['colorbar_extend'])
    cbar.set_label(legendlable, size=main_dt['fsize'])
    cbar.ax.tick_params(labelsize=main_dt['fsize'])
    cbar.set_clim(minvalue, maxvalue)

    m0 = int(minvalue)  # colorbar min value
    m4 = int(maxvalue)  # colorbar max value
    m1 = int(1 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 1
    m2 = int(2 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 2
    m3 = int(3 * (m4 - m0) / 4.0 + m0)  # colorbar mid value 3
    cbar.set_ticks([m0, m1, m2, m3, m4])
    cbar.set_ticklabels([m0, m1, m2, m3, m4])


def draw_coordinate_system(main_dt):
    'Draws parallels and meridians.'
    # Draw parallels and meridians
    if main_dt['floor_coord_labels']:
        main_dt['m'].drawparallels(
            np.arange(
                math.floor(main_dt['y1']), math.floor(main_dt['y2']),
                main_dt['grid_parts']), labels=[1, 0, 0, 0],
            color=main_dt['coord_system_color'],
            dashes=main_dt['parallels_dashes'], labelstyle='+/-',
            linewidth=0.2, fontsize=main_dt['fsize'])
        main_dt['m'].drawmeridians(
            np.arange(
                math.floor(main_dt['x1']), math.floor(main_dt['x2']),
                main_dt['grid_parts']), labels=[0, 0, 0, 1],
            color=main_dt['coord_system_color'],
            dashes=main_dt['meridians_dashes'], labelstyle='+/-',
            linewidth=0.2, fontsize=main_dt['fsize'])
    else:
        main_dt['m'].drawparallels(
            np.arange(main_dt['y1'], main_dt['y2'], main_dt['grid_parts']),
            labels=[1, 0, 0, 0], color=main_dt['coord_system_color'],
            dashes=main_dt['parallels_dashes'], labelstyle='+/-',
            linewidth=0.2, fontsize=main_dt['fsize'])
        main_dt['m'].drawmeridians(
            np.arange(main_dt['x1'], main_dt['x2'], main_dt['grid_parts']),
            labels=[0, 0, 0, 1], color=main_dt['coord_system_color'],
            dashes=main_dt['meridians_dashes'], labelstyle='+/-',
            linewidth=0.2, fontsize=main_dt['fsize'])


def get_trm_line_coordinates(main_dt, region_list, tr):
    '''Returns start and end coordinates of transmission lines'''

    main_dt['db'] = bdb.get_db_dict()

    # divide trm_line name in from and to region
    tr_split = tr.split('-')
    from_region = tr_split[0]
    to_region = tr_split[1]

    # create from and to region execution string
    exec_str_from = '''select st_astext(st_centroid({0})) from {1}.{2}
        where {3} = '{4}';
        '''.format(
        main_dt['geo_tables']['entsoe-eu']['geo_col'],
        main_dt['geo_tables'][region_list]['schema'],
        main_dt['geo_tables'][region_list]['table'],
        main_dt['geo_tables'][region_list]['id_col'], from_region.upper())
    exec_str_to = '''select st_astext(st_centroid({0})) from {1}.{2}
        where {3} = '{4}';
        '''.format(
        main_dt['geo_tables'][region_list]['geo_col'],
        main_dt['geo_tables'][region_list]['schema'],
        main_dt['geo_tables'][region_list]['table'],
        main_dt['geo_tables'][region_list]['id_col'], to_region.upper())

    # retrieve coordinate pairs from database
    coords_from = create_list_point(
        rdb.execute_read_db(main_dt['db'],
                            exec_str_from)[0][0])
    coords_to = create_list_point(
        rdb.execute_read_db(main_dt['db'],
                            exec_str_to)[0][0])

    # write into dict, convert to float
    coord_dc = {}
    coord_dc['from_lat'] = float(coords_from[1])
    coord_dc['from_lon'] = float(coords_from[0])
    coord_dc['to_lat'] = float(coords_to[1])
    coord_dc['to_lon'] = float(coords_to[0])

    # convert to map coordinates
    coord_dc['x_from'], coord_dc['y_from'] = main_dt['m'](
        coord_dc['from_lon'],
        coord_dc['from_lat'])
    coord_dc['x_to'], coord_dc['y_to'] = main_dt['m'](
        coord_dc['to_lon'],
        coord_dc['to_lat'])

    return coord_dc


def get_trm_lines_by_scenario(main_dt, scenario):
    '''Returns list of transmission line belonging to scenario'''

    main_dt['db'] = bdb.get_db_dict()

    energy_system = rdb.fetch_columns(
        main_dt['db'], 'pahesmf_dev_sim',
        'scenarios', 'energy_system', where_column='name_set',
        where_condition=scenario)['energy_system'][0]
    energy_system_transmission = rdb.fetch_columns(
        main_dt['db'],
        'pahesmf_dev_sim', 'energy_system', 'energy_system_transmission',
        where_column='name_set',
        where_condition=energy_system)['energy_system_transmission'][0]
    trm_lines = rdb.fetch_columns(
        main_dt['db'], 'pahesmf_dev_sim',
        'energy_system_transmission', 'name',
        where_column='name_set',
        where_condition=energy_system_transmission)['name']
    return trm_lines


def transmission_capacities(main_dt):
    '''
    Draw transmission capacities on map

    Notes
    -----
    Erfolg einen pfeil AUF eine karte gezeichnet [1]_, [2]_.

    References
    ----------
    .. [1] `http://matthiaseisen.com/matplotlib/shapes/arrow/`_
    .. [2] `http://stackoverflow.com/questions/27926513/how-to-draw-an-arrow-on-an-basemap-object-using-matplotlib`_
    '''

    # lat1 = 52.5  # berlin
    # lon1 = 13.5
    # lat2 = 52.25  # nahe warschau
    # lon2 = 42 #21.0
    # lat3 = 52.25  # warschau
    # lon3 = 21.0

    # x1, y1 = main_dt['m'](lon1, lat1)
    # x2, y2 = main_dt['m'](lon2, lat2)
    # x3, y3 = main_dt['m'](lon3, lat3)

    # plt.text(x3, y3, "Warschau", horizontalalignment='center')

    for region_list in main_dt['plot_region_list']:
        for tr in main_dt['geo_tables'][region_list]['transmission_lines']:
            # get map coordinates of transmission line
            coord_dc = get_trm_line_coordinates(main_dt, region_list, tr)

            # draw transmission line
            plt.arrow(
                coord_dc['x_from'], coord_dc['y_from'],
                coord_dc['x_to'] - coord_dc['x_from'],
                coord_dc['y_to'] - coord_dc['y_from'],
                ec="k", linewidth=4, zorder=2,
                alpha=0.8)


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

        from oemof.outputlib import geoplot as geo

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

        # Define the bounding box alterively by user input
        main_dt['x1'] = 3
        main_dt['x2'] = 16.
        main_dt['y1'] = 47.
        main_dt['y2'] = 56
        main_dt['grid_parts'] = 2
        main_dt['geo_tables']['lk_wtb']['simp_tolerance_bb'] = 0.1
        main_dt['geo_tables']['de_offshore']['simp_tolerance_bb'] = 0.4

        # Write the tables defined above in this list to be plotted.
        # One can define more tables and select the needed ones in this list.
        main_dt['plot_region_list'] = ['de_offshore', 'de_onshore', 'lk_wtb']

        geo.gplot(main_dt)

    Next example.....

    .. code:: python

        from oemof.outputlib import geoplot as geo
        from oemof.dblib import basic_pg as bdb
        from oemof.dblib import read_data_pg as rdb
        from oemof.dblib import write_data_pg as wdb
        import os


        def write_demand_data_table(regions, data_year, column, new=False):
            '''write indicator values of demand data to separate table'''
            main_dt['db'] = bdb.get_db_dict()
            for region in regions:
                # retrieve data
                col = region + '_' + str(data_year)
                sel_str = '''select max({0})/min({0}) from pahesmf_dat
                    .elec_demand_entso_e3;'''.format(col)
                # sel_str = '''select sum({0}) from pahesmf_dat.elec_demand_
                #    entso_e3;'''.format(col)
                data = rdb.execute_read_db(main_dt['db'], sel_str)[0][0]

                # write data to database table
                if new:
                    ins_str = '''insert into tmp_guido.test_data_demand(region,
                        {2}) values('{0}', {1});'''.format(region, data,
                                                           column)
                    wdb.execute_write_db(main_dt['db'], ins_str)

                else:
                    # insert values to existing rows
                    wdb.insert_value(
                        main_dt['db'], 'tmp_guido',
                        'test_data_demand', column, data, 'region', region,
                        numeric=False)


        def get_test_data(keys, column):
            main_dt['db'] = bdb.get_db_dict()
            tmp_dt = {}
            for key in keys:
                tmp_dt[key] = rdb.fetch_columns(
                    main_dt['db'], 'tmp_guido',
                    'test_data_demand', column, where_column='region',
                    where_condition=key)[column][0]
            return tmp_dt

        # fetch region names of given scenario
        regions = [
            'DNK', 'DEU', 'FIN', 'POL', 'XALP', 'XBNL', 'XBAL', 'NOR',
            'SWE', 'XFRA', 'XHUR', 'XCZS', 'XGBR', 'XGMA', 'XIBE', 'XITA',
            'XSKB', 'XFWY']

        # define main data tree
        main_dt = {}
        main_dt['geo_tables'] = {}

        # Europe (Entsoe + EU) 18 regions model
        main_dt['geo_tables']['entsoe-eu'] = {
            'table': 'gadm_countries',
            'geo_col': 'geom',
            'id_col': 'iso',  # 'gid',
            'schema': 'world',
            'simp_tolerance': '0.01',
            'where_col': 'iso',
            'where_cond': 'in {}'.format(tuple(regions))}

        # plot data instead on default face color
        main_dt['geo_tables']['entsoe-eu']['facecolor'] = 'data'

        # create examplary data table with annual demand of 18 entsoe eu
        # regions
        # write_demand_data_table(regions, 2012, 'max_spread_demand')

        # ...either by reading from database table
        # main_dt['geo_tables']['entsoe-eu']['data'] = get_test_data(regions,
        #    'max_spread_demand')

        # ...or by direct input
        main_dt['geo_tables']['entsoe-eu']['data'] = {}
        main_dt['geo_tables']['entsoe-eu']['data']['DEU'] = 2.55043
        main_dt['geo_tables']['entsoe-eu']['data']['DNK'] = 2.97794
        main_dt['geo_tables']['entsoe-eu']['data']['FIN'] = 2.6852
        main_dt['geo_tables']['entsoe-eu']['data']['NOR'] = 2.65042
        main_dt['geo_tables']['entsoe-eu']['data']['POL'] = 2.33107
        main_dt['geo_tables']['entsoe-eu']['data']['SWE'] = 2.85875
        main_dt['geo_tables']['entsoe-eu']['data']['XALP'] = 2.47458
        main_dt['geo_tables']['entsoe-eu']['data']['XBAL'] = 2.97318
        main_dt['geo_tables']['entsoe-eu']['data']['XBNL'] = 2.23776
        main_dt['geo_tables']['entsoe-eu']['data']['XCZS'] = 2.44953
        main_dt['geo_tables']['entsoe-eu']['data']['XFRA'] = 3.31207
        main_dt['geo_tables']['entsoe-eu']['data']['XFWY'] = 2.45466
        main_dt['geo_tables']['entsoe-eu']['data']['XGBR'] = 2.84529
        main_dt['geo_tables']['entsoe-eu']['data']['XGMA'] = 2.78189
        main_dt['geo_tables']['entsoe-eu']['data']['XHUR'] = 2.06565
        main_dt['geo_tables']['entsoe-eu']['data']['XIBE'] = 7.13539
        main_dt['geo_tables']['entsoe-eu']['data']['XITA'] = 2.57917
        main_dt['geo_tables']['entsoe-eu']['data']['XSKB'] = 2.97662

        # bounding box can be defined by user. If at least one coordinate is
        # not
        # given,bounding box will be determined automatically based on given
        # geo_tables
        # main_dt['x1'] = 3
        # main_dt['x2'] = 16.
        # main_dt['y1'] = 47.
        # main_dt['y2'] = 56

        # define resolution of lat/lon grid shown in plot
        main_dt['grid_parts'] = 15

        # simplify tolerance for automatic bounding box definition
        main_dt['geo_tables']['entsoe-eu']['simp_tolerance_bb'] = 0.5

        # print plot to file
        main_dt['plotname'] = os.getcwd() + '/geoplot_entsoe-eu_plain.pdf'
        main_dt['figure_format'] = 'pdf'
        main_dt['show'] = False

        # plot title, axes and other formatting
        main_dt['plottitle'] = 'Maximum spread of demand'
        main_dt['legendlable'] = 'Max(demand(t))/min(demand(t)) of year 2012'
        main_dt['floor_coord_labels'] = True

        # Write the tables defined above in this list to be plotted.
        # One can define more tables and select the needed ones in this list.
        main_dt['plot_region_list'] = ['entsoe-eu']

        geo.gplot(main_dt)
    """
    # Sets the default values
    set_default_values(main_dt)

    # Define bounding box, if not given by user
    if ((main_dt['x1'] is None) or (main_dt['x2'] is None) or
            (main_dt['y1'] is None) or (main_dt['y2'] is None)):
        get_bounding_box(main_dt)

    # Creates plot figure
    create_plot(main_dt)

    # Creates Basemap
    create_basemap(main_dt)
    draw_coordinate_system(main_dt)

    # draw transmission capacities
    if main_dt['transmission'] is True:
        transmission_capacities(main_dt)

    # Draw geometries
    fetch_geometries(main_dt)
    for key in main_dt['plot_region_list']:
        create_geoplot(main_dt, key)
        if 'maxvalue' in main_dt['geo_tables'][key]:
            maxvalue = main_dt['geo_tables'][key].pop('maxvalue')
            minvalue = main_dt['geo_tables'][key].pop('minvalue')
            if main_dt.get('cbar', []):
                draw_legend(main_dt, minvalue, maxvalue)

    # save and show plot
    plt.tight_layout()
    if main_dt['save']:
        plt.savefig(main_dt['plotname'], dpi=150,
                    format=main_dt['figure_format'])
    if main_dt['show']:
        plt.show()
    else:
        plt.close()
