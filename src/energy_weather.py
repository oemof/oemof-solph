# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:53:14 2015

@author: uwe
"""

import db
import pandas as pd
import logging
from shapely import geometry as shape


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
        where_str = ""
        if isinstance(self.datatypes, list):
            for t in self.datatypes:
                where_str += "dt.name = '{0}' or ".format(t)
            where_str = where_str[:-3]
        elif isinstance(self.datatypes, str):
            where_str += "dt.name = '{0}'".format(self.datatypes)
        else:
            logging.error("Wrong Tpye {0}".format(type(self.datatypes)))

        if self.geometry.geom_type == 'Polygon':
            print('Polygon')
            sql_part = """
                SELECT sp.gid, sp.geom
                FROM coastdat.spatial as sp
                WHERE st_contains(ST_GeomFromText('{wkt}',4326), sp.geom)
                """.format(wkt=self.geometry.wkt)
        elif self.geometry.geom_type == 'Point':
            print('Point')
            sql_part = """
                SELECT sp.gid, sp.geom
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
                where {where_string}) as tsptyd
            ON (tsptyd.id = sc.data_id))as tsptyti
        ON (tsptyti.time_id = y.year)
        where y.year = {year}
        ;'''.format(where_string=where_str, year=self.year, sql_part=sql_part)

    def get_raw_data(self):
        """
        Creates an sql-string to define a temporary view with a polygon.
        """
        sql = self.sql_join_string()

        print(sql)
        return pd.DataFrame(self.connection.execute(sql).fetchall(),
                            columns=['gid', 'wkb', 'data_id', 'time_series',
                                     'dat_id', 'type_id', 'type', 'year',
                                     'leap_year']).drop('dat_id', 1)


if __name__ == "__main__":
    conn = db.connection()
    geo = shape.Polygon(
        [(12.0, 50.0), (12.0, 50.5), (12.5, 50.5), (12.5, 50)])
    a = Weather(conn, geo, 2007, ['T_2M', 'WSS_10M', 'PS'])
    print(a.raw_data)
