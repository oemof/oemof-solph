#!/usr/bin/python
# -*- coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import os
from math import ceil
import plot_data
import plot_lists
import output


def y_ticks_list(lim):
    '''
    Returns a list with y-ticks. The y-tick interval depends on the maximum
    y-value.
    '''
    if lim <= 70:
        if lim % 10 == 0:
            max_tick = lim
        else:
            max_tick = lim + 10 - lim % 10
        y_ticks = np.arange(0, max_tick + 1, 10).tolist()
    elif lim > 70 and lim <= 140:
        if lim % 20 == 0:
            max_tick = lim
        else:
            max_tick = lim + 20 - lim % 20
        y_ticks = np.arange(0, max_tick + 1, 20).tolist()
    elif lim > 140 and lim <= 200:
        if lim % 40 == 0:
            max_tick = lim
        else:
            max_tick = lim + 40 - lim % 40
        y_ticks = np.arange(0, max_tick + 1, 40).tolist()
    elif lim > 200 and lim <= 300:
        if lim % 50 == 0:
            max_tick = lim
        else:
            max_tick = lim + 50 - lim % 50
        y_ticks = np.arange(0, max_tick + 1, 50).tolist()
    elif lim > 300 and lim <= 600:
        if lim % 100 == 0:
            max_tick = lim
        else:
            max_tick = lim + 100 - lim % 100
        y_ticks = np.arange(0, max_tick + 1, 100).tolist()
    else:
        if lim % 200 == 0:
            max_tick = lim
        else:
            max_tick = lim + 200 - lim % 200
        y_ticks = np.arange(0, max_tick + 1, 200).tolist()
    return y_ticks


