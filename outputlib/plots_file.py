#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

import dblib as db
import numpy as np
import matplotlib.pyplot as plt
import re


def get_name_and_color_single(basic_dc, comp):
    '''
    Fetch name and color from the database for a single component.
    '''
    name_col = 'name_eng'
    db_tmp = db.fetch_columns(basic_dc, 'a_rli_corporate',
        'technologie_definition', columns=['farbcode_hex', name_col],
        where_column='char4_code', where_condition=comp)
    if not db_tmp['farbcode_hex']:
        db_tmp.setdefault('farbcode_hex', [])
        db_tmp['farbcode_hex'] = ['#ff00c8']
    if not db_tmp[name_col]:
        db_tmp.setdefault(name_col, [])
        db_tmp[name_col] = ['no name']
    return db_tmp['farbcode_hex'], db_tmp[name_col][0]


def update_dict_annual_sums(result_dc, tables):
    '''calculate annual sums of hourly energy values and update results_dc
    with these values'''
    regions = result_dc[tables[0]].keys()
    for tab in tables:
        result_dc[tab].update({'all_reg_sum': {}})
        result_dc[tab].update({'all_reg_ts': {}})
        for c in result_dc[tab][result_dc[tab].keys()[0]].keys():
            tmp_sum = 0
            for r in regions:
                tmp_sum += result_dc[tab][r][c]
            result_dc[tab]['all_reg_sum'][c] = np.sum(tmp_sum)
            result_dc[tab]['all_reg_ts'][c] = tmp_sum
    return result_dc


def reduce_legend(handles, labels, ind, result_dc2):
    '''Reduces amount of legend elements for plot of several scenarios'''
    tmp_handles = handles[:len(handles) / len(ind)]
    tmp_labels = labels[:len(labels) / len(ind)]
    hand_ind = range(0, len(tmp_handles), 2)
    new_handles = list()
    new_labels = list()
    if result_dc2 is not None:
        for j in hand_ind:
            new_handles.append(tmp_handles[j])
            new_labels.append(tmp_labels[j])
    else:
        new_handles = tmp_handles
        new_labels = tmp_labels
    return new_handles, new_labels


def plot_system_bar(result_dc, scenario, basic_dc, title=None, xlabel=None,
    ylabel=None, energy=False, plottype=None, suffix='', result_dc2=None,
    plot_dir='plots/', fileFormat='pdf', showplot=False, printplot=True):
    if plottype is None:
        first_key = 'power_gen'
    else:
        first_key = plottype

    fig, ax = plt.subplots()

    #if 'all_reg_sum' in result_dc[first_key].keys():
    if plottype in result_dc.keys():
        ind = np.arange(len(result_dc[first_key]['all_reg_sum'].keys()))
        ax_mult, ax_unit = ax_units(get_max_value(result_dc[first_key]
            ['all_reg_sum']))
        years_str = result_dc['info']['year']
        if energy is True:
            ax_unit = ax_unit + 'h'
        for i, c in zip(ind, result_dc[first_key]['all_reg_sum'].keys()):
            [color, name] = get_name_and_color_single(basic_dc, c)
            pobj = ax.bar(i, result_dc[first_key]['all_reg_sum'][c] * ax_mult,
            label=name,
            width=0.98,
            color=color)
            if result_dc2:
                pobj2 = ax.bar(i, result_dc2['all_reg_sum'][c] * ax_mult,
                    label=name,
                    width=0.98,
                    color=color,
                    bottom=result_dc[first_key]['all_reg_sum'][c] * ax_mult,
                    alpha=0.7)
            if xlabel is not None:
                plt.xlabel(xlabel)
            if ylabel is not None:
                plt.ylabel(ylabel + ' in ' + ax_unit)
            if title is not None:
                plt.title(title)
            plt.legend()
            plt.tight_layout()
    else:
        # grouped bar plot
        b_width = 0.16
        ind = np.arange(len(result_dc.keys()))
        years_str = ''
        xticks = list()
        for i, kk in zip(ind, sorted(result_dc.keys())):
            ax_mult, ax_unit = ax_units(get_max_value(result_dc[kk][first_key]
                ['all_reg_sum']))
            year = result_dc[kk]['info']['year']
            years_str += '_' + str(year)
            xticks.append(str(year))
            if energy is True:
                ax_unit = ax_unit + 'h'
            b_width_step = 0
            for c in result_dc[kk][first_key]['all_reg_sum'].keys():
                [color, name] = get_name_and_color_single(basic_dc, c)
                ax.bar(i + b_width_step, result_dc[kk][first_key]
                    ['all_reg_sum'][c] * ax_mult,
                    label=name,
                    width=b_width,
                    color=color)
                if result_dc2:
                    ax.bar(i + b_width_step, result_dc2[kk][first_key]
                        ['all_reg_sum'][c] * ax_mult,
                    label=name,
                    width=b_width,
                    color=color,
                    bottom=result_dc[kk][first_key]['all_reg_sum'][c] * ax_mult,
                    alpha=0.7)
                if xlabel is not None:
                    plt.xlabel(xlabel)
                if ylabel is not None:
                    plt.ylabel(ylabel + ' in ' + ax_unit)
                if title is not None:
                    plt.title(title)
                handles, labels = ax.get_legend_handles_labels()
                b_width_step += b_width
    new_handles, new_labels = reduce_legend(handles, labels, ind, result_dc2)
    plt.xticks(ind + 0.4, xticks)
    leg = plt.legend(new_handles, new_labels, loc='best')
    leg.get_frame().set_alpha(0.5)
    plt.tight_layout()
    save_str = (plot_dir + '01_' + plottype + '_sys_' +
        str(years_str) + suffix + '.' + fileFormat)
    if showplot is True:
        plt.show()
    if printplot is True:
        plt.savefig(save_str, dpi=150, format=fileFormat)


