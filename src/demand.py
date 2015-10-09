# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 19:11:38 2015

@author: caro
"""

import numpy as np
import pandas as pd
from . import energy_buildings as eb


class electrical_demand():
    '''
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

        #TODO: implement
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
                    self.calculate_annual_demand_households(**kwargs))# +
#                    self.comm_e_slp / self.comm_e_slp.sum()) *
#                    self.calculate_annual_demand_sectors(**kwargs) +
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

    def households_calc_ann_dem(self):
        return

    def commerce_calc_ann_dem(self):
        return

    def industry_calc_ann_dem(self):
        return


class heat_demand():
    # Das Gebäudeprofil kommt aus der Datenbank einer Datei oder einer anderen
    # Funktion.
    pass
