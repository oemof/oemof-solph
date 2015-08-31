# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 11:08:15 2015

This is a collection of helper functions which work on there own an can be
used by various classes. If there are too many helper-functions, they will
be sorted in different modules.

All special import should be in try/except loops to avoid import errors.
"""

import logging
from datetime import date, timedelta

# get_polygon_from_nuts
hlp_fkt = 'get_polygon_from_nuts'
try:
    from shapely.wkt import loads as wkt_loads
except:
    logging.info(
        'You will not be able to use the helper function: {0}'.format(hlp_fkt))
    logging.info('Install shapely to use it.')

# get_polygon_from_shp_file
hlp_fkt = 'get_polygon_from_shp_file'
try:
    import fiona
    from shapely import geometry as shape
    from shapely.ops import cascaded_union
except:
    logging.info(
        'You will not be able to use the helper function: {0}'.format(hlp_fkt))
    logging.info('Install fiona, shapely to use it.')

# get_german_holidays
hlp_fkt = 'get_german_holidays'
try:
    from dateutil import easter
except:
    logging.info(
        'You will not be able to use the helper function: {0}'.format(hlp_fkt))
    logging.info('Install dateutil to use it.')

# fetch_admin_from_coord_osm
hlp_fkt = 'fetch_admin_from_coord_osm'
try:
    import urllib
    import xml.etree.ElementTree as ET
except:
    logging.info(
        'You will not be able to use the helper function: {0}'.format(hlp_fkt))
    logging.info('Install urllib, xml to use it.')

# fetch_admin_from_coord_google
hlp_fkt = 'fetch_admin_from_coord_google'
try:
    import geocoder
except:
    logging.info(
        'You will not be able to use the helper function: {0}'.format(hlp_fkt))
    logging.info('Install geocoder to use it.')


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


def get_polygon_from_shp_file(file):
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

    logging.debug('Loading polygon from file: {0}'.format(file))
    multi = shape.MultiPolygon(
        [shape.shape(pol['geometry']) for pol in fiona.open(file)])
    return cascaded_union(multi)


def get_german_holidays(year, place=[None, None, None], scope='legal'):
    r"""
    Returns German holiday dates. Use the abbreviations for the german
    federal states like 'BY' for Bayern.

    Parameters
    ----------
    year : int
        Year of which the holidays are wanted
    place : list of strings
        List of names: [country, state, city]
    scope : string
        Type of holidays. So far only legal is possible.

    Returns
    -------
    dictionary
        The keys are in the datetime format the values represent the names.

    Notes
    -----
    So far only the data of german holidays is available. Feel free to add
    other countries or to implement workalendar.
    https://github.com/novapost/workalendar

    Examples
    --------
    get_holidays(2015, place=['Germany', 'BE', 'Berlin'])
    """
    logging.debug('Feiertage für: {0}'.format(place))
    if place[0] not in ['Deutschland', 'deutschland', 'Germany', 'germany']:
        logging.error(
            'You are outside of Germany. The holidays will be incorrect.')
    # Determine Easter
    eastr = easter.easter(year)

    # Add national holidays
    adict = {
        date(year,  1,  1): 'Neujahr',
        date(year,  5,  1): 'Tag der Arbeit',
        date(year, 10,  3): 'Tag der Deutschen Einheit',
        date(year, 12, 25): '1. Weihnachtstag',
        date(year, 12, 26): '2. Weihnachtstag',
        eastr - timedelta(days=2): 'Karfreitag',
        eastr: 'Ostersonntag',
        eastr + timedelta(days=1): 'Ostermontag',
        eastr + timedelta(days=39): 'Christi Himmelfahrt',
        eastr + timedelta(days=50): 'Pfingstmontag',
        }

    # Add federal holidays
    if place[1].upper() in ('BW', 'BY', 'ST'):
        adict[date(year, 1, 6)] = 'Heilige Drei Könige'

    if place[1] in ('BW', 'BY', 'HE', 'NW', 'RP', 'SL'):
        adict[eastr + timedelta(days=60)] = 'Frohnleichnam'

    if place[1].upper() in ('BY', 'SL'):
        adict[date(year, 8, 15)] = 'Mariä Himmelfahrt'

    if place[1].upper() in ('BB', 'MV', 'SN', 'ST', 'TH'):
        adict[date(year, 10, 31)] = 'Reformationstag'

    if place[1].upper() in ('BW', 'BY', ):
        adict[date(year, 11, 1)] = 'Allerheiligen'

    return adict


def abbreviation_of_state(statename):
    r"""Get the abbreviation of a german state name or the other way round.

    Parameters
    ----------
    statename : string
        Fullname of the state or its abbreviation

    Returns
    -------
    string
        Fullname of the state or its abbreviation, depending on the input.
    """

    abbr_dict = {
        'Baden-Württemberg': 'BW',
        'Bayern': 'BY',
        'Berlin': 'BE',
        'Brandenburg': 'BB',
        'Bremen': 'HB',
        'Hamburg': 'HH',
        'Hessen': 'HE',
        'Mecklenburg-Vorpommern': 'MV',
        'Niedersachsen': 'NI',
        'Nordrhein-Westfalen': 'NW',
        'Rheinland-Pfalz': 'RP',
        'Saarland': 'SL',
        'Sachsen': 'SN',
        'Sachsen-Anhalt': 'ST',
        'Schleswig-Holstein': 'SH',
        'Thüringen': 'TH'}
    try:
        value = abbr_dict[statename]
    except:
        try:
            value = list(abbr_dict.keys())[list(abbr_dict.values()).index(
                statename)]
        except:
            value = None
    return value


def fetch_admin_from_coord_osm(coord):
    r"""Reverse geocoding using osm.

    Parameters
    ----------
    coord : array_like
        Geo-coordinates in the order (longitude, latitude)

    Returns
    -------
    list of strings
        Containing the name of the country and the name of the state if
        available

    See Also
    --------
    fetch_admin_from_coord_google

    Examples
    --------
    >>> fetch_admin_from_coord_osm((12.7, 51.8))
    ['Deutschland', 'ST']
    """

    def parse_result(res):
        root = ET.fromstring(res)
        address_parts = {}

        for a in root[1]:
            address_parts[a.tag] = a.text

        return address_parts

    lon = coord[0]
    lat = coord[1]

    query = "http://nominatim.openstreetmap.org/reverse?"
    query += "format=xml"
    query += "&lat={lat}".format(lat=lat)
    query += "&lon={lon}".format(lon=lon)
    query += "&zoom=18"
    query += "&addressdetails=1"

    conn = urllib.request.urlopen(query)
    rev_geocode = conn.read()
    address_parts = parse_result(rev_geocode)

    try:
        state = abbreviation_of_state(address_parts['state'])
    except KeyError:
        logging.error(
            "Didn't get the name of the state. " +
            "Maybe the coordinates ({0}) are outside of Germany.".format(
                str([lat, lon])))
        state = ''
    try:
        country = address_parts['country']
    except:
        country = None
    return [country, state]


def fetch_admin_from_coord_google(coord):
    r"""Reverse geocoding using google.

    Parameters
    ----------
    coord : array_like
        Geo-coordinates in the order (longitude, latitude)

    Returns
    -------
    list of strings
        Containing the name of the country and the name of the state if
        available

    See Also
    --------
    fetch_admin_from_coord_google

    Examples
    --------
    >>> fetch_admin_from_coord_osm((12.7, 51.8))
    ['Deutschland', 'ST']
    """

    new_coord = list((coord[1], coord[0]))
    g = geocoder.google(new_coord, method='reverse')
    return [g.country, g.state]


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
    timezone = connection.execute(sql).fetchone()
    if timezone is not None:
        timezone = timezone[0]
    else:
        timezone = 'Europe/Berlin'
        logging.error("Timezonefunction doesn't work for offshore regions.")
        logging.warning("Set timezone to {0} to avoid further errors".format(
            timezone))
    return timezone
