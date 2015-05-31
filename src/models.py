# -*- coding: utf-8 -*-
"""
Created on Wed May 13 08:43:54 2015

@author: dozeumwic
"""

from datetime import datetime
from functools import reduce
from random import random

import pandas as pd
import pvlib

class Photovoltaic:
    def __init__(self, required):
        self.required = required

    def feedin(self, **kwargs):
        
        time = pd.DataFrame(
                # TODO: the year variable in the line below is not defined
                #   index=pd.date_range(datetime(int(year), 1, 1, 0, 0, 0),
                # Somebody should check whether getting this from the 'kwargs'
                # is correct.
                index=pd.date_range(datetime(int(kwargs["year"]),
                                             1, 1, 0, 0, 0),
                # TODO: check whether 'site' should really be an attribute of
                #       the 'powerplant'. Again, it was a standalone variable
                #       which was never defined. As this looks like something
                #       which should belong to 'powrplant', I put it there.
                                    periods=self.powerplant.site['hoy'],
                                    freq='H',
                                    tz=self.powerplant.site['TZ']))
        
        return time


    def module_data_and_location(self, **kwargs):
        
        module_data = (pvlib.pvsystem.retrieve_sam('SandiaMod')
            [kwargs['module_name']])
            
        # area

        TZ = 'Europe/Berlin' # temp

        location = pvlib.location.Location(kwargs['latitude'],
                                                kwargs['longitude'],
                                                TZ)
            
        return [module_data, location]
    
    
    def solarposition(time, location):

        DaFrOut = pvlib.solarposition.get_solarposition(time=time,
            location=location, method='pyephem')  # method ephemeris

        sun_azimuth = DaFrOut['azimuth']
        sun_elevation = DaFrOut['elevation']
        app_sun_elevation = DaFrOut['apparent_elevation']
        solar_time = DaFrOut['solar_time']
        sun_zenith = DaFrOut['zenith']
#        data['SunZen_b'] = DaFrOut_b['zenith']
#        data['SunEl_b'] = DaFrOut_b['elevation']
        
        return [sun_azimuth, sun_elevation, sun_zenith]


    def irradiation_and_atmosphere(data, time, sun_zenith):
        
         # 4. Determine the global horizontal irradiation
        data['GHI'] = data['DirHI'] + data['DHI']

        # 5. Determine the extraterrestrial radiation
        H_extra = pvlib.irradiance.extraradiation(
            datetime_or_doy=time.dayofyear)

        # 6. Determine the relative air mass
        relative_airmass = pvlib.atmosphere.relativeairmass(z=data['SunZen'])
        
        return [H_extra, relative_airmass]
        
        
    def angle_of_incidence(sun_azimuth, sun_zenith, **kwargs):
        
        aoi = pvlib.irradiance.aoi(sun_az=sun_azimuth,
            sun_zen=sun_zenith, surf_tilt=kwargs['tilt'],
            surf_az=kwargs['azimuth'])
            
        return aoi


class ConstantModell:
    def __init__(self, required = ["nominal_power", "steps"]):
      self.required = required
    def feedin(self, **ks): return [ks["nominal_power"]*0.9] * ks["steps"]