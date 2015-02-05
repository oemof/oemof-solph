#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import matplotlib.pyplot as mpl
import database as db
import os
import plot_data
import plot_lists


def total_costs_emissions(p_set, input_data):

    # get optimization data
    [colnames, data] = plot_data.retrieve_data(
        p_set['schema'], p_set['output_table'])

    # temporary list with components that use fuel
    comp_list_temp = \
         ['Biomass Power', 'Gas Power', 'El Import',
         'Gas Heat', 'Oil Heat', 'Biomass Heat', 'Coal Heat',
         'Gas Cog unit Heat', 'Gas Cog unit Power', 'Gas Cog unit Boiler',
         'Biogas Cog unit Heat', 'Biogas Cog unit Power', 'ST Heat supp Gas',
         'DH Biogas Heat', 'DH Gas Heat', 'DH Excess Heat',
         'DH Biogas Cog unit Heat', 'DH Biogas Cog unit Power',
         'DH Gas Cog unit Heat', 'DH Gas Cog unit Power',
         'DH Biomass Cog Heat', 'DH Biomass Cog Power']
    # list with actual components
    comp_list = []
    for i in comp_list_temp:
        if i in colnames:
            comp_list.append(i)
    # efficiencies
    efficiency = {}
    for i in comp_list:
        if i == 'El Import' or i == 'DH Excess Heat':
            efficiency[i] = 1
        else:
            efficiency[i] = input_data['eta ' + i]
    # variable costs and emissions
    sum_var_costs = 0
    sum_var_co2 = 0
    for comp in comp_list:
        tmp = ([i for i, x in enumerate(colnames) if x == comp])
        comp_energy = sum(data[:, tmp])
        sum_var_co2 += (p_set['var_co2_dict'][comp] *
            (comp_energy / efficiency[comp]))
        sum_var_costs += (p_set['var_costs_dict'][comp] *
            (comp_energy / efficiency[comp]))

    return sum_var_costs, sum_var_co2


def sorted_annual_load_curve(output_dir, vec, component, show=False):
    '''
    Plots a sorted annual load curve of the input vector.
    '''
    figure1 = mpl.figure()
    handle1 = figure1.add_subplot(1, 1, 1)
    handle1.plot(sorted(vec, reverse=True))
    legend_dict = plot_lists.legend_dictionary()  # dictionary for label
    mpl.title("Jahresdauerlinie %s (maximale Leistung = %.1f MW)"
        % (legend_dict[component], max(vec)))
    handle1.set_ylabel('Leistung [MW]')
    handle1.set_xlabel('Stunden des Jahres')
    if show:
        mpl.show()
    png_name = output_dir + '/load_curve_' + component + '.png'
    figure1.savefig(os.path.join(os.path.expanduser("~"), png_name))
    mpl.close(figure1)
    return


def cop_over_temp(input_data, cop, output_dir, component, show=False):
    '''
    Plots the COP over the outside temperature.
    '''
    # open figure
    figure1 = mpl.figure()
    handle1 = figure1.add_subplot(1, 1, 1)
    # get temperature vector
    temp = db.get_try_data(input_data['district'])[:, 9]
    # sort cop from lowest to highest temperature
    plot_data = np.zeros((8760, 2))
    plot_data[:, 0] = temp
    plot_data[:, 1] = cop[:, 0]
    plot_data_sorted = plot_data[
        np.lexsort((plot_data[:, 1], plot_data[:, 0]))]
    # plot cop
    handle1.plot(plot_data_sorted[:, 0], plot_data_sorted[:, 1], '.')
    # set labels
    legend_dict = plot_lists.legend_dictionary()  # dictionary for label
    mpl.title("COP %s" % legend_dict[component])
    handle1.set_ylabel('COP')
    handle1.set_xlabel(u'Außentemperatur [°C]')
    if show:
        mpl.show()
    # save
    png_name = output_dir + '/cop_' + component + '.png'
    figure1.savefig(os.path.join(os.path.expanduser("~"), png_name))
    # close figure
    mpl.close(figure1)
    return