def stack(colnames, colnames_in, data, in_data, week, cols_p, cols_h, cols_h_DH,
    cd_p, cd_h, cd_h_DH, list_demand_p, list_demand_h, list_demand_h_DH,
    legend_p, legend_h, legend_h_DH,
    list_demand_p_legend, list_demand_h_legend, list_demand_h_DH_legend,
    efficiency_heat_pump,
    output_dir, stackplot_name, number_of_days, show):

    fig1 = plt.figure(figsize=(22.0, 14.0))
    ax1 = fig1.add_subplot(3, 1, 1)
    ax2 = fig1.add_subplot(3, 1, 2)
    ax3 = fig1.add_subplot(3, 1, 3)
    fig1.subplots_adjust(hspace=.1, wspace=-5)
    ax1.set_ylabel("Strom [MW]")
    ax2.set_ylabel("Dez. Heizungen [MW]")
    ax3.set_ylabel(u"Fernwärme [MW]")
    ax3.set_xlabel("Stunde des Jahres")

    # x-axis ticks
    x_ticks = np.arange(24 * 7 * (week - 1) + 24,
        (week - 1) * 7 * 24 + 24 * number_of_days + 1,
        24).tolist()
    ax1.xaxis.set_ticks(x_ticks)
    ax2.xaxis.set_ticks(x_ticks)
    ax3.xaxis.set_ticks(x_ticks)

    # font size
    plt.rcParams.update({'font.size': 23})  # 19
    plt.rc('legend', **{'fontsize': 12})  # 12

    ############################## subplot 1 ###############################

    #ax1.subplot(311)
    # plot two weeks as stacked bar plot
    sp = list(range(cols_p.shape[0]))
    for i in range(cols_p.shape[0]):
        sp[i] = ax1.bar(data[:, 0], data[:, cols_p[i]],
                    width=1,
                    linewidth=0,
                    color=cd_p[i],
                    bottom=data[:, cols_p[0:i]].sum(axis=1))

    # plot load and charge as line plot
    # all el Heating choices are combined into one charge line

    lp_range = []  # len(lp_range) defines number of different lines in
                   # el. plot [Battery Charge, El Heating, Heat Pump, El Load]
    lp_choice_el_heating = []  # list of el Heating demand
      # Battery Charge
    if 'Storage Battery Charge' in colnames:
        battery_charge_row = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[0][0]])
        lp_range.append('Battery Charge')
        battery_charge = data[:, battery_charge_row]
    else:
        battery_charge = np.zeros((number_of_days * 24, 1))
      # Gas el Heating
    if 'Gas el Heating' in colnames:
        el_gas = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[1][0]])
        lp_choice_el_heating.append(el_gas)
        lp_range.append('El Heating')
      # Oil el Heating
    if 'Oil el Heating' in colnames:
        el_oil = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[2][0]])
        lp_choice_el_heating.append(el_oil)
        if not 'El Heating' in lp_range:
            lp_range.append('El Heating')
      # Biomass el Heating
    if 'Biomass el Heating' in colnames:
        el_biomass = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[3][0]])
        lp_choice_el_heating.append(el_biomass)
        if not 'El Heating' in lp_range:
            lp_range.append('El Heating')
      # Coal el Heating
    if 'Coal el Heating' in colnames:
        el_coal = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[4][0]])
        lp_choice_el_heating.append(el_coal)
        if not 'El Heating' in lp_range:
            lp_range.append('El Heating')
      # DH el Heating
    if 'DH el Heating' in colnames:
        el_dh = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[5][0]])
        lp_choice_el_heating.append(el_dh)
        if not 'El Heating' in lp_range:
            lp_range.append('El Heating')
      # HP Mono Air Heating + el Heating
    sum_heat_pump = np.zeros((number_of_days * 24, 1))
    if 'HP Mono Air Heating' in colnames:
        hp_heating = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[6][0]])
        start = (week - 1) * 168
        end = start + number_of_days * 24
        lp_range.append('HP')
        # sum
        sum_heat_pump += (data[:, hp_heating] /
            efficiency_heat_pump['HP Mono Air Heating'][start: end])
        # el Heating
        hp_el_heating = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[11][0]])
        sum_heat_pump += data[:, hp_el_heating]
      # HP Mono Air WW + el Heating
    if 'HP Mono Air WW' in colnames:
        hp_water = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[7][0]])
        start = (week - 1) * 168
        end = start + number_of_days * 24
        if not 'HP' in lp_range:
            lp_range.append('HP')
        # sum
        sum_heat_pump += (data[:, hp_water] /
            efficiency_heat_pump['HP Mono Air WW'][start: end])
        # el Heating
        hp_el_heating = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[12][0]])
        sum_heat_pump += data[:, hp_el_heating]
      # HP Mono Brine Heating
    if 'HP Mono Brine Heating' in colnames:
        hp_heating = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[8][0]])
        start = (week - 1) * 168
        end = start + number_of_days * 24
        if not 'HP' in lp_range:
            lp_range.append('HP')
        # sum
        sum_heat_pump += (data[:, hp_heating] /
            efficiency_heat_pump['HP Mono Brine Heating'][start: end])
      # HP Mono Brine WW
    if 'HP Mono Brine WW' in colnames:
        hp_water = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[9][0]])
        start = (week - 1) * 168
        end = start + number_of_days * 24
        if not 'HP' in lp_range:
            lp_range.append('HP')
        # sum
        sum_heat_pump += (data[:, hp_water] /
            efficiency_heat_pump['HP Mono Brine WW'][start: end])
      # Gas Cog unit Heat el Heating
    if 'Gas Cog unit el Heating' in colnames:
        el_gas_cog = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[13][0]])
        lp_choice_el_heating.append(el_gas_cog)
        if not 'El Heating' in lp_range:
            lp_range.append('El Heating')
      # Biogas Cog unit Heat el Heating
    if 'Biogas Cog unit el Heating' in colnames:
        el_biogas_cog = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[15][0]])
        lp_choice_el_heating.append(el_biogas_cog)
        if not 'El Heating' in lp_range:
            lp_range.append('El Heating')
      # ST el Heating
    if 'ST el Heating' in colnames:
        el_st = ([i for i, x in enumerate(colnames)
            if x == list_demand_p[14][0]])
        lp_choice_el_heating.append(el_st)
        if not 'El Heating' in lp_range:
            lp_range.append('El Heating')

      # el Load
    el_demand_row = ([i for i, x in enumerate(colnames_in)
        if x == list_demand_p[10][0]])
    lp_range.append('El Demand')
    el_demand = in_data[:, el_demand_row]

    lp = list(range(len(lp_range)))

    # cumulated el load due to el heating systems
    sum_el_heating = np.zeros((number_of_days * 24, 1))
    if 'El Heating' in lp_range:
        for i in lp_choice_el_heating:
            sum_el_heating += data[:, i]

    if 'Battery Charge' in lp_range:

        if 'El Heating' in lp_range:

            if 'HP' in lp_range:

                  # Battery Charge
                lp[0] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_heat_pump + sum_el_heating + battery_charge,
                    '-', linewidth=2, color=list_demand_p_legend[3][1])
                  # el Heating
                lp[1] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_heat_pump + sum_el_heating,
                    '-', linewidth=2, color=list_demand_p_legend[2][1])
                  # Heat Pump
                lp[2] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_heat_pump,
                    '-', linewidth=2, color=list_demand_p_legend[1][1])
            else:
                  # Battery Charge
                lp[0] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_el_heating + battery_charge,
                    '-', linewidth=2, color=list_demand_p_legend[2][1])
                  # el Heating
                lp[1] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_el_heating,
                    '-', linewidth=2, color=list_demand_p_legend[1][1])

        else:

            if 'HP' in lp_range:

                  # Battery Charge
                lp[0] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_heat_pump + battery_charge,
                    '-', linewidth=2, color=list_demand_p_legend[2][1])
                  # Heat Pump
                lp[1] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_heat_pump,
                    '-', linewidth=2, color=list_demand_p_legend[1][1])
            else:
                  # Battery Charge
                lp[0] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + battery_charge,
                    '-', linewidth=2, color=list_demand_p_legend[1][1])

    else:

        if 'El Heating' in lp_range:

            if 'HP' in lp_range:

                  # el Heating
                lp[0] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_heat_pump + sum_el_heating,
                    '-', linewidth=2, color=list_demand_p_legend[2][1])
                  # Heat Pump
                lp[1] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_heat_pump,
                    '-', linewidth=2, color=list_demand_p_legend[1][1])
            else:
                  # el Heating
                lp[0] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_el_heating,
                    '-', linewidth=2, color=list_demand_p_legend[1][1])

        else:

            if 'HP' in lp_range:

                  # Heat Pump
                lp[0] = ax1.plot(in_data[:, 0] + 0.5,
                    el_demand + sum_heat_pump,
                    '-', linewidth=2, color=list_demand_p_legend[1][1])

      # el Load
    lp[len(lp_range) - 1] = ax1.plot(in_data[:, 0] + 0.5,
        el_demand,
        '-', linewidth=2, color=list_demand_p_legend[0][1])

    # Limits and y-axis ticks
    ax1_lim = ceil(1.2 * max(el_demand + battery_charge + sum_el_heating +
        sum_heat_pump) / 10) * 10
    ax1.set_ylim([0, ax1_lim])
    ax1.set_xlim([data[0, 0], data[-1, 0]])
    y_ticks_1 = y_ticks_list(ax1_lim)
    ax1.yaxis.set_ticks(y_ticks_1)

    # draw legend for subplot 311
    ax1.legend(tuple([sp[i][0] for i in range(len(sp), )] + [lp[i][0]
    for i in range(len(lp))][::-1]), (legend_p))

    ############################## subplot 2 ###############################

    #plt.subplot(312)
    # plot two weeks as stacked bar plot
    sp = list(range(cols_h.shape[0]))
    for i in range(cols_h.shape[0]):
        sp[i] = ax2.bar(data[:, 0], data[:, cols_h[i]],
                    width=1,
                    linewidth=0,
                    color=cd_h[i],
                    bottom=data[:, cols_h[0:i]].sum(axis=1))

    lp = list(range(len(list_demand_h_legend)))
    summe = np.zeros((number_of_days * 24, 1))

    # Biomass Heat Load
    if 'Biomass Heat' in colnames:
        l_1 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[1][0]])
        biomass_load = in_data[:, l_1]
        # Biomass Thermal Storage
        if 'Biomass Storage Thermal Charge' in colnames:
            l_2 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[0][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5, data[:, l_2] + biomass_load,
                '-', linewidth=2, color=list_demand_h[0][1]))
            summe += data[:, l_2]
        lp[0] = ax2.plot(in_data[:, 0] + 0.5, biomass_load,
                '-', linewidth=2, color=list_demand_h[1][1])
        summe += biomass_load

    # Gas Heat Load
    if 'Gas Heat' in colnames:
        l_3 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[3][0]])
        gas_load = in_data[:, l_3] + summe
        # Gas Thermal Storage
        if 'Gas Storage Thermal Charge' in colnames:
            l_4 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[2][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5, data[:, l_4] + gas_load,
                '-', linewidth=2, color=list_demand_h[2][1]))
            summe += data[:, l_4]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, gas_load,
                '-', linewidth=2, color=list_demand_h[3][1]))
        summe += in_data[:, l_3]

    # Oil Heat Load
    if 'Oil Heat' in colnames:
        l_5 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[5][0]])
        oil_load = in_data[:, l_5] + summe
        # Oil Thermal Storage
        if 'Oil Storage Thermal Charge' in colnames:
            l_6 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[4][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5, data[:, l_6] + oil_load,
                '-', linewidth=2, color=list_demand_h[4][1]))
            summe += data[:, l_6]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, oil_load,
                '-', linewidth=2, color=list_demand_h[5][1]))
        summe += in_data[:, l_5]

    # Coal Heat Load
    if 'Coal Heat' in colnames:
        l_7 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[7][0]])
        coal_load = in_data[:, l_7] + summe
        # Coal Thermal Storage
        if 'Coal Storage Thermal Charge' in colnames:
            l_8 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[6][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5, data[:, l_8] + coal_load,
                '-', linewidth=2, color=list_demand_h[6][1]))
            summe += data[:, l_8]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, coal_load,
                '-', linewidth=2, color=list_demand_h[7][1]))
        summe += in_data[:, l_7]

    # HP Mono Air Heating Heat Load
    if 'HP Mono Air Heating' in colnames:
        l_9 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[9][0]])
        heat_pump_heating_load = in_data[:, l_9] + summe
        # HP Mono Air Heating Thermal Storage
        if 'HP Mono Air Heating Storage Thermal Charge' in colnames:
            l_10 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[8][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5,
                data[:, l_10] + heat_pump_heating_load,
                '-', linewidth=2, color=list_demand_h[8][1]))
            summe += data[:, l_10]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, heat_pump_heating_load,
                '-', linewidth=2, color=list_demand_h[9][1]))
        summe += in_data[:, l_9]

    # HP Mono Air WW Heat Load
    if 'HP Mono Air WW' in colnames:
        l_11 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[11][0]])
        heat_pump_water_load = in_data[:, l_11] + summe
        # HP Mono Air WW Thermal Storage
        if 'HP Mono Air WW Storage Thermal Charge' in colnames:
            l_12 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[10][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5,
                data[:, l_12] + heat_pump_water_load,
                '-', linewidth=2, color=list_demand_h[10][1]))
            summe += data[:, l_12]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, heat_pump_water_load,
                '-', linewidth=2, color=list_demand_h[11][1]))
        summe += in_data[:, l_11]

    # HP Mono Brine Heating Heat Load
    if 'HP Mono Brine Heating' in colnames:
        l_13 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[13][0]])
        heat_pump_heating_load = in_data[:, l_13] + summe
        # HP Mono Brine Heating Thermal Storage
        if 'HP Mono Brine Heating Storage Thermal Charge' in colnames:
            l_14 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[12][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5,
                data[:, l_14] + heat_pump_heating_load,
                '-', linewidth=2, color=list_demand_h[12][1]))
            summe += data[:, l_14]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, heat_pump_heating_load,
                '-', linewidth=2, color=list_demand_h[13][1]))
        summe += in_data[:, l_13]

    # HP Mono Brine WW Heat Load
    if 'HP Mono Brine WW' in colnames:
        l_15 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[15][0]])
        heat_pump_water_load = in_data[:, l_15] + summe
        # HP Mono Brine WW Thermal Storage
        if 'HP Mono Brine WW Storage Thermal Charge' in colnames:
            l_16 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[14][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5,
                data[:, l_16] + heat_pump_water_load,
                '-', linewidth=2, color=list_demand_h[14][1]))
            summe += data[:, l_16]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, heat_pump_water_load,
                '-', linewidth=2, color=list_demand_h[15][1]))
        summe += in_data[:, l_15]

    # Gas Cog unit Heat Load
    if 'Gas Cog unit Heat' in colnames:
        l_17 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[17][0]])
        gas_cog_load = in_data[:, l_17] + summe
        # Gas Cog unit Heat Load Thermal Storage
        if 'Gas Cog unit Storage Thermal Charge' in colnames:
            l_18 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[16][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5,
                data[:, l_18] + gas_cog_load,
                '-', linewidth=2, color=list_demand_h[16][1]))
            summe += data[:, l_18]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, gas_cog_load,
                '-', linewidth=2, color=list_demand_h[17][1]))
        summe += in_data[:, l_17]

    # Biogas Cog unit Heat Load
    if 'Biogas Cog unit Heat' in colnames:
        l_19 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[19][0]])
        biogas_cog_load = in_data[:, l_19] + summe
        # Biogas Cog unit Heat Load Thermal Storage
        if 'Biogas Cog unit Storage Thermal Charge' in colnames:
            l_20 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[18][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5,
                data[:, l_20] + biogas_cog_load,
                '-', linewidth=2, color=list_demand_h[18][1]))
            summe += data[:, l_20]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, biogas_cog_load,
                '-', linewidth=2, color=list_demand_h[19][1]))
        summe += in_data[:, l_19]

    # ST Heat Load
    if 'ST Heat' in colnames:
        l_21 = ([i for i, x in enumerate(colnames_in)
            if x == list_demand_h[21][0]])
        st_load = in_data[:, l_21] + summe
        # ST Heat Load Thermal Storage
        if 'ST Storage Thermal Charge' in colnames:
            l_22 = ([i for i, x in enumerate(colnames)
                if x == list_demand_h[20][0]])
            lp[1] = (ax2.plot(in_data[:, 0] + 0.5,
                data[:, l_22] + st_load,
                '-', linewidth=2, color=list_demand_h[20][1]))
            summe += data[:, l_22]
        lp[0] = (ax2.plot(in_data[:, 0] + 0.5, st_load,
                '-', linewidth=2, color=list_demand_h[21][1]))
        summe += in_data[:, l_21]

    # Limits and y-axis ticks
    ax2_lim = ceil(1.1 * max(summe) / 10) * 10
    ax2.set_ylim([0, ax2_lim])
    ax2.set_xlim([data[0, 0], data[-1, 0]])
    y_ticks_2 = y_ticks_list(ax2_lim)
    ax2.yaxis.set_ticks(y_ticks_2)

    # draw legend for subplot 312
    list_sp = [sp[i][0] for i in range(len(sp))]
    list_lp = [lp[i][0] for i in range(len(lp))]  # [::-1]
    list_sp, legend_h = plot_lists.modify_legend(list_sp, legend_h)
    ax2.legend((list_sp + list_lp), (legend_h))

    ############################### subplot 3 ###############################

    #plt.subplot(313)
    # plot two weeks as stacked bar plot
    sp = list(range(cols_h_DH.shape[0]))
    for i in range(cols_h_DH.shape[0]):
        sp[i] = ax3.bar(data[:, 0], data[:, cols_h_DH[i]],
                    width=1,
                    linewidth=0,
                    color=cd_h_DH[i],
                    bottom=data[:, cols_h_DH[0:i]].sum(axis=1))

    # plot load and charge as line plot
      # DH Heat Load
    t = ([i for i, x in enumerate(colnames_in) if x == list_demand_h_DH[0][0]])

    if 'DH Storage Thermal Charge' in colnames:
        lp = list(range(2))
        socp = list(range(1))
          # DH Thermal Storage
        s = ([i for i, x in enumerate(colnames) if x == list_demand_h_DH[1][0]])
        lp[0] = ax3.plot(in_data[:, 0] + 0.5, in_data[:, t] +
                data[:, s], '-', linewidth=2, color=list_demand_h_DH[1][1])
          # DH Heat Load
        lp[1] = ax3.plot(in_data[:, 0] + 0.5, in_data[:, t],
                '-', linewidth=2, color=list_demand_h_DH[0][1])

        # sum for limits
        sum_dh = in_data[:, t] + data[:, s]

        # second y-axis for SoC
        ax4 = ax3.twinx()
        ax4.set_ylabel(u"SoC [MWh]")

          # SoC
        SoC = ([i for i, x in enumerate(colnames)
            if x == 'DH Storage Thermal SoC'])
        socp[0] = ax4.plot(in_data[:, 0] + 0.5, data[:, SoC],
                '--', linewidth=2, color='b')

        ax4_lim = ceil(1.1 * max(data[:, SoC]) / 10) * 10
        ax4.set_ylim([0, ax4_lim])
        y_ticks_4 = y_ticks_list(ax4_lim)
        ax4.yaxis.set_ticks(y_ticks_4)

        # draw legend for subplot 313
        ax4.legend(([sp[i][0] for i in range(len(sp))] + [lp[i][0]
            for i in range(len(lp))][::-1] + [socp[0][0]]), (legend_h_DH))

    else:
        lp = list(range(1))
          # DH Heat Load
        lp[0] = ax3.plot(in_data[:, 0] + 0.5, in_data[:, t],
                '-', linewidth=2, color=list_demand_h_DH[0][1])
        # sum for limits
        sum_dh = in_data[:, t]

        # draw legend for subplot 313
        ax3.legend(([sp[i][0] for i in range(len(sp))] + [lp[i][0]
            for i in range(len(lp))][::-1]), (legend_h_DH))

    # Limits and y-axis ticks
    ax3_lim = ceil(1.1 * max(sum_dh) / 10) * 10
    ax3.set_ylim([0, ax3_lim])
    ax3.set_xlim([data[0, 0], data[-1, 0]])
    y_ticks_3 = y_ticks_list(ax3_lim)
    ax3.yaxis.set_ticks(y_ticks_3)

    # save
    fig1.savefig(os.path.join(os.path.expanduser("~"),
        output_dir + '/' + stackplot_name + '.png'))
    if show:
        plt.show(fig1)
    return


