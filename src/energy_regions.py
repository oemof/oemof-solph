# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""
import logging
import holiday
import pandas as pd
from matplotlib import pyplot as plt
from shapely import geometry as shape
from descartes import PolygonPatch
import fiona
from shapely.ops import cascaded_union
import urllib
import xml.etree.ElementTree as ET


class region():

    def __init__(self, year, geometry=None, nuts=None, file=None):

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
                self.__geometry__ = geometry
            else:
                raise TypeError('No valid geometry given.')
        except:
            if isinstance(nuts, list):
                self.__geometry__ = self.get_polygon_from_nuts(nuts)
            elif isinstance(file, str):
                    self.__geometry__ = self.get_polygon_from_shp_file(file)
            else:
                logging.error('No valid geometry given.')
                raise

        # Initialise the DataFrame for the demand time series.
        self.__place__ = self.fetch_admin_from_coord(self.centroid().coords[0])

        self.__demand__ = self.create_basic_dataframe(year)

    def create_basic_dataframe(self, year):
        '''Create a basic hourly dataframe for the given year.'''

        # Create a temporary DataFrame to calculate the heat demand
        time_df = pd.DataFrame(
            index=pd.date_range(
                pd.datetime(year, 1, 1, 0), periods=8760, freq='H'),
            columns=['weekday', 'hour', 'date'])

        holidays = holiday.get_german_holidays(year, self.__place__)

        # Add a column 'hour of the day to the DataFrame
        time_df['hour'] = time_df.index.hour + 1
        time_df['weekday'] = time_df.index.weekday + 1
        time_df['date'] = time_df.index.date
        time_df['elec'] = 0
        time_df['heat'] = 0

        # Set weekday to Holiday (0) for all holidays
        time_df['weekday'].mask(pd.to_datetime(time_df['date']).isin(
            pd.to_datetime(list(holidays.keys()))), 0, True)
        return time_df

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
        return self.__geometry__.centroid

    def plot(self):
        'Simple plot to check the geometry'
        BLUE = '#6699cc'
        GRAY = '#9FF999'
        fig, ax = plt.subplots()
        if self.__geometry__.geom_type == 'MultiPolygon':
            for polygon in self.__geometry__:
                patch = PolygonPatch(polygon, fc=GRAY, ec=BLUE, alpha=0.5)
                ax.add_patch(patch)
        else:
            patch = PolygonPatch(
                self.__geometry__, fc=GRAY, ec=BLUE, alpha=0.5)
            ax.add_patch(patch)
        ax.set_xlim(self.__geometry__.bounds[0], self.__geometry__.bounds[2])
        ax.set_ylim(self.__geometry__.bounds[1], self.__geometry__.bounds[3])

    @property
    def demand(self):
        return self.__demand__

    @property
    def elec_demand(self):
        return self.__demand__['elec']

    @property
    def country(self):
        return self.__place__[0]

    @property
    def state(self):
        return self.abbreviation_of_state(self.__place__[1])


if __name__ == "__main__":
    geo = shape.Polygon([(0, 0), (1, 1), (1, 0), (2, 5)])
    a = region(2007, geometry=geo)
#    b = region(2007, nuts=['1234', '1236'])
    c = region(2007, file='/home/uwe/Wittenberg.shp')

    c.plot()
    plt.plot(c.centroid().x, c.centroid().y, 'x', color='r')
    plt.show()
    print(c.state)
    print(c.country)
    print(c.elec_demand)

    a.plot()
    plt.plot(a.centroid().x, a.centroid().y, 'x', color='r')
    plt.show()

    print(a.state)
    print(a.country)
    print(a.elec_demand)
