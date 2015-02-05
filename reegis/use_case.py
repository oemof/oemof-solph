#!/usr/bin/python
# -*- coding: utf-8

import heat_load_profile_res as hlp_res
import el_load_profile_res as elp_res
import heat_load_profile_com as hlp_com
import el_load_profile_com as elp_com
import heat_load_profile_ind as hlp_ind
import el_load_profile_ind as elp_ind
import wka
import pv
import st
import biomass
import heat_supply
import model
import evaluation
import co2_emissions
import costs
import output
import plot
import database as db
import heat_pump_calc
import cog_unit_calc
import numpy as np


def hlp(p_set, input_data):
    '''
    Returns the heat load profiles of the three sectors households,
    commercial businesses and industry.
    '''
    # residential
    # EFH heat
    hourly_heat_demand_res_efh = hlp_res.get_hourly_heat_load_profile(
        input_data, p_set['hlp_res_use_case'], res_type='EFH',
        schema=p_set['schema'], table_name=p_set['hlp_res_table'],
        column_name=p_set['hlp_res_column']['EFH'],
        filename=p_set['hlp_res_filename'],
        directory=p_set['hlp_res_directory'], save=p_set['save'],
        save_to_table=p_set['load_pot_table'],
        save_to_column='res_heat_load_efh',
        annual_demand={'EFH': p_set['annual_heat_demand_res']['EFH']})
    # MFH heat
    hourly_heat_demand_res_mfh = hlp_res.get_hourly_heat_load_profile(
        input_data, p_set['hlp_res_use_case'], res_type='MFH',
        schema=p_set['schema'], table_name=p_set['hlp_res_table'],
        column_name=p_set['hlp_res_column']['MFH'],
        filename=p_set['hlp_res_filename'],
        directory=p_set['hlp_res_directory'], save=p_set['save'],
        save_to_table=p_set['load_pot_table'],
        save_to_column='res_heat_load_mfh',
        annual_demand={'MFH': p_set['annual_heat_demand_res']['MFH']})

    # commercial
    hourly_heat_demand_com = hlp_com.get_hourly_heat_load_profile(
        input_data, p_set['hlp_com_use_case'],
        schema=p_set['schema'], table_name=p_set['hlp_com_table'],
        column_name=p_set['hlp_com_column'], filename=p_set['hlp_com_filename'],
        directory=p_set['hlp_com_directory'], save=p_set['save'],
        annual_demand=p_set['annual_heat_demand_com'],
        save_to_table=p_set['load_pot_table'])

    # industrial
    hourly_heat_demand_ind = hlp_ind.get_hourly_heat_load_profile(
        input_data, p_set['hlp_ind_use_case'],
        schema=p_set['schema'], table_name=p_set['hlp_ind_table'],
        column_name=p_set['hlp_ind_column'], filename=p_set['hlp_ind_filename'],
        directory=p_set['hlp_ind_directory'],
        step_load_profile_factors=p_set['step_load_profile_ind_factors'],
        save=p_set['save'],
        save_to_table=p_set['load_pot_table'],
        annual_demand=p_set['annual_heat_demand_ind'])

    return (hourly_heat_demand_res_efh, hourly_heat_demand_res_mfh,
        hourly_heat_demand_com, hourly_heat_demand_ind)


