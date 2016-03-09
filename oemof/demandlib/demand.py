# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 19:11:38 2015

@author: caro
"""

import numpy as np
import pandas as pd
from oemof.demandlib import energy_buildings as eb
from oemof.tools import helpers


class electrical_demand():
    '''Calculate the electrical demand for a region with different methods.

    This class calculates the electrical demand for a region. Therefore
    several different methods can be applied.

    Parameters
    ----------
    method : {'scale_profile_csv', scale_profile_db',
                  scale_entsoe', calculate_profile'}, required
        Method to calculate the demand for your region.
        Explanation:

        'scale_profile_csv': read only profile from csv and scale it with
            given or calculated demand

        'scale_profile_db': read only profile from database and scale it with
            given or calculated demand

        'scale_entsoe': read entsoe profile from database and scale it with
            given or calculated demand

        'calculate_profile: Calculate profile from the standard load profiles
            of the three demand sectors (households, service, industry) and
            the corresponding annual electric demand.

    Other Parameters
    ----------------
    Required according to chosen method.

    {'scale_profile_csv'} :
        path : str
            '/path/to/file'
        filename : str
            'filename.csv'

    {'scale_profile_db', 'scale_profile_entsoe'} :
        conn :

    {'scale_profile_csv', 'scale_profile_db', 'scale_profile_entsoe'} :
        annual_elec_demand : int
            Annual demand of your region. Works so far only with a given
            value. Calculating the demand from statistic data for the whole
            region can be an option for further development.

    {'calculate_profile'} :
        ann_el_demand_per_sector : dictionary
            Specification of annual electric demand and the corresponding
            standard load profile type (selp_type) for every sector. Dictionary
            is structured as follows. Key defining the sector is followed by
            value that can be int, float, None or can be omitted, e.g.
                ann_el_demand_per_sector = {
                    'h0': int, 
                    'g0': float,
                    'g1': None,
                    ...                    
                    'g6': int,
                    'i0': int}
                    
            if ann_el_demand is None, more parameters to calculate the demand
            are necessary: (works so far only if ann_el_demand for every or
                no sector is specified)

        population : int
            Population of your region.

        ann_el_demand_per_person : list of dictionaries
            Specification of the annual electric demand for one household
            according to the household type (from single to four-person
            households), e.g.
                ann_el_demand_per_person = [
                    {'ann_el_demand': int,
                     'household_type': {'one', 'two', 'three', 'four'}},
                     ...]

        household_structure : list of dictionaries
            Number of people living in every household type. Specification
            for your region, e.g.
                household_structure = [
                    {household_members': int,
                     'household_type': {'one', 'two', 'three', 'four'}},
                     ...]

        comm_ann_el_demand_state : int
            Annual electric demand of the service sector of the next bigger
            region, if not given for your region.

        comm_number_of_employees_state : int
            Number of employees in the service sector of the next bigger
            region.

        comm_number_of_employees_region : int
            Number of employees in the service sector of your region.


    Attributes
    ----------
    annual_demand : int
        Included in **kwargs. Given with initialization or calculated or
        to be calculated within this class according to selected method.

    dataframe : pandas dataframe

    elec_demand : array_like

    profile :

    e_slp :

    Returns
    -------

    Notes
    -----
    .. math::

    References
    ----------
    statistics ...

    B. Schachler: Bewertung des Einsatzes von Kraft-Wärme-Kopplungsanlagen
    hinsichtlich der CO2-Emissionen bei wachsendem Anteil Erneuerbarer
    Energien, Masterarbeit, Technische Universität Berlin, 2014

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    z. B. Summe bilden von elec_demand und abgleichen mit ann_el_demand


    '''
    def __init__(self, method, **kwargs):
        self.annual_demand = kwargs.get('annual_elec_demand')
        if self.annual_demand is None:
            self.annual_demand = self.calculate_annual_demand_region()

        self.dataframe = helpers.create_basic_dataframe(kwargs.get('year'))

        self.decider(method, **kwargs)

    def decider(self, method, **kwargs):
        '''
        '''
        if method == 'scale_profile_csv':
            self.profile = self.read_from_csv(path=
                                              kwargs.get('path'),
                                              filename=
                                              kwargs.get('filename'))
            self.elec_demand = self.scale_profile()

        #TODO: implement
        elif method == 'scale_profile_db':
            conn = kwargs.get('conn')
            self.elec_demand = np.array([111, 222])

        #TODO: implement
        elif method == 'scale_entsoe':
            conn = kwargs.get('conn')
            self.elec_demand = np.array([111, 222])

        #TODO: implement industry + def scale_profile() verwenden
        elif method == 'calculate_profile':
            self.conn = kwargs.get('conn')
            self.e_slp = self.read_selp().slp

            # normalize slp timeseries to annual sum of one
            self.e_slp = self.e_slp / self.e_slp.sum(axis=0)
            
            # calculate annual demand for sectors with `None`
            for key in kwargs['ann_el_demand_per_sector'].keys():
                
                if kwargs['ann_el_demand_per_sector'][key] is None:
                    if key.startswith('g', 0, 1):
                        kwargs['ann_el_demand_per_sector'][key] = (
                            self.calculate_annual_demand_commerce(**kwargs))
                    elif key.startswith('h', 0, 1):
                        kwargs['ann_el_demand_per_sector'][key] = (
                            self.calculate_annual_demand_households(**kwargs))
                    elif key.startswith('i', 0, 1):
                        pass
            
            # multiply given annual demand with timeseries
            self.elec_demand = self.e_slp.multiply(pd.Series(
                kwargs['ann_el_demand_per_sector']), axis=1).dropna(how='all',
                axis=1)

        return self.elec_demand

    def read_from_csv(self, **kwargs):
        '''
        read entire demand timeseries or only profile for further
        processing from csv
        '''
        self.profile = pd.read_csv(kwargs.get('path') +
                                   kwargs.get('filename'),
                                   sep=",")

        return self.profile

    def read_from_db(self):
        '''
        read entire demand timeseries or only profile for further
        processing from database
        '''
        return

    def read_entsoe(self):
        return

    def read_selp(self):
        self.e_slp = eb.bdew_elec_slp(self.conn, self.dataframe)
        return self.e_slp

    def scale_profile(self):
        '''
        scale a given profile to a given annual demand, which is the sum
        of the single profile values
        '''
        self.elec_demand = (self.profile /
                            self.profile.sum() *
                            self.annual_demand)
        return self.elec_demand

    #TODO: implement??
    def calculate_annual_demand_region(self):
        '''
        calculate annual demand from statistic data
        '''
        self.annual_demand = 50 + 50
        return self.annual_demand

    def calculate_annual_demand_households(self, **kwargs):
        hh_ann_el_demand_per_person = (kwargs.get('household_structure')[0][
            'household_members'] / kwargs.get('household_members_all') *
            kwargs.get('ann_el_demand_per_person')[0]['ann_el_demand'] +
            kwargs.get('household_structure')[1][
                'household_members'] / kwargs.get('household_members_all') *
            kwargs.get('ann_el_demand_per_person')[1]['ann_el_demand'] +
            kwargs.get('household_structure')[2][
                'household_members'] / kwargs.get('household_members_all') *
            kwargs.get('ann_el_demand_per_person')[2]['ann_el_demand'] +
            kwargs.get('household_structure')[3][
                'household_members'] / kwargs.get('household_members_all') *
            kwargs.get('ann_el_demand_per_person')[3]['ann_el_demand'])

        return  kwargs.get('population') * hh_ann_el_demand_per_person

    def calculate_annual_demand_commerce(self, **kwargs):
        return (kwargs.get('comm_ann_el_demand_state') /
                    kwargs.get('comm_number_of_employees_state') *
                    kwargs.get('comm_number_of_employees_region'))


class heat_demand():
    # not implemented yet
    pass
