#!/usr/bin/python
# -*- coding: utf-8
import numpy as np
import database as db
import heat_supply


def calc_share_ww_efh_mfh(p_set, hp):
    '''
    Calculates the share of the warm water demand of the single-familiy
    houses to the total warm water demand of each hour.
    '''
    # retrieve warm water profiles from the database
    ww_efh = db.retrieve_from_db_table(p_set['schema'], p_set['load_pot_table'],
        (('res_ww_load_efh_' + hp).lower()).replace(" ", "_"), order='yes')
    ww_mfh = db.retrieve_from_db_table(p_set['schema'],
        p_set['load_pot_table'],
        (('res_ww_load_mfh_' + hp).lower()).replace(" ", "_"), order='yes')
    ww_ghd = db.retrieve_from_db_table(p_set['schema'],
        p_set['load_pot_table'],
        (('com_ww_load_' + hp).lower()).replace(" ", "_"), order='yes')
    # calculate share
    share_efh = ww_efh / (ww_efh + ww_mfh + ww_ghd)
    share_mfh_ghd = 1.0 - share_efh
    return share_efh, share_mfh_ghd


def calc_sole_vl_temp():
    '''
    Returns the supply temperature of a brine heat pump
    '''
    T_sole = np.zeros((8760, ))

    for i in range(8760):
        T_sole[i] = (3.42980994954735 * 10 ** -18) * i ** 5 \
        - (6.28828944308818 * 10 ** -14) * i ** 4 \
        + (2.44607151047512 * 10 ** -10) * i ** 3 \
        + (6.25819661168072 * 10 ** -7) * i ** 2 \
        - 0.0020535109 * i \
        + 4.1855152734

    return T_sole


def calc_cop_hp_air_heating(input_data, p_set):
    '''
    Returns the COP of an air heat pump for heating
    '''
    district = input_data['district']
    T_sup_heating_fbh =\
        heat_supply.calc_hp_heating_supply_temp(input_data, 'FBH')
    T_sup_heating_radiator =\
        heat_supply.calc_hp_heating_supply_temp(input_data, 'radiator')
    eta_g_air = input_data['eta_g_air']
    share_hp_new_b = input_data['share_hp_new_building']
    share_hp_old_b = 1 - share_hp_new_b
    share_fbh_old_b = input_data['share_fbh_old_build']
    share_radiator_old_b = 1.0 - share_fbh_old_b
    # share_radiator_old_b = input_data['share_radiator_old_build']
    share_fbh = share_hp_new_b + share_hp_old_b * share_fbh_old_b
    share_rad = share_hp_old_b * share_radiator_old_b
    cop_max = 7

    # temp vector
    temp = db.get_try_data(district)[:, 9]

    # COP Heat Pump Heating Air for radiator and underfloor heating
    cop_hp_heating_fbh = np.zeros((8760, 1))
    cop_hp_heating_rad = np.zeros((8760, 1))
    for i in range(8760):
        if T_sup_heating_fbh[i] > temp[i]:
            cop_hp_heating_fbh[i] = (eta_g_air * (
                (273.15 + T_sup_heating_fbh[i]) / (
                (273.15 + T_sup_heating_fbh[i]) - (273.15 + temp[i]))))
        else:
            cop_hp_heating_fbh[i] = cop_max
        if T_sup_heating_radiator[i] > temp[i]:
            cop_hp_heating_rad[i] = (eta_g_air * (
                (273.15 + T_sup_heating_radiator[i]) / (
                (273.15 + T_sup_heating_radiator[i]) - (273.15 + temp[i]))))
        else:
            cop_hp_heating_rad[i] = cop_max

    # FOR NOW: limitation of the cop to 10

    cop_hp_heating_fbh[cop_hp_heating_fbh > cop_max] = cop_max
    cop_hp_heating_rad[cop_hp_heating_rad > cop_max] = cop_max
    cop_hp_heating = share_fbh * cop_hp_heating_fbh + \
        share_rad * cop_hp_heating_rad

    return cop_hp_heating


