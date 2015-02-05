#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien
'''

import logging
#from ..basic import basic_functions as bf


def chp_ratio(main_dc, prob):
    '''
    Adding constraints to connect the heat and the power stream
    '''
    logging.debug("Adding chp-constraints")
    for r in main_dc['energy_system']['regions']:
        for i in main_dc['energy_system']['transformer']['chp']:
            for t in main_dc['timesteps']:
                prob += (main_dc['lp']['heat_gen']['data'][i][t][r] /
                    main_dc['parameter']['component'][r][i]
                        ['efficiency4heat']
                    == main_dc['lp']['power_gen']['data'][i][t][r] /
                    main_dc['parameter']['component'][r][i]
                        ['efficiency'])
    return prob