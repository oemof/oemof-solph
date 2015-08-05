from oemof.feedinlib.base_feed import Feed
import numpy as np
from scipy.interpolate import interp1d


class WindFeed(Feed):

    def __init__(self, conn, site, year, region, elevation_mean):
        """
        private class for the implementation of a Wind Feed as timeseries
        :param year: the year to get the data for
        :param region: the region to get the data for
        """
        self.connection = conn
        super(WindFeed, self).__init__(
            conn, site, year, region, elevation_mean)

    def _apply_model(self, site, year, weather, elevation_mean):
        """
        implementation of the model to generate the _timeseries data from
            the _weatherdata
        :return:
        """
        self.turbine_power_output(site, weather)
#                              h_hub, d_rotor, h_windmast, z_0,
#                              cp_data, v_wind, p_data, T_data, h_data_amsl)

    #TODO: setup the model, currently being done by clemens
    def rho_hub(self, site, weather):
        '''
        Calculates the density of air in kg/m³ at hub height.
            (temperature in °C, height in m, pressure in hPa)
        Assumptions:
            Temperature gradient of -6.5 K/km
            Density gradient of -1/8 hPa/m
        '''
        h_temperature_data = weather.get_data_heigth('temp_air')
        h_pressure_data = 0  # heigth of pressure measurement?
        T_hub = weather.data.temp_air - 0.0065 * (
            site['h_hub'] - h_temperature_data)
        return (weather.data.pressure - (site['h_hub'] - h_pressure_data) *
                1 / 8) / (2.8706 * T_hub)

    def v_wind_hub(self, site, weather):
        '''
        Calculates the wind speed in m/s at hub height.
        h_windmast is the hight in which the wind velocity is measured.
        (height in m, velocity in m/s)
        '''
        return (weather.data.v_wind * np.log(site['h_hub'] / weather.data.z0)
                / np.log(weather.get_data_heigth('v_wind') / weather.data.z0))

    def cp_values(self, site, v_wind):
        '''
        Interpolates the cp value as a function of the wind velocity between
        data obtained from the power curve of the specified wind turbine type.
        '''
        # TODO@Günni
        sql = '''SELECT * FROM ee_komponenten.wea_cpcurves
            WHERE rli_anlagen_id = '{0}'
            '''.format(site['wka_model'])
        ncols = ['rli_anlagen_id', 'p_nenn', 'source', 'modificationtimestamp']

        db_res = self.connection.execute(sql)
        res_ls = db_res.fetchall()[0]
        n = 0
        cp_data = np.array([0, 0])
        for col in db_res.keys():
            if col not in ncols:
                if res_ls[n] is not None:
                    cp_data = np.vstack((cp_data, np.array(
                        [float(col), float(res_ls[n])])))
            n += 1
        cp_data = np.delete(cp_data, 0, 0)
        v_wind[v_wind > np.max(cp_data[:, 0])] = np.max(cp_data[:, 0])
        return interp1d(cp_data[:, 0], cp_data[:, 1])(v_wind)

    def number_wka_sqkm(self, d_rotor):
        '''
        Calculates the possible number of wind power stations per km²
        (Hau, 2008). According to Hau the distance between two turbines should
        be 8 - 10 rotor diameters in the prevailing wind direction and 3 - 5
        rotor diameters perpendicular to the prevailing wind direction.
        (diameter in m)
        '''
        dist_wd = 8  # prevailing wind direction
        dist_pwd = 4  # perpendicular to prevailing wind direction
        return 1 / (dist_wd * dist_pwd * (float(d_rotor) / 1000) ** 2)

    def number_wka_district(self, d_rotor, area):
        '''
        Returns the possible number of wind turbines in a district.
        '''
        return round(area * self.number_wka_sqkm(d_rotor))

    def turbine_power_output(self, site, weather):
#                             h_hub, d_rotor, h_windmast, z_0, cp_data,
#                             v_wind, p_data, T_data, h_data_amsl):
        '''
        Calculates the power output in W of one wind turbine.

        mamsl (meters above sea level) of the base of the wind turbine are
        set to mamsl of the weather station
        (height in m, diameter in m, power in W, density in kg/m³, temp.
        in °C, pressure in hPa, velocity in m/s)
        '''

#        h_base_amsl = h_data_amsl

        P_wka = (
            (self.rho_hub(site, weather) / 2) *
            (((site['d_rotor'] / 2) ** 2) * np.pi) *
            np.power(self.v_wind_hub(site, weather), 3) *
            self.cp_values(site, self.v_wind_hub(site, weather)))
        return P_wka
