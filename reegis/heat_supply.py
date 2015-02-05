#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import database as db
import shlp_bdew


def heat_hw_splitting(annual_heat_demand, annual_heating_demand,
    input_data, consumer_type):
    ''
    # total demand
    demand = {}
    demand[consumer_type] = annual_heat_demand
    res_hourly_heat_demand, com_hourly_heat_demand = \
        shlp_bdew.generate_load_profile(input_data, demand)
    if consumer_type == 'EFH' or consumer_type == 'MFH':
        total_demand = res_hourly_heat_demand
    else:
        total_demand = com_hourly_heat_demand

    # heating demand (demand without hot water)
    demand = {}
    demand[consumer_type] = annual_heating_demand
    res_hourly_heating_demand, com_hourly_heating_demand = \
        shlp_bdew.generate_load_profile(input_data, demand, ww_incl='no')
    if consumer_type == 'EFH' or consumer_type == 'MFH':
        heating_demand = res_hourly_heating_demand
    else:
        heating_demand = com_hourly_heating_demand

    # hot water demand
    hw_demand = total_demand - heating_demand
    return heating_demand, hw_demand


def heat_hw_splitting_ind(heat_load_profile, input_data):
    ''

    heating_demand = heat_load_profile * input_data['share heating ind']
    hw_demand = heat_load_profile - heating_demand

    return heating_demand, hw_demand


def split_hp_mono(p_set, input_data):
    '''
    Devides the given share of monoenergetic heat pumps of all decentralized
    heating systems into the share of air and brine heat pumps.
    '''
    # initialization of dictionaries
    p_set['heat_source_shares']['HP Mono Air'] = {}
    p_set['heat_source_shares']['HP Mono Brine'] = {}

    # splitting
    for key in p_set['heat_source_shares']['HP Mono']:
        p_set['heat_source_shares']['HP Mono Air'][key] = \
            (1.0 - input_data['share_brine_hp']) * \
            p_set['heat_source_shares']['HP Mono'][key]
        p_set['heat_source_shares']['HP Mono Brine'][key] = \
            input_data['share_brine_hp'] * \
            p_set['heat_source_shares']['HP Mono'][key]

    # delete unnacessary keys
      # HP Mono
    p_set['heat_source_shares'].pop('HP Mono', None)
      # maybe HP Mono Air or Brine if not chosen in input_data
    for hp in ['HP Mono Air', 'HP Mono Brine']:
        if input_data['Heat source ' + hp] == 'no':
            p_set['heat_source_shares'].pop(hp, None)

    return p_set


def allocate_dh(p_set, heat_load_profile, res_hlp_efh, res_hlp_mfh, com_hlp):
    '''
    Allocates the different district heating systems to the decentralized
    heating systems.
    '''
    for i in list(p_set['DH systems'].keys()):
        # calculate hourly heat demand to be allocated
        allocate = (res_hlp_efh *
            p_set['heat_source_shares']['DH']['res_efh'] *
            p_set['DH systems'][i] +
                res_hlp_mfh *
            p_set['heat_source_shares']['DH']['res_mfh'] *
            p_set['DH systems'][i] +
                com_hlp *
            p_set['heat_source_shares']['DH']['com'] *
            p_set['DH systems'][i])
        # drauf
        heat_load_profile[i] = heat_load_profile[i] + allocate
        # abziehen
        heat_load_profile['DH'] = heat_load_profile['DH'] - allocate
    return heat_load_profile