def hours_between_charges(soc):
    '''
    Returns the maximum number of hours the thermal storage has benn charged
    without being newly charged in between.
    '''
    discharge_time = 0
    end = 0
    start = 0
    for i in range(1, len(soc) - 1):
        if soc[i - 1] < soc[i] and soc[i + 1] <= soc[i]:
            start = i
        if soc[i - 1] >= soc[i] and soc[i - 1] > soc[i]:
            end = i
        if start < end:
            discharge_time_new = end - start
            if discharge_time_new > discharge_time:
                discharge_time = discharge_time_new
    comment = ('The maximum number of hours the thermal storage is not '
        + 'charged is ' + str(discharge_time))
    return comment


def check_charge_discharge(charge, discharge):
    '''
    Checks if the thermal storage is charged and discharged at the same time.
    '''
    control_vec = np.zeros((len(charge), ))
    for i in range(len(charge)):
        if abs(charge[i] - discharge[i]) - (charge[i] + discharge[i]) != 0:
            control_vec[i] = 1
    if 1 in control_vec:
        comment = ('The thermal storage is charged and ' +
            'discharged at the same time!')
    else:
        comment = ('The thermal storage is NOT charged and ' +
            'discharged at the same time.')
    return comment


def check_charge_discharge_equal(charge, discharge):
    '''
    Checks if the thermal storage charge and discharge are at any point equal.
    '''
    control_vec = np.zeros((len(charge), ))
    for i in range(len(charge)):
        if charge[i] - discharge[i] == 0 and charge[i] != 0:
            control_vec[i] = 1
    if 1 in control_vec:
        print (('The thermal storage charge and discharge are equal!'))
    return