def pie(data, colnames, cols_p, cols_h, cols_h_DH, list_p, list_h,
    list_h_DH, output_dir, pie_p_name, pie_h_name, show, p_set):

    ############################### pie chart ###############################

    sumdata = ((data.sum(axis=0))) / 1000
    sumall_p = sumdata[cols_p].sum()
    cols_h_total = np.hstack([cols_h, cols_h_DH])
    sumall_h = sumdata[cols_h_total].sum()

        ######################### Power ############################

    pielabel = []  # label of piechart
    piecolor = []  # color of piechart
    legend_dict = plot_lists.legend_dictionary()  # dictionary for legend
    nc_p = []
    for j in list_p:
        if j[2] == 'provide':
            tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
            if sumdata[tmp[0]] > 0:
                nc_p.append(tmp[0])  # number of column (nc)
                piecolor.append(j[1])
                pielabel.append(legend_dict[j[0]])

    pielabel_values = []
    for i in range(len(pielabel)):
        pielabel_values.append(pielabel[i] + ' - %.0f MWh (%.1f %%)' %
            (sumdata[nc_p][i], sumdata[nc_p][i] / sumall_p * 100))

    # The slices will be ordered and plotted counter-clockwise.
    labels = pielabel_values[:]  # [i for i in pielabel]
    sizes = (sumdata[nc_p])
    colors = piecolor

    fig2 = plt.figure(figsize=(23.0, 19.0))
    p1 = fig2.add_subplot(1, 1, 1)
    patches, texts = p1.pie(sizes, colors=colors, startangle=-160)
    plt.legend(patches, labels, loc="best")

    #title
    title = "Gesamtproduktion %d GWh" % sumall_p
    p1.text(0.0, 1.13, title, horizontalalignment='center', fontsize=20)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    p1.axis('equal')
    fig2.savefig(os.path.join(os.path.expanduser("~"),
        output_dir + '/' + pie_p_name + '.png'))
    if show:
        plt.show(fig2)

        ########################## Heat ############################

    pielabel = []  # label of piechart
    piecolor = []  # color of piechart
    nc_p = []
    # modify list_h for electric heating
    list_heat = list_h + list_h_DH
    list_heat = plot_lists.list_h_pie_plot(list_heat, p_set['output_table'])
    for j in list_heat:
        if j[2] == 'provide':
            tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
            if sumdata[tmp[0]] > 0:
                nc_p.append(tmp[0])  # number of column (nc)
                piecolor.append(j[1])
                pielabel.append(legend_dict[j[0]])

    pielabel_values = []
    for i in range(len(pielabel)):
        pielabel_values.append(pielabel[i] + ' - %.0f MWh (%.1f %%)' %
            (sumdata[nc_p][i], sumdata[nc_p][i] / sumall_h * 100))

    # The slices will be ordered and plotted counter-clockwise.
    labels = pielabel_values[:]  # [i for i in pielabel]
    sizes = (sumdata[nc_p])
    colors = piecolor

    fig3 = plt.figure(figsize=(23.0, 19.0))
    p2 = fig3.add_subplot(1, 1, 1)
    patches, texts = p2.pie(sizes, colors=colors, startangle=-160)
    plt.legend(patches, labels, loc="best")

    #title
    title = "Gesamtproduktion %d GWh" % sumall_h
    p2.text(0.0, 1.13, title, horizontalalignment='center', fontsize=20)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    p2.axis('equal')
    fig3.savefig(os.path.join(os.path.expanduser("~"),
        output_dir + '/' + pie_h_name + '.png'))
    if show:
        plt.show(fig3)

    return sumall_p


