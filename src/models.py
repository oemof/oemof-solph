# -*- coding: utf-8 -*-
"""
Created on Wed May 13 08:43:54 2015

@author: dozeumwic
"""
import numpy as np
import pandas as pd
import pvlib
from scipy.interpolate import interp1d


class Photovoltaic:
    ''

    def __init__(self, required):
        self.required = required

    def feedin(self, **kwargs):

        feedin_pd = self.feedin_as_pd(**kwargs)

        return list(feedin_pd)

    def feedin_as_pd(self, **kwargs):

        df = self.get_normalized_pv_time_series(**kwargs)

        return df.p_pv_norm

    def solarposition_hourly_mean(self, location, data, **kwargs):
        '''
        Determine the position of the sun as an hourly mean of all angles
        above the horizon.'''
        data_5min = pd.DataFrame(
            index=pd.date_range(data.index[0],
                                periods=kwargs['hoy']*12, freq='5Min',
                                tz=kwargs['tz']))

        data_5min = pvlib.solarposition.get_solarposition(
            time=data_5min.index, location=location, method='ephemeris')

        return pd.concat(
            [data, data_5min.clip_lower(0).resample('H', how='mean')],
            axis=1, join='inner')

    def solarposition(location, data, **kwargs):
        'Determine the position of the sun unsing the time of the time index.'
        return pd.concat(
            [data, pvlib.solarposition.get_solarposition(
                time=data.index, location=location, method='ephemeris')],
            axis=1, join='inner')

    def angle_of_incidence(self, data, **kwargs):
        'Determine the angle of incidence'
        return pvlib.irradiance.aoi(
            solar_azimuth=data['zenith'], solar_zenith=data['zenith'],
            surface_tilt=kwargs['tilt'], surface_azimuth=kwargs['azimuth'])

    def global_in_plane_irradiation(self, data, **kwargs):
        ''

        # Determine the extraterrestrial radiation
        data['dni_extra'] = pvlib.irradiance.extraradiation(
            datetime_or_doy=data.index.dayofyear)

        # Determine the relative air mass
        data['airmass'] = pvlib.atmosphere.relativeairmass(data['zenith'])

        # Determine direct normal irradiation
        data['dni'] = (data['dirhi']) / np.sin(np.radians(data['elevation']))

        # what for??
        data['dni'][data['zenith'] > 88] = data['dirhi']

        # Determine the sky diffuse irradiation in plane
        # with model of Perez (modell switch would be good)
        data['poa_sky_diffuse'] = pvlib.irradiance.perez(
            surface_tilt=kwargs['tilt'],
            surface_azimuth=kwargs['azimuth'],
            dhi=data['dhi'],
            dni=data['dni'],
            dni_extra=data['dni_extra'],
            solar_zenith=data['zenith'],
            solar_azimuth=data['azimuth'],
            airmass=data['airmass'])

        # Set NaN values to zero
        data['poa_sky_diffuse'][
            pd.isnull(data['poa_sky_diffuse'])] = 0

        # Determine the diffuse irradiation from ground reflection in plane
        data['poa_ground_diffuse'] = pvlib.irradiance.grounddiffuse(
            ghi=data['dirhi'] + data['dhi'],
            albedo=kwargs['albedo'],
            surface_tilt=kwargs['tilt'])

        # Determine total in-plane irradiance
        data = pd.concat(
            [data, pvlib.irradiance.globalinplane(
                aoi=data['aoi'],
                dni=data['dni'],
                poa_sky_diffuse=data['poa_sky_diffuse'],
                poa_ground_diffuse=data['poa_ground_diffuse'])],
            axis=1, join='inner')

        return data

    def pv_module_output(self, data, **kwargs):
        ''
        # Determine module and cell temperature
        data['temp_air_celsius'] = data['temp_air'] - 273.15
        data = pd.concat([data, pvlib.pvsystem.sapm_celltemp(
            irrad=data['poa_global'],
            wind=data['v_wind'],
            temp=data['temp_air_celsius'],
            model='Open_rack_cell_polymerback')], axis=1, join='inner')

        # Retrieve the module data object
        module_data = (pvlib.pvsystem.retrieve_sam('SandiaMod')
                       [kwargs['module_name']])

        # Apply the Sandia PV Array Performance Model (SAPM) to get a
        data = pd.concat([data, pvlib.pvsystem.sapm(
            poa_direct=data['poa_direct'],
            poa_diffuse=data['poa_diffuse'],
            temp_cell=data['temp_cell'],
            airmass_absolute=data['airmass'],
            aoi=data['aoi'],
            module=module_data)], axis=1, join='inner')

        # Set NaN values to zero
        data['p_mp'][
            pd.isnull(data['p_mp'])] = 0

        # Determine the peak power of one module
        p_peak = module_data.Impo * module_data.Vmpo

        # Normalize the time series to 1 kW_peak
        data['p_pv_norm'] = data['p_mp'] * 10 ** 3 / p_peak

        return data

    def get_normalized_pv_time_series(self, **kwargs):
        'Normalized to one kW_peak'
        # If no DataFrame is given, try to get the data from a weather object
        if kwargs.get('data', None) is None:
            data = kwargs['weather'].get_feedin_data(
                gid=kwargs.get('gid', None))
        else:
            data = kwargs.pop('data')

        # Create a location object
        location = pvlib.location.Location(kwargs['latitude'],
                                           kwargs['longitude'],
                                           kwargs['tz'])

        # Determine the position of the sun
        data = self.solarposition_hourly_mean(location, data, **kwargs)

        # A zenith angle greater than 90° means, that the sun is down.
        data['zenith'][data['zenith'] > 90] = 90

        # Determine the angle of incidence
        data['aoi'] = self.angle_of_incidence(data, **kwargs)

        # Determine the irradiation in plane
        data = self.global_in_plane_irradiation(data, **kwargs)

        # Determine the output of the pv module
        data = self.pv_module_output(data, **kwargs)

        return data