def elp(p_set, input_data):
    '''
    Returns the electricity load profiles of the three sectors households,
    commercial businesses and industry.
    '''
    # residential
    hourly_el_demand_res = elp_res.get_hourly_el_load_profile(
        input_data, p_set['elp_res_use_case'],
        schema=p_set['schema'], table_name=p_set['elp_res_table'],
        column_name=p_set['elp_res_column'], filename=p_set['elp_res_filename'],
        directory=p_set['elp_res_directory'], save=p_set['save'],
        save_to_table=p_set['load_pot_table'],
        annual_demand=p_set['annual_el_demand_res'])

    # commercial
    hourly_el_demand_com = elp_com.get_hourly_el_load_profile(
        input_data, p_set['elp_com_use_case'],
        schema=p_set['schema'], table_name=p_set['elp_com_table'],
        column_name=p_set['elp_com_column'], filename=p_set['elp_com_filename'],
        directory=p_set['elp_com_directory'], save=p_set['save'],
        annual_demand=p_set['annual_el_demand_com'],
        save_to_table=p_set['load_pot_table'])

    # industrial
    hourly_el_demand_ind = elp_ind.get_hourly_el_load_profile(
        input_data, p_set['elp_ind_use_case'],
        schema=p_set['schema'], table_name=p_set['elp_ind_table'],
        column_name=p_set['elp_ind_column'], filename=p_set['elp_ind_filename'],
        directory=p_set['elp_ind_directory'],
        step_load_profile_factors=p_set['step_load_profile_ind_factors'],
        save=p_set['save'],
        save_to_table=p_set['load_pot_table'],
        annual_demand=p_set['annual_el_demand_ind'])

    return hourly_el_demand_res, hourly_el_demand_com, hourly_el_demand_ind


def ren_potentials(p_set, input_data, hourly_heat_demand,
    incl_wind='yes', incl_pv='yes', incl_biogas='yes', incl_biomass='yes',
    incl_st='yes'):
    '''
    Returns the hourly wind and PV potentials as well as the hourly biogas
    and annual biomass potential of a region.
    '''
    # Wind
    if incl_wind:
        if not p_set['wind_pot'] == 'scaled_mixed':
            hourly_wind_potential, number_wka = wka.get_hourly_wind_pot(
                input_data, p_set, p_set['wind_pot'],
                p_set['wind_pot_use_case'],
                schema=p_set['schema'], table_name=p_set['wind_pot_table'],
                column_name=p_set['wind_pot_column'],
                filename=p_set['wind_pot_file'],
                directory=p_set['wind_pot_directory'], save=p_set['save'],
                save_to_table=p_set['load_pot_table'],
                share_pot_used=p_set['share_wind_pot_used'])
        else:
            hourly_wind_potential = np.zeros((8760, ))
            number_wka = None
    else:
        hourly_wind_potential = np.zeros((8760, ))
        number_wka = None

    # PV
    if incl_pv:
        hourly_pv_potential, pv_area = pv.get_hourly_pv_pot(
            input_data, p_set['pv_pot'], p_set['pv_pot_use_case'],
            schema=p_set['schema'], table_name=p_set['pv_pot_table'],
            column_name=p_set['pv_pot_column'], filename=p_set['pv_pot_file'],
            directory=p_set['pv_pot_directory'], save=p_set['save'],
            save_to_table=p_set['load_pot_table'],
            share_pot_used=p_set['share_pv_pot_used'])
    else:
        hourly_pv_potential = np.zeros((8760, ))
        pv_area = None

    # Solarthermal Heat
    if input_data['Heat source ST Heat'] == 'no':
        incl_st = None
    if incl_st:
        hourly_st_potential, st_area = st.get_hourly_st_pot(
            p_set, input_data, hourly_heat_demand, schema=p_set['schema'],
            save=p_set['save'], save_to_table=p_set['load_pot_table'])
    else:
        hourly_st_potential = np.zeros((8760, ))
        st_area = None

    # Biogas
    if incl_biogas:
        hourly_biogas_pot = biomass.get_hourly_biogas_pot(
            input_data, potential=p_set['biogas_pot'],
            share_pot_used=p_set['share_biogas_pot_used'],
            hourly_potential=p_set['hourly_biogas_pot'])
        hourly_biogas_potential = biomass.split_biogas_potential(
            input_data, hourly_biogas_pot)
    else:
        hourly_biogas_potential = {'dec': None,
                                   'central': None}

    # Biomass
    if incl_biomass:
        annual_biomass_potential = biomass.get_annual_biomass_pot(
            input_data, potential=p_set['biomass_pot'],
            annual_potential=p_set['annual_biomass_pot'])
    else:
        annual_biomass_potential = None

    return (hourly_wind_potential, hourly_pv_potential,
        hourly_biogas_potential, annual_biomass_potential,
        pv_area, number_wka, hourly_st_potential, st_area)


