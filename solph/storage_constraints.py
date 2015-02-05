#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by Uwe Krien (uwe.krien:
Responsibility: Guido Plessmann
'''

from . import basic_functions as bm


def storage_state(main_dc, storage_type, prob):
    '''
    Constraint to connect the actual storage_state with the previous.

    soc(t) = soc(t-1) + (charge(t) / eta_charge) - (discharge(t) / eta_dischrg)
    '''
    prev_timesteps = bm.get_prev_timsteps(main_dc)

    m = storage_type

    for r in main_dc['energy_system']['regions']:
        for t in main_dc['timesteps']:
            prev_t = prev_timesteps[t]
            for s in main_dc['energy_system']['storages'][m]:
                prob += (
                    main_dc['lp'][m + '_storage_soc']['data'][s][t][r] ==
                    main_dc['lp'][m + '_storage_soc']['data'][s][prev_t][r] -
                    main_dc['lp'][m + '_storage_discharge']['data'][s][t][r] /
                    main_dc['parameter']['component'][r][s]['efficiency_out'] +
                    main_dc['lp'][m + '_storage_charge']['data'][s][t][r] *
                    main_dc['parameter']['component'][r][s]['efficiency_in'],
                    m + ' storage state ' + s + ' in ' + r + '_' + str(t))
    return prob


def storage_power_lim(main_dc, storage_type, prob):
    '''
    Constraints to connect the charge and discharge of the storage with the soc
    and the maximal possible charge/discharge.
    '''
    m = storage_type

    for r in main_dc['energy_system']['regions']:
        for s in main_dc['energy_system']['storages'][m]:
            hs = main_dc['parameter']['component'][r][s].get('heating_system')
            domestic = hs in main_dc['energy_system']['hc']['domestic']
            for t in main_dc['timesteps']:
                # Discharge limitation by maximal discharge power
                prob += (
                    main_dc['lp'][m + '_storage_discharge']['data'][s][t][r] <=
                    (((main_dc['lp'][m + '_storage_inst']['data'][s][r]
                        if main_dc['simulation']['investment'] else 0) +
                        main_dc['parameter']['component'][r][s][
                            'installed_capacity']) /
                        main_dc['parameter']['component'][r][s][
                            'energy_power_ratio_out']) * (
                        main_dc['timeseries']['demand'][r][hs][t] /
                        main_dc['parameter']['component'][r][hs][
                            'installed_capacity'] if domestic else 1), (
                        m + ' storage discharge limit EP ' +
                        s + '_' + r + '_t_' + str(t)))

                # Discharge limitation by minmal SOC
                prob += (
                    main_dc['lp'][m + '_storage_discharge']['data'][s][t][r] <=
                    main_dc['lp'][m + '_storage_soc']['data'][s][t][r] *
                    main_dc['parameter']['component'][r][s]['efficiency_out'],
                    (m + ' storage discharge limit SoC ' + s +
                        '_' + r + '_t_' + str(t)))

                # Charge limitation by maximal charge power
                prob += (
                    main_dc['lp'][m + '_storage_charge']['data'][s][t][r] <=
                    ((main_dc['lp'][m + '_storage_inst']['data'][s][r]
                        if main_dc['simulation']['investment'] else 0) +
                        main_dc['parameter']['component'][r][s][
                            'installed_capacity']) /
                    main_dc['parameter']['component'][r][s][
                        'energy_power_ratio_in'],
                    (m + ' storage charge limit EP '
                        + s + '_' + r + '_t_' + str(t)))

                # Charge limitation by maximal SOC
                prob += (
                    main_dc['lp'][m + '_storage_charge']['data'][s][t][r] <=
                    ((main_dc['lp'][m + '_storage_inst']['data'][s][r]
                        if main_dc['simulation']['investment'] else 0)
                        + main_dc['parameter']['component'][r][s]
                        ['installed_capacity']),
                    (m + 'storage charge limit SoC ' + s + '_' + r + '_' +
                        str(t)))

                # Charge limitation by maximal power in the same building
                if domestic:
                    prob += (
                        main_dc['lp'][m + '_storage_charge']['data'][s][t][r]
                        <= main_dc['parameter']['component'][r][s][
                            'installed_capacity'],
                        (m + 'storage charge limit mpb ' + s + '_' + r + '_' +
                            str(t)))
    return prob
