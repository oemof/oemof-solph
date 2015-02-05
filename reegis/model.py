#!/usr/bin/python
# -*- coding: utf-8

import pulp
import time
import database as db
import prepare_model
import heat_supply
import co2_emissions
import costs


def calculation(hourly_heat_demand, hourly_el_demand, hourly_wind_pot,
    hourly_pv_pot, hourly_st_pot, hourly_biogas_potential,
    annual_biomass_potential, hourly_hydro_pot, begin, input_data, p_set, cop):
    '''
    Cost-optimizes the utilization of the considered system components
    (Power plants and storages).
    '''

    ################################# input ################################

    print (("Starte Modellerstellung %r" % time.strftime("%H:%M:%S")))

    # hours of the year
    hoy = p_set['hoy']
    # Supply temp profile
    T_sup = heat_supply.calc_dh_supply_temp(input_data)
    # get source lists
    [heat_gas, el_heating_gas, ts_gas,
        heat_oil, el_heating_oil, ts_oil,
        heat_biomass, el_heating_biomass, ts_biomass,
        heat_coal, el_heating_coal, ts_coal,
        heat_DH, el_heating_DH, ts_DH, cogeneration_DH,
        power, storages, storages_bio, storages_vars, battery,
        dec_biogas_sinks, biogas_sinks, biomass_sinks,
        heat_hpm_air, ts_hpm_air_heating, ts_hpm_air_ww,
        el_heating_hpm_air_heating, el_heating_hpm_air_ww, heat_hpm_brine,
        ts_hpm_brine_heating, ts_hpm_brine_ww, hp_ts_dict, el_heating,
        dec_cog_units, dec_cog_units_boiler, dec_cog_units_excess,
        heat_st, heat_st_supp_gas, el_heating_st, ts_st] = \
        prepare_model.lists(input_data)
    # get dictionaries
    if p_set['optimize_for'] == 'Costs':
        dep_var = costs.variable(input_data)
    else:
        dep_var = co2_emissions.variable(input_data)
    efficiency = prepare_model.efficiency_dict(input_data, power, heat_gas,
        heat_oil, heat_biomass, heat_coal, heat_DH, heat_st, heat_st_supp_gas,
        cogeneration_DH, dec_cog_units, dec_cog_units_boiler)
    capacity = prepare_model.capacity_dict(input_data, power, heat_gas,
        heat_oil, heat_biomass, heat_st, heat_st_supp_gas, heat_coal, heat_DH,
        el_heating, cogeneration_DH, storages, battery,
        storages_bio, hoy, hourly_wind_pot, hourly_pv_pot, hourly_st_pot,
        hourly_hydro_pot,
        efficiency, heat_hpm_air, heat_hpm_brine, annual_biomass_potential,
        hourly_biogas_potential, dec_cog_units, dec_cog_units_boiler,
        hourly_heat_demand)
    discharge_rate = prepare_model.discharge_rate_dict(input_data,
        storages, battery, hoy, hourly_heat_demand)
    soc_loss = prepare_model.soc_loss_dict(input_data, storages, battery, hoy)
    discharge_loss = prepare_model.discharge_loss_dict(
        input_data, storages, hoy)

    ############################ problem creation ##########################

    prob = pulp.LpProblem('CO2 Optimum', pulp.LpMinimize)

    ############################ problem variables ##########################

    variables = prepare_model.variables_list(power, heat_gas, heat_oil,
        heat_biomass, heat_st, heat_st_supp_gas, heat_coal, heat_DH,
        cogeneration_DH, el_heating,
        storages_vars, heat_hpm_air, heat_hpm_brine,
        dec_cog_units, dec_cog_units_boiler, dec_cog_units_excess)
    lp_variables = pulp.LpVariable.dicts('Energy', (variables,
        list(range(hoy))), 0)

    print (("Zwischenzeit (Start-Prob): %.0f Sekunden" % (time.time() - begin)))

    ########################### objective function ########################

    prob += ((pulp.lpSum([(dep_var[i] / efficiency[i] * lp_variables[i][hour]
            for i in (heat_gas + heat_oil + heat_biomass + heat_coal + heat_DH +
            heat_st + heat_st_supp_gas + dec_cog_units_boiler + power))]
            for hour in range(hoy)))
        + (pulp.lpSum([(dep_var[i + ' Power'] / efficiency[i + ' Power']
            * lp_variables[i + ' Power'][hour]
            + dep_var[i + ' Heat'] / efficiency[i + ' Heat']
            * lp_variables[i + ' Heat'][hour]
            for i in (cogeneration_DH + dec_cog_units))]
            for hour in range(hoy))),
        'Total costs of power and heat')

    print (("Zwischenzeit (Obj-Func.): %.0f Sekunden" % (time.time() - begin)))

    ############################## constraints ############################

    # satisfaction of heat and power demand
      # Power
    for hour in range(hoy):
        prob += (pulp.lpSum([lp_variables[i][hour] for i in power])
        + pulp.lpSum([lp_variables[i + ' Power'][hour]
            for i in (cogeneration_DH + dec_cog_units)])
        + pulp.lpSum([lp_variables[i + ' Discharge'][hour]
            for i in battery])
        - pulp.lpSum([lp_variables[i + ' Charge'][hour]
            for i in battery])
        - pulp.lpSum([lp_variables[i][hour]
            for i in el_heating])
        - pulp.lpSum([lp_variables[i][hour] / cop[i][hour]
            for i in (heat_hpm_air + heat_hpm_brine)])
        >= hourly_el_demand[hour],
        'Power demand ' + str(hour))
      # Gas Heating
    if input_data['Heat source Gas Heat'] == 'yes':
        for hour in range(hoy):
            prob += (pulp.lpSum([lp_variables[i][hour]
                for i in (heat_gas + el_heating_gas)])
            + pulp.lpSum([lp_variables['Gas Storage Thermal Discharge'][hour]
                if 'Gas Storage Thermal' in ts_gas else 0])
            - pulp.lpSum([lp_variables[i + ' Charge'][hour]
                for i in ts_gas])
            >= hourly_heat_demand['Gas'][hour],
            'Heat demand Gas ' + str(hour))
      # Oil Heating
    if input_data['Heat source Oil Heat'] == 'yes':
        for hour in range(hoy):
            prob += (pulp.lpSum([lp_variables[i][hour]
                for i in (heat_oil + el_heating_oil)])
            + pulp.lpSum([lp_variables[i + ' Discharge'][hour]
                for i in ts_oil])
            - pulp.lpSum([lp_variables[i + ' Charge'][hour]
                for i in ts_oil])
            >= hourly_heat_demand['Oil'][hour],
            'Heat demand Oil ' + str(hour))
      # Biomass Heating
    if input_data['Heat source Biomass Heat'] == 'yes':
        for hour in range(hoy):
            prob += (pulp.lpSum([lp_variables[i][hour]
                for i in (heat_biomass + el_heating_biomass)])
            + pulp.lpSum([lp_variables[i + ' Discharge'][hour]
                for i in ts_biomass])
            - pulp.lpSum([lp_variables[i + ' Charge'][hour]
                for i in ts_biomass])
            >= hourly_heat_demand['Biomass'][hour],
            'Heat demand Biomass ' + str(hour))
      # Solarthermal Heat
    if input_data['Heat source ST Heat'] == 'yes':
        for hour in range(hoy):
            prob += (pulp.lpSum([lp_variables[i][hour]
                for i in (heat_st + heat_st_supp_gas + el_heating_st)])
            + pulp.lpSum([lp_variables[i + ' Discharge'][hour]
                for i in ts_st])
            - pulp.lpSum([lp_variables[i + ' Charge'][hour]
                for i in ts_st])
            >= hourly_heat_demand['ST'][hour],
            'Heat demand ST Heat' + str(hour))
      # Coal Heating
    if input_data['Heat source Coal Heat'] == 'yes':
        for hour in range(hoy):
            prob += (pulp.lpSum([lp_variables[i][hour]
                for i in (heat_coal + el_heating_coal)])
            + pulp.lpSum([lp_variables[i + ' Discharge'][hour]
                for i in ts_coal])
            - pulp.lpSum([lp_variables[i + ' Charge'][hour]
                for i in ts_coal])
            >= hourly_heat_demand['Coal'][hour],
            'Heat demand Coal ' + str(hour))
      # Dec. Cog units
    for cog_unit in dec_cog_units:
        for hour in range(hoy):
            prob += (pulp.lpSum([lp_variables[cog_unit + ' Heat'][hour]])
            + pulp.lpSum([lp_variables[cog_unit + ' Boiler'][hour]
                if (cog_unit + ' Boiler') in dec_cog_units_boiler else 0.0])
            + pulp.lpSum([lp_variables[cog_unit + ' el Heating'][hour]
                if (cog_unit + ' el Heating') in el_heating else 0.0])
            + pulp.lpSum([lp_variables[
                cog_unit + ' Storage Thermal Discharge'][hour]
                if (cog_unit + ' Storage Thermal Discharge') in storages_vars
                else 0.0])
            - pulp.lpSum([lp_variables[
                cog_unit + ' Storage Thermal Charge'][hour]
                if (cog_unit + ' Storage Thermal Charge') in storages_vars
                else 0.0])
            - pulp.lpSum([lp_variables[
                cog_unit + ' Excess Heat'][hour]
                if (cog_unit + ' Excess Heat') in dec_cog_units_excess
                else 0.0])
            == hourly_heat_demand[cog_unit][hour],
            'Heat demand ' + cog_unit + ' ' + str(hour))
    if 'Biogas Cog unit' in dec_cog_units:
        for hour in range(hoy):
            prob += (pulp.lpSum([
            lp_variables['Biogas Cog unit Heat Demand'][hour]])
            + pulp.lpSum([lp_variables['Biogas Cog unit Boiler'][hour]
                if ('Biogas Cog unit Boiler') in dec_cog_units_boiler else 0.0])
            + pulp.lpSum([lp_variables['Biogas Cog unit el Heating'][hour]
                if ('Biogas Cog unit el Heating') in el_heating else 0.0])
            + pulp.lpSum([lp_variables[
                'Biogas Cog unit Storage Thermal Discharge'][hour]
                if 'Biogas Cog unit Storage Thermal Discharge'
                in storages_vars else 0.0])
            - pulp.lpSum([lp_variables[
                'Biogas Cog unit Storage Thermal Charge'][hour]
                if 'Biogas Cog unit Storage Thermal Charge'
                in storages_vars else 0.0])
            == hourly_heat_demand[cog_unit][hour],
            'Heat needed ' + cog_unit + ' ' + str(hour))
      # HP Mono Air
    for heat_pump in heat_hpm_air:
        for hour in range(hoy):
            prob += (pulp.lpSum([lp_variables[heat_pump][hour]])
            + pulp.lpSum([lp_variables[heat_pump + ' el Heating'][hour]])
            + pulp.lpSum([lp_variables[i + ' Discharge'][hour]
                for i in hp_ts_dict[heat_pump]])
            - pulp.lpSum([lp_variables[i + ' Charge'][hour]
                for i in hp_ts_dict[heat_pump]])
            >= hourly_heat_demand[heat_pump][hour],
            'Heat demand ' + heat_pump + ' ' + str(hour))
      # HP Mono Brine
    for heat_pump in heat_hpm_brine:
        for hour in range(hoy):
            prob += (pulp.lpSum([lp_variables[heat_pump][hour]])
            + pulp.lpSum([lp_variables[i + ' Discharge'][hour]
                for i in hp_ts_dict[heat_pump]])
            - pulp.lpSum([lp_variables[i + ' Charge'][hour]
                for i in hp_ts_dict[heat_pump]])
            >= hourly_heat_demand[heat_pump][hour],
            'Heat demand ' + heat_pump + ' ' + str(hour))
      # District Heating
    for hour in range(hoy):
        prob += (pulp.lpSum([lp_variables[i][hour]
            for i in (heat_DH + el_heating_DH)])
        + pulp.lpSum([lp_variables[i + ' Heat'][hour]
            for i in cogeneration_DH])
        + pulp.lpSum([lp_variables[i + ' Discharge'][hour]
            for i in ts_DH])
        - pulp.lpSum([lp_variables[i + ' Charge'][hour]
            for i in ts_DH])
        >= hourly_heat_demand['DH'][hour],
        'Heat demand DH ' + str(hour))

    print (("Zwischenzeit (C1_demand): %.0f Sekunden" % (time.time() - begin)))

    # energy amount must be smaller or equal to the PP capacity
    for hour in range(hoy):
        for i in (power + heat_gas + heat_oil + heat_biomass + heat_st +
            heat_st_supp_gas + heat_coal + heat_DH + el_heating +
            heat_hpm_air + heat_hpm_brine + dec_cog_units_boiler):
            prob += (lp_variables[i][hour]
                <= capacity[i][hour],
                'Energy smaller cap ' + str(hour) + ' ' + i)

    for hour in range(hoy):
        for i in (cogeneration_DH + dec_cog_units):
            prob += (lp_variables[i + ' Power'][hour]
                <= capacity[i + ' Power'][hour],
                'Energy smaller cap ' + str(hour) + ' ' + i)

    if 'DH Biogas Heat' in heat_DH and 'DH Thermal Storage Boiler' in heat_DH \
    and input_data['fuel DH Thermal Storage Boiler'] == 'Biogas':
        for hour in range(hoy):
            prob += (lp_variables['DH Biogas Heat'][hour]
                + lp_variables['DH Thermal Storage Boiler'][hour]
                - capacity['DH Biogas Heat'][hour]
                <= 0,
                'Energy smaller cap ' + str(hour) + ' Boiler')

    if 'Biomass Power' in power and 'DH Biomass Cog' in cogeneration_DH:
        for hour in range(hoy):
            prob += (lp_variables['Biomass Power'][hour]
                / efficiency['Biomass Power']
                + lp_variables['DH Biomass Cog Power'][hour]
                / efficiency['DH Biomass Cog Power']
                - capacity['Biomass Power'][hour]
                / efficiency['Biomass Power']
                <= 0,
                'Biomass Power smaller cap ' + str(hour))

    # state of charge must be smaller or equal to the storage capacity
    for hour in range(hoy):
        for i in (storages + battery + storages_bio):
            prob += (lp_variables[i + ' SoC'][hour]
                <= capacity[i][hour],
                i + ' SoC smaller cap ' + str(hour))

    print (("Zwischenzeit (C2_capacity): %.0f Sekunden"
        % (time.time() - begin)))

    # dependencies of power and heat output of cogeneration
    for hour in range(hoy):
        for i in (cogeneration_DH + dec_cog_units):
            prob += (pulp.lpSum(
                lp_variables[i + ' Power'][hour] / efficiency[i + ' Power']
                - lp_variables[i + ' Heat'][hour] / efficiency[i + ' Heat'])
                == 0,
                i + ' dependency ' + str(hour))

    print (("Zwischenzeit (C3_Cogen): %.0f Sekunden" % (time.time() - begin)))

    # storages discharge rates
    for i in (storages + battery):
        for hour in range(hoy):
            prob += (lp_variables[i + ' Discharge'][hour]
                <= discharge_rate[i][hour],
                i + ' discharge smaller discharge rate ' + str(hour))

    # decentral biogas discharge and charge
    if 'Storage Biogas dec' in storages_bio:
        for hour in range(hoy):
            prob += (lp_variables['Storage Biogas dec Discharge'][hour]
                - pulp.lpSum([(lp_variables[i][hour] / efficiency[i]
                for i in dec_biogas_sinks)])
                == 0,
                'Biogas discharge (decentral) ' + str(hour))

            prob += (lp_variables['Storage Biogas dec Charge'][hour]
                == hourly_biogas_potential['dec'],
                'Biogas charge (decentral) ' + str(hour))

    # biogas discharge and charge
    if 'Storage Biogas' in storages_bio:
        for hour in range(hoy):
            prob += (lp_variables['Storage Biogas Discharge'][hour]
                - pulp.lpSum([(lp_variables[i][hour] / efficiency[i]
                for i in biogas_sinks)])
                == 0,
                'Biogas discharge ' + str(hour))

            prob += (lp_variables['Storage Biogas Charge'][hour]
                == hourly_biogas_potential['central'],
                'Biogas charge ' + str(hour))

    # biomass discharge and charge
    if 'Storage Biomass' in storages_bio:
        for hour in range(hoy):
            prob += (lp_variables['Storage Biomass Discharge'][hour]
                - pulp.lpSum([(lp_variables[i][hour] / efficiency[i]
                for i in biomass_sinks)])
                == 0,
                'Biomass discharge ' + str(hour))

            prob += (lp_variables['Storage Biomass Charge'][hour]
                == 0,
                'Biomass charge ' + str(hour))

    # soc thermal storages
    # state of charge of hour is equal to the state of charge of hour-1
    # plus/minus charge/discharge in the hour
    for i in storages:
        prob += (lp_variables[i + ' SoC'][0]
            - lp_variables[i + ' SoC'][hoy - 1]
            + lp_variables[i + ' SoC'][0] * soc_loss[i][0]
            + lp_variables[i + ' Discharge'][0]
            + lp_variables[i + ' Discharge'][0] * discharge_loss[i][0]
            - lp_variables[i + ' Charge'][0]
            == 0,
            i + ' SoC ' + str(0))

        for hour in range(1, hoy):
            prob += (lp_variables[i + ' SoC'][hour]
                - lp_variables[i + ' SoC'][hour - 1]
                + lp_variables[i + ' SoC'][hour] * soc_loss[i][hour]
                + lp_variables[i + ' Discharge'][hour]
                + lp_variables[i + ' Discharge'][hour] * discharge_loss[i][hour]
                - lp_variables[i + ' Charge'][hour]
                == 0,
                i + ' SoC ' + str(hour))

    # soc battery
    # state of charge of hour is equal to the state of charge of hour-1
    # plus/minus charge/discharge in the hour
    if 'Storage Battery' in battery:
        prob += (lp_variables['Storage Battery SoC'][0]
            - lp_variables['Storage Battery SoC'][hoy - 1]
            + lp_variables['Storage Battery SoC'][0]
            * soc_loss['Storage Battery'][0]
            + lp_variables['Storage Battery Discharge'][0]
            / input_data['eta Storage Battery']
            - lp_variables['Storage Battery Charge'][0]
            == 0,
            'Storage Battery SoC ' + str(0))

        for hour in range(1, hoy):
            prob += (lp_variables['Storage Battery SoC'][hour]
                - lp_variables['Storage Battery SoC'][hour - 1]
                + lp_variables['Storage Battery SoC'][hour]
                * soc_loss['Storage Battery'][hour]
                + lp_variables['Storage Battery Discharge'][hour]
                / input_data['eta Storage Battery']
                - lp_variables['Storage Battery Charge'][hour]
                == 0,
                'Storage Battery SoC ' + str(hour))

    # soc biogas storage
    # state of charge of hour is equal to the state of charge of hour-1
    # plus/minus charge/discharge in the hour
    for i in ['Storage Biogas', 'Storage Biogas dec']:
        if i in storages_bio:
            prob += (lp_variables[i + ' SoC'][0]
                - lp_variables[i + ' SoC'][hoy - 1]
                + lp_variables[i + ' Discharge'][0]
                - lp_variables[i + ' Charge'][0]
                == 0,
                i + ' SoC ' + str(0))

            for hour in range(1, hoy):
                prob += (lp_variables[i + ' SoC'][hour]
                    - lp_variables[i + ' SoC'][hour - 1]
                    + lp_variables[i + ' Discharge'][hour]
                    - lp_variables[i + ' Charge'][hour]
                    == 0,
                    i + ' SoC ' + str(hour))

    # soc biomass storage
    # state of charge of hour is equal to the state of charge of hour-1
    # plus/minus charge/discharge in the hour
    if 'Storage Biomass' in storages_bio:
        prob += (lp_variables['Storage Biomass SoC'][0]
            + lp_variables['Storage Biomass Discharge'][0]
            == annual_biomass_potential,
            'Storage Biomass SoC ' + str(0))

        for hour in range(1, hoy):
            prob += (lp_variables['Storage Biomass SoC'][hour]
                - lp_variables['Storage Biomass SoC'][hour - 1]
                + lp_variables['Storage Biomass Discharge'][hour]
                - lp_variables['Storage Biomass Charge'][hour]
                == 0,
                'Storage Biomass SoC ' + str(hour))

    print (("Zwischenzeit (C4_Storages): %.0f Sekunden"
        % (time.time() - begin)))

    # provide supply temperature
    if 'DH Storage Thermal' in storages:
        for hour in range(hoy):
            if T_sup[hour] > input_data['DH T_storage']:
                prob += (lp_variables['DH Thermal Storage Boiler'][hour]
                    * (input_data['DH T_storage'] - input_data['DH T_return'])
                    - lp_variables['DH Storage Thermal Discharge'][hour]
                    * (T_sup[hour] - input_data['DH T_storage'])
                    == 0,
                    'Provide supply temp ' + str(hour))

            else:
                prob += (lp_variables['DH Thermal Storage Boiler'][hour]
                    == 0,
                    'Provide supply temp ' + str(hour))

    print (("Zwischenzeit (C5_DH): %.0f Sekunden"
        % (time.time() - begin)))

    ############################## call solver ############################

    # problem data is written to an .lp file
    #prob.writeLP('Opt.lp')

    # problem is solved using the solver of choice
    solvertime = time.time()
    solver_choice = input_data['Solver']

    print (("Zwischenzeit (Solverstart): %.0f Sekunden"
        % (time.time() - begin)))
    print (("Start %s at %s" %
        (solver_choice, time.strftime("%H:%M:%S"))))
    if solver_choice == 'PULP_CBC_CMD':
        prob.solve(pulp.PULP_CBC_CMD(msg=p_set['solver_message']))
    elif solver_choice == 'GUROBI_CMD':
        prob.solve(pulp.GUROBI_CMD(msg=p_set['solver_message']))
    elif solver_choice == 'GUROBI':
        prob.solve(pulp.GUROBI(msg=p_set['solver_message']))
    elif solver_choice == 'GLPK_CMD':
        prob.solve(pulp.GLPK_CMD(msg=p_set['solver_message']))
    elif solver_choice == 'PYGLPK':
        prob.solve(pulp.PYGLPK(msg=p_set['solver_message']))
    elif solver_choice == 'COIN_CMD':
        prob.solve(pulp.COIN_CMD(msg=p_set['solver_message']))
    else:
        prob.solve(pulp.PULP_CBC_CMD(msg=p_set['solver_message']))
        print (('The solver choice was not valid. Therefore the default' +
        'solver PULP CBC CMD was used.'))

    print (("%s: %.0f Sekunden" % (solver_choice, (time.time() - solvertime))))
    print (("Zwischenzeit (Nach Solver): %.0f Sekunden"
        % (time.time() - begin)))

    ############################# write to db ############################

    db.data2db(p_set['schema'], p_set['output_table'],
        variables, lp_variables)

    print (("Zwischenzeit (Nach DB): %.0f Sekunden" % (time.time() - begin)))
    sum_dep_var = pulp.value(prob.objective)
    del(prob)

    ######################### component dictionary ########################

    components_dict = {'Power Sources': power,
        'Heat Sources': heat_DH,
        'Cog Sources': cogeneration_DH,
        'Storages': (battery + storages),
        'Heating Systems': (heat_gas + heat_oil + heat_biomass + heat_coal),
        'Heat Pump Mono': (heat_hpm_air + heat_hpm_brine),
        'dec Cog units': (dec_cog_units + dec_cog_units_boiler),
        'Solarthermal System': (heat_st + heat_st_supp_gas),
        'el Heating': el_heating}

    return sum_dep_var, components_dict