def get_profiles(p_set, input_data,
    incl_wind='yes', incl_pv='yes', incl_biogas='yes', incl_biomass='yes',
    incl_st='yes', pahesmf=None):

    # heat load profiles
    [hourly_heat_demand_res_efh, hourly_heat_demand_res_mfh,
        hourly_heat_demand_com, hourly_heat_demand_ind] = hlp(
        p_set, input_data)
    # heat load splitting
    hourly_heat_demand = heat_supply.heat_load_splitting(
        hourly_heat_demand_res_efh, hourly_heat_demand_res_mfh,
        hourly_heat_demand_com, hourly_heat_demand_ind, p_set, input_data)

    # el. load profiles
    hourly_el_demand_res, hourly_el_demand_com, hourly_el_demand_ind = elp(
        p_set, input_data)
    hourly_el_demand = (hourly_el_demand_res + hourly_el_demand_com +
        hourly_el_demand_ind)

    # renewable potentials
    [hourly_wind_potential, hourly_pv_potential,
        hourly_biogas_potential, annual_biomass_potential,
        pv_area, number_wka, hourly_st_potential, st_area] = \
        ren_potentials(p_set, input_data, hourly_heat_demand,
            incl_wind=incl_wind, incl_pv=incl_pv,
            incl_biogas=incl_biogas, incl_biomass=incl_biomass)

    # write profiles to db
    db.write_profiles_to_db(p_set, hourly_el_demand, hourly_heat_demand,
        hourly_wind_potential, hourly_pv_potential, hourly_st_potential,
        pahesmf=pahesmf)

    return (hourly_heat_demand, hourly_el_demand,
        hourly_biogas_potential, annual_biomass_potential,
        hourly_pv_potential, hourly_wind_potential,
        number_wka, pv_area, hourly_st_potential, st_area)


