__package__ = "rawdatalib"

import oemof.iolib.postgis as pg
import sys
import pandas as pd
from datetime import datetime
sys.path.append('/home/caro/rlihome/Git/pahesmf')
import src.basic.postgresql_db as db


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

    def get_raw_data(self, DIC, site, year, region):
        """
        use this method to retrieve the whole raw dataset
        :return: the weatherdata
        """

        # 1) CREATE EMPTY DATA FRAME
        self.data = pd.DataFrame(index=pd.date_range(datetime(int(year), 1, 1, 0, 0, 0),
                periods=8760, freq='H', tz='Europe/Berlin'))

        #temporary: Infos for DB-Call
        schema = 'weather'
        tables = ['solar_direct_timeseries_dlr_osna',
            'solar_diffus_pvmodelcomparison', 'solar_global_pvmodelcomparison']
        columns = ['solar_radiation']
        orderby = 'hour'

        # 2) UPDATE SITE INFORMATION WITH INFORMATION FROM DATABASE
        table = 'solar_raster_register'
        #columns = ['longitude', 'latitude', 'site_id', 'idx_lat', 'idx_lon']
        site.update(db.fetch_row(DIC, schema, table, where_column='raster_id',
            where_condition=int(region)))

        # 3) GET WEATHER TIMESERIES FROM DATABASE
        tmp = {}
        #for table in tables:
            #tmp[table] = db.fetch_columns(DIC, schema, table, columns,
                #orderby=orderby, as_np=True, where_string=whr_str)['solar_radiation']

        for table in tables:
            tmp[table] = db.fetch_columns(DIC, schema, table, columns,
                orderby=orderby, as_np=True)['solar_radiation']

        self.data['temp'] = db.fetch_columns(DIC, 'wittenberg', 'try_2010_av_year',
            'air_temp', orderby='id', as_np=True, where_column='region',
            where_condition=4)['air_temp']

        self.data['v_wind'] = db.fetch_columns(DIC, 'wittenberg', 'try_2010_av_year',
            'v_wind', orderby='id', as_np=True, where_column='region',
            where_condition=4)['v_wind']

        #data['GHI'] = (tmp['solar_direct_timeseries'] + tmp['solar_diffus_timeseries'])
        #data['DHI'] = tmp['solar_diffus_timeseries']

        self.data['GHI'] = tmp['solar_global_pvmodelcomparison']
        self.data['DHI'] = tmp['solar_diffus_pvmodelcomparison']

        #return self._data
        return self.data
