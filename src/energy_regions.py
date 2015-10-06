# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""
import logging
import pandas as pd
import calendar
import pickle

from . import helpers
from . import energy_weather as w
from . import energy_power_plants as pp
from . import demand as dm
from . import powerplants as plants
from . import models

from matplotlib import pyplot as plt
from descartes import PolygonPatch
import os.path as path


class region():
    r"""A class to define a region of an energy system.

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

    Attributes
    ----------

    Attributes that are properties and have their own docstrings
    can be simply listed by name

    place : list of strings
        Containing the name of the state [0] and the name of the country
    weather : instance of class Weather
        Containing the weather data of all raster fields touching the region
    tz : str
        Timezone of the region
    name : str
        Name of the region. Default: 'No name'.
    year : int
        Year for the data sets of the region
    connection : sqlalchemy.connection object
        Containing a connection to an aktive database

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

    def __init__(self, year, geometry, **kwargs):

        self.geometry = geometry
        self.place = kwargs.get('place', None)
        self.year = year
        self.demand = None  # self.create_basic_dataframe()
        self.weather = None
        self.name = kwargs.get('name', 'No name')
        self._code = kwargs.get('code', None)
        self._df = None
        self.tz = kwargs.get('tz', None)
        self.connection = kwargs.get('conn', None)
        self.power_plants = {}

    def create_basic_dataframe(self, conn=None):
        r"""Giving back a DataFrame containing weekdays and holidays for the
        given year and region.


        Parameters
        ----------
        conn: sqlalchemy.connection object
            Only needed if not already present as an attribute.

        Returns
        -------
        pandas.DataFrame : DataFrame with a time index containing the time zone

        See Also
        --------
        fetch_admin_from_coord : provides the names of the state and country
        set_connection : can be used to set the connection attribute

        Notes
        -----
        Using Pandas > 0.16

        """
        if conn is None:
            conn = self.connection
            if conn is None:
                try:
                    conn = self.weather.connection
                except AttributeError:
                    print('No connection. Use set_connection to get one.')
                    raise
        self.connection = conn
        if self.tz is None:
            self.tz_from_geom(conn)
        if calendar.isleap(self.year):
            hoy = 8784
        else:
            hoy = 8760

        time_df = pd.DataFrame(
            index=pd.date_range(pd.datetime(self.year, 1, 1, 0), periods=hoy,
                                freq='H', tz=self.tz),
            columns=['weekday', 'hour', 'date'])

        if self.place is None:
            self.place = self.fetch_admin_from_coord(
                self.centroid().coords[0]).place

        holidays = helpers.get_german_holidays(self.year, self.place)

        # Add a column 'hour of the day to the DataFrame
        time_df['hour'] = time_df.index.hour + 1
        time_df['weekday'] = time_df.index.weekday + 1
        time_df['date'] = time_df.index.date

        # Set weekday to Holiday (0) for all holidays
        time_df['weekday'].mask(pd.to_datetime(time_df['date']).isin(
            pd.to_datetime(list(holidays.keys()))), 0, True)
        self._df = time_df

    def set_connection(self, conn):
        self.connection = conn

    def fetch_admin_from_coord(self, coord):
        """
        Receive reverse geocoded information from lat/lon point
        :rtype : dict
        :param lat: latitude
        :param lon: longitude
        :param zoom: detail level of information
        :return: list: [country, state]
        """

        try:
            self.place = helpers.fetch_admin_from_coord_osm(coord)
        except:
            logging.debug('Cannot fetch admin names from OSM.')
            try:
                self.place = helpers.fetch_admin_from_coord_google(coord)
            except:
                logging.debug('Cannot fetch admin names from Google.')

        return self

    def tz_from_geom(self, connection):
        'Docstring'
        self.tz = helpers.tz_from_geom(connection, self.geometry)
        return self

    def centroid(self):
        'Returns the centroid of the given geometry as a shapely point-object.'
        return self.geometry.centroid

    def fetch_weather_raster(self, conn):
        self.weather = w.Weather(conn, self.geometry, self.year)
        return self

    def fetch_ee_plants(self, conn):
        self.power_plants['re'] = (
            pp.Power_Plants().get_all_re_power_plants(conn, self.geometry))
        return self

    def fetch_fossil_power_plants(self, conn):
        self.power_plants['fossil'] = (
            pp.Power_Plants().get_all_fossil_power_plants(conn, self.geometry))
        return self

    def fetch_demand_series(self, method, **kwargs):
        ''
#        if self._df is None:
#            self.create_basic_dataframe(conn=conn)

#        # TODO @ Birgit, Caro
#        # Nur temporär, damit es funktioniert. Wird ersetzt durch demandlib.
#        sql = 'select * from oemof_test.demand_test order by id;'
#        table = conn.execute(sql)
#        print(table.keys)
#
#        self.demand = pd.DataFrame(
#            table.fetchall(), index=self._df.index, columns=table.keys())
#        self.demand.drop(['id'], inplace=True, axis=1)
#
#        # Spaltennamen brauchen dann aber weder das Jahr noch die Region
#        # Können wir noch diskutieren, der Name ist noch vollkommen offen.
#        self.demand.rename(columns={
#            'lk_wtb_2013': 'electrical',
#            'thoi_lk_wtb_2013': 'district_0',
#            'thng_lk_wtb_2013': 'gas_hs_0',
#            'twcb_lk_wtb_2013': 'wood_hs_0',
#            'dst0_lk_wtb_2013': 'oil_hs_0',
#            }, inplace=True)

        # Am Ende soll ein DataFrame rauskommen, dass wie self.demand ist.

        if method == 'csv':
            self.demand = pd.read_csv(kwargs.get('path') +
                                      kwargs.get('filename'),
                                      sep=",")

        elif method == 'db':
            conn = kwargs.get('conn')
            self.demand = 12345
#            not implemented yet

        elif method == 'scale_profile_csv':
            self.demand = dm.electrical_demand(
                            annual_elec_demand=kwargs.get('ann_el_demand'),
                            profile=pd.read_csv(kwargs.get('path') +
                                              kwargs.get('filename'),
                                              sep=","))

            print(self.demand.elec_demand.sum())




#                         year muss noch raus
#            print(self.demand)

#            print(eb.electric_building().annual_demand)
#            print(eb.electric_building(annual_elec_demand=200).annual_demand)

        elif method == 'scale_profile_db':
            conn = kwargs.get('conn')
            self.demand = 67890
#           not implemented yet

        elif method == 'scale_entsoe':
            conn = kwargs.get('conn')

        elif method == 'calculate_profile':
            self.demand = 666
#           not implemented yet

#        print(self.demand.sum())

        return self

    def fetch_ee_feedin(self, conn, **site):
        wind_model = models.WindPowerPlant(required=[])
        wind_model.get_wind_pp_types(conn)  # remove this output
        pv_model = models.Photovoltaic(required=[])
        site['connection'] = conn
        site['tz'] = self.weather.tz
        pv_df = 0
        wind_df = 0
        if self.power_plants.get('re', None) is None:
            self.power_plants['re'] = (
                pp.Power_Plants().get_empty_power_plant_df())

        laenge = len(list(self.weather.grouped_by_gid().keys()))

        for gid in self.weather.grouped_by_gid().keys():
            logging.debug(laenge)
            # Get the geometry for the given weather raster field
            tmp_geom = self.weather.get_geometry_from_gid(gid)

            # Get all Power Plants for raster field
            ee_pp = pp.Power_Plants().get_all_re_power_plants(
                conn, tmp_geom, self.geometry)

            # Add the powerplants to the power plant table of the region
            self.power_plants['re'] = pd.concat(
                [ee_pp, self.power_plants['re']], ignore_index=True)

            # Find type of wind turbine and its parameters according to the
            # windzone.
            wz = helpers.get_windzone(conn, tmp_geom)
            site['wka_model'] = (site['wka_model_dc'].get(
                wz, site['wka_model']))
            site['d_rotor'] = (site['d_rotor_dc'].get(wz, site['d_rotor']))
            site['h_hub'] = (site['h_hub_dc'].get(wz, site['h_hub']))

            site['weather'] = self.weather
            site['gid'] = gid
            site['latitude'] = tmp_geom.centroid.y
            site['longitude'] = tmp_geom.centroid.x

            # Determine the feedin time series for the weather field
            # Wind energy
            wind_peak_power = ee_pp[ee_pp.type == 'Windkraft'].p_kw_peak.sum()
            wind_power_plant = plants.WindPowerPlant(
                wind_peak_power, model=wind_model)
            wind_series = wind_power_plant.feedin_as_pd(**site)
            wind_series.name = gid

            # PV
            pv_peak_power = ee_pp[ee_pp.type == 'Solarstrom'].p_kw_peak.sum()
            pv_plant = plants.Photovoltaic(pv_peak_power, model=pv_model)
            pv_series = pv_plant.feedin_as_pd(**site)
            pv_series.name = gid

            # Combine the results to a DataFrame
            try:
                pv_df = pd.concat([pv_df, pv_series], axis=1)
                wind_df = pd.concat([wind_df, wind_series], axis=1)
            except:
                pv_df = pv_series.to_frame()
                wind_df = wind_series.to_frame()

            laenge -= 1

        if site.get('store'):
            dpath = site.get(
                'dpath', path.join(path.expanduser("~"), '.oemof'))
            filename = site.get('filename', self.name)
            fullpath = path.join(dpath, filename)

            if site['store'] == 'hf5':
                pv_df.to_hdf(fullpath + '.hf5', 'pv_pwr')
                wind_df.to_hdf(fullpath + '.hf5', 'wind_pwr')

            if site['store'] == 'csv':
                pv_df.to_csv(fullpath + '_pv.csv')
                wind_df.to_csv(fullpath + '_wind.csv')

        # Summerize the results to one column for pv and one for wind
        df = pd.concat([pv_df.sum(axis=1), wind_df.sum(axis=1)], axis=1)
        self.feedin = df.rename(columns={0: 'pv_pwr', 1: 'wind_pwr'})
        return self

    def dump(self, dpath=None, filename=None, keep_weather=True):
        ''

        # Remove database connections, which cannot be dumped.
        self.connection = None
        if keep_weather:
            self.weather.connection = None
        else:
            self.weather = None

        if dpath is None:
            dpath = path.join(path.expanduser("~"), '.oemof')

        if filename is None:
            filename = self.name + '.oemof'

        pickle.dump(self.__dict__, open(path.join(dpath, filename), 'wb'))

        return('Attributes dumped to: {0}'.format(path.join(dpath, filename)))

    def restore(self, conn=None, dpath=None, filename=None):
        ''
        if dpath is None:
            dpath = path.join(path.expanduser("~"), '.oemof')

        if filename is None:
            filename = self.name + '.oemof'

        self.__dict__ = pickle.load(open(path.join(dpath, filename), "rb"))

        if conn is not None:
            self.connection = conn
            self.weather.connection = conn

    def plot(self):
        'Simple plot to check the geometry'
        BLUE = '#6699cc'
        GRAY = '#9FF999'
        fig, ax = plt.subplots()
        if self.geometry.geom_type == 'MultiPolygon':
            for polygon in self.geometry:
                patch = PolygonPatch(polygon, fc=GRAY, ec=BLUE, alpha=0.5)
                ax.add_patch(patch)
        else:
            ax.add_patch(PolygonPatch(
                self.geometry, fc=GRAY, ec=BLUE, alpha=0.5))
        ax.set_xlim(self.geometry.bounds[0], self.geometry.bounds[2])
        ax.set_ylim(self.geometry.bounds[1], self.geometry.bounds[3])
        fig.suptitle(self.name, fontsize='20')

    @property
    def code(self):
        if self._code is None:
            name_parts = self.name.replace('_', ' ').split(' ', 1)
            self._code = ''
            for part in name_parts:
                self._code += part[:1].upper() + part[1:3]
        return self._code

    @property
    def df(self):
        if self._df is None:
            self.create_basic_dataframe()
        return self._df

    @property
    def elec_demand(self):
        return self.demand['elec']

    @property
    def country(self):
        if self.place is None:
            self.fetch_admin_from_coord(self.centroid().coords[0])
        return self.place[0]

    @property
    def state(self):
        if self.place is None:
            self.fetch_admin_from_coord(self.centroid().coords[0])
        return helpers.abbreviation_of_state(self.place[1])