def cap_variation(input_data, p_set,
    hourly_heat_demand, hourly_el_demand,
    hourly_biogas_potential, annual_biomass_potential,
    hourly_pv_pot, hourly_wind_pot,
    number_wka, pv_area, cap_pv, cap_wind,
    hourly_st_potential, st_area, begin):

    hourly_pv_potential = hourly_pv_pot * cap_pv
    hourly_wind_potential = hourly_wind_pot * cap_wind

    # pv area
    pv_area = pv.pv_total_area(input_data, cap_pv / max(hourly_pv_pot))

    # heat pump parameters
    # Extend input_data by heat pump parameters + get COPs
    input_data, cop_dict = heat_pump_calc.gather_hp_parameters(
        input_data, p_set)
    # Extend input_data by a mixed efficiency for old and new fossil fuel
    # heating systems
    tmp_list = ['Gas', 'Oil', 'Coal']
    for i in tmp_list:
        if i in list(hourly_heat_demand.keys()):
            input_data = heat_supply.mixed_eff(
                i, input_data, p_set['ref_state'])

    # dec. Cog unit parameters
    if 'Gas Cog unit' in list(hourly_heat_demand.keys()):
        input_data = cog_unit_calc.gas_cog_cap(input_data, p_set)

    # Output directory
    db.create_dir(p_set['output_dir'])
    # Optimization
    [sum_dep_var, components_dict] = \
        model.calculation(
            hourly_heat_demand, hourly_el_demand,
            hourly_wind_potential, hourly_pv_potential, hourly_st_potential,
            hourly_biogas_potential, annual_biomass_potential,
            p_set['hourly_hydropower_pot'],
            begin, input_data, p_set, cop_dict)
    # Evaluation
    [comment_1, comment_2, full_load_hours_dict, biomass_used,
        cap_gas_power, cap_dh_gas_heat, cap_dh_excess_heat, max_el_import,
        storage_losses, storage_energy,
        cap_hpm_air_heating, cap_hpm_air_ww, cap_hpm_brine_heating,
        cap_hpm_brine_ww, max_el_demand_hp,
        total_power_demand, end_energy_demand] = \
        evaluation.calc(p_set, input_data,
            hourly_pv_potential, hourly_wind_potential, cop_dict)

    # CO2 + Costs dictionaries
      # variable
    p_set['var_costs_dict'] = costs.variable(input_data)
    p_set['var_co2_dict'] = co2_emissions.variable(input_data)
    sum_var_costs, sum_var_co2 = evaluation.total_costs_emissions(
        p_set, input_data)

      # fixed
    p_set['fixed_co2_dict'], number_wka = co2_emissions.fixed(
        input_data, pv_area, cap_pv,
        number_wka, cap_wind, st_area,
        cap_dh_gas_heat, cap_gas_power, components_dict, cap_hpm_air_heating,
        cap_hpm_air_ww, cap_hpm_brine_heating, cap_hpm_brine_ww, p_set)
    p_set['fixed_costs_dict'] = costs.fixed(
        input_data, cap_pv,
        cap_wind, st_area,
        cap_dh_gas_heat, cap_gas_power, components_dict, cap_hpm_air_heating,
        cap_hpm_air_ww, cap_hpm_brine_heating, cap_hpm_brine_ww, p_set)
    total_emissions = (sum_var_co2 +
        sum(p_set['fixed_co2_dict'].values()))
    total_costs = (sum_var_costs +
        sum(p_set['fixed_costs_dict'].values()))
      # dependent variable
    if p_set['optimize_for'] == 'Costs':
        dep_var_dict = p_set['var_costs_dict']
        dep_var_fixed_dict = p_set['fixed_costs_dict']
    else:
        dep_var_dict = p_set['var_co2_dict']
        dep_var_fixed_dict = p_set['fixed_co2_dict']

    # OUTPUTS
    # Plot
    filename = ('Output_Unterszenario_' + str(p_set['counter']))
    plot.command(input_data, p_set, cop_dict, p_set['schema'],
        p_set['output_dir'], p_set['output_table'], p_set['load_pot_table'],
        p_set['week_summer'], p_set['week_winter'],
        p_set['pie_p_name'], p_set['pie_h_name'],
        p_set['stackplot_name_winter'], p_set['stackplot_name_summer'],
        p_set['show'], filename, sum_var_co2, total_emissions,
        sum_var_costs, total_costs, storage_losses,
        hourly_pv_potential, hourly_wind_potential, total_power_demand,
        end_energy_demand, max_el_demand_hp, components_dict,
        full_load_hours_dict)
    # tex-File
    output.tex_file(filename, input_data, p_set,
        dep_var_fixed_dict, dep_var_dict,
        total_emissions, sum_var_co2,
        total_costs, sum_var_costs,
        components_dict, full_load_hours_dict,
        pv_area, number_wka, cap_pv,
        cap_wind, cap_gas_power,
        cap_dh_gas_heat, cap_dh_excess_heat, max_el_import,
        annual_biomass_potential, hourly_biogas_potential,
        comment_1, comment_2, storage_losses,
        storage_energy, biomass_used)
    # export db tables
    if p_set['export_output_table'] == 'yes':
        db.db_table_2_file(p_set['schema'], p_set['output_table'],
            p_set['output_dir'] + '/' + p_set['output_table'] + '.txt')
    if p_set['export_load_pot_table'] == 'yes':
        db.db_table_2_file(p_set['schema'], p_set['load_pot_table'],
            p_set['output_dir'] + '/' + p_set['load_pot_table'] + '.txt')
    # export p_set
    db.dict_2_file(p_set, p_set['output_dir'] + '/' + 'p_set', delimiters=';')

    return