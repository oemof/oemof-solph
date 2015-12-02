# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""
import logging
import pandas as pd
import calendar
import pickle

from ..tools import helpers
from ..tools import pg_helpers

from . import energy_weather as w
from . import energy_power_plants as pp
from oemof.demandlib import demand as dm
from feedinlib import powerplants as plants
from feedinlib import models

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
        self.tz = pg_helpers.tz_from_geom(connection, self.geometry)
        return self

    def centroid(self):
        'Returns the centroid of the given geometry as a shapely point-object.'
        return self.geometry.centroid

    def fetch_weather_raster(self, conn):
        self.weather = w.Weather(connection=conn, geometry=self.geometry,
                                 year=self.year)
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
#        if 'csv' in ('db', 'profile_db', 'calculate_profile'):
#            if self._df is None:
#                self.set_connection(conn=kwargs.get('conn'))
#                self.create_basic_dataframe(conn=kwargs.get('conn'))

        self.demand = dm.electrical_demand(method,
                                           dataframe=self.df,
                                           annual_elec_demand=
                                           kwargs.get('ann_el_demand'),
                                           path=kwargs.get('path'),
                                           filename=kwargs.get('filename'),
                                           conn=kwargs.get('conn'),
                                           population=
                                           kwargs.get('population'),
                                           ann_el_demand_per_sector=kwargs.get(
                                           'ann_el_demand_per_sector'),
                                           ann_el_demand_per_person=kwargs.get(
                                           'ann_el_demand_per_person'),
                                           household_structure=kwargs.get(
                                           'household_structure'),
                                           household_members_all=kwargs.get(
                                           'household_members_all'),
                                           comm_ann_el_demand_state=kwargs.get(
                                           'comm_ann_el_demand_state'),
                                           comm_number_of_employees_state=
                                           kwargs.get(
                                           'comm_number_of_employees_state'),
                                           comm_number_of_employees_region=
                                           kwargs.get(
                                           'comm_number_of_employees_region'),
                                           ind_number_of_employees=kwargs.get(
                                           'ind_number_of_employees'))

        print('self.demand: ', self.demand.elec_demand.sum())


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

        return self

    def fetch_ee_feedin(self, conn, **site):
        site['connection'] = conn
        pv_df = 0
        wind_df = 0
        if self.power_plants.get('re', None) is None:
            self.power_plants['re'] = (
                pp.Power_Plants().get_empty_power_plant_df())

        # Define height dict
        data_height = {}
        for key in self.weather.datatypes:
            name = self.weather.name_dc[key]
            data_height[name] = self.weather.get_data_heigth(name)
            if data_height[name] is None:
                data_height[name] = 0

        laenge = len(self.weather.gid)

        for gid in self.weather.gid:
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
            wz = pg_helpers.get_windzone(conn, tmp_geom)
            site['wind_conv_type'] = (site['wka_model_dc'].get(
                wz, site['wka_model']))
            site['d_rotor'] = (site['d_rotor_dc'].get(wz, site['d_rotor']))
            site['h_hub'] = (site['h_hub_dc'].get(wz, site['h_hub']))

            # Define weather object of the feedinlib
            self.weather.set_feedin_dataset(gid)

            # Determine the feedin time series for the weather field
            # Wind energy
            wind_peak_power = ee_pp[ee_pp.type == 'Windkraft'].p_kw_peak.sum()
            wind_power_plant = plants.WindPowerPlant(**site)
            wind_series = wind_power_plant.feedin(
                weather=self.weather,
                installed_capacity=wind_peak_power)
            wind_series.name = gid

            # PV
            pv_peak_power = ee_pp[ee_pp.type == 'Solarstrom'].p_kw_peak.sum()
            pv_plant = plants.Photovoltaic(**site)
            pv_series = pv_plant.feedin(
                weather=self.weather, peak_power=pv_peak_power)
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
