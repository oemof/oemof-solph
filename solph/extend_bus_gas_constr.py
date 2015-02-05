#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by:
Responsibility: Guido Plessmann
'''


import pulp
from . import basic_functions as bm


def gas_bus(main_dc, prob):
    '''
    This function generates the constraint describing the gas bus
    '''
    storage4gas = main_dc['energy_system']['storages'].get('gas', [])
    ptg = main_dc['energy_system']['transformer'].get('gas', [])
    gas_pp = ([x for x in (main_dc['energy_system']
        ['transformer']['elec']) if x in ['tocg', 'tccg']])

    for r in main_dc['energy_system']['regions']:
        for t in main_dc['timesteps']:
                prob += (
                pulp.lpSum(
                main_dc['lp']['gas_storage_discharge']['data'][s][t][r]
                for s in storage4gas) +
                (main_dc['lp']['gas_gen']['data']['tptg'][t][r] if ptg else 0)
                == pulp.lpSum(
                main_dc['lp']['gas_storage_charge']['data'][s][t][r]
                for s in storage4gas) +
                (pulp.lpSum((main_dc['lp']['sng_resources']['data'][c][t][r])
                for c in (main_dc['energy_system']['resources']['rnga']['elec'])
                if gas_pp)), "gas bus" + str(t) + r)
    return prob


def ptg_power_lim(main_dc, prob):
    """
    Defines maximum power input to PtG (electrolysis process) according to rated
    capacity of PtG
    """

    for r in main_dc['energy_system']['regions']:
        for t in main_dc['timesteps']:
            for i in main_dc['energy_system']['transformer'].get('gas', []):
                if main_dc['simulation']['investment'] is True:
                    prob += (main_dc['lp']['gas_gen']['data'][i][t][r] <=
                    main_dc['lp']['gas_inst']['data'][i][r] +
                    main_dc['parameter']['component'][r][i]
                    ['installed_capacity'],
                    "Gas conv. power lim" + i + r + str(t))
                else:
                    prob += (main_dc['lp']['gas_gen']['data'][i][t][r] <=
                    main_dc['parameter']['component'][r][i]
                    ['installed_capacity'],
                    "feed-in energy" + i + r + str(t))
    return prob


def fossil_gas_flow_split(main_dc, prob):
    '''
    Defines relation between natural gas resource and two separated gas input
    flows into tocg and tccg
    '''

    for r in main_dc['energy_system']['regions']:
        for t in main_dc['timesteps']:
            prob += (main_dc['lp']['fossil_resources']['data']
                ['rnga'][t][r] ==
                pulp.lpSum(main_dc['lp']['splitted_gas_flow']['data']
                        [c][t][r]
                for c in main_dc['energy_system']['resources']['rnga']['elec']),
                "Gas_split" + r + str(t))
    return prob


def fossil_gas_consumption_split(main_dc, prob):
    '''resource consumption of gas power plants'''
    for r in main_dc['energy_system']['regions']:
        for c in main_dc['energy_system']['resources']['rnga']['elec']:
            for t in main_dc['timesteps']:
                prob += ((main_dc['lp']['power_gen']['data'][c][t][r] /
                    main_dc['parameter']['component']
                    [r][c]['efficiency']) == (
                    main_dc['lp']['splitted_gas_flow']['data'][c][t][r] +
                    (main_dc['lp']['sng_resources']['data'][c][t][r]
                    if ('gas' in main_dc['energy_system']
                    ['transformer']) else 0)), (
                    "Resources_" + c + r + str(t)))
    return prob


def biogas_bus(main_dc, prob):
    '''
    '''
    prev_timesteps = bm.get_prev_timsteps(main_dc)
    for r in main_dc['energy_system']['regions']:
        hourly_input = (main_dc['parameter']['resources'][r]['rbig']
            ['yearly_limit'] / 8760)
        soc_lim = size_of_biogas_storage(hourly_input, main_dc, r)
        for t in main_dc['timesteps']:
            prev_t = prev_timesteps[t]

            # connects input, state and output of the biogas storage
            prob += (main_dc['lp']['biogas_storage_soc']['data']['sbig'][t][r]
            == main_dc['lp']['biogas_storage_soc']['data']['sbig'][prev_t][r] -
            main_dc['lp']['fossil_resources']['data']['rbig'][t][r] /
            main_dc['parameter']['component'][r]['sbig']
            ['efficiency_out'] + hourly_input * main_dc['parameter']
            ['component'][r]['sbig']['efficiency_in'],
            'Biogas Storage state ' + ' in ' + r + '_t_' + str(t))

            # Limit of the state of charge of the biogas storage
            prob += (main_dc['lp']['biogas_storage_soc']['data']['sbig'][t][r]
                <= soc_lim)
    return prob


def size_of_biogas_storage(hourly_input, main_dc, r):
    '''
    A typical biogas plant has an integrated storage that can buffer biogas
    for some hours. This is defined in the parameter table of the biogas
    storage.
    In the presetting section can be added a addtional storage.
    In the model both storages are represented by one 'big' storage.
    '''
    return (hourly_input * main_dc['parameter']['component'][r]
        ['sbig']['buffer_time_hours']) + (
        main_dc['parameter']['component'][r]['sbig']['installed_capacity'])