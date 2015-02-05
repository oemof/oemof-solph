#!/usr/bin/python
# -*- coding: utf-8

import os
import plot_lists
import plot_data
import numpy as np
import matplotlib.pyplot as plt


def var_pie(cols_p, cols_h, cols_h_DH, list_p, list_h,
    list_h_DH, output_dir, pie_p_name, pie_h_name, show, p_set, input_data,
    components_dict):

    ################## total electricity and heat produced ##################

    # retrieve produced energies of each component from the output table
    data, colnames = plot_data.get_pie(p_set)
    # sum of energy produced by each component
    sumdata = ((data.sum(axis=0))) / 1000
    # total electricity produced
    sumall_p = sumdata[cols_p].sum()
    # total heat produced
    cols_h_total = np.hstack([cols_h, cols_h_DH])
    sumall_h = sumdata[cols_h_total].sum()
    # dict with variable and fixed costs/emissions
    if p_set['optimize_for'] == 'Costs':
        var_dict = p_set['var_costs_dict']
        fixed_dict = p_set['fixed_costs_dict']
    else:
        var_dict = p_set['var_co2_dict']
        fixed_dict = p_set['fixed_co2_dict']
    # splitting of fixed costs/emissions of cog units into heat and power
    # share
    for cog in (components_dict['Cog Sources'] +
    components_dict['dec Cog units']):
        print cog
        fixed_dict[cog + ' Power'] = fixed_dict[cog] / 2
        fixed_dict[cog + ' Heat'] = fixed_dict[cog] / 2

        ######################### Power ############################

    pielabel = []  # label of piechart
    pielabel_orig = []  # name of component as used in the model
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
                pielabel_orig.append(j[0])

    print pielabel_orig

    # The slices will be ordered and plotted counter-clockwise.
    labels = pielabel[:]  # [i for i in pielabel]

    #sizes = sumdata[nc_p]
    sizes = np.zeros((len(nc_p), ))
    for i in range(len(nc_p)):
        if pielabel_orig[i] == 'FEE':
            sizes[i, ] = (sumdata[nc_p[i]] *
                var_dict['PV'] +
                fixed_dict['PV'] + fixed_dict['Wind'])
        #if pielabel_orig[i] in [components_dict['Cog Sources'],
        #components_dict['Cog Sources']]:
            #sizes[i, ] = (sumdata[nc_p[i]] /
                #input_data['eta ' + pielabel_orig[i]] *
                #var_dict[pielabel_orig[i]] + fixed_dict[pielabel_orig[i]])
        else:
            sizes[i, ] = (sumdata[nc_p[i]] /
                input_data['eta ' + pielabel_orig[i]] *
                var_dict[pielabel_orig[i]] + fixed_dict[pielabel_orig[i]])
    print sizes

    colors = piecolor
    explode = tuple([0 for i in range(len(nc_p))])

    fig2 = plt.figure(figsize=(23.0, 19.0))
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
                pielabel.append(legend_dict[j[0]])

    # The slices will be ordered and plotted counter-clockwise.
    labels = pielabel[:]
    sizes = (sumdata[nc_p])
    colors = piecolor
    explode = tuple([0 for i in range(len(nc_p))])

    fig3 = plt.figure(figsize=(23.0, 19.0))
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
    if show:
        plt.show(fig3)

    return sumall_p


def command(input_data, p_set, cop_dict, schema, output_dir,
    results_table, load_table, week_summer, week_winter,
    pie_p_name, pie_h_name, stackplot_name_winter, stackplot_name_summer,
    show, filename, sum_var_co2_emissions, total_co2_emissions,
    storage_losses, bar_plot_name, pv_pot, wind_pot, components_dict):
    '''
    Plot for output.tex.
    '''
    # get data
    [data_summer, data_winter, in_data_summer, in_data_winter,
        colnames, colnames_in] = plot_data.get_stack(p_set)
    # prepare plots
    [cols_p, cols_h, cols_h_DH, cd_p, cd_h, cd_h_DH,
        list_p, list_h, list_h_DH,
        list_demand_p, list_demand_h, list_demand_h_DH,
        legend_p, legend_h, legend_h_DH,
        list_demand_p_legend, list_demand_h_legend, list_demand_h_DH_legend] = \
        plot_lists.get(colnames, data_winter)
    # pie plot
    var_pie(cols_p, cols_h, cols_h_DH,
        list_p, list_h, list_h_DH,
        output_dir, pie_p_name, pie_h_name, show, p_set, input_data,
        components_dict)
    return


import parameter_set
import database as db
import heat_pump_calc
import costs
import co2_emissions

p_set = parameter_set.get_p_set()
input_data['cap Gas Cog unit Boiler'] = 82
input_data['cap HP Mono Air Heating el Heating'] = 16.3
input_data['cap HP Mono Air WW el Heating'] = 2.6

# write dictionary with COPs
cop_dict = {}
func_dict = {'HP Mono Air Heating': heat_pump_calc.calc_cop_hp_air_heating,
             'HP Mono Air WW': heat_pump_calc.calc_cop_hp_air_ww}
             #'HP Mono Brine Heating': heat_pump_calc.calc_cop_hp_brine_heating,
             #'HP Mono Brine WW': heat_pump_calc.calc_cop_hp_brine_ww}
for i in func_dict.keys():
    cop_dict[i] = func_dict[i](input_data, p_set)

# components dict
components_dict = {'Power Sources': ['PV', 'Wind', 'Gas Power',
        'Biomass Power'],
    'Heat Sources': ['DH Gas Heat', 'DH Biogas Heat'],
    'Cog Sources': ['DH Biogas Cog unit', 'DH Gas Cog unit', 'DH Biomass Cog'],
    'Storages': ['Storage Battery', 'Gas Cog unit Storage Thermal',
        'Biogas Cog unit Storage Thermal'],
    'Heating Systems': ['Gas Heat', 'Coal Heat', 'Oil Heat'],
    'Heat Pump Mono': ['HP Mono Air Heating', 'HP Mono Air WW'],
    'dec Cog units': ['Gas Cog unit', 'Biogas Cog unit', 'Gas Cog unit Boiler'],
    'el Heating': ["HP Mono Air Heating el Heating",
        "HP Mono Air WW el Heating", 'Gas Cog unit el Heating']}

# maximum demands
p_set['max_heat_gas'] = 116
p_set['max_heat_oil'] = 60
p_set['max_heat_coal'] = 60
p_set['max_heat_dh'] = 30

# variable and fixed costs
p_set['var_costs_dict'] = costs.variable(input_data)
p_set['fixed_costs_dict'] = costs.fixed(
        input_data, None, 300,
        None, 300, 300,
        0, 140, components_dict, 22.5,
        4, 0, 0, p_set)

# variable and fixed co2-emissions
p_set['var_co2_dict'] = co2_emissions.variable(input_data)
p_set['fixed_co2_dict'] = co2_emissions.fixed(
        input_data, None, 300,
        300, 99, 300,
        0, 140, components_dict, 22.5,
        4, 0, 0, p_set)

command(input_data, p_set, cop_dict, 'wittenberg', p_set['output_dir'],
        p_set['output_table'], p_set['load_pot_table'],
        p_set['week_summer'], p_set['week_winter'],
        p_set['pie_p_name'], p_set['pie_h_name'],
        p_set['stackplot_name_winter'], p_set['stackplot_name_summer'],
        p_set['show'], 'test', 200, 200,
        200, p_set['bar_plot_name'], 1, 1, components_dict)