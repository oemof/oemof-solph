__package__ = "rawdatalib"

import oemof.iolib.postgis as pg
import sys
import dblib as db
import pandas as pd
from datetime import datetime
import numpy as np


class Weather:
    """
    Main-Interface for loading weather data.

    """

    def __init__(self, year, region, params):
        """
        constructor for the weather-object.
        Test for config, to set up which source shall be used
        """
        #self._data = pg.raw_query("year: " + year + ", region: " + region + ", params: ")

    def sql_join_string(self, year, types, datatype=None):
        '''
        Creates an sql-string to read all datasets within a given polygon.
        The polygon must be defined in a view named coastdat.tmpview
        '''
        where_str = ""
        if datatype is None:
            for t in types:
                where_str += "dt.name = '{0}' or ".format(t[0])
            where_str = where_str[:-3]
        else:
            where_str += "dt.name = '{0}'".format(datatype)

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
                                SELECT *
                                FROM coastdat.tmpview
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
        ;'''.format(where_str, year)

    def get_data(self, DIC, site, year, region):
        """
        use this method to retrieve the whole raw dataset
        :return: the weatherdata
        """

        sql = 'DROP VIEW IF EXISTS coastdat.tmpview;'

        # Creates an sql-string to define a temporary view with a polygon.
        # TODO: Regionsinformationen, muessen ausgelagert werden

        # a) Uebergabe Polygon, mehrere Datenpunkte, funktioniert noch nicht
        #sql += '''
        #CREATE VIEW coastdat.tmpview as
        #SELECT sp.*
        #FROM coastdat.spatial as sp,
            #osnabrueck.eos_krs as eos
        #where st_contains(st_transform(eos.geom,4326), sp.geom);
        #'''

        # b) Uebergabe ein Datenpunkt
        sql += '''
        CREATE VIEW coastdat.tmpview AS
        SELECT sp.gid, sp.geom
        FROM coastdat.cosmoclmgrid sp
        WHERE st_contains(sp.geom, ST_GeomFromText('POINT(12.63 51.85)',4326));
        '''

        #datatype = 'ASWDIFD_S'
        select_str = "select name from coastdat.datatype;"
        types = db.execute_read_db(DIC, select_str)

        # Connect the two strings
        #sql += self.sql_join_string(year, types, datatype)
        sql += self.sql_join_string(year, types)

        # Execute sql commands
        data = db.execute_read_db(DIC, sql)

        self.data_dc = {}
        count = 0
        for t in types:
            t = data[count][6]
            for n in range(len(data) / 6):
                self.data_dc.setdefault(data[n][0], {})
                self.data_dc[data[n][0]][t] = np.array(data[count][3])
                count += 1

        return self.data_dc

    def get_data_for_pv(self, data_dc, DIC, site, year, region):

        # 1. Update site information with information from database
        # TODO: this information must be also found in the coastdat schema,
        # maybe this operation can also be somewhere else
        schema = 'weather'
        table = 'solar_raster_register'
        #columns = ['longitude', 'latitude', 'site_id', 'idx_lat', 'idx_lon']
        site.update(db.fetch_row(DIC, schema, table, where_column='raster_id',
            where_condition=int(region)))

        # 2. Create an empty data frame
        self.data = pd.DataFrame(
                index=pd.date_range(datetime(int(year), 1, 1, 0, 0, 0),
                periods=8760, freq='H', tz='Europe/Berlin'))

        # 3. Get weather timeseries from database

        # Required datatypes for PV calculation
        regions = data_dc.keys()
        keys = ['ASWDIFD_S', 'ASWDIR_S', 'T_2M', 'WSS_10M']

        tmp = {}
        for r in regions:
            for key in keys:
                tmp[key] = data_dc[r][key]

        self.data['DirHI'] = tmp['ASWDIR_S']
        self.data['DHI'] = tmp['ASWDIFD_S']
        self.data['temp'] = tmp['T_2M']
        self.data['v_wind'] = tmp['WSS_10M']

        return self.data

    def get_raw_data(self, DIC, site, year, region):

        data_dc = self.get_data(DIC, site, year, region)
        data = self.get_data_for_pv(data_dc, DIC, site, year, region)

        return data
