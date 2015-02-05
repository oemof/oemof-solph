#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by: Uwe Krien (uwe.krien@rl-institut.de)
Responsibility: Guido Plessmann, Uwe Krien
'''

import pulp
import logging
from . import basic_functions as bf


def resource_bus(main_dt, prob):
    '''
    Creates the busses for all resources.
    '''
    resource_list = list(main_dt['energy_system']['resources'].keys())

    # Removes 'natural gas (rnga)' from the resource list, if an extended gas
    # bus for natural gas will be needed.
    if main_dt['check']['extend_nat_gas_bus']:
        resource_list.remove('rnga')

    # Defines the connection between transformers and resources.
    prob = resource_consumption(main_dt, prob)

    ## Removes 'biogas (rbig)' from the resource list, because biogas allways
    ## doesn't need an yearly_limit but a dayly limit.
    if main_dt['check']['biogas']:
        resource_list.remove('rbig')

    # Sets the yearly limit for all resources, without the exceptions above.
    prob = resource_limitation(main_dt, prob)

    return prob


def resource_consumption(main_dt, prob):
    '''
    Defines the connection between resource consumption and power output of
    transformers
    '''
    logging.debug("Adding the connection between Resources and Transformers")

    for i in list(main_dt['energy_system']['resources'].keys()):
        variable_chp_ls = bf.cut_lists(
            main_dt['energy_system']['resources'][i]['chp'],
            main_dt['energy_system']['chp']['variable'])
        fixed_chp_ls = bf.cut_lists(
            main_dt['energy_system']['resources'][i]['chp'],
            main_dt['energy_system']['chp']['fixed'])
        if not (i == 'rnga' and 'splitted_gas_flow' in main_dt['lp']):
            for r in main_dt['energy_system']['regions']:
                for t in main_dt['timesteps']:
                    prob += (
                        # power from condensation power plants
                        pulp.lpSum((
                            main_dt['lp']['power_gen']['data'][c][t][r] /
                            main_dt['parameter']['component'][r][c]
                            ['efficiency'])
                            for c in
                            main_dt['energy_system']['resources'][i]['elec'])

                        # heat from heating systems
                        + pulp.lpSum((
                            main_dt['lp']['heat_gen']['data'][c][t][r] /
                            main_dt['parameter']['component'][r][c]
                            ['efficiency4heat']) for c in
                            main_dt['energy_system']['resources'][i]['heat'])

                        # power from chp plants with fixed ratio
                        + pulp.lpSum((
                            main_dt['lp']['power_gen']['data'][c][t][r] /
                            main_dt['parameter']['component'][r][c]
                            ['efficiency'])
                            for c in fixed_chp_ls)

                        # power from chp plants with variable ratio
                        + pulp.lpSum((
                            main_dt['lp']['power_gen']['data'][
                                main_dt['energy_system']['chp']['dict'][c]
                                ][t][r] /
                            main_dt['parameter']['component'][r][c]
                            ['efficiency4elec_cond'])
                            for c in variable_chp_ls)
                        + pulp.lpSum((
                            main_dt['lp']['power_gen']['data'][c][t][r] /
                            main_dt['parameter']['component'][r][c]
                            ['efficiency'])
                            for c in variable_chp_ls)

                        # gas from gas converters
                        + pulp.lpSum(((
                            main_dt['lp']['gas_gen']['data'][c][t][r] /
                            main_dt['parameter']['component'][r][c]
                            ['efficiency'])
                            for c in
                            main_dt['energy_system']['resources'][i].get(
                                'gas', []))
                            if 'gas' in main_dt['energy_system']['resources']
                            [i]else 0)

                        # equals resource usage
                        == main_dt['lp']['fossil_resources']['data'][i][t][r],
                        "ResourceConsumption_" + i + r + str(t))
    return prob


def resource_limitation(main_dt, prob):
    '''
    Adds constraints for the yearly limitation of a resource if set.
    '''
    logging.debug("Adding the yearly limitation of resource use if set.")

    for i in list(main_dt['energy_system']['resources'].keys()):
        for r in main_dt['energy_system']['regions']:
            yearly_limit = (main_dt['parameter']['resources']
                            [r][i]['yearly_limit'])
            if yearly_limit < (10 ** 99):
                # Will reduce the yearly limit,
                # if the time interval is less than 8760 hours.
                yearly_limit = yearly_limit * ((
                    main_dt['simulation']['timestep_end'] -
                    main_dt['simulation']['timestep_start']) / 8760.)
                prob += (
                    pulp.lpSum(
                        main_dt['lp']['fossil_resources']['data'][i][t][r]
                        for t in main_dt['timesteps']) <= yearly_limit,
                    'Resource_limit_year_{0}_{1}'.format(r, i))
    return prob