def calc_cop_hp_air_ww(input_data, p_set):
    '''
    Returns the COP of an air heat pump for warm water
    '''
    share_hp_efh, share_hp_mfh_ghd = calc_share_ww_efh_mfh(p_set, 'HP Mono Air')
    district = input_data['district']
    eta_g_air = input_data['eta_g_air']
    ones = np.ones((8760, 1))
    cop_max = 7

    # Calculates mixed WW supply Temperatur for single- and multi-familiy houses
    T_sup_ww = share_hp_efh * input_data['T WW EFH'] + share_hp_mfh_ghd * \
        input_data['T WW MFH']

    # temp vector
    temp = np.ones((8760, 1))
    temp[:, 0] = db.get_try_data(district)[:, 9]

    # COP Heat Pump Water
    cop_hp_ww = ((eta_g_air * ones) * (
        (T_sup_ww + 273.15 * ones) / (
        (T_sup_ww + 273.15 * ones) - (temp + 273.15 * ones))))
    cop_hp_ww[cop_hp_ww > cop_max] = cop_max

    return cop_hp_ww


def calc_cop_hp_brine_heating(input_data, p_set):
    '''
    Returns the COP of a brine heat pump for heating
    '''
    T_sup_heating_fbh = \
        heat_supply.calc_hp_heating_supply_temp(input_data, 'FBH')
    T_sup_heating_radiator = \
        heat_supply.calc_hp_heating_supply_temp(input_data, 'radiator')
    T_sole = calc_sole_vl_temp()
    eta_g_brine = input_data['eta_g_brine']
    share_hp_new_b = input_data['share_hp_new_building']
    share_hp_old_b = 1 - share_hp_new_b
    share_fbh_old_b = input_data['share_fbh_old_build']
    share_radiator_old_b = 1.0 - share_fbh_old_b
    cop_max = 7

    # COP Heat Pump Heating Brine for radiator and underfloor heating
    cop_hp_heating = np.zeros((8760, 1))
    for i in range(8760):
        if T_sup_heating_radiator[i] > T_sole[i]:
            cop_hp_heating[i] = ((share_hp_new_b + share_hp_old_b *
                share_fbh_old_b) *
                (eta_g_brine * ((273.15 + T_sup_heating_fbh[i])
                / ((273.15 + T_sup_heating_fbh[i]) - (273.15 + T_sole[i]))))
                + (share_hp_old_b * share_radiator_old_b *
                (eta_g_brine * ((273.15 + T_sup_heating_radiator[i])
                / ((273.15 + T_sup_heating_radiator[i]) - (273.15 +
                T_sole[i]))))))
        else:
            cop_hp_heating[i] = cop_max

    cop_hp_heating[cop_hp_heating > cop_max] = cop_max

    return cop_hp_heating


def calc_cop_hp_brine_ww(input_data, p_set):
    '''
    Returns the COP of a brine heat pump for warm water.
    '''
    share_hp_efh, share_hp_mfh_ghd = calc_share_ww_efh_mfh(
        p_set, 'HP Mono Brine')
    eta_g_brine = input_data['eta_g_brine']
    ones = np.ones((8760, 1))
    cop_max = 7

    # T_sole
    T_sole = np.ones((8760, 1))
    T_sole[:, 0] = calc_sole_vl_temp()

    # Calculates mixed WW supply Temperatur for single- and multi-familiy houses
    T_sup_ww = share_hp_efh * input_data['T WW EFH'] + share_hp_mfh_ghd * \
    input_data['T WW MFH']

    # COP Heat Pump Water
    cop_hp_ww = ((eta_g_brine * ones) * (
        (T_sup_ww + 273.15 * ones) / (
        (T_sup_ww + 273.15 * ones) - (T_sole + 273.15 * ones))))
    cop_hp_ww[cop_hp_ww > cop_max] = cop_max

    return cop_hp_ww


def max_load_hp(schema, tbname, colname):
    '''
    Returns the maximum heat load.
    '''
    if db.table_exists(tbname):
        max_load = db.retrieve_max_from_db_table(schema, tbname, colname)
    else:
        print (('Table to retrieve the max load does not exist.'))

    return max_load


