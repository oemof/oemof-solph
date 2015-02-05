#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by: Uwe Krien (uwe.krien@rl-institut.de)
Responsibility: Guido Plessmann, Uwe Krien
'''

import pulp


def elec_demand_coverage(main_dt, prob):
    r"""Adds constraint: electrical demand coverage

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

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
    Electric demand : main_dt['timeseries']['demand'][r]['lele'][t]
        r = region, t = timesteps
    main_dt['energy_system'] : dict-branch with lists of components
        Definition of the 'energy_system' see: :py:mod:`solph.extenddc`
    main_dt['lp'] : dict-branch with all lp-variables
        Definition of lp-variables see: :py:mod:`solph.lp_definition`


    Raises
    ------
    NoException
        So far no exceptions will be raised.

    See Also
    --------
    solph.extenddc
    solph.main_model.create_model_equations

    Notes
    -----
    Equation for the demand coverage [3]_:

    .. math:: \underset{i}{\sum(}P_{gen}\left(r,i,t\right)+P_{
        trans}\left(r,t\right)+P_{discharge}\left(r,i,t\right)-P_{charge}(
        r,i,t)-P_{electrlysis} \\ -P_{p2HotHeat}-P_{excess}\left(r,t\right)=P_{
        demand}\left(r,t\right)) \quad \forall r \in R, t \in T

    References
    ----------
    .. [1] Link to the description of the main_dt for solph.
    .. [2] `PuLP <https://code.google.com/p/pulp-or/>`_, PuLP Documentation.
    .. [3] Linkt zu mehr Infos zu LP-Gleichungen.
    .. [4] Link zur Beschreibung des branch: 'energy_system'.
    """

    comp_elec_output = list(
        main_dt['energy_system']['transformer']['elec'] +
        main_dt['energy_system']['transformer']['chp'] +
        main_dt['energy_system']['re'] +
        main_dt['energy_system']['chp']['virtuell'])

    for r in main_dt['energy_system']['regions']:
        for t in main_dt['timesteps']:
            prob += ((
                # electricity production
                pulp.lpSum([
                    main_dt['lp']['power_gen']['data'][i][t][r]
                    for i in comp_elec_output])

                # import via transmission line
                - (main_dt['lp']['trm_power']['data'][r][t]
                    if main_dt['energy_system']['transmission'] else 0)

                # excess variable
                - main_dt['lp']['excess']['data']['eexc'][t][r]

                # electrical need of components that have an electrical input
                - (main_dt['lp']['fossil_resources']['data']['rele'][t][r]
                    if 'rele' in main_dt['lp']['fossil_resources']['data']
                    else 0)

                # electrical storage charge and discharge
                + pulp.lpSum([
                    main_dt['lp']['elec_storage_discharge']['data'][s][t][r] -
                    main_dt['lp']['elec_storage_charge']['data'][s][t][r]
                    for s in main_dt['energy_system']['storages'].get(
                        'elec', [])
                    if main_dt['energy_system']['storages']['elec']])

                # equals electrical demand (not greater due to excess variable)
                == main_dt['timeseries']['demand'][r]['lele'][t],
                "elec demand coverage " + str(t) + r))
    return prob


def heat_demand_coverage(main_dt, prob):
    '''
    Heat demand constraints:
    The production of all heat providing transformer has to satisfy the demand
    for every timestep.
    '''
    for r in main_dt['energy_system']['regions']:
        # demand coverage for domestic heating systems
        if main_dt['energy_system']['hc']['domestic']:
            for c in main_dt['energy_system']['hc']['domestic']:
                for t in main_dt['timesteps']:
                    prob += (
                        # heat provided by specific heating system
                        main_dt['lp']['heat_gen']['data'][c][t][r] +

                        # heat provided by additional components
                        pulp.lpSum([
                            main_dt['lp']['heat_gen']['data'][ac][t][r]
                            for ac in main_dt['energy_system']['hc'][c]]) +

                        # heat provided by thermal storage
                        (main_dt['lp']['heat_storage_discharge']['data'][
                            main_dt['energy_system']['hstorage2system'][c]]
                            [t][r]) -

                        # loading the thermal storage
                        (main_dt['lp']['heat_storage_charge']['data'][
                            main_dt['energy_system']['hstorage2system'][c]]
                            [t][r])

                        # equals heat demand
                        == main_dt['timeseries']['demand'][r][c][t],
                        "heat demand coverage " + c + str(t) + r)

        # demand coverage for district heating systems
        c = 'dst0'  # so far only one system
        if main_dt['energy_system']['hc']['district']:
            for t in main_dt['timesteps']:
                prob += (
                    # heat provided by district heating systems
                    pulp.lpSum([
                        main_dt['lp']['heat_gen']['data'][i][t][r]
                        for i in main_dt['energy_system']['hc']['district']])

                    # excess variable
                    - main_dt['lp']['heat_excess']['data']['hexc'][t][r]

                    # equals heat demand (not greater due to excess variable)
                    == main_dt['timeseries']['demand'][r][c][t],
                    "heat demand coverage_dst0_" + str(t) + r)
    return prob


def demand_coverage(main_dt, prob):
    '''
    defines equation for each hour which ensure coverage of given demand
    '''
    prob = elec_demand_coverage(main_dt, prob)
    if main_dt['check']['heat']:
        prob = heat_demand_coverage(main_dt, prob)
    return prob