class WindPowerPlant():
    ''

    def __init__(self, required):
        self.required = required

    def feedin(self, **kwargs):

        feedin_pd = self.feedin_as_pd(**kwargs)

        return list(feedin_pd)

    def feedin_as_pd(self, **kwargs):

        df = self.get_normalized_wind_pp_time_series(**kwargs)

        return df.p_wpp_norm

    def get_wind_pp_types(self, conn):
        # TODO@Günni
        sql = 'SELECT rli_anlagen_id, p_nenn FROM oemof_test.wea_cpcurves;'
        df = pd.DataFrame(conn.execute(sql).fetchall(), columns=[
            'type', 'p_peak']).sort(columns='type').reset_index(drop=True)
        pd.set_option('display.max_rows', len(df))
        print(df)
        pd.reset_option('display.max_rows')
        return df

    def fetch_data_heights_from_weather_object(self, **kwargs):
        ''
        dic = {}
        for key in kwargs['data'].keys():
            dic[key] = kwargs['weather'].get_data_heigth(key)
            if dic[key] is None:
                dic[key] = 0
        return dic

    def rho_hub(self, **kwargs):
        '''
        Calculates the density of air in kg/m³ at hub height.
            (temperature in K, height in m, pressure in Pa)
        Assumptions:
            Temperature gradient of -6.5 K/km
            Density gradient of -1/8 hPa/m
        '''
        print(kwargs['data_height'])
        h_temperature_data = kwargs['data_height']['temp_air']
        h_pressure_data = kwargs['data_height']['pressure']
        T_hub = kwargs['data'].temp_air - 0.0065 * (
            kwargs['h_hub'] - h_temperature_data)
        return (
            kwargs['data'].pressure / 100 -
            (kwargs['h_hub'] - h_pressure_data) * 1 / 8) / (2.8706 * T_hub)

    def v_wind_hub(self, **kwargs):
        '''
        Calculates the wind speed in m/s at hub height.
        h_windmast is the hight in which the wind velocity is measured.
        (height in m, velocity in m/s)
        '''
        return (kwargs['data'].v_wind * np.log(kwargs['h_hub'] /
                kwargs['data'].z0)
                / np.log(kwargs['data_height']['v_wind'] / kwargs['data'].z0))

    def cp_values(self, v_wind, **kwargs):
        '''
        Interpolates the cp value as a function of the wind velocity between
        data obtained from the power curve of the specified wind turbine type.
        '''
        ncols = ['rli_anlagen_id', 'p_nenn', 'source', 'modificationtimestamp']
        if kwargs.get('connection', None) is None:
            df = pd.read_hdf(
                join(expanduser("~"), '.oemof', 'cp_values.hf5'), 'cp')
            res_ls = df[df.rli_anlagen_id == kwargs[
                'wind_conv_type']].reset_index(drop=True)
        else:
            sql = '''SELECT * FROM oemof_test.wea_cpcurves
                WHERE rli_anlagen_id = '{0}';
                '''.format(kwargs['wka_model'])
            db_res = kwargs['connection'].execute(sql)
            res_ls = pd.DataFrame(db_res.fetchall(), columns=db_res.keys())

        cp_data = np.array([0, 0])
        for col in res_ls.keys():
            if col not in ncols:
                if res_ls[col][0] is not None:
                    cp_data = np.vstack((cp_data, np.array(
                        [float(col), float(res_ls[col])])))
        cp_data = np.delete(cp_data, 0, 0)
        self.nominal_power_wind_turbine = res_ls['p_nenn'][0]
        v_wind[v_wind > np.max(cp_data[:, 0])] = np.max(cp_data[:, 0])
        return interp1d(cp_data[:, 0], cp_data[:, 1])(v_wind)

    def turbine_power_output(self, **kwargs):
        '''
        Calculates the power output in W of one wind turbine.

        mamsl (meters above sea level) of the base of the wind turbine are
        set to mamsl of the weather station
        (height in m, diameter in m, power in W, density in kg/m³, temp.
        in °C, pressure in hPa, velocity in m/s)
        '''
        kwargs['data'].p_wpp = (
            (self.rho_hub(**kwargs) / 2) *
            (((kwargs['d_rotor'] / 2) ** 2) * np.pi) *
            np.power(self.v_wind_hub(**kwargs), 3) *
            self.cp_values(self.v_wind_hub(**kwargs), **kwargs))
        return kwargs['data'].p_wpp.clip(
            upper=(self.nominal_power_wind_turbine * 10 ** 3))

    def get_normalized_wind_pp_time_series(self, **kwargs):
        'Normalized to one kW installed capacity.'
        # If no DataFrame is given, try to get the data from a weather object
        if kwargs.get('data', None) is None:
            kwargs['data'] = kwargs['weather'].get_feedin_data(
                gid=kwargs.get('gid', None))
            kwargs['data_height'] = (
                self.fetch_data_heights_from_weather_object(**kwargs))

        kwargs['data']['p_wpp'] = np.array(list(map(
            float, self.turbine_power_output(**kwargs))))

        kwargs['data']['p_wpp_norm'] = (kwargs['data']['p_wpp'] /
                                        float(self.nominal_power_wind_turbine))
        return kwargs['data']


class ConstantModell:
    ''
    def __init__(self, required=["nominal_power", "steps"]):
        self.required = required

    def feedin(self, **ks):
        return [ks["nominal_power"]*0.9] * ks["steps"]
