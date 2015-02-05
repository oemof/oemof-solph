#!/usr/bin/python
# -*- coding: utf-8

import sys
import database as db


def gas_cog_cap(input_data, p_set):

    # retrieve maximum demand for gas cogeneration units
    max_demand = db.retrieve_max_from_db_table(
        p_set['schema'], p_set['load_pot_table'], "Gas Cog unit")

    # list of cogeneration units used in the model
    cog_unit_list = []
    if input_data['Heat source Gas Cog unit'] == 'yes':
        cog_unit_list.append('Gas Cog unit')

    # set capacities
    for cog_unit in cog_unit_list:
        # if cog. unit capacity is unrestrained
        if input_data['cap ' + cog_unit + ' Power'] == 9999:
            # if additional boiler, the capacity of the cog unit and the boiler
            # are restrained by "ratio Backup"
            if input_data['Heat source ' + cog_unit + ' Boiler'] == 'yes':
                cap_cog_unit_heat = \
                    (max_demand *
                    (1 - input_data['ratio Backup ' + cog_unit])) * 1.01
                input_data['cap ' + cog_unit + ' Power'] = (cap_cog_unit_heat /
                    input_data['eta ' + cog_unit + ' Heat'] *
                    input_data['eta ' + cog_unit + ' Power'])
                input_data['cap ' + cog_unit + ' Boiler'] = \
                    (max_demand *
                    input_data['ratio Backup ' + cog_unit]) * 1.01
            # if additional thermal storage, the capacity of the cog unit and
            # the thermal storage discharge rate are restrained by
            # "ratio Backup"; the thermal storage capacity is set to
            # max. load * t_st_heating
            elif input_data[cog_unit + ' Storage Thermal'] == 'yes':
                cap_cog_unit_heat = (max_demand *
                    (1 - input_data['ratio Backup ' + cog_unit])) * 1.01
                input_data['cap ' + cog_unit + ' Power'] = (cap_cog_unit_heat /
                    input_data['eta ' + cog_unit + ' Heat'] *
                    input_data['eta ' + cog_unit + ' Power'])
                input_data['cap ' + cog_unit + ' Boiler'] = 0.0
                input_data['Discharge rate ' + cog_unit + ' Storage Thermal'] =\
                    (max_demand *
                    input_data['ratio Backup ' + cog_unit]) * 1.01
                input_data['cap ' + cog_unit + ' Storage Thermal'] = \
                    (max_demand *
                    input_data['t_st_heating'])
            else:
                cap_cog_unit_heat = max_demand * 1.01
                input_data['cap ' + cog_unit + ' Power'] = \
                    (cap_cog_unit_heat /
                    input_data['eta ' + cog_unit + ' Heat'] *
                    input_data['eta ' + cog_unit + ' Power'])
                input_data['cap ' + cog_unit + ' Boiler'] = 0.0
        # if cog. unit capacity is restrained
        else:
            cap_cog_unit_heat = (input_data['cap ' + cog_unit + ' Power'] /
                input_data['eta ' + cog_unit + ' Power'] *
                input_data['eta ' + cog_unit + ' Heat'])
            # if additional boiler, the capacity of the boiler is set to meet
            # the residual demand
            if input_data['Heat source ' + cog_unit + ' Boiler'] == 'yes':
                input_data['cap ' + cog_unit + ' Boiler'] = \
                    max_demand * input_data['ratio Backup ' + cog_unit]
                # if capacity is negative it is set to zero
                if input_data['cap ' + cog_unit + ' Boiler'] < 0:
                    input_data['cap ' + cog_unit + ' Boiler'] = 0
            # if additional thermal storage, the capacity of the cog unit and
            # the thermal storage discharge rate are restrained by
            # "ratio Backup"; the thermal storage capacity is set to
            # max. load * t_st_heating
            #elif input_data[cog_unit + ' Storage Thermal'] == 'yes':
                #input_data['cap ' + cog_unit + ' Boiler'] = 0.0
                #input_data['Discharge rate ' + cog_unit + ' Storage Thermal']\
                    #= (max_demand - cap_cog_unit_heat) * 1.01
                ## if capacity is negative it is set to zero
                #if input_data['cap ' + cog_unit + ' Boiler'] < 0:
                    #input_data['cap ' + cog_unit + ' Boiler'] = 0
                #input_data['cap ' + cog_unit + ' Storage Thermal'] = \
                    #(max_demand * input_data['t_st_heating'])
            else:
                if cap_cog_unit_heat < max_demand:
                    sys.exit('The capacity of the ' + cog_unit +
                        ' is too small to meet the heat demand.')

    return input_data