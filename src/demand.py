# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 19:11:38 2015

@author: caro
"""

import numpy as np
import pandas as pd
from . import energy_buildings as eb


class electrical_demand():
    '''Calculate the electrical demand for a region with different methods.

    This class calculates the electrical demand for a region. Therefore
    several different methods can be applied.

    Parameters
    ----------
    method : {'csv', 'db', 'scale_profile_csv', scale_profile_db',
                  scale_entsoe', calculate_profile'}, required
        Method to calculate the demand for a region.
        Explanation:

        'csv' : read from csv

        'db' : read from database

        'scale_profile_csv': read only profile from csv and scale it with
            given or calculated demand

        'scale_profile_db': read only profile from database and scale it with
            given or calculated demand

        'scale_entsoe': read entsoe profile from database and scale it with
            given or calculated demand

        'calculate_profile: Calculate profile from the profiles of the
            three demand sectors (households, service, industry)

    Other Parameters
    ----------------
    'csv' :
        path :
        filename :

    'db' :
        conn :

    'scale_profile_csv' :
        path :
        filename :
        ann_el_demand :

    'scale_profile_db' and 'scale_profile_entsoe' :
        conn :
        ann_el_demand :

    'calculate_profile' :
        define_elec_buildings : ann_el_demand and selp_type for each sector


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

    Examples
    --------
    Examples?

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
        if method == 'csv':
            self.elec_demand = self.read_from_csv(path=
                                                  kwargs.get('path'),
                                                  filename=
                                                  kwargs.get('filename'))

        #TODO: implement
        elif method == 'db':
            conn = kwargs.get('conn')
            self.elec_demand = np.array([111, 222])

        elif method == 'scale_profile_csv':
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
                    'ann_el_demand'] is 'calculate':
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
