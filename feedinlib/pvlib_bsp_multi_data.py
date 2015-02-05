#!/usr/bin/python
# -*- coding: utf-8
import sys
from os import path

# Imports parts of the pahesmf package.
sys.path.append('/home/uwe/rli-lokal/git_home/pahesmf')
import src.basic.postgresql_db as db
import src.dinput.read_pahesmf as din

DIC = din.read_basic_dc()

##append the parent directory to the system path
#sys.path.append('/home/uwe/rli-lokal/git_home/reegis')
#import pv

#append the parent directory to the system path
#appends the parent directory to the system path
pvl_pth = path.join(path.dirname(path.realpath(__file__)), 'PVLIB_Python')
sys.path.append(pvl_pth)

import pvlib  # imports pvlib into the namespace
import pandas as pd  # imports pandas into the namespace and renames it to pd
from datetime import datetime  # functions for dealing with dates and times
import matplotlib.pyplot as plt
import numpy as np


#Example script for using PVLIB with coastDAT

# 0. Define Parameter for this test field
raster_id = 49
year = 2010
schema = 'weather'
tables = ['solar_direct_timeseries', 'solar_diffus_timeseries']
columns = ['solar_radiation']
orderby = 'hour'
module_name = 'Advent_Solar_Ventura_210___2008_'

# Folgende Werte sollten eigentlich ermittelt werden
region = {'azimuth': 0,
      'tilt': 0,
      'parallelStrings': 1,
      'seriesModules': 1,
      'TZ': 0.5,
      'albedo': .2}

region_id = 11001
table_polygon_region = 'deutschland.deu3_21'
column_reg_id = 'region_id'
table_point_raster = 'weather.solar_raster_register'
column_raster_id = 'raster_id'

sql_str = ('select r.{0} from {1} as p, {2} as r ' +
'''where st_contains(p.geom, r.geom) and p.{3}={4};''')

db_str = sql_str.format(column_raster_id, table_polygon_region,
    table_point_raster, column_reg_id, region_id)

raster_id_tp = db.execute_read_db(DIC, db_str)

data = pd.DataFrame(index=pd.date_range(datetime(year, 1, 1, 0, 0, 0),
        periods=8760, freq='H', tz='Europe/Berlin'))

# 1. Read solar radiation from database

tmp = {}
for rid in raster_id_tp:
    whr_str = 'raster_id={0} and year={1}'.format(rid[0], year)
    #print whr_str
    for table in tables:
        key = str(rid[0]) + table
        tmp[key] = db.fetch_columns(DIC, schema, table, columns,
            orderby=orderby, as_np=True,
            where_string=whr_str)['solar_radiation']
        print key
        print sum(tmp[key])

exit(0)

data['temp'] = db.fetch_columns(DIC, 'wittenberg', 'try_2010_av_year',
    'air_temp', orderby='id', as_np=True, where_column='region',
    where_condition=4)['air_temp']

data['v_wind'] = db.fetch_columns(DIC, 'wittenberg', 'try_2010_av_year',
    'v_wind', orderby='id', as_np=True, where_column='region',
    where_condition=4)['v_wind']

data['GHI'] = tmp['solar_direct_timeseries'] + tmp['solar_diffus_timeseries']
data['DHI'] = tmp['solar_diffus_timeseries']

# 2. Fetch region data (longitude, latitude,...)
table = 'solar_raster_register'
columns = ['longitude', 'latitude', 'region_id', 'idx_lat', 'idx_lon']

region.update(db.fetch_row(DIC, schema, table, where_column='raster_id',
    where_condition=raster_id))

## Testblock
#plt.plot(I['global_horizontal'])
#plt.plot(I['diffus_horizontal'])
#plt.show()

# Determines the postion of the sun
(data['SunAz'], data['SunEl'], data['AppSunEl'], data['SolarTime'],
    data['SunZen']) = pvlib.pvl_ephemeris(Time=data.index, Location=region)

#date = data.index
#h, az = pv.position_sun(region['latitude'], region['longitude'], year,
        #date.month, date.day, date.hour)
#h[h < 0] = 0
beam_hrz = data['GHI'] - data['DHI']

data['HExtra'] = pvlib.pvl_extraradiation(doy=data.index.dayofyear)
data['AM'] = pvlib.pvl_relativeairmass(z=data['SunZen'])
data['AOI'] = pvlib.pvl_getaoi(SunAz=data['SunAz'], SunZen=data['SunZen'],
    SurfTilt=region['tilt'], SurfAz=region['azimuth'])