def heat_load_splitting(res_hlp_efh, res_hlp_mfh, com_hlp, ind_hlp,
    p_set, input_data):
    '''
    Generates heat load profiles to be covered by the different heat sources.
    '''
    heat_load_profile = {}  # dictionary with heat load profile of every
                            # heating system

    # split heat pump systems in p_set['heat_source_shares'] dictionary
    heat_pumps = []
    if input_data['Heat source HP Mono Air'] == 'yes':
        heat_pumps.append('HP Mono Air')
    if input_data['Heat source HP Mono Brine'] == 'yes':
        heat_pumps.append('HP Mono Brine')
    if len(heat_pumps) > 0:
        p_set = split_hp_mono(p_set, input_data)
    else:
        p_set['heat_source_shares'].pop('HP Mono', None)

    # calculation of heat load profile for every heating system
    for i in list(p_set['heat_source_shares'].keys()):
        heat_load_profile[i] = \
            (res_hlp_efh * p_set['heat_source_shares'][i]['res_efh'] +
            res_hlp_mfh * p_set['heat_source_shares'][i]['res_mfh'] +
            com_hlp * p_set['heat_source_shares'][i]['com'] +
            ind_hlp * p_set['heat_source_shares'][i]['ind'])
        p_set['max_heat_' + i.lower()] = max(heat_load_profile[i])

    # district heating: allocation
    heat_load_profile = allocate_dh(
        p_set, heat_load_profile, res_hlp_efh, res_hlp_mfh, com_hlp)

    # heat pump: splitting of warm water and heating demand
    consumer = ['EFH', 'MFH', 'GHD', 'ind']
    heating_demand = {}
    hw_demand = {}
    for i in heat_pumps:
        # EFH
        heating_demand['EFH'], hw_demand['EFH'] = heat_hw_splitting(
            sum(res_hlp_efh * p_set['heat_source_shares'][i]['res_efh']),
            sum(res_hlp_efh * p_set['heat_source_shares'][i]['res_efh']) *
            input_data['share heating res'], input_data, 'EFH')
          # warm water load profile to db (load_pot_table)
        db.save_results_to_db(p_set['schema'], p_set['load_pot_table'],
            ('res_ww_load_efh_' + i).replace(" ", "_"), hw_demand['EFH'])
        # MFH
        heating_demand['MFH'], hw_demand['MFH'] = heat_hw_splitting(
            sum(res_hlp_mfh * p_set['heat_source_shares'][i]['res_mfh']),
            sum(res_hlp_mfh * p_set['heat_source_shares'][i]['res_mfh']) *
            input_data['share heating res'], input_data, 'MFH')
          # warm water load profile to db (load_pot_table)
        db.save_results_to_db(p_set['schema'], p_set['load_pot_table'],
            ('res_ww_load_mfh_' + i).replace(" ", "_"), hw_demand['MFH'])
        # GHD
        heating_demand['GHD'], hw_demand['GHD'] = heat_hw_splitting(
            sum(com_hlp * p_set['heat_source_shares'][i]['com']),
            sum(com_hlp * p_set['heat_source_shares'][i]['com']) *
            input_data['share heating com'], input_data, 'GHD')
        db.save_results_to_db(p_set['schema'], p_set['load_pot_table'],
            ('com_ww_load_' + i).replace(" ", "_"), hw_demand['GHD'])
        # Industrie
        heating_demand['ind'], hw_demand['ind'] = heat_hw_splitting_ind(
            ind_hlp * p_set['heat_source_shares'][i]['ind'], input_data)

        heating = np.zeros((heating_demand['EFH'].shape))
        hw = np.zeros((heating_demand['EFH'].shape))
        for j in consumer:
            heating += heating_demand[j]
            hw += hw_demand[j]
        heat_load_profile[i + ' Heating'] = heating
        heat_load_profile[i + ' WW'] = hw

        # drop key in heat_load_profile
        heat_load_profile.pop(i, None)

    # solar heat: splitting of warm water and heating demand
    if input_data['Heat source ST Heat'] == 'yes':
        # EFH
        heat_load_profile['ST EFH'] = (res_hlp_efh *
            p_set['heat_source_shares']['ST']['res_efh'])
        p_set['max_heat_st_efh'] = max(heat_load_profile['ST EFH'])
        # MFH
        heat_load_profile['ST MFH'] = (res_hlp_mfh *
            p_set['heat_source_shares']['ST']['res_mfh'])
        p_set['max_heat_st_mfh'] = max(heat_load_profile['ST MFH'])

    return heat_load_profile