def calc_cap_hp(input_data, schema, tbname, colname):
    '''
    Returns the installed heat pump capacity needed.
    '''
    max_cap = max_load_hp(schema, tbname, colname)

    if colname == 'HP Mono Air Heating' or colname == 'HP Mono Air WW':
        cap_hp = max_cap * (1.0 - input_data['share el heating HP'])
    elif colname == 'HP Mono Brine Heating' or colname == 'HP Mono Brine WW':
        cap_hp = max_cap
    else:
        print (('HP capacity cannot be retrieved because of invalid ' +
            'colname. The chosen colname was : %s' % colname))

    return cap_hp


def calc_cap_hp_el_heating(input_data, schema, tbname, colname):
    '''
    Returns the installed heat pump capacity needed.
    '''
    max_cap_hp = max_load_hp(schema, tbname, colname)
    cap_el_heating = max_cap_hp * input_data['share el heating HP']
    return cap_el_heating


def calc_cap_hp_storage(input_data, schema, tbname, colname):
    '''
    Returns the thermal storage capacity of a heat pump thermal storage.
    '''
    max_load = max_load_hp(schema, tbname, colname)
    share_hp_new_b = input_data['share_hp_new_building']
    share_hp_old_b = 1 - share_hp_new_b
    share_storage = input_data['share_hp_storage']

    if colname == 'HP Mono Air Heating' or colname == 'HP Mono Brine Heating':
        cap_storage = (share_hp_new_b * share_storage + share_hp_old_b *
         share_storage) * input_data['t_st_heating'] * max_load
    elif colname == 'HP Mono Air WW' or colname == 'HP Mono Brine WW':
        cap_storage = input_data['t_st_ww'] * max_load
    else:
        print (('Storage cap cannot be calculated because of invalid ' +
            'colname. The chosen colname was : %s' % colname))

    return cap_storage


def calc_discharge_hp_storage(schema, tbname, colname):
    '''
    Returns the discharge rate of the heat pump thermal storages.
    The discharge rate is set to equal the maximum demand so that
    the maximum demand can always be supplied by the thermal storage.
    '''
    discharge_rate = max_load_hp(schema, tbname, colname)

    return discharge_rate


def gather_hp_parameters(input_data, p_set):

    # create list with all heat pumps to be considered
    hp_air = []
    hp_brine = []
    if input_data['Heat source HP Mono Air'] == 'yes':
        hp_air.append('HP Mono Air Heating')
        hp_air.append('HP Mono Air WW')
    if input_data['Heat source HP Mono Brine'] == 'yes':
        hp_brine.append('HP Mono Brine Heating')
        hp_brine.append('HP Mono Brine WW')

    # create list with all thermal storages to be considered
    ts_list = []
    for i in (hp_air + hp_brine):
        if input_data[i + ' Storage Thermal'] == 'yes':
            ts_list.append(i)

    # extend input_data dictionary by heat pump capacities
    for i in (hp_air + hp_brine):
        input_data['cap ' + i] = calc_cap_hp(
            input_data, p_set['schema'], p_set['load_pot_table'], i) * 1.01

    # extend input_data dictionary by el heating for air heat pump capacities
    for i in hp_air:
        input_data['cap ' + i + ' el Heating'] = calc_cap_hp_el_heating(
            input_data, p_set['schema'], p_set['load_pot_table'], i) * 1.01

    # extend input_data dictionary by thermal storage capacity and discharge
    # rate
    for i in ts_list:
        input_data['cap ' + i + ' Storage Thermal'] = calc_cap_hp_storage(
            input_data, p_set['schema'], p_set['load_pot_table'], i)
        input_data['Discharge rate ' + i + ' Storage Thermal'] = \
            calc_discharge_hp_storage(
            p_set['schema'], p_set['load_pot_table'], i)

    # write dictionary with COPs
    cop_dict = {}
    func_dict = {'HP Mono Air Heating': calc_cop_hp_air_heating,
                 'HP Mono Air WW': calc_cop_hp_air_ww,
                 'HP Mono Brine Heating': calc_cop_hp_brine_heating,
                 'HP Mono Brine WW': calc_cop_hp_brine_ww}
    for i in (hp_air + hp_brine):
        cop_dict[i] = func_dict[i](input_data, p_set)

    return input_data, cop_dict