def full_load_hours(colnames, data, input_data, pv_cap, wind_cap):
    '''
    Returns a dictionary with the full load hours of the power plants.
    '''

    full_load_hours_dict = {}

    # Wind turbines
    if 'Wind' in colnames:
         # total energy produced
        tmp = ([i for i, x in enumerate(colnames) if x == 'Wind'])
        wind_work = sum(data[:, tmp[0]])
         # full load hours
        if wind_cap == 0:
            full_load_hours_dict['Wind'] = 0
        else:
            full_load_hours_dict['Wind'] = round(wind_work / wind_cap)

    # PV
    if 'PV' in colnames:
         # total energy produced
        tmp = ([i for i, x in enumerate(colnames) if x == 'PV'])
        pv_work = sum(data[:, tmp[0]])
         # full load hours
        if pv_cap == 0:
            full_load_hours_dict['PV'] = 0
        else:
            full_load_hours_dict['PV'] = round(pv_work / pv_cap)

    # Biomass Cog Power
    if 'DH Biomass Cog Power' in colnames:
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'DH Biomass Cog Power'])
         # maximum capacity
        dh_biomass_cog_cap = (input_data['cap Biomass Power'] /
            input_data['eta Biomass Power'] *
            input_data['eta DH Biomass Cog Power'])
         # total energy produced
        dh_biomass_cog_work = sum(data[:, tmp[0]])
         # full load hours
        if dh_biomass_cog_cap == 0:
            full_load_hours_dict['DH Biomass Cog Power'] = 0
        else:
            full_load_hours_dict['DH Biomass Cog Power'] = \
                round(dh_biomass_cog_work / dh_biomass_cog_cap)

    # Gas Cog unit Heat
    if 'Gas Cog unit Heat' in colnames:
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'Gas Cog unit Heat'])
         # maximum capacity
        gas_cog_cap = (input_data['cap Gas Cog unit Power'] /
            input_data['eta Gas Cog unit Power'] *
            input_data['eta Gas Cog unit Heat'])
         # total energy produced
        gas_cog_work = sum(data[:, tmp[0]])
         # full load hours
        if gas_cog_cap == 0:
            full_load_hours_dict['Gas Cog unit Heat'] = 0
        else:
            full_load_hours_dict['Gas Cog unit Heat'] = \
                round(gas_cog_work / gas_cog_cap)

    # Biogas Cog unit Heat
    if 'Biogas Cog unit Heat Demand' in colnames:
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'Biogas Cog unit Heat Demand'])
         # maximum capacity
        biogas_cog_cap = (input_data['cap Biogas Cog unit Power'] /
            input_data['eta Biogas Cog unit Power'] *
            input_data['eta Biogas Cog unit Heat'])
         # total energy produced
        biogas_cog_work = sum(data[:, tmp[0]])
         # full load hours
        if biogas_cog_cap == 0:
            full_load_hours_dict['Biogas Cog unit Heat'] = 0
        else:
            full_load_hours_dict['Biogas Cog unit Heat'] = \
                round(biogas_cog_work / biogas_cog_cap)

    # Gas Heat and Power, El Import
    gas_backup = ['Gas Power', 'DH Gas Heat', 'El Import']
    for comp in gas_backup:
        if comp in colnames:
            tmp = ([i for i, x in enumerate(colnames)
                if x == comp])
             # maximum capacity
            comp_cap = max(data[:, tmp[0]])
             # total energy produced
            comp_work = sum(data[:, tmp[0]])
             # full load hours
            if comp_cap == 0:
                full_load_hours_dict[comp] = 0
            else:
                full_load_hours_dict[comp] = round(comp_work / comp_cap)

    # HP Mono Air
    hp_air_list = ['HP Mono Air Heating', 'HP Mono Air WW']
    for hp in hp_air_list:
        if hp in colnames:
            tmp = ([i for i, x in enumerate(colnames)
                if x == hp])
            tmp_el = ([i for i, x in enumerate(colnames)
                if x == (hp + ' el Heating')])
             # maximum capacity
            hp_cap = input_data['cap ' + hp] + \
                input_data['cap ' + hp + ' el Heating']
             # total energy produced
            hp_work = sum(data[:, tmp[0]]) + sum(data[:, tmp_el[0]])
             # full load hours
            if hp_cap == 0:
                full_load_hours_dict[hp] = 0
            else:
                full_load_hours_dict[hp] = round(hp_work / hp_cap)

    # other components
    list_1 = ['Biomass Power', 'DH Biogas Heat', 'DH Thermal Storage Boiler',
        'DH Biogas Cog unit Power', 'DH Gas Cog unit Power',
        'Gas Cog unit Boiler', 'Gas Cog unit Power', 'Biogas Cog unit Boiler',
        'Biogas Cog unit Power', 'HP Mono Brine Heating', 'HP Mono Brine WW']
    for comp in list_1:
        if comp in colnames:
            tmp = ([i for i, x in enumerate(colnames)
                if x == comp])
             # maximum capacity
            comp_cap = input_data['cap ' + comp]
             # total energy produced
            comp_work = sum(data[:, tmp[0]])
             # full load hours
            if comp_cap == 0:
                full_load_hours_dict[comp] = 0
            else:
                full_load_hours_dict[comp] = round(comp_work / comp_cap)

    return full_load_hours_dict


def storage_losses(colnames, data, comp_name):
    '''
    Calculates the total losses of a storage.
    '''
    # retrieve number of column containing charge and discharge data
    tmp_charge = ([i for i, x in enumerate(colnames)
            if x == comp_name + ' Charge'])
    tmp_discharge = ([i for i, x in enumerate(colnames)
            if x == comp_name + ' Discharge'])

    # calculate sum of charge and discharge
    charge = sum(data[:, tmp_charge[0]])
    discharge = sum(data[:, tmp_discharge[0]])

    return charge - discharge


def storage_energy_in(colnames, data, comp_name):
    '''
    Calculates the energy input into a storage.
    '''
    # retrieve number of column containing charge data
    tmp_charge = ([i for i, x in enumerate(colnames)
            if x == comp_name + ' Charge'])
    return sum(data[:, tmp_charge[0]])


