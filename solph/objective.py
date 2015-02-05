#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by: Uwe Krien (uwe.krien@rl-institut.de)
Responsibility: Guido Plessmann, Uwe Krien
'''

import pulp
import logging
from . import financial_calc as fc


def objective(main_dt, prob):
    '''Generates the objective function of the optimization problem which is
    basically the sum of all annuities plus the sum of operating cost

    Parameters
    ----------
    timesteps : list
        Simulation timesteps.
    gen_components : list
        Components with electrical output
    fossil_resources : list
        Fossil resource components (such as natural gas)
    feedin_power : Pulp Lp-Variable
        Hourly power output of gen_components
    inst_power : Pulp Lp-Variable
        Installed power gen_components
    main_dt : dictionary
        Scenario parameters
    prob : Pulp LpProblem
        Optimization problem
    regions : list
        Considered regions
    resource_activity : list
        Hourly power output of fossil_resources
    storages : list
        Considered storage technologies
    inst_power_storages : Pulp Lp-Variable
        Installed power of storages

    Returns
    -------
    prob : PuPulp LpProblem
        (altered) Optimization problem
    '''
    # Index of global shortcuts for shorter calls
    p = 'parameter'
    comp = 'component'
    es = 'energy_system'

    cost_min_ls = ['minimising_costs', 'minimising costs', 'minimizing_costs',
                   'minimizing costs']
    co2_min_ls = ['minimising_co2', 'minimising co2', 'minimizing_co2',
                  'minimizing co2']

    if main_dt['simulation']['opt_target'] in cost_min_ls:
        # Defining the optimisation shortcuts for cost optimisation
        unit_var = 'opex_var'
        unit_fix = 'opex_fix'
        capacity_fix = 'capex'
        cost_opt = True
    elif main_dt['simulation']['opt_target'] in co2_min_ls:
        # Defining the optimisation shortcuts for co2 optimisation
        unit_var = 'co2_var'
        unit_fix = 'co2_fix'
        capacity_fix = 'co2_capacity'
        cost_opt = False
    else:
        logging.error('Unknown optimisation target defined ({0})'.format(
            main_dt['simulation']['opt_target']))
        logging.error('Use "minimising costs" or "minimising co2"')

    # Remove domestic heating systems from the list.
    # Domestic heating systems do allways have the right capacity to
    # satisfy the domestic heat demand. Additional device like heating rods
    # for domestic systems are not(!) removed.
    heat_sys_not_domestic = ([x for x in list(
        main_dt['energy_system']['transformer']['heat']) if x not in set(
        main_dt['energy_system']['hc']['domestic'])])

    # creating objective function
    # Cost of presetted power plants in a separate block in order to switch
    # correctly between investment decision and dispatch of existing
    # capacities.
    prob += (
        # variable costs of elec transformers
        pulp.lpSum(
            [main_dt[p][comp][r][c][unit_var]
                * main_dt['lp']['power_gen']['data'][c][t][r]]
            for c in main_dt[es]['transformer']['elec']
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions'])

        # variable costs of heat transformers
        + pulp.lpSum(
            [main_dt[p][comp][r][c][unit_var]
                * main_dt['lp']['heat_gen']['data'][c][t][r]]
            for c in main_dt[es]['transformer']['heat']
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions'])

        # variable costs of chp transformers (chp mode)
        + pulp.lpSum(
            [main_dt[p][comp][r][c][unit_var]
                * main_dt['lp']['power_gen']['data'][c][t][r]
                + main_dt[p][comp][r][c]['opex_var4heat']
                * main_dt['lp']['heat_gen']['data'][c][t][r]]
            for c in main_dt[es]['transformer']['chp']
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions'])

        # variable costs of chp transformers (condensing mode)
        + pulp.lpSum(
            [main_dt[p][comp][r][c][unit_var]
                * main_dt['lp']['power_gen']['data'][
                    main_dt[es]['chp']['dict'][c]][t][r]]
            for c in main_dt[es]['chp']['variable']
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions'])

        # variable costs of transformers for renewable sources
        + pulp.lpSum(
            [main_dt[p][comp][r][c][unit_var]
                * main_dt['lp']['power_gen']['data'][c][t][r]]
            for c in main_dt[es]['re']
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions'])

        # variable cost of gas converters
        + pulp.lpSum(
            [main_dt[p][comp][r][c][unit_var]
                * main_dt['lp']['gas_gen']['data'][c][t][r]
                / main_dt[p][comp][r][c]['efficiency']]
            for c in main_dt[es]['transformer'].get('gas', [])
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions'])

        # fix costs of elec transformers for fossil sources
        + pulp.lpSum(
            [(main_dt[p][comp][r][c][capacity_fix] *
                fc.crf_calc(main_dt[p][comp][r][c]['lifetime'],
                            main_dt[p][comp][r][c]['wacc'])
                + main_dt[p][comp][r][c][unit_fix]) *
                main_dt['lp']['power_inst']['data'][c][r]]
            for c in main_dt[es]['transformer']['elec']
            for r in main_dt[es]['regions']
            if main_dt['simulation']['investment'] is True)

        # fix costs of heat transformers for renewable sources
        + pulp.lpSum(
            [(main_dt[p][comp][r][c][capacity_fix] *
                fc.crf_calc(main_dt[p][comp][r][c]['lifetime'],
                            main_dt[p][comp][r][c]['wacc'])
                + main_dt[p][comp][r][c][unit_fix]) *
                main_dt['lp']['heat_inst']['data'][c][r]]
            for c in heat_sys_not_domestic
            for r in main_dt[es]['regions']
            if main_dt['simulation']['investment'] is True)

        # fix costs of chp transformers for fossil sources
        + pulp.lpSum(
            [(main_dt[p][comp][r][c][capacity_fix] *
                fc.crf_calc(main_dt[p][comp][r][c]['lifetime'],
                            main_dt[p][comp][r][c]['wacc'], cost_opt)
                + main_dt[p][comp][r][c][unit_fix]) *
                main_dt['lp']['heat_inst']['data'][c][r]]
            for c in main_dt[es]['transformer']['chp']
            for r in main_dt[es]['regions']
            if main_dt['simulation']['investment'] is True)

        # fix costs of transformers for renewable sources
        + pulp.lpSum(
            [(main_dt[p][comp][r][c][capacity_fix] *
                fc.crf_calc(main_dt[p][comp][r][c]['lifetime'],
                            main_dt[p][comp][r][c]['wacc'], cost_opt)
                + main_dt[p][comp][r][c][unit_fix]) *
                main_dt['lp']['power_inst']['data'][c][r]]
            for c in main_dt[es]['re']
            for r in main_dt[es]['regions']
            if main_dt['simulation']['investment'] is True)

        # fix costs of gas converters
        + pulp.lpSum(
            [(main_dt[p][comp][r][c][capacity_fix] *
                fc.crf_calc(main_dt[p][comp][r][c]['lifetime'],
                            main_dt[p][comp][r][c]['wacc'], cost_opt)
                + main_dt[p][comp][r][c][unit_fix]) *
                main_dt['lp']['gas_inst']['data'][c][r]
                / main_dt[p][comp][r][c]['efficiency']]
            for c in main_dt[es]['transformer'].get('gas', [])
            for r in main_dt[es]['regions']
            if main_dt['simulation']['investment'] is True)

        # fuel costs
        + pulp.lpSum(
            [main_dt[p]['resources'][r][c][unit_var]
                * main_dt['lp']['fossil_resources']['data'][c][t][r]]
            for c in list(main_dt[es]['resources'].keys())
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions'])

        # grids costs
        + pulp.lpSum(
            [(main_dt[p]['transmission'][l][capacity_fix] *
                fc.crf_calc(main_dt[p]['transmission'][l]['lifetime'],
                            main_dt[p]['transmission'][l]['wacc'], cost_opt) +
                main_dt[p]['transmission'][l][unit_fix]) *
                main_dt['lp']['trm_inst']['data'][l] *
                main_dt[p]['transmission'][l]['length']]
            for l in list(main_dt[p]['transmission'].keys()))

        ## ramping costs re
        + pulp.lpSum(
            [main_dt[p][comp][r][c]['ramping_costs']
                * main_dt['lp']['ramping_power']['data'][c][t][r]]
            for c in main_dt[es]['re']
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions']
            if main_dt[p][comp][r][c]['ramping_costs'] > 0)

        # ramping costs elec fossil
        + pulp.lpSum(
            [main_dt[p][comp][r][c]['ramping_costs']
                * main_dt['lp']['ramping_power']['data'][c][t][r]]
            for c in main_dt[es]['transformer'].get('elec', [])
            for t in main_dt['timesteps']
            for r in main_dt[es]['regions']
            if main_dt[p][comp][r][c]['ramping_costs'] > 0)

        # costs of electrical storages
        + pulp.lpSum(
            [(main_dt[p][comp][r][s][capacity_fix] *
                fc.crf_calc(main_dt[p][comp][r][s]['lifetime'],
                            main_dt[p][comp][r][s]['wacc'], cost_opt) +
                main_dt[p][comp][r][s][unit_fix]) *
                main_dt['lp']['elec_storage_inst']['data'][s][r]]
            for s in main_dt[es]['storages'].get('elec', [])
            for r in main_dt[es]['regions']
            if (main_dt[es]['storages']['elec'] and main_dt['simulation']
                ['investment']))

        # fix costs of biogas storages
        + pulp.lpSum(
            [(main_dt[p][comp][r][s][capacity_fix] *
                fc.crf_calc(main_dt[p][comp][r][s]['lifetime'],
                            main_dt[p][comp][r][s]['wacc'], cost_opt) +
                main_dt[p][comp][r][s][unit_fix]) *
                main_dt['lp']['biogas_storage_inst']['data'][s][r]]
            for s in main_dt[es]['storages'].get('biogas', [])
            for r in main_dt[es]['regions']
            if (main_dt['simulation']['investment']))

        # costs of gas storages
        + pulp.lpSum(
            [(main_dt[p][comp][r][s][capacity_fix] *
                fc.crf_calc(main_dt[p][comp][r][s]['lifetime'],
                            main_dt[p][comp][r][s]['wacc'], cost_opt) +
                main_dt[p][comp][r][s][unit_fix]) *
                main_dt['lp']['gas_storage_inst']['data'][s][r]]
            for s in main_dt[es]['storages'].get('gas', [])
            for r in main_dt[es]['regions']
            if (main_dt['simulation']['investment'])),

        # target needs to be at end of obj fkt
        "{0}".format(main_dt['simulation']['opt_target']))

    return prob