data['AOI'][data['AOI'] > 90] = 90

data['DNI'] = (beam_hrz) / np.cos(np.radians(data['SunZen']))
#data['DNI'] = (data['GHI'] - data['DHI']) / np.sin(h)

data['DNI'][data['SunZen'] > 88] = beam_hrz


#plt.plot(data['DNI'])
#plt.plot(beam_hrz)
##plt.plot(np.degrees(h)[2160:2180] * 10)
#plt.plot((90 - data['SunZen']) * 10)
##plt.plot((data['GHI']))
##plt.plot((data['GHI'] - data['DHI']))
###plt.plot((data['GHI']))
###plt.plot((data['DHI']))
###plt.plot((data['SunZen']))
###plt.plot((np.cos(data['SunZen'] / 180 * np.pi) * 100))

#plt.show()

data['In_Plane_SkyDiffuseP'] = pvlib.pvl_perez(SurfTilt=region['tilt'],
                                            SurfAz=region['azimuth'],
                                            DHI=data['DHI'],
                                            DNI=data['DNI'],
                                            HExtra=data['HExtra'],
                                            SunZen=data['SunZen'],
                                            SunAz=data['SunAz'],
                                            AM=data['AM'])

data['In_Plane_SkyDiffuseP'][pd.isnull(data['In_Plane_SkyDiffuseP'])] = 0

data['In_Plane_SkyDiffuse'] = pvlib.pvl_klucher1979(region['tilt'],
    region['azimuth'], data['DHI'], data['GHI'], data['SunZen'], data['SunAz'])

#plt.plot(data['In_Plane_SkyDiffuse'])
#plt.plot(data['In_Plane_SkyDiffuseP'])
#plt.plot(data['DHI'])
#plt.show()

data['GR'] = pvlib.pvl_grounddiffuse(GHI=data['GHI'], Albedo=region['albedo'],
    SurfTilt=region['tilt'])

print data['DNI'][data['DNI'] < 0]
print 'GR'
print data['GR'][data['GR'] < 0]
print 'dif'
print data['In_Plane_SkyDiffuse'][data['In_Plane_SkyDiffuse'] < 0]
print 'res'

data['E'], data['Eb'], data['EDiff'] = pvlib.pvl_globalinplane(AOI=data['AOI'],
                                DNI=data['DNI'],
                                In_Plane_SkyDiffuse=data['In_Plane_SkyDiffuse'],
                                GR=data['GR'],
                                SurfTilt=region['tilt'],
                                SurfAz=region['azimuth'])

print data['AOI'][data['E'] < 0]

#plt.plot(data['GHI'])
plt.plot(data['temp'])
plt.show()

print sum(data['E'])
print sum(data['GHI'])

data['Tcell'], data['Tmodule'] = pvlib.pvl_sapmcelltemp(E=data['E'],
                            Wspd=data['v_wind'],
                            Tamb=data['temp'],
                            modelt='Open_rack_cell_polymerback')

print (('Breche ab, wegen fehlender Moduldatenbank.'))
exit(0)

# 3. Fetch module parameter from Sandia Database
module_data = (pvlib.pvl_retreiveSAM('SandiaMod')[module_name])

DFOut = pvlib.pvl_sapm(Eb=data['Eb'],
                    Ediff=data['EDiff'],
                    Tcell=data['Tcell'],
                    AM=data['AM'],
                    AOI=data['AOI'],
                    Module=module_data)


data['Pmp'] = DFOut['Vmp'] * DFOut['Imp']


print sum(data['Pmp'])
#Data['Imp']=DFOut['Imp']*meta['parallelStrings']
#Data['Voc']=DFOut['Voc']
#Data['Vmp']=DFOut['Vmp']*meta['seriesModules']
#Data['Pmp']=Data.Imp*Data.Vmp
#Data['Ix']=DFOut['Ix']
#Data['Ixx']=DFOut['Ixx']


## Wenn die Sonne untergegangen ist entstehen NaN-Werte im Diffus-Vektor
## Entweder auf Null setzen oder in der entsprechenden Funktion korrigieren.
#blubb = Data.as_blocks()['float64'].as_blocks()['float64']['Imp'].values
#bla = Data.as_blocks()['float64'].as_blocks()['float64']['Vmp'].values

#blubber = blubb * bla

#print blubb

plt.plot(data['Pmp'])
plt.plot(data['E'])
#plt.plot(bla)
#plt.plot(blubber)
plt.show()