def pie_dep_var(data, colnames, cols_p, cols_h, cols_h_DH, list_p, list_h,
    list_h_DH, output_dir, pie_p_name, pie_h_name, show, p_set):

    sumdata = ((data.sum(axis=0))) / 1000
    sumall_p = sumdata[cols_p].sum()
    cols_h_total = np.hstack([cols_h, cols_h_DH])
    sumall_h = sumdata[cols_h_total].sum()

        ######################### Power ############################

    pielabel = []  # label of piechart
    piecolor = []  # color of piechart

    nc_p = []
    for j in list_p:
        if j[2] == 'provide':
            tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
            if sumdata[tmp[0]] > 0:
                nc_p.append(tmp[0])  # number of column (nc)
                piecolor.append(j[1])
                pielabel.append(j[0])

    # The slices will be ordered and plotted counter-clockwise.
    labels = pielabel[:]  # [i for i in pielabel]
    sizes = (sumdata[nc_p])
    colors = piecolor
    explode = tuple([0 for i in range(len(nc_p))])

    fig2 = plt.figure(figsize=(19.0, 19.0))
    p1 = fig2.add_subplot(1, 1, 1)
    p1.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=-160)

    #title
    title = "Gesamtproduktion %d GWh" % sumall_p
    p1.text(0.0, 1.13, title, horizontalalignment='center', fontsize=20)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    p1.axis('equal')
    fig2.savefig(os.path.join(os.path.expanduser("~"),
        output_dir + '/' + pie_p_name + '.png'))
    fig2.savefig(os.path.join(os.path.expanduser("~"),
        pie_p_name + '.png'))
    if show:
        plt.show(fig2)

        ########################## Heat ############################

    pielabel = []  # label of piechart
    piecolor = []  # color of piechart
    nc_p = []
    # modify list_h for electric heating
    list_h = plot_lists.list_h_pie_plot(list_h, p_set['output_table'])
    for j in (list_h + list_h_DH):
        if j[2] == 'provide':
            tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
            if sumdata[tmp[0]] > 0:
                nc_p.append(tmp[0])  # number of column (nc)
                piecolor.append(j[1])
                pielabel.append(j[0])

    # The slices will be ordered and plotted counter-clockwise.
    labels = pielabel[:]
    sizes = (sumdata[nc_p])
    colors = piecolor
    explode = tuple([0 for i in range(len(nc_p))])

    fig3 = plt.figure(figsize=(19.0, 19.0))
    p2 = fig3.add_subplot(1, 1, 1)
    p2.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=90)

    #title
    title = "Gesamtproduktion %d GWh" % sumall_h
    p2.text(0.0, 1.13, title, horizontalalignment='center', fontsize=20)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    p2.axis('equal')
    fig3.savefig(os.path.join(os.path.expanduser("~"),
        output_dir + '/' + pie_h_name + '.png'))
    fig3.savefig(os.path.join(os.path.expanduser("~"),
        pie_h_name + '.png'))
    if show:
        plt.show(fig3)

    return