# Berechnung des gemischten COP

#def calc_cop_heat_pump_heating(input_data, district_data=None):

    #district = input_data['district']
    #T_sup_heating = calc_heat_pump_heating_supply_temp(input_data,
    #district_data=None)
    #T_sole = calc_sole_vl_temp()
    #T_heat_period = input_data['Heat Pump T_heat_period']
    #T_bivalent = input_data['T_bivalent']
    #share_air = input_data['share_air']
    #share_brine = input_data['share_brine']
    #eta_g_air = input_data['eta_g_air']
    #eta_g_brine = input_data['eta_g_brine']
    #share_el_heating = input_data['share el heating HP']

    ## temp vector
    #if district_data:
        #temp = district_data['try_data'][:, 9]
    #else:
        #temp = db.get_try_data(district)[:, 9]

    ## COP Heat Pump Heating
    #for i in range(8760):
        #if temp[i] <= T_heat_period and temp[i] < T_bivalent \
        #and share_el_heating > 0:
            #COP_air = (((share_el_heating / 2) * 1)
            #+ ((1 - share_el_heating / 2) * eta_g_air * ((
                #273.15 + T_sup_heating[i]) / ((
                #273.15 + T_sup_heating[i]) - (273.15 + temp[i])))))
            #COP_brine = (eta_g_brine * ((
                    #273.15 + T_sup_heating[i]) / ((
                #273.15 + T_sup_heating[i]) - (273.15 + T_sole[i]))))
            #cop_heat_pump_heating = (share_air * COP_air + share_brine *
            #COP_brine)
        #elif temp[i] <= T_heat_period and temp[i] >= T_bivalent:
            #cop_heat_pump_heating = (share_air * eta_g_air * ((
                #273.15 + T_sup_heating[i]) / ((
                #273.15 + T_sup_heating[i]) - (273.15 + temp[i])))
                #+ share_brine * eta_g_brine * ((273.15 + T_sup_heating[i]) / ((
                #273.15 + T_sup_heating[i]) - (273.15 + T_sole[i]))))

    ##import matplotlib.pyplot as mpl
    ##mpl.plot(cop_heat_pump_heating, 'r')
    ###mpl.plot(cop_heat_pump_heating, 'm')
    ##mpl.show()

    #return cop_heat_pump_heating


#def calc_cop_heat_pump_water(input_data, district_data=None):

    #district = input_data['district']
    #T_sup_water = input_data['Heat Pump sup_water']
    #T_sole = calc_sole_vl_temp()
    #T_bivalent = input_data['T_bivalent']
    #share_air = input_data['share_air']
    #share_brine = input_data['share_brine']
    #eta_g_air = input_data['eta_g_air']
    #eta_g_brine = input_data['eta_g_brine']
    #share_el_heating = input_data['share el heating HP']

    ## temp vector
    #if district_data:
        #temp = district_data['try_data'][:, 9]
    #else:
        #temp = db.get_try_data(district)[:, 9]

    ## COP Heat Pump Water
    #for i in range(8760):
        #if temp[i] < T_bivalent and share_el_heating > 0:
            #COP_air = ((share_el_heating / 2 * 1)
            #+ ((1 - share_el_heating / 2) * eta_g_air * ((
                #T_sup_water + 273.15) / ((
                #T_sup_water + 273.15) - (temp[i] + 273.15)))))
            #COP_brine = (eta_g_brine * ((
                #T_sup_water + 273.15) / ((
                #T_sup_water + 273.15) - (T_sole[i] + 273.15))))
            #cop_heat_pump_water = (share_air * COP_air
                #+ share_brine * COP_brine)
        #elif temp[i] >= T_bivalent:
            #cop_heat_pump_water = (share_air * eta_g_air * ((
                #T_sup_water + 273.15) / ((
                #T_sup_water + 273.15) - (temp[i] + 273.15)))
                #+ share_brine * eta_g_brine * ((
                #T_sup_water + 273.15) / ((
                #T_sup_water + 273.15) - (T_sole[i] + 273.15))))

    #return cop_heat_pump_water