def calc(p_set, input_data, pv_pot, wind_pot, cop_dict):
    '''
    Calculates various things
    '''

    ########################## retrieve from database ######################

    # open connection to the database
    conn = db.open_db_connection()
    cur = conn.cursor()

    # read the names of the columns of the solver output table
    cur.execute('''SELECT column_name FROM information_schema.columns
                WHERE table_name = '%s';''' % p_set['output_table'])
    colnames = np.asarray(cur.fetchall())

    # read data from the solver output table
    table = p_set['schema'] + '.' + p_set['output_table']
    cur.execute('''
                SELECT * FROM %s ORDER BY id
                ''' % table)
    data = np.asarray(cur.fetchall())

    ############################## call functions ##########################

        ########################## Thermal storage ##########################

    if 'DH Storage Thermal SoC' in colnames:
        # check if thermal storage is charged and discharged at the same time
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'DH Storage Thermal Charge'])
        charge = data[:, tmp[0]]
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'DH Storage Thermal Discharge'])
        discharge = data[:, tmp[0]]
        comment_1 = check_charge_discharge(charge, discharge)

        # get number of hours between charges of the thermal storage
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'DH Storage Thermal SoC'])
        soc = data[:, tmp[0]]
        comment_2 = hours_between_charges(soc)

        # plot SoC
        figure1 = mpl.figure()
        handle1 = figure1.add_subplot(1, 1, 1)
        handle1.plot(soc, 'r')
        mpl.title("Thermal storage SoC")
        handle1.set_ylabel('Speicherinhalt [MWh]')
        handle1.set_xlabel('Stunden des Jahres')
        png_name = p_set['output_dir'] + '/thermal_storage_soc.png'
        figure1.savefig(os.path.join(os.path.expanduser("~"), png_name))
        png_name = 'thermal_storage_soc.png'

    else:
        comment_1 = 'No thermal storage!'
        comment_2 = 'No thermal storage!'

        ####################### Full load hours ##########################

    full_load_hours_dict = \
        full_load_hours(colnames, data, input_data, max(pv_pot), max(wind_pot))

        ##################### Sorted load profiles #######################

    # El Import
    tmp = ([i for i, x in enumerate(colnames) if x == 'El Import'])
    el_import = data[:, tmp[0]]
    sorted_annual_load_curve(p_set['output_dir'], el_import, 'El Import')
    max_el_import = max(data[:, tmp[0]])

    # Gas Power
    if input_data['Power source Gas Power'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames) if x == 'Gas Power'])
        gas_power = data[:, tmp[0]]
        sorted_annual_load_curve(p_set['output_dir'], gas_power, 'Gas Power')
    else:
        gas_power = np.zeros((data[:, 0].shape[0], ))

    # Battery
    if input_data['Storage Battery'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'Storage Battery Discharge'])
        battery_dis = data[:, tmp[0]]
        sorted_annual_load_curve(p_set['output_dir'], battery_dis,
            'Storage Battery Discharge')

    # DH Gas Heat
    if input_data['Heat source DH Gas Heat'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames) if x == 'DH Gas Heat'])
        dh_gas_heat = data[:, tmp[0]]
        sorted_annual_load_curve(
            p_set['output_dir'], dh_gas_heat, 'DH Gas Heat')
    else:
        dh_gas_heat = np.zeros((data[:, 0].shape[0], ))

    # DH Excess Heat
    if input_data['Heat source DH Excess Heat'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames) if x == 'DH Excess Heat'])
        dh_excess_heat = data[:, tmp[0]]
        sorted_annual_load_curve(
            p_set['output_dir'], dh_excess_heat, 'DH Excess Heat')
    else:
        dh_excess_heat = np.zeros((data[:, 0].shape[0], ))

    # Biomasse HKW (Jahresdauerlinie der Wärmeerzeugung)
    if input_data['Cog source DH Biomass Cog'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'DH Biomass Cog Heat'])
        cog_biomass = data[:, tmp[0]]
        sorted_annual_load_curve(
            p_set['output_dir'], cog_biomass, 'DH Biomass Cog Heat')
    else:
        cog_biomass = np.zeros((data[:, 0].shape[0], ))

    # DH Biogas Cog unit
    if input_data['Cog source DH Biogas Cog unit'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'DH Biogas Cog unit Heat'])
        cog_dh_biogas = data[:, tmp[0]]
        sorted_annual_load_curve(p_set['output_dir'], cog_dh_biogas,
            'DH Biogas Cog unit Heat')
    else:
        cog_dh_biogas = np.zeros((data[:, 0].shape[0], ))

    # DH Gas Cog unit
    if input_data['Cog source DH Gas Cog unit'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'DH Gas Cog unit Heat'])
        cog_dh_gas = data[:, tmp[0]]
        sorted_annual_load_curve(p_set['output_dir'], cog_dh_gas,
            'DH Gas Cog unit Heat')
    else:
        cog_dh_gas = np.zeros((data[:, 0].shape[0], ))

    # Biogas Cog unit
    if input_data['Heat source Biogas Cog unit'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'Biogas Cog unit Heat'])
        cog_biogas = data[:, tmp[0]]
        sorted_annual_load_curve(p_set['output_dir'], cog_biogas,
            'Biogas Cog unit Heat')
    else:
        cog_biogas = np.zeros((data[:, 0].shape[0], ))

    # Gas Cog unit
    if input_data['Heat source Gas Cog unit'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'Gas Cog unit Heat'])
        cog_gas = data[:, tmp[0]]
        sorted_annual_load_curve(p_set['output_dir'], cog_gas,
            'Gas Cog unit Heat')
    else:
        cog_gas = np.zeros((data[:, 0].shape[0], ))

    # KWK ges
    sorted_annual_load_curve(
        p_set['output_dir'],
        cog_biomass + cog_dh_biogas + cog_dh_gas + cog_gas + cog_biogas,
        'Sum Cog')

    # Gas Cog unit Storage Thermal
    if input_data['Gas Cog unit Storage Thermal'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'Gas Cog unit Storage Thermal Discharge'])
        cog_gas_storage_dis = data[:, tmp[0]]
        sorted_annual_load_curve(p_set['output_dir'], cog_gas_storage_dis,
            'Gas Cog unit Storage Thermal Discharge')

    # Biogas Cog unit Storage Thermal
    if input_data['Biogas Cog unit Storage Thermal'] == 'yes':
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'Biogas Cog unit Storage Thermal Discharge'])
        cog_biogas_storage_dis = data[:, tmp[0]]
        sorted_annual_load_curve(p_set['output_dir'], cog_biogas_storage_dis,
            'Biogas Cog unit Storage Thermal Discharge')

        ################### HP (load curve + COP plot) ####################

    # Heat Pump Mono Air
    if input_data['Heat source HP Mono Air'] == 'yes':
        # Heat Pump Mono Heating
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Air Heating'])
        hpm_air_heating = data[:, tmp[0]]
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Air Heating el Heating'])
        hp_air_heating_el_heating = data[:, tmp[0]]
        sorted_annual_load_curve(
            p_set['output_dir'], hpm_air_heating, 'HP Mono Air Heating')
        cop_over_temp(
            input_data, cop_dict['HP Mono Air Heating'],
            p_set['output_dir'], 'HP Mono Air Heating')
        # Heat Pump Mono Water
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Air WW'])
        hpm_air_ww = data[:, tmp[0]]
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Air WW el Heating'])
        hp_air_ww_el_heating = data[:, tmp[0]]
        sorted_annual_load_curve(
            p_set['output_dir'], hpm_air_ww, 'HP Mono Air WW')
        cop_over_temp(
            input_data, cop_dict['HP Mono Air WW'],
            p_set['output_dir'], 'HP Mono Air WW')
    else:
        hpm_air_heating = np.array([0])
        hpm_air_ww = np.array([0])

    # Heat Pump Mono Brine
    if input_data['Heat source HP Mono Brine'] == 'yes':
        # Heat Pump Mono Heating
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Brine Heating'])
        hpm_brine_heating = data[:, tmp[0]]
        sorted_annual_load_curve(
            p_set['output_dir'], hpm_brine_heating, 'HP Mono Brine Heating')
        cop_over_temp(
            input_data, cop_dict['HP Mono Brine Heating'],
            p_set['output_dir'], 'HP Mono Brine Heating')
        # Heat Pump Mono Water
        tmp = ([i for i, x in enumerate(colnames)
            if x == 'HP Mono Brine WW'])
        hpm_brine_ww = data[:, tmp[0]]
        sorted_annual_load_curve(
            p_set['output_dir'], hpm_brine_ww, 'HP Mono Brine WW')
        cop_over_temp(
            input_data, cop_dict['HP Mono Brine WW'],
            p_set['output_dir'], 'HP Mono Brine WW')
    else:
        hpm_brine_heating = np.array([0])
        hpm_brine_ww = np.array([0])

        ##################### Total power demand ######################

    # power demand
    power_demand = sum(db.retrieve_from_db_table(
        p_set['schema'], p_set['load_pot_table'], 'El'))[0]

    # power demand for electrical heating
    el_heating_list = plot_lists.get_list_el_heating(p_set['output_table'])

    sum_el_heating = 0
    for el_heating in el_heating_list:
        tmp = ([i for i, x in enumerate(colnames) if x == el_heating])
        sum_el_heating += sum(data[:, tmp[0]])

    # power demand for heat pumps
    hp_el_demand = np.zeros((8760, ))
    if input_data['Heat source HP Mono Air'] == 'yes':
        hp_el_demand += (hpm_air_heating / np.reshape(
            cop_dict['HP Mono Air Heating'], (-1, )) +
            hp_air_heating_el_heating)
        hp_el_demand += (hpm_air_ww / np.reshape(
            cop_dict['HP Mono Air WW'], (-1, )) + hp_air_ww_el_heating)
    if input_data['Heat source HP Mono Brine'] == 'yes':
        hp_el_demand += hpm_brine_heating / np.reshape(
            cop_dict['HP Mono Brine Heating'], (-1, ))
        hp_el_demand += hpm_brine_ww / np.reshape(
            cop_dict['HP Mono Brine WW'], (-1, ))

    total_power_demand = power_demand + sum_el_heating + sum(hp_el_demand)

        ##################### Total end energy demand ######################

    # power demand
    power_demand = sum(db.retrieve_from_db_table(
        p_set['schema'], p_set['load_pot_table'], 'El'))[0]

    # heat demand
    heat_demand = sum(db.retrieve_from_db_table(
        p_set['schema'], p_set['load_pot_table'], 'res_heat_load_efh'))[0]
    heat_demand += sum(db.retrieve_from_db_table(
        p_set['schema'], p_set['load_pot_table'], 'res_heat_load_mfh'))[0]
    heat_demand += sum(db.retrieve_from_db_table(
        p_set['schema'], p_set['load_pot_table'], 'com_heat_load'))[0]
    heat_demand += sum(db.retrieve_from_db_table(
        p_set['schema'], p_set['load_pot_table'], 'ind_heat_load'))[0]

    # end energy demand
    end_energy_demand = power_demand + heat_demand

        ##################### Biomass and biogas used ######################

    biomass_used = {}
    for storage in ['Storage Biomass', 'Storage Biogas', 'Storage Biogas dec']:
        if (storage + ' SoC') in colnames:
            tmp = ([i for i, x in enumerate(colnames)
                if x == (storage + ' Discharge')])
            biomass_used[storage] = sum(data[:, tmp[0]])

        ############### storage losses and energy input ####################

    storage_losses_dict = {}
    storage_energy = {}
    storages = ['Storage Battery', 'DH Storage Thermal',
        'Gas Storage Thermal', 'Oil Storage Thermal',
        'Biomass Storage Thermal', 'Coal Storage Thermal',
        'HP Mono Air Heating Storage Thermal', 'HP Mono Air WW Storage Thermal',
        'HP Mono Brine Heating Storage Thermal',
        'HP Mono Brine WW Storage Thermal', 'Gas Cog unit Storage Thermal',
        'Biogas Cog unit Storage Thermal', 'ST Storage Thermal']

    for storage in storages:
        if (storage + ' SoC') in colnames:
            storage_losses_dict[storage] = storage_losses(
                colnames, data, storage)
            storage_energy[storage] = storage_energy_in(
                colnames, data, storage)

    cur.close()
    conn.close()

    return (comment_1, comment_2, full_load_hours_dict, biomass_used,
        max(gas_power), max(dh_gas_heat), max(dh_excess_heat), max_el_import,
        storage_losses_dict, storage_energy, max(hpm_air_heating),
        max(hpm_air_ww), max(hpm_brine_heating), max(hpm_brine_ww),
        max(hp_el_demand), total_power_demand, end_energy_demand)