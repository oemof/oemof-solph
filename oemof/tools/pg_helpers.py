# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 11:08:15 2015

This is a collection of helper functions which work on there own an can be
used by various classes. If there are too many helper-functions, they will
be sorted in different modules.

All special import should be in try/except loops to avoid import errors.
"""

import logging
import pandas as pd
import numpy as np
from pytz import timezone
from datetime import datetime
from feedinlib import weather


# get_polygon_from_nuts
hlp_fkt = 'get_polygon_from_nuts'
try:
    from shapely.wkt import loads as wkt_loads
except:
    logging.info(
        'You will not be able to use the helper function: {0}'.format(hlp_fkt))
    logging.info('Install shapely to use it.')


def get_polygons_from_table(conn, schema, table, g_col='geom', n_col='name'):
    sql = '''
        SELECT {n_col}, st_astext({g_col})
        FROM {schema}.{table};
    '''.format(
        **{'n_col': n_col, 'g_col': g_col, 'schema': schema, 'table': table})
    logging.debug(sql)
    raw_data = conn.execute(sql).fetchall()
    polygon_dc = {}
    for d in raw_data:
        polygon_dc[d[0]] = [d[0], wkt_loads(d[1])]
    return polygon_dc


def get_polygon_from_nuts(conn, nuts):
    r"""A one-line summary that does not use variable names or the
    function name.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
        (e.g. ``int``), or describe the type of the variable in more
        detail, e.g. ``(N,) ndarray`` or ``array_like``.
    Long_variable_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.

    Returns
    -------
    type
        Explanation of anonymous return value of type ``type``.
    describe : type
        Explanation of return value named `describe`.
    out : type
        Explanation of `out`.

    Other Parameters
    ----------------
    only_seldom_used_keywords : type
        Explanation
    common_parameters_listed_above : type
        Explanation

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    otherfunc : relationship (optional)
    newfunc : Relationship (optional), which could be fairly long, in which
              case the line wraps here.
    thirdfunc, fourthfunc, fifthfunc

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a greek symbol like :math:`omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a=[1,2,3]
    >>> print [x + 3 for x in a]
    [4, 5, 6]
    >>> print "a\n\nb"
    a
    b

    """
    # TODO@Günni
    if isinstance(nuts, str):
        nuts = [nuts, 'xyz']
    logging.debug('Getting polygon from DB')
    sql = '''
        SELECT st_astext(ST_Transform(st_union(geom), 4326))
        FROM oemof.geo_nuts_rg_2013
        WHERE nuts_id in {0};
    '''.format(tuple(nuts))
    return wkt_loads(conn.execute(sql).fetchone()[0])


def get_polygon_from_postgis(conn, schema, table, gcol='geom', union=False):
    r"""A one-line summary that does not use variable names or the
    function name.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
        (e.g. ``int``), or describe the type of the variable in more
        detail, e.g. ``(N,) ndarray`` or ``array_like``.
    Long_variable_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.

    Returns
    -------
    type
        Explanation of anonymous return value of type ``type``.
    describe : type
        Explanation of return value named `describe`.
    out : type
        Explanation of `out`.

    Other Parameters
    ----------------
    only_seldom_used_keywords : type
        Explanation
    common_parameters_listed_above : type
        Explanation

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    otherfunc : relationship (optional)
    newfunc : Relationship (optional), which could be fairly long, in which
              case the line wraps here.
    thirdfunc, fourthfunc, fifthfunc

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a greek symbol like :math:`omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a=[1,2,3]
    >>> print [x + 3 for x in a]
    [4, 5, 6]
    >>> print "a\n\nb"
    a
    b

    """
    # TODO@Günni
    logging.debug('Getting polygon from DB table')
    if union:
        geo_string = 'st_union({0})'.format(gcol)
    else:
        geo_string = '{0}'.format(gcol)

    sql = '''
        SELECT st_astext(ST_Transform({geo_string}, 4326))
        FROM {schema}.{table};
    '''.format(**{'geo_string': geo_string, 'schema': schema, 'table': table})
    return wkt_loads(conn.execute(sql).fetchone()[0])


def tz_from_geom(connection, geometry):
    r"""Finding the timezone of a given point or polygon geometry, assuming
    that the polygon is not crossing a border of a timezone.

    Parameters
    ----------
    connection : sqlalchemy connection object
        A valid connection to a postigs database containing the timezone table
    geometry : shapely geometry object
        A point or polygon object. The polygon should not cross a timezone.

    Returns
    -------
    string
        Timezone using the naming of the IANA time zone database
    """

    # TODO@Günni
    if geometry.geom_type in ['Polygon', 'MultiPolygon']:
        coords = geometry.centroid
    else:
        coords = geometry
    sql = """
        SELECT tzid FROM oemof_test.tz_world
        WHERE st_contains(geom, ST_PointFromText('{wkt}', 4326));
        """.format(wkt=coords.wkt)
    return connection.execute(sql).fetchone()[0]


def get_windzone(conn, geometry):
    'Find windzone from map.'
    # TODO@Günni
    if geometry.geom_type in ['Polygon', 'MultiPolygon']:
        coords = geometry.centroid
    else:
        coords = geometry
    sql = """
        SELECT zone FROM oemof_test.windzones
        WHERE st_contains(geom, ST_PointFromText('{wkt}', 4326));
        """.format(wkt=coords.wkt)
    zone = conn.execute(sql).fetchone()
    if zone is not None:
        zone = zone[0]
    else:
        zone = 0
    return zone


def get_CoastDat_weather(conn, geometry, year):
    r"""
    Get the weather data for the given geometry and create a weather object.
    """
    rename_dc = {
        'ASWDIFD_S': 'dhi',
        'ASWDIR_S': 'dirhi',
        'PS': 'pressure',
        'T_2M': 'temp_air',
        'WSS_10M': 'v_wind',
        'Z0': 'z0'}

    if geometry.geom_type in ['Polygon', 'MultiPolygon']:
        # Create MultiWeather
        # If polygon covers only one data set switch to SingleWeather
        sql_part = """
            SELECT sp.gid, ST_AsText(sp.geom)
            FROM coastdat.cosmoclmgrid as sp
            WHERE st_intersects(ST_GeomFromText('{wkt}',4326), sp.geom)
            """.format(wkt=geometry.wkt)
        df = fetch_raw_data(sql_weather_string(conn, geometry, year, sql_part),
                            conn, geometry)
        obj = create_multi_weather(df, geometry, rename_dc)
    elif geometry.geom_type == 'Point':
        # Create SingleWeather
        sql_part = """
            SELECT sp.gid, ST_AsText(sp.geom)
            FROM coastdat.cosmoclmgrid sp
            WHERE st_contains(sp.geom, ST_GeomFromText('{wkt}',4326))
            """.format(wkt=geometry.wkt)
        df = fetch_raw_data(sql_weather_string(conn, geometry, year, sql_part),
                            conn, geometry)
        obj = create_single_weather(df, geometry, rename_dc)
    else:
        logging.error('Unknown geometry type: {0}'.format(geometry.geom_type))
    return obj


def sql_weather_string(conn, geometry, year, sql_part):
        '''
        Creates an sql-string to read all datasets within a given polygon.
        The polygon must be defined in a view named coastdat.tmpview
        '''

        # TODO@Günni. Replace sql-String with alchemy/GeoAlchemy
        # Create string parts for where conditions

        return '''
        SELECT tsptyti.*, y.leap
        FROM coastdat.year as y
        INNER JOIN (
            SELECT tsptyd.*, sc.time_id
            FROM coastdat.scheduled as sc
            INNER JOIN (
                SELECT tspty.*, dt.name, dt.height
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
                                {sql_part}
                                ) as sps
                            INNER JOIN coastdat.located as l
                            ON (sps.gid = l.spatial_id)) as spl
                        ON (spl.data_id = t.id)) as tsp
                    ON (tsp.id = typ.data_id)) as tspty
                ON (tspty.type_id = dt.id)) as tsptyd
            ON (tsptyd.id = sc.data_id))as tsptyti
        ON (tsptyti.time_id = y.year)
        where y.year = '{year}'
        ;'''.format(year=year, sql_part=sql_part)


def fetch_raw_data(sql, connection, geometry):
    """
    Creates an sql-string to define a temporary view with a polygon.
    """
    tmp_dc = {}
    weather_df = pd.DataFrame(
        connection.execute(sql).fetchall(), columns=[
            'gid', 'geom', 'data_id', 'time_series', 'dat_id', 'type_id',
            'type', 'height', 'year', 'leap_year']).drop('dat_id', 1)

    # Get the timezone of the geometry
    tz = tz_from_geom(connection, geometry)

    for ix in weather_df.index:
        # Convert the point of the weather location to a shapely object
        weather_df.loc[ix, 'geom'] = wkt_loads(weather_df['geom'][ix])

        # Roll the dataset forward according to the timezone, because the
        # dataset is based on utc (Berlin +1, Kiev +2, London +0)
        utc = timezone('utc')
        offset = int(utc.localize(datetime(2002, 1, 1)).astimezone(
            timezone(tz)).strftime("%z")[:-2])

        # Roll the dataset backwards because the first value (1. Jan, 0:00)
        # contains the measurements of the hour before (coasDat2).
        roll_value = offset - 1

        # Get the year and the length of the data array
        db_year = weather_df.loc[ix, 'year']
        db_len = len(weather_df['time_series'][ix])

        # Set absolute time index for the data sets to avoid errors.
        tmp_dc[ix] = pd.Series(
            np.roll(np.array(weather_df['time_series'][ix]), roll_value),
            index=pd.date_range(pd.datetime(db_year, 1, 1, 0),
                                periods=db_len, freq='H', tz=tz))
    weather_df['time_series'] = pd.Series(tmp_dc)
    return weather_df


def create_single_weather(df, geo, rename_dc):
    ''
    my_weather = weather.FeedinWeather()
    data_height = {}

    # Create a pandas.DataFrame with the time series of the weather data set
    weather_df = pd.DataFrame(index=df.time_series.iloc[0].index)
    for row in df.iterrows():
        key = rename_dc[row[1].type]
        weather_df[key] = row[1].time_series
        data_height[key] = row[1].height if not np.isnan(row[1].height) else 0
    my_weather.data = weather_df
    my_weather.timezone = weather_df.index.tz
    if geo.geom_type == 'Point':
        my_weather.longitude = geo.x
        my_weather.latitude = geo.y
    else:
        my_weather.longitude = geo.centroid.x
        my_weather.latitude = geo.centroid.y
    my_weather.geometry = geo
    my_weather.data_height = data_height
    my_weather.name = row[1].gid
    return my_weather


def create_multi_weather(df, geo, rename_dc):
    ''
    weather_list = []
    # Create a pandas.DataFrame with the time series of the weather data set
    for gid in df.gid.unique():
        gid_df = df[df.gid == gid]
        obj = create_single_weather(gid_df, gid_df.geom.iloc[0], rename_dc)
        weather_list.append(obj)
    return weather_list
