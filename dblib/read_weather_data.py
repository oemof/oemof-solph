#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import dblib as db


def sql_join_string(year, types):
    r"""
    Creates an sql-string to read all datasets within a given polygon.
    The polygon must be defined in a view named coastdat.pyview.

    Parameters
    ----------
    year : integer
        Year of the needed data series
    types : list
        List of parameters of the coastdat2 dataset.
        Only the following values are available:
        ['ASWDIFD_S', 'ASWDIR_S', 'PS', 'T_2M', 'WSS_10M', 'Z0'].

    Returns
    -------
    string
        sql-string to join the tables of the rli-coastdat2 schema.
    """
    where_str = ""
    for t in types:
        where_str += "dt.name = '{0}' or ".format(t)
    where_str = where_str[:-3]
    return'''
    SELECT tsptyti.*, y.leap
    FROM coastdat.year as y
    INNER JOIN (
        SELECT tsptyd.*, sc.time_id
        FROM coastdat.scheduled as sc
        INNER JOIN (
            SELECT tspty.*, dt.name
            FROM coastdat.datatype as dt
            INNER JOIN (
                SELECT tsp.*, typ.type_id
                FROM coastdat.typified as typ
                INNER JOIN (
                    SELECT spl.*, t.tsarray, t.id
                    FROM coastdat.timeseries as t
                    INNER JOIN (
                        SELECT sps.*, l.data_id
                        FROM (
                            SELECT *
                            FROM coastdat.pyview
                            ) as sps
                        INNER JOIN coastdat.located as l
                        ON (sps.gid = l.spatial_id)) as spl
                    ON (spl.data_id = t.id)) as tsp
                ON (tsp.id = typ.data_id)) as tspty
            ON (tspty.type_id = dt.id)
            where {0}) as tsptyd
        ON (tsptyd.id = sc.data_id))as tsptyti
    ON (tsptyti.time_id = y.year)
    where y.year = {1}
    order by gid, name
    ;'''.format(where_str, year)


def read_coastdat2(main_dt):
    r"""Reads coastdat2 data series for six different parameters from the rli
    postgresql-postgis-database.

    The following dataseries are available [1]_
        * ASWDIFD_S: Diffuse irradiation on a horizontal surface [W/m²]
        * ASWDIR_S: Direct (beam) irradiation on a horizontal surface [W/m²]
        * PS: Atmospheric pressure [Pa]
        * T_2M: Ambient temperature at 2m [K]
        * WSS_10M: Windspeed at 10m [m/s]
        * Z0: Roughness []

    Parameters
    ----------
    main_dc : dictionary
        Main dictionary as described below.

    Returns
    -------
    main_dt['data'] : adding the branch ['data'] to the main_dt dictionary
        Contains the geo-id of the dataset as the dictionary key.
        The timeseries is a numpy array.

    Other Parameters
    ----------------
    main_dt['year'] = integer
        The year of the data set. Not all years from coastdat2 are available.
    main_dt['select'] = string
        Sql string, wich selects a region or a point from the database.

    Raises
    ------
    NoException
        So far no exceptions will be raised.

    See Also
    --------
    dblib.basic_pg.get_db_dict
    dblib.read_weather_data.read_one_coastdat2_set_nns

    Notes
    -----
    Please note that there must be a file named init_local.py in the folder
    named: '[$HOME].python_local/'.
    See the :py:func:`definition of init_local.py <dblib.basic_pg.get_db_dict>`

    References
    ----------
    .. [1] `CoastDat2 <http://www.coastdat.de/data_all/index.php>`_, CoastDat2

    Examples
    --------
    Using this module by clipping the dataset with another polygon:

    .. code:: python

        import dblib as db

        main_dt = {}
        main_dt['year'] = 2012

        main_dt['select'] = '''
            SELECT sp.*
            FROM coastdat.spatial as sp,
                schema.polygon_layer as poly
            WHERE st_contains(poly.geom, sp.geom)
                AND poly.cond_column='condition';
            '''
        db.read_coastdat2(main_dt)
    """
    main_dt['db'] = db.get_db_dict()

    if not 'typelist' in main_dt:
        select_str = "select name from coastdat.datatype;"
        main_dt['typelist'] = []
        tmp = db.execute_read_db(main_dt['db'], select_str)
        for t in tmp:
            main_dt['typelist'].extend(t)

    sql = 'CREATE VIEW coastdat.pyview as'

    # Add the sql string for the selection
    sql += main_dt['select']

    # Connect the two strings.
    sql += sql_join_string(main_dt['year'], main_dt['typelist'])

    data = db.execute_read_db(main_dt['db'], sql)

    count = 0
    main_dt['data'] = {}
    for n in range(len(data) / len(main_dt['typelist'])):
        for c in range(len(main_dt['typelist'])):
            t = data[c][6]
            main_dt['data'].setdefault(data[count][0], {})
            main_dt['data'][data[count][0]][t] = np.array(data[count][3])
            count += 1


def read_one_coastdat2_set_nns(main_dt):
    r"""Using the nearest neighbor search to get the nearest coastdat2 set for
    the given coordinates (lon/lat).

    The following dataseries are available [1]_
        * ASWDIFD_S: Diffuse irradiation on a horizontal surface [W/m²]
        * ASWDIR_S: Direct (beam) irradiation on a horizontal surface [W/m²]
        * PS: Atmospheric pressure [Pa]
        * T_2M: Ambient temperature at 2m [K]
        * WSS_10M: Windspeed at 10m [m/s]
        * Z0: Roughness []

    Parameters
    ----------
    main_dc : dictionary
        Main dictionary as described below.

    Returns
    -------
    main_dt['data'] : adding the branch ['data'] to the main_dt dictionary
        Contains the geo-id of the dataset as the dictionary key.
        The timeseries is a numpy array.

    Other Parameters
    ----------------
    main_dt['year'] = integer
        The year of the data set. Not all years from coastdat2 are available.
    main_dt['coordinate']['lon'] = float
        Longitude of the coordinate (east = positiv).
    main_dt['coordinate']['lat'] = float
        Latitude of the coordinate (east = positiv).

    Raises
    ------
    NoException
        So far no exceptions will be raised.

    See Also
    --------
    dblib.basic_pg.get_db_dict
    dblib.read_weather_data.read_coastdat2

    Notes
    -----
    Please note that there must be a file named init_local.py in the folder
    named: '[$HOME].python_local/'.
    See the :py:func:`definition of init_local.py <dblib.basic_pg.get_db_dict>`

    References
    ----------
    .. [1] `CoastDat2 <http://www.coastdat.de/data_all/index.php>`_, CoastDat2

    Examples
    --------
    Using this module one needs to define only the year, longitude and latitude.

    .. code:: python

        import dblib as db

        main_dt = {}
        main_dt['year'] = 2011
        main_dt['coordinate'] = {}
        main_dt['coordinate']['lon'] = 12.63
        main_dt['coordinate']['lat'] = 51.85

        db.read_one_coastdat2_set_nns(main_dt)

    """
    main_dt['select'] = '''
        SELECT sp.*
        FROM coastdat.cosmoclmgrid sp
        WHERE st_contains(sp.geom, ST_GeomFromText('POINT({0} {1})',4326));
        '''.format(main_dt['coordinate']['lon'], main_dt['coordinate']['lat'])

    read_coastdat2(main_dt)