def ax_units(val):
    if val <= 1000:
        ax_mult = 1
        ax_unit = 'kW'
    elif val > 1000 and val <= 1e6:
        ax_mult = 1e-3
        ax_unit = 'MW'
    elif val > 1e6 and val <= 1e10:
        ax_mult = 1e-6
        ax_unit = 'GW'
    elif val > 1e10:
        ax_mult = 1e-9
        ax_unit = 'TW'
    else:
        ax_mult = 1
        ax_unit = 'unknown'
    return ax_mult, ax_unit


def get_max_value(dict):
    '''returns maximum value of first level keys of a given dict'''
    val_list = []
    for c in dict.keys():
        val_list.append(dict[c])
    return max(val_list)


def get_previous_results(basic_dc, presetting_set, components):
    dc = {}
    for c in components:
        db_str = '''select sum(presetted_summed_power) from
            pahesmf_dat.presetting where presetting_set = '{0}'
            and component = '{1}'
            and eoo_year >= {2};'''.format(presetting_set, c, int(
                re.findall('\d{4}', presetting_set)[0]))
        dc[c] = db.execute_read_db(basic_dc, db_str)[0][0]
        if dc[c] is None:
            dc[c] = 0
    return dc


def update_dict_indicator_values(result_dc):
    '''Returns a dict containing indicator values of scenario results'''
    indicator_dc = {}

    # renewables share
    re_power_plants = ['rpvo', 'rwin']
    tmp_val = 0
    for c in re_power_plants:
        tmp_val += result_dc['power_gen']['all_reg_sum'][c]
    indicator_dc['ren_share'] = {'all_reg_sum': tmp_val /
        result_dc[ 'demand_elec_total_all']}

    # resulting cost
    # excess energy
    indicator_dc['excess_rel'] = {'all_reg_sum': result_dc['excess']
        ['all_reg_sum']['eexc'] / result_dc[ 'demand_elec_total_all']}

    # energy supply from storages
    return indicator_dc