def share_wind_pv(pv_pot, wind_pot, fee, demand,
    show=None, save=None, output_dir=None, plot_name='FEE_theo_real',
    y_label=None):

    # Get data
    data = np.zeros((2, 4))
    data[1, 0] = 1
    data[0, 1] = 100 * sum(pv_pot) / demand  # theo. share PV
    data[0, 2] = 100 * sum(wind_pot) / demand  # theo. share Wind

    data[1, 3] = 100 * sum(fee) / demand  # actual share FEE

    # Dictionary for color and label definition
    prop_dict = {
        'column': {1: 'PV',
            2: 'Wind',
            3: 'FEE'},
        'color': {1: 'yellow',
            2: 'lightskyblue',
            3: 'orange'}
                }

    # Initialize figure and axes
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(1, 1, 1)

    # Font
    plt.rcParams.update({'font.size': 34})
    plt.rc('legend', **{'fontsize': 30})
    #plt.rc('font', **{'family': p_set['font']})

    # Plot
    sp = list(range(data.shape[1] - 1))
    for i in range(data.shape[1] - 1):
        sp[i] = ax.bar(data[:, 0], data[:, (i + 1)],
                    width=1,
                    linewidth=0,
                    color=prop_dict['color'][i + 1],
                    bottom=data[:, 1:(i + 1)].sum(axis=1))

    # x-axis label
    ax.set_xticks([0.5, 1.5])
    xtickNames = ax.set_xticklabels(['theo.', 'real'])
    plt.setp(xtickNames, rotation=45)
    # y-axis label
    if y_label:
        ax.set_ylabel(y_label)

    # Legend
    ax.legend(tuple([sp[i][0] for i in range(len(sp), )]),
        (prop_dict['column'][i] for i in prop_dict['column']))

    # Limits
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(0, (ceil(sum(data[0, :])) * 1.1 / 10) * 10)

    # Anzeigen
    if show:
        plt.show(fig)

    # Speichern
    if save:
        fig.savefig(os.path.join(os.path.expanduser("~"),
        output_dir + '/' + plot_name + '.png'))

    return


