# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:53:14 2015

@author: uwe
"""

from matplotlib import pyplot as plt
import db
import pandas as pd
import logging
from shapely import geometry as shape
from shapely.wkt import loads as wkt_loads
from shapely import geos


class Weather:
    """
    Main-Interface for loading weather data.

    """

    def __init__(self, conn, geometry, year, datatypes):
        """
        constructor for the weather-object.
        Test for config, to set up which source shall be used
        """
        self.connection = conn
        self.year = year
        self.datatypes = datatypes
        self.geometry = geometry
        self.raw_data = self.get_raw_data()

    def sql_join_string(self):
        '''
        Creates an sql-string to read all datasets within a given polygon.
        The polygon must be defined in a view named coastdat.tmpview
        '''

        # TODO@Günni. Replace sql-String with alchemy/GeoAlchemy
        # Decide wether datatype is one type or a list
        where_str1 = ""
        if isinstance(self.datatypes, list):
            for t in self.datatypes:
                where_str1 += "dt.name = '{0}' or ".format(t)
            where_str1 = where_str1[:-3]
        elif isinstance(self.datatypes, str):
            where_str1 += "dt.name = '{0}'".format(self.datatypes)
        else:
            logging.error("Wrong data type: {0}".format(type(self.datatypes)))

        # Decide wether year is one type or a list
        where_str2 = ""
        if isinstance(self.year, list):
            for y in self.year:
                where_str2 += "y.year = '{0}' or ".format(y)
            where_str2 = where_str2[:-3]
        elif isinstance(self.year, int):
            where_str2 += "y.year = '{0}'".format(self.year)
        else:
            logging.error("Wrong year type: {0}".format(type(self.year)))

        # Decide wether geometry is of type Polygon or point
        if self.geometry.geom_type == 'Polygon':
            print('Polygon')
            sql_part = """
                SELECT sp.gid, ST_AsText(sp.geom)
                FROM coastdat.spatial as sp
                WHERE st_contains(ST_GeomFromText('{wkt}',4326), sp.geom)
                """.format(wkt=self.geometry.wkt)
        elif self.geometry.geom_type == 'Point':
            print('Point')
            sql_part = """
                SELECT sp.gid, ST_AsText(sp.geom)
                FROM coastdat.cosmoclmgrid sp
                WHERE st_contains(sp.geom, ST_GeomFromText('{wkt}',4326))
                """.format(wkt=self.geometry.wkt)
        else:
            print('Häääh')

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
        weather_df = pd.DataFrame(self.connection.execute(sql).fetchall(),
                            columns=['gid', 'geom', 'data_id', 'time_series',
                                     'dat_id', 'type_id', 'type', 'year',
                                     'leap_year']).drop('dat_id', 1)

        for ix in weather_df.index:
            weather_df.loc[ix, 'geom'] = wkt_loads(weather_df['geom'][ix])
            db_year = weather_df.loc[ix, 'year']
            tmp_dc[ix] = pd.Series(weather_df['time_series'][ix],
                index=pd.date_range(
                    pd.datetime(db_year, 1, 1, 0), periods=8760, freq='H'))
        weather_df['time_series']=pd.Series(tmp_dc)
        return weather_df

    def grouped_by_gid(self):
        res = []
        for year in self.year:
            dic = {}
            for gid in self.raw_data.gid.unique():
                dic[gid] = {}
                tmp = self.raw_data[
                    (self.raw_data.year == year) & (self.raw_data.gid == gid)]
                for t in tmp.time_series.iteritems():
                    dic[gid][tmp.type[t[0]]] = t[1]
                dic[gid] = pd.DataFrame(dic[gid])
            res.append(dic)
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


if __name__ == "__main__":
    conn = db.connection()
    geo = shape.Polygon(
        [(12.0, 50.0), (12.0, 50.5), (12.5, 50.5), (12.5, 50)])
    a = Weather(conn, geo, [2007, 2010], ['T_2M', 'WSS_10M', 'PS'])
    for row in a.raw_data[a.raw_data.type == 'T_2M'].geom.iteritems():
        print(row[1])
    plt.show()
#    print(a.raw_data[a.raw_data.type == 'T_2M'])
#    print(a.raw_data['geom'][0].x)
#    print(type(a.raw_data['time_series'][0]))
#    print(a.raw_data['time_series'][0])
