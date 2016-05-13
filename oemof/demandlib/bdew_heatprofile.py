# -*- coding: utf-8 -*-
"""
Implementation of the bdew heat load profiles


"""
from math import ceil
import numpy as np
import pandas as pd
import os
from oemof.tools.helpers import create_basic_dataframe as basic_df


def weighted_temperature(df, how="geometric_series"):
    r'''
    A new temperature vector is generated containing a multi-day
    average temperature as needed in the load profile function.

    Parameters
    ----------
    df : pandas.DataFrame
        dataframe containing hourly temperature data in column with label
        "temperature"
    how : string
        string which type to return ("geometric_series" or "mean")

    Notes
    -----
    Equation for the mathematical series of the average tempaerature [1]_:

    .. math::
        T=\frac{T_{D}+0.5\cdot T_{D-1}+0.25\cdot T_{D-2}+
                0.125\cdot T_{D-3}}{1+0.5+0.25+0.125}

    with :math:`T_D` = Average temperature on the present day
         :math:`T_{D-i}` = Average temperature on the day - i

    References
    ----------
    .. [1] `BDEW <https://www.avacon.de/cps/rde/xbcr/avacon/15-06-30_Leitfaden_Abwicklung_SLP_Gas.pdf>`_, BDEW Documentation for heat profiles.
    '''

    # calculate daily mean temperature
    T = df["temperature"].resample('D', how='mean').reindex(
                                               df.index).fillna(method="ffill")
    if how == "geometric_series":
        Tmean = (T + 0.5 * np.roll(T, 24) +
                 0.25 * np.roll(T, 48) +
                 0.125 * np.roll(T, 72)) / 1.875

    if how == "mean":
        Tmean = T

    return Tmean


def get_temperature_interval(df):
    """
    Appoints the corresponding temperature interval to each temperature in
    the temperature vector.

    Parameters
    ----------

    df : pandas.DataFrame
        dataframe containing informations on temperature in column "temperature"



    """
    intervals = ({
        -20: 1, -19: 1, -18: 1, -17: 1, -16: 1, -15: 1, -14: 2,
        -13: 2, -12: 2, -11: 2, -10: 2, -9: 3, -8: 3, -7: 3, -6: 3, -5: 3,
        -4: 4, -3: 4, -2: 4, -1: 4, 0: 4, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5,
         6: 6, 7: 6, 8: 6, 9: 6, 10: 6, 11: 7, 12: 7, 13: 7, 14: 7, 15: 7,
        16: 8, 17: 8, 18: 8, 19: 8, 20: 8, 21: 9, 22: 9, 23: 9, 24: 9,
        25: 9, 26: 10, 27: 10, 28: 10, 29: 10, 30: 10, 31: 10, 32: 10,
        33: 10, 34: 10, 35: 10, 36: 10, 37: 10, 38: 10, 39: 10, 40: 10})

    temperature_rounded = [ceil(i) for i in df['temperature_geo']]

    temperature_interval = [intervals[i] for i in temperature_rounded]

    return np.transpose(np.array(temperature_interval))


def get_SF_values(df, datapath, filename="shlp_hour_factors.csv",
                 building_class=None, shlp_type=None):
    """ Determine the h-values

    Parameters
    ----------
    datapath : string
        path where csv files are located
    filename : string
        name of file where sigmoid factors are stored
    building_class: int
        class of building according to bdew classification

    """
    file = os.path.join(datapath, filename)
    hour_factors = pd.read_csv(file, index_col=0)
    hour_factors = hour_factors.query(
        'building_class=={0} and shlp_type=="{1}"'
        .format(building_class, shlp_type))

    # Join the two DataFrames on the columns 'hour' and 'hour_of_the_day'
    # or ['hour' 'weekday'] and ['hour_of_the_day', 'weekday'] if it is
    # not a residential slp.
    residential = building_class > 0
    left_cols = ['hour_of_day'] + (['weekday'] if not residential else [])
    right_cols = ['hour'] + (['weekday'] if not residential else [])
    SF_mat = pd.DataFrame.merge(
        hour_factors, df, left_on=left_cols, right_on=right_cols,
        how='outer', left_index=True).sort_index()

    # drop unnecessary columns
    drop_cols = (['hour_of_day', 'hour', 'building_class', 'shlp_type',
        'date', 'temperature'] + (['weekday_x'] if residential else []) +
        (['weekday_y'] if residential else []) +
        (['weekday'] if not residential else []))
    SF_mat = SF_mat.drop(drop_cols, 1)

    # Determine the h values
    SF = (np.array(SF_mat)[np.array(list(range(0, 8760)))[:],
        (get_temperature_interval(df) - 1)[:]])
    return np.array(list(map(float, SF[:])))