def surplus_fee(surplus, output_dir, show=None, save=None):

    fig = plt.figure(figsize=([22.0, 14.0]))
    ax1 = fig.add_subplot(1, 1, 1)

    # Plot
    ax1.plot(surplus, color='orange')

    # Achsenbeschriftung
    ax1.set_xlabel('Stunde des Jahres')
    ax1.set_ylabel(u'Überschussleistung [MW]')

    # Limits
    from math import ceil
    ax1.set_ylim(0, (ceil(max(surplus)) * 1.1 / 10) * 10)

    # Title
    title = u"Gesamtüberschüsse %d MWh/a" % sum(surplus)
    plt.title(title)

    # Schriftgröße
    plt.rcParams.update({'font.size': 23})
    plt.rc('legend', **{'fontsize': 18})

    # Anzeigen
    if show:
        plt.show(fig)

    # Speichern
    if save:
        fig.savefig(os.path.join(os.path.expanduser("~"),
            output_dir + '/surplus_fee.png'))

    return


def command(input_data, p_set, cop_dict, schema, output_dir,
    results_table, load_table, week_summer, week_winter,
    pie_p_name, pie_h_name, stackplot_name_winter, stackplot_name_summer,
    show, txt_filename, sum_var_co2, total_emissions,
    sum_var_costs, total_costs,
    storage_losses, pv_pot, wind_pot, total_power_demand,
    end_energy_demand, max_el_demand_hp, components_dict, full_load_hours_dict):
    '''
    Plot for output.tex.
    '''
    # get stack data
    [data_summer, data_winter, in_data_summer, in_data_winter,
        colnames, colnames_in] = plot_data.get_stack(p_set)
    # prepare plots
    [cols_p, cols_h, cols_h_DH, cd_p, cd_h, cd_h_DH,
        list_p, list_h, list_h_DH,
        list_demand_p, list_demand_h, list_demand_h_DH,
        legend_p, legend_h, legend_h_DH,
        list_demand_p_legend, list_demand_h_legend, list_demand_h_DH_legend] = \
        plot_lists.get(colnames, data_winter)
    # stackplot winter
    stack(colnames, colnames_in, data_winter, in_data_winter, week_winter,
        cols_p, cols_h, cols_h_DH,
        cd_p, cd_h, cd_h_DH,
        list_demand_p, list_demand_h, list_demand_h_DH,
        legend_p, legend_h, legend_h_DH,
        list_demand_p_legend, list_demand_h_legend, list_demand_h_DH_legend,
        cop_dict,
        output_dir, stackplot_name_winter, 7, show)
    # stackplot summer
    stack(colnames, colnames_in, data_summer, in_data_summer, week_summer,
        cols_p, cols_h, cols_h_DH,
        cd_p, cd_h, cd_h_DH,
        list_demand_p, list_demand_h, list_demand_h_DH,
        legend_p, legend_h, legend_h_DH,
        list_demand_p_legend, list_demand_h_legend, list_demand_h_DH_legend,
        cop_dict,
        output_dir, stackplot_name_summer, 7, show)
    # get pie data
    data, colnames = plot_data.get_pie(p_set)
    # pie plot
    pie(data, colnames, cols_p, cols_h, cols_h_DH,
        list_p, list_h, list_h_DH,
        output_dir, pie_p_name, pie_h_name, show, p_set)
    # fee used
    fee_tmp = ([i for i, x in enumerate(colnames) if x == 'FEE'])
    fee = data[:, fee_tmp[0]]
    # txt-file
    output.text_file(p_set, data, colnames, list_p, list_h, list_h_DH,
        total_power_demand, end_energy_demand, pv_pot, wind_pot, sum(fee),
        output_dir, txt_filename, sum_var_co2, total_emissions,
        sum_var_costs, total_costs,
        storage_losses, cop_dict, max_el_demand_hp, components_dict,
        full_load_hours_dict)
    # bar plot share wind and pv of total power demand
    share_wind_pv(pv_pot, wind_pot, fee, total_power_demand,
        show=p_set['show'], save=p_set['save'], output_dir=p_set['output_dir'],
        plot_name='share_FEE_power_demand', y_label='Anteil am Stromverbrauch')
    # bar plot share wind and pv of end energy demand
    share_wind_pv(pv_pot, wind_pot, fee, end_energy_demand,
        show=p_set['show'], save=p_set['save'], output_dir=p_set['output_dir'],
        plot_name='share_FEE_end_energy_demand',
        y_label='Anteil am Endenergieverbrauch')
    #surplus plot
    surplus_fee(pv_pot + wind_pot - fee, output_dir=p_set['output_dir'],
        show=p_set['show'], save=p_set['save'])
    return


