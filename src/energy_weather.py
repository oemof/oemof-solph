# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:53:14 2015

@author: uwe
"""

import pandas as pd
import logging
import numpy as np
from shapely.wkt import loads as wkt_loads
from pytz import timezone
from datetime import datetime


class Weather:
    """
    Main-Interface for loading weather data.

    """

    def __init__(self, conn, geometry, year, dataset='CoastDat2',
                 tz=None, datatypes=None):
        """
        constructor for the weather-object.
        Test for config, to set up which source shall be used
        """
        if dataset == 'CoastDat2':
            self.dataset = dataset
            self.name_dc = {
                'ASWDIFD_S': 'dhi',
                'ASWDIR_S': 'dirhi',
                'PS': 'pressure',
                'T_2M': 'temp_air',
                'WSS_10M': 'v_wind',
                'Z0': 'z0'}

        self.connection = conn
        self.year = self.check_year(year)
        self.datatypes = self.check_datatypes(datatypes)
        self.geometry = geometry
        self.raw_data = self.get_raw_data()
        self.data = None
        self.gid_geom = None

    def check_datatypes(self, datatypes):
        '''
        Convert datatypes to a list if it is not a list.
        If datatypes is None all possible types are used.
        '''
        if isinstance(datatypes, str):
            datatypes = list([datatypes])
        elif datatypes is None:
            datatypes = []
            sql = 'SELECT name FROM coastdat.datatype;'
            for x in self.connection.execute(sql).fetchall():
                datatypes.append(x[0])
        return datatypes

    def check_year(self, year):
        if isinstance(year, int):
            year = list([year])
        return year

    def tz_from_geom(self, geom):
        if geom.geom_type in ['Polygon', 'MultiPolygon']:
            coords = geom.centroid
        else:
            coords = geom
        sql = """
            SELECT tzid FROM world.tz_world
            WHERE st_contains(geom, ST_PointFromText('{wkt}', 4326));
            """.format(wkt=coords.wkt)
        return self.connection.execute(sql).fetchone()[0]

    def sql_join_string(self):
        '''
        Creates an sql-string to read all datasets within a given polygon.
        The polygon must be defined in a view named coastdat.tmpview
        '''

        # TODO@Günni. Replace sql-String with alchemy/GeoAlchemy
        # Create string parts for where conditions
        where_str1 = ""
        for t in self.datatypes:
            where_str1 += "dt.name = '{0}' or ".format(t)
        where_str1 = where_str1[:-3]

        where_str2 = ""
        for y in self.year:
            where_str2 += "y.year = '{0}' or ".format(y)
        where_str2 = where_str2[:-3]

        # Decide wether geometry is of type Polygon or point
        if self.geometry.geom_type in ['Polygon', 'MultiPolygon']:
            logging.debug('Polygon')
            sql_part = """
                SELECT sp.gid, ST_AsText(sp.geom)
                FROM coastdat.cosmoclmgrid as sp
                WHERE st_intersects(ST_GeomFromText('{wkt}',4326), sp.geom)
                """.format(wkt=self.geometry.wkt)
        elif self.geometry.geom_type == 'Point':
            logging.debug('Point')
            sql_part = """
                SELECT sp.gid, ST_AsText(sp.geom)
                FROM coastdat.cosmoclmgrid sp
                WHERE st_contains(sp.geom, ST_GeomFromText('{wkt}',4326))
                """.format(wkt=self.geometry.wkt)
        else:
            logging.error('Unknown geometry type: {0}'.format(
                self.geometry.geom_type))

        return '''
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
                                {sql_part}
                                ) as sps
                            INNER JOIN coastdat.located as l
                            ON (sps.gid = l.spatial_id)) as spl
                        ON (spl.data_id = t.id)) as tsp
                    ON (tsp.id = typ.data_id)) as tspty
                ON (tspty.type_id = dt.id)
                where {where_string1}) as tsptyd
            ON (tsptyd.id = sc.data_id))as tsptyti
        ON (tsptyti.time_id = y.year)
        where {where_string2}
        ;'''.format(where_string1=where_str1, year=self.year,
                    sql_part=sql_part, where_string2=where_str2)

    def get_raw_data(self):
        """
        Creates an sql-string to define a temporary view with a polygon.
        """
        tmp_dc = {}
        sql = self.sql_join_string()
        weather_df = pd.DataFrame(
            self.connection.execute(sql).fetchall(), columns=[
                'gid', 'geom', 'data_id', 'time_series', 'dat_id', 'type_id',
                'type', 'year', 'leap_year']).drop('dat_id', 1)

        for ix in weather_df.index:
            # Convert the point of the weather location to a shapely object
            weather_df.loc[ix, 'geom'] = wkt_loads(weather_df['geom'][ix])

            # Get the timezone of the weather location
            tz = self.tz_from_geom(weather_df.loc[ix, 'geom'])

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
        self.data = weather_df
        return weather_df

    def grouped_by_gid(self):
        # Hier caching einfügen? Wenn es schon gibt, dann nicht neu berechnen?
        res = []
        self.gid_geom = {}
        for year in self.year:
            dic = {}
            for gid in self.raw_data.gid.unique():
                dic[gid] = {}
                # Get the data for the given year and gid.
                tmp = self.raw_data[
                    (self.raw_data.year == year) & (self.raw_data.gid == gid)]

                # Write the data to pandas.Series within in the
                # pandas.DataFrame.
                for t in tmp.time_series.iteritems():
                    dic[gid][tmp.type[t[0]]] = t[1]
                dic[gid] = pd.DataFrame(dic[gid])

                # Create the gid-geom dictionary
                tmp_geo = self.raw_data.geom[
                    (self.raw_data.year == year) &
                    (self.raw_data.gid == gid)]
                self.gid_geom[gid] = tmp_geo[tmp_geo.index[0]]
            res.append(dic)

        # Return a list of dictionaries for all years or a dictionary if only
        # one year is given.
        if len(res) == 1:
            res = res[0]
        return res

    def grouped_by_datatype(self):
        res = []
        for year in self.year:
            dic = {}
            for typ in self.raw_data.type.unique():
                dic[typ] = {}
                tmp = self.raw_data[
                    (self.raw_data.year == year) & (self.raw_data.type == typ)]
                for t in tmp.time_series.iteritems():
                    dic[typ][tmp.gid[t[0]]] = t[1]
                dic[typ] = pd.DataFrame(dic[typ])
            res.append(dic)
        if len(res) == 1:
            res = res[0]
        return res

    def get_feedin_data(self, gid=None):
        data_dict = self.grouped_by_gid()
        if gid is None:
            data = data_dict[list(data_dict.keys())[0]]
        else:
            data = data_dict[gid]
        return data.rename(columns=self.name_dc)

    def get_geometry_from_gid(self, gid):
        return self.gid_geom[gid]

    def get_data_heigth(self, name):
        ''
        internal_name = [k for k, v in self.name_dc.items() if v == name][0]
        sql = "Select height from coastdat.datatype where name='{0}';".format(
            internal_name)
        return self.connection.execute(sql).fetchone()[0]