def example_result_dc():
    '''Example (parts of) results dict for testing'''
    result_dc = {'power_inst': {'all_reg_sum': {'rpvo': 600293430.87959242,
                                'rwin': 1011169901.2536359,
                                'tccg': 22536930.099600002,
                                'tcpp': 0.0,
                                'tocg': 161082439.3105},
                'all_reg_ts': {'rpvo': np.array([6.00293431e+08]),
                               'rwin': np.array([1.01116990e+09]),
                               'tccg': np.array([22536930.0996]),
                               'tcpp': np.array([0.]),
                               'tocg': np.array([1.61082439e+08])},
                'deu': {'rpvo': np.array([0.37136]),
                        'rwin': np.array([0.196399]),
                        'tccg': np.array([1634080.]),
                        'tcpp': np.array([0.]),
                        'tocg': np.array([8768480.])},
                'dnk': {'rpvo': np.array([11.9752]),
                        'rwin': np.array([4.18688000e+08]),
                        'tccg': np.array([5578290.]),
                        'tcpp': np.array([0.]),
                        'tocg': np.array([28666100.])},
                'fin': {'rpvo': np.array([39061200.]),
                        'rwin': np.array([0.0628476]),
                        'tccg': np.array([12.3696]),
                        'tcpp': np.array([0.]),
                        'tocg': np.array([7950650.])},
                'nor': {'rpvo': np.array([0.141775]),
                        'rwin': np.array([9705360.]),
                        'tccg': np.array([291017.]),
                        'tcpp': np.array([0.]),
                        'tocg': np.array([2542520.])},
                'pol': {'rpvo': np.array([39147100.]),
                        'rwin': np.array([31106100.]),
                        'tccg': np.array([831160.]),
                        'tcpp': np.array([0.]),
                        'tocg': np.array([6627350.])},
                'swe': {'rpvo': np.array([15980300.]),
                        'rwin': np.array([0.0339412]),
                        'tccg': np.array([365329.]),
                        'tcpp': np.array([0.]),
                        'tocg': np.array([2761250.])},
                'xalp': {'rpvo': np.array([3.99042]),
                         'rwin': np.array([0.014443]),
                         'tccg': np.array([394624.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([5815750.])},
                'xbal': {'rpvo': np.array([6875210.]),
                         'rwin': np.array([9484540.]),
                         'tccg': np.array([254782.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([740265.])},
                'xbnl': {'rpvo': np.array([0.615825]),
                         'rwin': np.array([1.11754000e+08]),
                         'tccg': np.array([1224810.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([6597210.])},
                'xczs': {'rpvo': np.array([0.67376]),
                         'rwin': np.array([0.0883449]),
                         'tccg': np.array([506.73]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([5827680.])},
                'xfra': {'rpvo': np.array([3.05934]),
                         'rwin': np.array([78825900.]),
                         'tccg': np.array([523259.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([11703700.])},
                'xfwy': {'rpvo': np.array([20239500.]),
                         'rwin': np.array([0.0163646]),
                         'tccg': np.array([572481.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([3183690.])},
                'xgbr': {'rpvo': np.array([0.0519123]),
                         'rwin': np.array([3.51606000e+08]),
                         'tccg': np.array([3776760.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([19215300.])},
                'xgma': {'rpvo': np.array([81932200.]),
                         'rwin': np.array([0.242581]),
                         'tccg': np.array([1476830.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([84.3105])},
                'xhur': {'rpvo': np.array([44049400.]),
                         'rwin': np.array([0.0333485]),
                         'tccg': np.array([280779.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([8144640.])},
                'xibe': {'rpvo': np.array([1.67659000e+08]),
                         'rwin': np.array([0.476438]),
                         'tccg': np.array([2635210.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([15233900.])},
                'xita': {'rpvo': np.array([1.75387000e+08]),
                         'rwin': np.array([0.0610841]),
                         'tccg': np.array([2523470.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([24771200.])},
                'xskb': {'rpvo': np.array([9962500.]),
                         'rwin': np.array([0.0278439]),
                         'tccg': np.array([173530.]),
                         'tcpp': np.array([0.]),
                         'tocg': np.array([2532670.])}}}
    return result_dc


def example_result_dc_power_gen():
    '''Example (parts of) results dict for testing'''
    result_dc = (
        {'entsoe_eu_18_2040':
            {'power_gen':
                {'all_reg_sum':
                    {'rpvo': 311893620407.75671,
                    'rwin': 2681842012022.9512,
                    'tccg': 103838062383.29791,
                    'tcpp': 630068978530.50562,
                    'tocg': 23849963358.706039}},
            'info':
                {'year': 2040,
                'scenario': 'entsoe_eu_18_2040'
                }
            },
        'entsoe_eu_18_2050':
            {'power_gen':
                {'all_reg_sum':
                    {'rpvo': 763277393699.50134,
                    'rwin': 3105711378134.7798,
                    'tccg': 74530034902.827545,
                    'tcpp': 0.0,
                    'tocg': 60843415240.383011}},
            'info':
                {'year': 2050,
                'scenario': 'entsoe_eu_18_2050'
                }
            }
        })
    return result_dc