#import parameter_set_ist
#import database as db
#import heat_pump_calc

#p_set = parameter_set_ist.get_p_set()
#input_data = db.get_input_data(77)

## write dictionary with COPs
#cop_dict = {}
#func_dict = {'HP Mono Air Heating': heat_pump_calc.calc_cop_hp_air_heating,
             #'HP Mono Air WW': heat_pump_calc.calc_cop_hp_air_ww,
             #'HP Mono Brine Heating': heat_pump_calc.calc_cop_hp_brine_heating,
             #'HP Mono Brine WW': heat_pump_calc.calc_cop_hp_brine_ww}
#for i in func_dict.keys():
    #cop_dict[i] = func_dict[i](input_data, p_set)

#pv_pot = db.retrieve_from_db_table(
    #'wittenberg', p_set['load_pot_table'], 'pv_pot', order='yes')

#wind_pot = db.retrieve_from_db_table(
    #'wittenberg', p_set['load_pot_table'], 'wind_pot', order='yes')

#command(input_data, p_set, cop_dict, schema, output_dir,
    #results_table, load_table, week_summer, week_winter,
    #pie_p_name, pie_h_name, stackplot_name_winter, stackplot_name_summer,
    #show, txt_filename, sum_dep_var, dep_var_total,
    #storage_losses, pv_pot, wind_pot, total_power_demand,
    #end_energy_demand)

#command(input_data, p_set, cop_dict, 'wittenberg', p_set['output_dir'],
        #p_set['output_table'], p_set['load_pot_table'],
        #p_set['week_summer'], p_set['week_winter'],
        #p_set['pie_p_name'], p_set['pie_h_name'],
        #p_set['stackplot_name_winter'], p_set['stackplot_name_summer'],
        #p_set['show'], 'test', 200, 200,
        #200, pv_pot, wind_pot, 200, 200)