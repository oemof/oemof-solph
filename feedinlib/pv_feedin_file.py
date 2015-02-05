#!/usr/bin/python
# -*- coding: utf-8
import sys
from os import path
import dblib as db

#appends the parent directory to the system path
pvl_pth = path.join(path.dirname(path.realpath(__file__)), 'PVLIB_Python')
sys.path.append(pvl_pth)

import pvlib  # imports pvlib into the namespace
import pandas as pd  # imports pandas into the namespace and renames it to pd
from datetime import datetime  # functions for dealing with dates and times
import numpy as np
import time


def param_definition():
    param = {}
    param['year'] = 2012
    param['module_name'] = 'Advent_Solar_Ventura_210___2008_'

    # Folgende Werte sollten eigentlich ermittelt werden
    region = {'azimuth': 0,
          'tilt': 0,
          'parallelStrings': 1,
          'seriesModules': 1,
          'TZ': 0.5,
          'albedo': .2}
    return param, region


def coastdat_timeseries_string(region, year, datasets, datatype=None):
    '''returns selected coastdat datasets'''

    where_str = ""
    if datatype is None:
        for t in datasets:
            where_str += "dt.name = '{0}' or ".format(t)
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
                            SELECT gid, geom
                            FROM coastdat.cosmoclmgrid
                            where st_contains(geom, st_setsrid(st_makepoint({2}, {3}),4326))
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
    ;'''.format(where_str, year, region['longitude'], region['latitude'])

def retrieve_coastdat_data(DIC, region, data, year, dataset):
    '''Returns coastDat data sets for given coordinates. Output can be either
    timeseries for a single point or dict containing coordinates of given
    region depending of data input type.

    If data input type == pair of coordinates, return is single point
    If data input type == geom, return is dict of multiple points'''
    tmp_array = coastdat_get_line(DIC, region, year, dataset)
    data = tmp_array

    return data


def empty_data_frame(param):
    '''Returns an empty panda data frame with shape of one year'''
    return pd.DataFrame(index=pd.date_range(datetime(param['year'], 1, 1, 0,
        0, 0), periods=8760, freq='H', tz='Europe/Berlin'))


def scale_output_power(module_data):
    '''Scales modules to 1kWp output Power (based on Impo and Vmpo)'''
    module_data['Area'] = (1000 / (module_data['Impo'] * module_data['Vmpo']) *
        module_data['Area'])
    return module_data


def apply_pvlib_model(data, region, param):
    '''Apply main PVlib equations in order to retrieve power output of PV
    array'''
    # fetch module parameter from Sandia Database
    module_data = (pvlib.pvl_retreiveSAM('SandiaMod')[param['module_name']])

    # Determines the postion of the sun
    (data['SunAz'], data['SunEl'], data['AppSunEl'], data['SolarTime'],
        data['SunZen']) = pvlib.pvl_ephemeris(Time=data.index, Location=region)

    # calculate horizontal beam fraction
    beam_hrz = data['GHI'] - data['ASWDIFD_S']

    # get extraterrestrial radiation, air mass (AM) and angle of incidence (AOI)
    data['HExtra'] = pvlib.pvl_extraradiation(doy=data.index.dayofyear)
    data['AM'] = pvlib.pvl_relativeairmass(z=data['SunZen'])
    data['AOI'] = pvlib.pvl_getaoi(SunAz=data['SunAz'], SunZen=data['SunZen'],
        SurfTilt=region['tilt'], SurfAz=region['azimuth'])

    # limit angle of incidence to 90°
    data['AOI'][data['AOI'] > 90] = 90

    # ??
    data['DNI'] = (beam_hrz) / np.cos(np.radians(data['SunZen']))

    # ??
    data['DNI'][data['SunZen'] > 88] = beam_hrz

    # apply perez model
    data['In_Plane_SkyDiffuseP'] = pvlib.pvl_perez(SurfTilt=region['tilt'],
                                                SurfAz=region['azimuth'],
                                                DHI=data['ASWDIFD_S'],
                                                DNI=data['DNI'],
                                                HExtra=data['HExtra'],
                                                SunZen=data['SunZen'],
                                                SunAz=data['SunAz'],
                                                AM=data['AM'])

    # handle isnull data
    data['In_Plane_SkyDiffuseP'][pd.isnull(data['In_Plane_SkyDiffuseP'])] = 0

    # apply klucher model
    data['In_Plane_SkyDiffuse'] = pvlib.pvl_klucher1979(region['tilt'],
        region['azimuth'], data['ASWDIFD_S'], data['GHI'], data['SunZen'],
        data['SunAz'])

    # estimates diffuse irradiance from ground reflections
    data['GR'] = pvlib.pvl_grounddiffuse(GHI=data['GHI'],
    Albedo=region['albedo'], SurfTilt=region['tilt'])

    # global in-plane irradiance
    data['E'], data['Eb'], data['EDiff'] = pvlib.pvl_globalinplane(
        AOI=data['AOI'],
        DNI=data['DNI'],
        In_Plane_SkyDiffuse=data['In_Plane_SkyDiffuse'],
        GR=data['GR'],
        SurfTilt=region['tilt'],
        SurfAz=region['azimuth'])

    # estimate cell temperature
    data['Tcell'], data['Tmodule'] = pvlib.pvl_sapmcelltemp(E=data['E'],
                                Wspd=data['WSS_10M'],
                                Tamb=data['T_2M'],
                                modelt='Open_rack_cell_polymerback')

    # apply sandia array performance model
    DFOut = pvlib.pvl_sapm(Eb=data['Eb'],
                        Ediff=data['EDiff'],
                        Tcell=data['Tcell'],
                        AM=data['AM'],
                        AOI=data['AOI'],
                        Module=module_data)

    # calculate output power from voltage and current
    data['Pmp'] = DFOut['Pmp']

    return data['Pmp'] / (module_data['Impo'] * module_data['Vmpo'])


def pv_timeseries(param, region, DIC, year, time_range=None):
    '''returns a timeseries for a given photovoltaic system at a given location
    '''
    start = time.time()

    if time_range is None:
        time_range = range(0,8760)

    # define translation dict between coastDat and PBlib data sets
    datasets = ['ASWDIFD_S', 'ASWDIR_S','WSS_10M', 'T_2M']

    # create empty data frame
    data = empty_data_frame(param)

    # view creation string
    #TODO: later ;)

    # retrieve coastdat timeseries
    read_str = coastdat_timeseries_string(region, year, datasets)

    # Execute sql commands.
    data_raw = db.execute_read_db(DIC, read_str)

    # Writes all datasets into a dict.
    # The keys of the dict are the GEO-IDs (gid).
    data_dc = {}
    for t in xrange(len(data_raw)):
        t_key = data_raw[t][6]
        for n in range(len(data_raw) / len(datasets)):
            data_dc.setdefault(data_raw[n][0], {})
            data_dc[data_raw[n][0]][t_key] = np.array(data_raw[t][3])

    # temporarily get spatial_id from only key of data_dc
    spatial_id = data_dc.keys()[0]

    # determine global horizontal irradiation from fractions
    for k in data_dc[spatial_id].keys():
        data[k] = data_dc[spatial_id][k][time_range]
    data['GHI'] = data['ASWDIR_S'] + data['ASWDIFD_S']

    # hack on temperature data: convert celsius to kelvin
    data['T_2M'] = data['T_2M'] - 273.15

    # apply PVlib model
    timeseries = apply_pvlib_model(data, region, param)

    print('Total time: ' + str((time.time() - start)))
    # timeseries is currently relativ to peak power
    return timeseries