def mixed_eff(heating_system, input_data, ref_state):
    '''
    Returns a mixed efficiency for old and new fossil fuel
    heating systems.
    '''
    # share of partially refurbished buildings with new heating systems
    share_part_ref_new_hs = 0.5
    # share of buildings with new heating systems
    share_new = (ref_state['EFH']['fully ref'] +
        ref_state['MFH']['fully ref'] +
        share_part_ref_new_hs * (ref_state['EFH']['partially ref'] +
        ref_state['MFH']['partially ref'])) / 2
    # share of buildings with old heating systems
    share_old = (ref_state['EFH']['unrenovated'] +
        ref_state['MFH']['unrenovated'] +
        (1 - share_part_ref_new_hs) * (ref_state['EFH']['partially ref'] +
        ref_state['MFH']['partially ref'])) / 2
    # mixed efficiency
    input_data['eta ' + heating_system + ' Heat'] = (
        input_data['eta ' + heating_system + ' Heat old'] * share_old +
        input_data['eta ' + heating_system + ' Heat new'] * share_new)
    return input_data


def calc_dh_supply_temp(input_data, district_data=None):
    '''
    Generates an hourly supply temperature profile depending on the ambient
    temperature.
    For ambient temperatures above T_heat_period the load for tap water
    preparation dominates the heat laod. The district heating system is then
    mass flow controlled and the supply temperature kept at a constant
    temperature of T_sup_min.
    For ambient temperatures below T_heat the supply temperature increases
    linearly to T_sup_max with decreasing ambient temperature.
    '''
    T_sup_max = input_data['DH T_sup_max']
    T_sup_min = input_data['DH T_sup_min']
    T_heat_period = input_data['DH T_heat_period']
    T_amb_min = input_data['DH T_amb_design']
    district = input_data['district']

    # temp vector
    if district_data:
        temp = district_data['try_data'][:, 9]
    else:
        temp = db.get_try_data(district)[:, 9]

    # linear correlation between Q and T_sup
    T_sup = np.zeros((8760, ))
    slope = (T_sup_min - T_sup_max) / (T_heat_period - T_amb_min)
    y_intercept = T_sup_max - slope * T_amb_min

    for i in range(8760):
        T_sup[i] = slope * temp[i] + y_intercept
    T_sup[T_sup < T_sup_min] = T_sup_min
    T_sup[T_sup > T_sup_max] = T_sup_max

    return T_sup


def calc_hp_heating_supply_temp(input_data, heating, district_data=None):
    '''
    Generates an hourly supply temperature profile depending on the ambient
    temperature.
    For ambient temperatures above T_heat_period the load, the load is 0.
    For ambient temperatures below T_heat the supply temperature increases
    linearly to T_sup_max with decreasing ambient temperature.
    '''

    T_heat_period = input_data['Heat Pump T_heat_period']
    T_amb_min = input_data['Heat Pump T_amb_design']
    district = input_data['district']

    # temp vector
    if district_data:
        temp = district_data['try_data'][:, 9]
    else:
        temp = db.get_try_data(district)[:, 9]

    if heating == 'FBH':
        T_sup_max_fbh = input_data['T FBH max']
        T_sup_min_fbh = input_data['T FBH min']

        # linear correlation between Q and T_sup
        T_sup_heating = np.zeros((8760, ))
        slope = (T_sup_min_fbh - T_sup_max_fbh) / (T_heat_period - T_amb_min)
        y_intercept = T_sup_max_fbh - slope * T_amb_min

        for i in range(8760):
            T_sup_heating[i] = slope * temp[i] + y_intercept
            T_sup_heating[T_sup_heating < T_sup_min_fbh] = T_sup_min_fbh
            T_sup_heating[T_sup_heating > T_sup_max_fbh] = T_sup_max_fbh

    elif heating == 'radiator':
        T_sup_max_radiator = input_data['T radiator max']
        T_sup_min_radiator = input_data['T radiator min']

        # linear correlation between Q and T_sup
        T_sup_heating = np.zeros((8760, ))
        slope = (T_sup_min_radiator - T_sup_max_radiator) / (T_heat_period -
        T_amb_min)
        y_intercept = T_sup_max_radiator - slope * T_amb_min

        for i in range(8760):
            T_sup_heating[i] = slope * temp[i] + y_intercept
            T_sup_heating[T_sup_heating <
            T_sup_min_radiator] = T_sup_min_radiator
            T_sup_heating[T_sup_heating >
            T_sup_max_radiator] = T_sup_max_radiator
    else:
        print (('Invalid heating system. The chosen heating was: %s'
        % heating))

    return T_sup_heating