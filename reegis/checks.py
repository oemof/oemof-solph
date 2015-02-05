#!/usr/bin/python
# -*- coding: utf-8


import sys


def evaluate(input_data, hourly_heat_demand,
    annual_biomass_pot, hourly_biogas_pot):
    '''
    Checks for various things that could lead to an infeasible problem
    definition and exits the execution in case the condition is not met.
    '''
    # biomass potential not sufficient
    if input_data['Heat source Biomass Heat'] == 'yes':
        if sum(hourly_heat_demand['Biomass']) / input_data['eta Biomass Heat'] \
        > annual_biomass_pot:
            sys.exit('The biomass potential is too small to meet the' +
                    ' heat demand.' + '\n' +
                    'The total biomass potential is: %s.'
                    % annual_biomass_pot + '\n' +
                    'The total biomass demand for domestic heating is: %s'
                    % sum(hourly_heat_demand['Biomass']))

    if input_data['Heat source Biogas Cog unit'] == 'yes':
        # annual biogas potential not sufficient to meet heat demand
        if (sum(hourly_heat_demand['Biogas Cog unit']) /
        input_data['eta Biogas Cog unit Heat']) > \
        (8760 * hourly_biogas_pot['dec']) and \
        input_data['Heat source Biogas Cog unit Boiler'] == 'no' and \
        input_data['Heat source Biogas Cog unit el Heating'] == 'no':
            sys.exit('The biogas potential for the decentralized biogas' +
                    ' cogeneration units is too small to meet the heat' +
                    ' demand.' + '\n' +
                    'The total biogas potential is: %s.'
                    % (8760 * hourly_biogas_pot['dec']) + '\n' +
                    'The total biogas demand is: %s'
                    % (sum(hourly_heat_demand['Biogas Cog unit']) /
                    input_data['eta Biogas Cog unit Heat']))
        # cap of biogas cogeneration units is not sufficient
        cap_heat = (input_data['cap Biogas Cog unit Power'] /
            input_data['eta Biogas Cog unit Power'] *
            input_data['eta Biogas Cog unit Heat'])
        if input_data['Biogas Cog unit Storage Thermal'] == 'yes':
            cap_heat += \
                input_data['Discharge rate Biogas Cog unit Storage Thermal']
        if cap_heat < max(hourly_heat_demand['Biogas Cog unit']) and \
        input_data['Heat source Biogas Cog unit Boiler'] == 'no':
                sys.exit('The capacity of the decentralized biogas' +
                        ' cogeneration units is too small to meet the heat' +
                        ' demand.' + '\n' +
                        'The total capacity (Heat) is: %s.' % cap_heat + '\n' +
                        'The total capacity (Power) should be at least: %s.'
                        % (max(hourly_heat_demand['Biogas Cog unit']) /
                        input_data['eta Biogas Cog unit Heat'] *
                        input_data['eta Biogas Cog unit Power']) + '\n' +
                        'The maximum heat demand is: %s'
                        % max(hourly_heat_demand['Biogas Cog unit']))
        # hourly potential (in combination with a limited storage capacity)
        # may not be sufficient to meet the heat demand in winter
        if hourly_biogas_pot['dec'] * input_data['eta Biogas Cog unit Heat'] < \
        max(hourly_heat_demand['Biogas Cog unit']):
            print (('The hourly biogas potential may not be sufficient ' +
                'to meet the heat demand of dec. biogas units in the winter.'))
    return