# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 19:11:38 2015

@author: caro
"""

import numpy as np
import pandas as pd
from oemof.demandlib import energy_buildings as eb


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
        ann_el_demand_per_sector : list of dictionaries
            Specification of annual electric demand and the corresponding
            standard load profile type (selp_type) for every sector, e.g.
                ann_el_demand_per_sector = [
                    {'ann_el_demand': int or None,
                     'selp_type: {'h0', 'g0', 'g1', 'g2', 'g3', 'g4', 'g5',
                                  'g6', 'i0'}},
                                  ...]
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

        self.dataframe = kwargs.get('dataframe')

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

#            self.hh_e_slp = self.e_slp['h0']
            self.hh_e_slp = self.e_slp[kwargs.get(
                                       'ann_el_demand_per_sector')[0][
                                       'selp_type']]
            self.comm_e_slp = self.e_slp[kwargs.get(
                                         'ann_el_demand_per_sector')[1][
                                         'selp_type']]
            self.ind_e_slp = self.e_slp[kwargs.get(
                                        'ann_el_demand_per_sector')[2][
                                        'selp_type']]

            if kwargs.get('ann_el_demand_per_sector')[0][
                    'ann_el_demand'] is None:
                self.elec_demand = (
                    self.hh_e_slp / self.hh_e_slp.sum() *
                    self.calculate_annual_demand_households(**kwargs) +
                    self.comm_e_slp / self.comm_e_slp.sum() *
                    self.calculate_annual_demand_commerce(**kwargs)) #+
#                    self.ind_e_slp / self.ind_e_slp.sum()) *
#                    self.calculate_annual_demand_sectors(**kwargs))

            else:

                self.elec_demand = (self.hh_e_slp / self.hh_e_slp.sum() *
                                    kwargs.get(
                                        'ann_el_demand_per_sector')[0][
                                        'ann_el_demand'] +
                                    self.comm_e_slp / self.comm_e_slp.sum() *
                                    kwargs.get(
                                        'ann_el_demand_per_sector')[1][
                                        'ann_el_demand'] +
                                    self.ind_e_slp / self.ind_e_slp.sum() *
                                    kwargs.get(
                                        'ann_el_demand_per_sector')[2][
                                        'ann_el_demand'])

        return self.elec_demand

    def read_from_csv(self, **kwargs):
        '''
        read entire demand timeseries or only profile for further
        processing from csv
        '''
        self.profile = pd.read_csv(kwargs.get('path') +
                                   kwargs.get('filename'),
                                   sep=",")

        self.year = 2010  # TODO: year temporarily

        self.profile = self.profile['deu_' + str(self.year)]

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
