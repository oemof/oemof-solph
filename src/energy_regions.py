# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""
import logging
import fiona
import urllib
import pandas as pd
import xml.etree.ElementTree as ET

from . import holiday
from . import energy_weather as w
from . import energy_power_plants as pp
from . import powerplants as plants
from . import models

from matplotlib import pyplot as plt
from descartes import PolygonPatch

from shapely import geometry as shape
from shapely.ops import cascaded_union


class region():

    def __init__(self, year, geometry=None, nuts=None, file=None,
                 name='No Name'):

        # Das muss noch schlauer gemacht werden
        # 3 Möglichkeiten entweder wird ein fertiges shapely-Objekt übergeben
        # oder eine List mit mindestens einem Nuts-Code oder ein Pfad zu
        # einer shp-Datei.
        try:
            # Der Ausdruck ist irreführend, denn ein Fehler wird ausgeworfen,
            # wenn 'geometry kein shapely-Objekt ist, denn dann gibt es die
            # Methode 'is_valid' nicht. Wenn es aber ein shaply-Objekt ist
            # dann gibt es keinen Fehler. Ist die Geometry fehlerhaft wird
            # False zurückgegeben, aber das hat keine Auswirkung. Ei
            if geometry.is_valid:
                self.geometry = geometry
            else:
                raise TypeError('No valid geometry given.')
        except:
            if isinstance(nuts, list):
                self.geometry = self.get_polygon_from_nuts(nuts)
            elif isinstance(file, str):
                    self.geometry = self.get_polygon_from_shp_file(file)
            else:
                logging.error('No valid geometry given.')
                raise

        # Initialise the DataFrame for the demand time series.
        self.place = None
        self.year = year
        self.demand = None  # self.create_basic_dataframe()
        self.weather = None
        self.name = name
        self._df = None

    def create_basic_dataframe(self):
        '''Create a basic hourly dataframe for the given year.'''
        # TODO: Replace hard coded "hour of the year".
        # Create a temporary DataFrame to calculate the heat demand
        time_df = pd.DataFrame(
            index=pd.date_range(
                pd.datetime(self.year, 1, 1, 0), periods=8760, freq='H'),
            columns=['weekday', 'hour', 'date'])

        if self.place is None:
            self.place = self.fetch_admin_from_coord(self.centroid().coords[0])

        holidays = holiday.get_german_holidays(self.year, self.place)

        # Add a column 'hour of the day to the DataFrame
        time_df['hour'] = time_df.index.hour + 1
        time_df['weekday'] = time_df.index.weekday + 1
        time_df['date'] = time_df.index.date

        # Set weekday to Holiday (0) for all holidays
        time_df['weekday'].mask(pd.to_datetime(time_df['date']).isin(
            pd.to_datetime(list(holidays.keys()))), 0, True)
        self._df = time_df

    def fetch_admin_from_coord(self, coord):
        """
        Receive reverse geocoded information from lat/lon point
        :rtype : dict
        :param lat: latitude
        :param lon: longitude
        :param zoom: detail level of information
        :return: list: [country, state]
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
            state = self.abbreviation_of_state(address_parts['state'])
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

    def abbreviation_of_state(self, statename):
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

    def get_polygon_from_nuts(self, nuts):
        'If at least one nuts-id is given, the polygon is loaded from the db.'
        logging.debug('Getting polygon from DB')

    def get_polygon_from_shp_file(self, file):
        'If a file name is given the polygon is loaded from the file.'
        logging.debug('Loading polygon from file: {0}'.format(file))
        multi = shape.MultiPolygon(
            [shape.shape(pol['geometry']) for pol in fiona.open(file)])
        return cascaded_union(multi)

    def centroid(self):
        'Returns the centroid of the given geometry as a shapely point-object.'
        return self.geometry.centroid

    def get_weather_raster(self, conn):
        self.weather = w.Weather(conn, self.geometry, self.year)
        return self

    def get_power_plants(self, conn):
        self.power_plants = pp.Power_Plants().get_all_power_plants(
            conn, self.geometry)
        return self

    def get_ee_feedin(self, conn, **site):
        wind_model = models.WindPowerPlant(required=[])
        pv_model = models.Photovoltaic(required=[])
        site['connection'] = conn
        site['tz'] = self.weather.tz_from_geom(self.geometry)
        pv_df = 0
        wind_df = 0
        for gid in self.weather.grouped_by_gid():
            # Get the geometry for the given weather raster field
            tmp_geom = self.weather.get_geometry_from_gid(gid)

            # Get all Power Plants for raster field
            ee_pp = pp.Power_Plants().get_all_ee_power_plants(
                conn, tmp_geom, self.geometry)

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

        # Summerize the results to one column for pv and one for wind
        df = pd.concat([pv_df.sum(axis=1), wind_df.sum(axis=1)], axis=1)
        self.feedin = df.rename(columns={0: 'pv_pwr', 1: 'wind_pwr'})
        return self

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
            self.place = self.fetch_admin_from_coord(self.centroid().coords[0])
        return self.place[0]

    @property
    def state(self):
        if self.place is None:
            self.place = self.fetch_admin_from_coord(self.centroid().coords[0])
        return self.abbreviation_of_state(self.place[1])
