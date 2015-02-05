#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by:
Responsibility: Guido Plessmann
'''

from . import basic_functions as bf


def direct_feed_in(main_dt, prob):
    '''
    Adds constraint: Hourly feed-in energy of renewables.

    Adds a constraint for power generation of volatile renewables power plants
    for each hour of the year. The hourly power output is limited by the
    installed capacity. It depends of the given normalised hourly feedin value.
    Installed capacity is either an exogenous given parameter or a model
    endogenous determined variable.

    Parameters
    ----------
    main_dt : dictionary
        Main dictionary as described below [1]_
    prob : pulp.lp-problem
        LP-Problem-Variable, which contains the linear problem [2]_

    Returns
    -------
    prob : pulp.lp-problem
        LP-Problem-Variable, which contains the linear problem [2]_

    Other Parameters
    ----------------
    Regions [r] : main_dt['energy_system']['regions']
    Renewable power plants [i] : main_dt['energy_system']['re']
    Timesteps [t] : main_dt['timesteps']
    main_dt['simulation']['investment'] : <boolean>, indicates if investment
        decision is considered or not

    Raises
    ------
    Currently no exeption handling.

    See Also
    --------
    main_model.create_model_equations

    Notes
    -----

    References
    ----------
    .. [1] Link to the description of the main_dt for solph.
    .. [2] Link to the description of the lp-variables.
        '''
    for r in main_dt['energy_system']['regions']:
        for i in main_dt['energy_system']['re']:
            for t in main_dt['timesteps']:
                if main_dt['simulation']['investment'] is True:
                    prob += (main_dt['lp']['power_gen']['data'][i][t][r] == (
                        main_dt['lp']['power_inst']['data'][i][r] + main_dt
                        ['parameter']['component'][r][i]['installed_capacity'])
                        * main_dt['timeseries']['feedin'][r][i][t],
                        "feed-in energy" + i + r + str(t))
                else:
                    prob += (main_dt['lp']['power_gen']['data'][i][t][r] == (
                        (main_dt['parameter']['component'][r][i]
                            ['installed_capacity']) *
                        main_dt['timeseries']['feedin'][r][i][t]),
                        "feed-in energy" + i + r + str(t))
    return prob


def domestic_heat_limit(main_dt, prob):
    r"""Adding the limit of the heat output of additional domestic heating
    devices.

    Adding the limit of the heat output of additional domestic heating devices.
    The main domestic heating device don't have any limit, considering that the
    main domestic heating system is build to satisfy the domestic demand.

    Parameters
    ----------
    main_dt : dictionary
        Main dictionary as described below [1]_
    prob : pulp.lp-problem
        LP-Problem-Variable, which contains the linear problem [2]_

    Returns
    -------
    prob : pulp.lp-problem
        LP-Problem-Variable, which contains the extended linear problem [2]_

    Other Parameters
    ----------------
    Timesteps [t] : main_dt['timesteps']
        np-array with the timesteps according to the timeseries
    Regions [r] : main_dt['energy_system']['regions']
        See: solph.extenddc [4]_
    Thermal demand : main_dt['timeseries']['demand'][r][c][t]
        r = region, t = timesteps
    main_dt['energy_system'] : dict-branch with lists of components
        Definition of the 'energy_system' see: :py:mod:`solph.extenddc`
    main_dt['lp'] : dict-branch with all lp-variables
        Definition of lp-variables see: :py:mod:`solph.lp_definition`

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    solph.extenddc

    Notes
    -----
    Capacity limit for additional devices(AC(C)) for domestic heating
    systems (C). Each additional component (AC) belongs to a corresponding
    main heating system (C).

    .. math::

        H_{gen}(r,t,ac(c))\leq H_{demand}(r,t,c)\cdot\frac{\left(cap(r,ac(c))+
        H_{inst}(r,ac(c))\right)}{cap(r,c)}\quad\forall r\in R,t\in T,c\in C

    References
    ----------

    .. [1] Link to the description of the main_dt for solph.
    .. [2] `PuLP <https://code.google.com/p/pulp-or/>`_, PuLP Documentation.

    """
    for c in main_dt['energy_system']['hc']['domestic']:
        for r in main_dt['energy_system']['regions']:
            for ac in main_dt['energy_system']['hc'][c]:
                for t in main_dt['timesteps']:
                    prob += (main_dt['lp']['heat_gen']['data'][ac][t][r] <= (
                        main_dt['timeseries']['demand'][r][c][t] *
                        ((main_dt['parameter']['component'][r][ac]
                            ['installed_capacity']) +
                            (main_dt['lp']['heat_inst']['data'][ac][r]
                                if main_dt['simulation']['investment'] else 0))
                        / (main_dt['parameter']['component'][r][c]
                            ['installed_capacity'])),
                        "peak_power_limit_" + ac + r + str(t))
    return prob


def gen_power_lim(main_dt, prob):
    '''
    Power limits for centralized power plants. So far it's not possible to add
    limits for domestic plants.
    '''
    district_heat_plants = bf.cut_lists(
        main_dt['energy_system']['hc']['district'],
        main_dt['energy_system']['transformer']['heat'])
    invest = main_dt['simulation']['investment']

    prob = domestic_heat_limit(main_dt, prob)

    for r in main_dt['energy_system']['regions']:
        for t in main_dt['timesteps']:
            for c in main_dt['energy_system']['transformer']['elec']:
                prob += (main_dt['lp']['power_gen']['data'][c][t][r] <= (
                    main_dt['lp']['power_inst']['data'][c][r] if invest else 0)
                    + main_dt['parameter']['component'][r][c]
                    ['installed_capacity'],
                    "peak_power_limit_" + c + r + str(t))
            for c in district_heat_plants:
                prob += (main_dt['lp']['heat_gen']['data'][c][t][r] <= (
                    main_dt['lp']['heat_inst']['data'][c][r] if invest else 0)
                    + main_dt['parameter']['component'][r][c]
                    ['installed_capacity'],
                    "peak_power_limit_" + c + r + str(t))

            for c in main_dt['energy_system']['chp']['fixed']:
                prob += (main_dt['lp']['heat_gen']['data'][c][t][r] <= (
                    main_dt['lp']['heat_inst']['data'][c][r] if invest else 0)
                    + main_dt['parameter']['component'][r][c]
                    ['installed_capacity'],
                    "peak_power_limit_" + c + r + str(t))

            for c in main_dt['energy_system']['chp']['variable']:
                v_c = main_dt['energy_system']['chp']['dict'][c]
                prob += ((
                    main_dt['lp']['power_gen']['data'][v_c][t][r] /
                    main_dt['parameter']['component'][r][c]
                    ['efficiency4elec_cond']) + (
                    main_dt['lp']['power_gen']['data'][c][t][r] / main_dt[
                        'parameter']['component'][r][c]['efficiency']) <= (
                    (main_dt['lp']['heat_inst']['data'][c][r]
                        if invest else 0)
                    + main_dt['parameter']['component'][r][c]
                    ['installed_capacity']) / main_dt['parameter']
                    ['component'][r][c]['efficiency'],
                    "peak_power_limit_" + c + r + str(t))
    return prob


def ramping_power(main_dt, prob):
    '''
    defines the change of power in every timestep for use
    in the ramping costs. Ramping power >=0
    '''
    for i in list(main_dt['energy_system']['re'] +
                  main_dt['energy_system']['transformer']['elec']):
        for r in main_dt['energy_system']['regions']:
            for t in main_dt['timesteps']:
                if t > 0:
                    prob += (main_dt['lp']['ramping_power']['data'][i][t][r]
                             >= (
                                 main_dt['lp']['power_gen']['data'][i][t][r] -
                                 main_dt['lp']['power_gen']['data'][i][t - 1]
                                 [r]),
                             "ramping_powerpos" + i + r + str(t))
                        # ramping_power >= power_gen(t_2) - power_gen(t_1)

                    prob += (
                        main_dt['lp']['ramping_power']['data'][i][t][r]
                        >= (main_dt['lp']['power_gen']['data'][i][t - 1][r] -
                            main_dt['lp']['power_gen']['data'][i][t][r]),
                        "ramping_powerneg" + i + r + str(t))
                        # ramping_power >= power_gen(t_2) - power_gen(t_1)

                elif t == 0:  # exception for timestep 0
                    prob += (
                        main_dt['lp']['ramping_power']['data'][i][t][r]
                        >= (main_dt['lp']['power_gen']['data'][i][t][r] -
                            main_dt['lp']['power_gen']['data'][i][
                                main_dt['timesteps'][-1]][r]),
                        "ramping_powerpos" + i + r + str(t))

                    prob += (
                        main_dt['lp']['ramping_power']['data'][i][t][r]
                        >= (main_dt['lp']['power_gen']['data'][i][
                            main_dt['timesteps'][-1]][r] -
                            main_dt['lp']['power_gen']['data'][i][t][r]),
                        "ramping_powerneg" + i + r + str(t))
    return prob


def caps(main_dt, prob):
    #lp_vars_dc, prob, regions, powerplants, storages, name_set, caps,
    #presetting):
    '''
    Sets a maximal limit for a specific component as constraint
    '''
    #power plant caps
    for r in main_dt['energy_system']['regions']:
        for i in list(main_dt['energy_system']['re'] +
                      main_dt['energy_system']['transformer']['elec']):
            if main_dt['parameter']['component'][r][i]['capacity_limit']:
                prob += ((
                    main_dt['lp']['power_inst']['data'][i][r] +
                    main_dt['parameter']['component'][r][i]
                    ['installed_capacity']) <= (
                    main_dt['parameter']['component']
                    [r][i]['capacity_limit']),
                    "cap_powerplant" + i + r)

    #storages caps
    for e in main_dt['energy_system']['storages']:
        for i in main_dt['energy_system']['storages'][e]:
            for r in main_dt['energy_system']['regions']:
                if main_dt['parameter']['component'][r][i]['capacity_limit']:
                    prob += ((
                        main_dt['lp'][e + '_storage_inst']['data'][i][r] +
                        main_dt['parameter']['component'][r][i]
                        ['installed_capacity']) <= (
                        main_dt['parameter']
                        ['component'][r][i]['capacity_limit']),
                        "cap_storages" + i + r)

    #resources caps
    #TODO: Wait for implementing of power to gas to have no problems of
    #TODO: restructuring
    return prob