def get_sigmoid_parameters(datapath, building_class=None, shlp_type=None,
                           wind_class=None, ww_incl=True,
                           filename="shlp_sigmoid_factors.csv"):
    """ Retrieve the sigmoid parameters from csv-files

    Parameters
    ----------
    datapath : string
        path where csv files are located
    filename : string
        name of file where sigmoid factors are stored
    building_class: int
        class of building according to bdew classification
    shlp_type : string
        type of standard heat load profile according to bdew
    wind_class : int
        wind classification for building location (0=not windy or 1=windy)
    ww_incl : boolean
        decider whether warm water load is included in the heat load profile
    """

    file = os.path.join(datapath, filename)
    sigmoid = pd.read_csv(file, index_col=0)
    sigmoid = sigmoid.query(
        'building_class=={0} and '.format(building_class) +
        'shlp_type=="{0}" and '.format(shlp_type) +
        'wind_impact=={0}'.format(wind_class))

    A = float(sigmoid['parameter_a'])
    B = float(sigmoid['parameter_b'])
    C = float(sigmoid['parameter_c'])
    if ww_incl:
        D = float(sigmoid['parameter_d'])
    else:
        D = 0
    return A, B, C, D


def get_weekday_parameters(df, datapath, filename="shlp_weekday_factors.csv",
                           shlp_type=None):
    """ Retrieve the weekday parameter from csv-file

    Parameters
    ----------
    df : pandas.DataFrame
        dataframe containing informations on temperature and date/time
    datapath : string
        path where csv files are located
    filename : string
        name of file where sigmoid factors are stored
    shlp_type : string
        type of standard heat load profile according to bdew
    """
    file = os.path.join(datapath, filename)
    F_df = pd.read_csv(file, index_col=0)

    F_df = (F_df.query('shlp_type=="{0}"'.format(shlp_type)))

    F_df.drop('shlp_type', axis=1, inplace=True)

    F_df['weekdays'] = np.array(list(range(7))) + 1

    return np.array(list(map(float, pd.DataFrame.merge(
        F_df, df, left_on='weekdays', right_on='weekday', how='outer',
        left_index=True).sort()['wochentagsfaktor'])))


def create_bdew_profile(datapath, year, temperature, annual_heat_demand,
                        shlp_type, wind_class, **kwargs):
    """ Calculation of the hourly heat demand using the bdew-equations

    Parameters
    ----------
    year : int
        year or which the profile is created
    datapath : string
        path where csv-files with bdew data are located
    annual_heat_demand : float
        annual heat demand of building in kWh
    building_class: int
        class of building according to bdew classification
        possible numbers are: 1 - 11
    shlp_type : string
        type of standardized heat load profile according to bdew
        possible types are:
        GMF, GPD, GHD, GWA, GGB, EFH, GKO, MFH, GBD, GBA, GMK, GBH, GGA, GHA
    wind_class : int
        wind classification for building location (1 if windy, else 0)
    """

    df = basic_df(year, holidays=kwargs.get('holidays'))

    df["temperature"] = temperature.values

    df["temperature_geo"] = weighted_temperature(df, how="geometric_series")

    df['weekday'].mask(df['weekday'] == 0, 7, True)

    SF = get_SF_values(df=df, datapath=datapath,
                      building_class=kwargs.get('building_class', 0),
                      shlp_type=shlp_type)

    [A, B, C, D] = get_sigmoid_parameters(
                      datapath=datapath,
                      building_class=kwargs.get('building_class', 0),
                      wind_class=wind_class,
                      shlp_type=shlp_type,
                      ww_incl=kwargs.get('ww_incl', True))

    F = get_weekday_parameters(df, datapath, shlp_type=shlp_type)
    h = (A / (1 + (B / (df["temperature_geo"] - 40)) ** C) + D)
    KW = annual_heat_demand / (sum(h * F) / 24)
    heat_profile = (KW * h * F * SF)

    return heat_profile