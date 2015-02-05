#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by:
Responsibility: Guido Plessmann
'''

import pulp


def grid_constraint(main_dc, prob):
    #regions, timesteps,
    #transmission_line_power_neg, transmission_line_power_pos, lines,
    #prob, transmission_power, param_dict):
    '''
    defines sum of transmission power in each region according to kirchhoffs
    law for each time step
    # TODO
    # Definition von 'neg' und 'pos' klar machen
    '''
    lines_regions = main_dc['parameter']['transmission']
    lines = main_dc['energy_system']['transmission']

    eta = create_losses(main_dc)
    for r in main_dc['energy_system']['regions']:
        for t in main_dc['timesteps']:
            prob += (pulp.lpSum([[
                main_dc['lp']['trline_transfer']['data']['neg'][l][t] -
                main_dc['lp']['trline_transfer']['data']['pos'][l][t] * eta[l]
                for l in lines if (lines_regions[l]['from_region'] == r)] + [
                main_dc['lp']['trline_transfer']['data']['pos'][l][t] -
                main_dc['lp']['trline_transfer']['data']['neg'][l][t] * eta[l]
                for l in lines if (lines_regions[l]['to_region'] == r)]]) ==
                main_dc['lp']['trm_power']['data'][r][t],
                'Transmission power in ' + r + '_t_' + str(t))
    return prob


def create_losses(main_dc):
    """defines losses of power-lines"""
    eta = {}
    for l in main_dc['energy_system']['transmission']:
        eta[l] = 1 - \
        (main_dc['parameter']['transmission'][l]['length'] *
        main_dc['parameter']['transmission'][l]['relative_losses_per_1000_km']
            / 1000)
        # eta = 1-(length * relative losses /1000)
    return eta


def trg_power_lim(main_dc, prob):
    """limits transfered power to installed power """
    for t in main_dc['timesteps']:
        for l in main_dc['energy_system']['transmission']:
            prob += (main_dc['lp']['trline_transfer']['data']['neg'][l][t] +
                main_dc['lp']['trline_transfer']['data']['pos'][l][t] <= (
                main_dc['lp']['trm_inst']['data'][l]),
                'transmission limit ' + l + '_t_' + str(t))
    return prob