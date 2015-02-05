#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by:
Responsibility: Guido Plessmann
'''

import pulp
import logging


def renewables_share(main_dc, prob):
    '''
    This functions defines constraints which limit fossil power generation
    to a user given share on total power generation
    '''
    logging.debug('Adding control constraint: renewable share.')
    other_fossil = ([x for x in main_dc['energy_system']['transformer']['elec']
        if x not in ['tccg', 'tocg', 'tnuc', 'twpp']])

    demand_elec_total_all = 0
    for r in main_dc['energy_system']['regions']:
        demand_elec_total_all += sum(main_dc['timeseries']['demand'][r]['lele'])

    prob += (pulp.lpSum(
                main_dc['lp']['splitted_gas_flow']['data'][c][t][r] *
                (main_dc['parameter']['component'][r][c]['efficiency'])
                for c in (main_dc['energy_system']['resources']['rnga']['elec'])
                for t in main_dc['timesteps']
                for r in main_dc['energy_system']['regions'])

            + pulp.lpSum(
                main_dc['lp']['power_gen']['data'][i][t][r]
                for i in other_fossil
                for t in main_dc['timesteps']
                for r in main_dc['energy_system']['regions'])
                == (1 - main_dc['simulation']['re_share']) *
                demand_elec_total_all, "renewables share")
    return prob