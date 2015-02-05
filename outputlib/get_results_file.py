#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

import dblib as db
import logging


def read_results_from_db(var, basic_dc=None, parameter_dc=None):
    '''
    Reads the result data sets from the database as np-arrays.

    Returns a result dictionary, where the keys are the names of the result
    tables.

    by Uwe Krien (uwe.krien@rl-institut.de)
    '''
    if basic_dc is None:
        logging.info('Reading basic_dc.')
        basic_dc = read_basic_dc()
    if parameter_dc is None:
        logging.info('Reading parameter_dc.')
        parameter_dc = parameter_from_db(basic_dc, var)

    res_data_dc = res.read_results(basic_dc, parameter_dc)

    return res_data_dc


def read_plot_results_from_db(scen_id, basic_dc, parameter_dc):
    '''
    Reads the result data sets from the database as np-arrays.

    Returns a result dictionary suitable for e.g. stack plots

    by Uwe Krien (uwe.krien@rl-institut.de)
    '''
    res_data_dc = res.read_plot_results(scen_id, parameter_dc, basic_dc)
    return res_data_dc


def results(scen_id, *args):
    '''This function calls subfunction in order to show results'''
    #get basic db dict (db connection setup)
    basic_dc = rp.read_basic_dc(overwrite=True, failsafe=True)

    # get parameter dict
    parameter_dc = rp.parameter_from_db(basic_dc, scen_id)

    # read raw results from database
    res_data = read_results(scen_id, parameter_dc, basic_dc)

    # print some annual sums...
    if 'balance_check' in list(args)[0]:
        check_balance(res_data, parameter_dc)


def read_results(scen_id, parameter_dc, basic_dc):
    'Reads results.'
    gen_list = (parameter_dc['energy_system']['energy_system_transformer4elec'] +
            parameter_dc['energy_system']['energy_system_re'])

    res_data = {}
    res_data['generation'] = {}
    res_data['demand'] = {}
    res_data['charge'] = {}
    res_data['discharge'] = {}
    res_data['soc'] = {}
    res_data['trm_power'] = {}
    res_data['splitted_gas_flow'] = {}
    res_data = read_results_to_dict(basic_dc, res_data, parameter_dc)
    return res_data



def read_results_to_dict(basic_dc, res_data, parameter_dc):

    results_to_dict_generation(basic_dc, res_data, parameter_dc)
    results_to_dict_demand(basic_dc, res_data, parameter_dc)
    results_to_dict_charge(basic_dc, res_data, parameter_dc)
    results_to_dict_soc(basic_dc, res_data, parameter_dc)
    results_to_dict_discharge(basic_dc, res_data, parameter_dc)
    results_to_dict_trm_power(basic_dc, res_data, parameter_dc)

    if (parameter_dc['energy_system']['energy_system_transformer4gas'] or
        parameter_dc['input']['input_general']['re_share']):
        results_to_dict_splitted_gas_flow(basic_dc, res_data, parameter_dc)

    return res_data


def check_balance(res_data, parameter_dc):
    ptg = parameter_dc['energy_system']['energy_system_transformer4gas']
    ren_share = parameter_dc['input']['input_general']['re_share']
    gas_pp = ([x for x in (parameter_dc['energy_system']
        ['energy_system_transformer4elec']) if x in ['tocg', 'tccg']])
    generation = sumup_dict(res_data['generation'])
    renewables = (sumup_dict_one_level(res_data['generation']['rwin']) +
        sumup_dict_one_level(res_data['generation']['rpvo']))
    other_comp_list = ['twpp', 'tnuc']
    other = 0
    for c in ([x for x in parameter_dc['energy_system']
            ['energy_system_transformer4elec'] if x in other_comp_list]):
        print(c)
        other = other + sumup_dict_one_level(res_data['generation'][c])
    print(str(other))
    if ptg or ren_share:
        # calculate total power generation of gas power plants
        gas_pp_generation_total = 0
        gas_pp_generation_fos = 0
        for c in gas_pp:
            gas_pp_generation_total = (gas_pp_generation_total +
                sumup_dict_one_level(res_data['generation'][c]))
            gas_pp_generation_fos = (gas_pp_generation_fos +
                sumup_dict_one_level(res_data['splitted_gas_flow'][c]) *
                parameter_dc['parameter']['parameter_transformer4elec']
                    [parameter_dc['energy_system']['energy_system_regions'][0]]
                    [c]['efficiency'])
        fossils = (generation - renewables - other - gas_pp_generation_total +
            gas_pp_generation_fos)
    else:
        fossils = generation - renewables - other

    demand = sumup_dict(res_data['demand'])
    trm_power = sumup_dict_one_level(res_data['trm_power'])
    if parameter_dc['energy_system']['energy_system_transformer4gas']:
        ptg_ann_input = sumup_dict_one_level(res_data['demand']['tptg'])

    discharge = {}
    for c in res_data['discharge'].keys():
        discharge[c] = sumup_dict_one_level(res_data['discharge'][c])
    charge = {}
    for c in res_data['charge'].keys():
        charge[c] = sumup_dict_one_level(res_data['charge'][c])
    losses = {}
    losses_sum = 0
    for c in res_data['discharge'].keys():
        losses[c] =  charge[c] - discharge[c]
        losses_sum = losses_sum + losses[c]

    #Generation
    balance = generation -  demand - losses_sum - trm_power
    print('---------------------------------------------------')
    print('Generation: ' +str(generation))
    print('\t Renewables: ' + str(renewables) + '\t ren. share: ' +
        str(renewables / sumup_dict_one_level(res_data['demand']['demand_elec'])))
    print('\t Fossil: ' + str(fossils) + '\t fossil share: ' + str(fossils /
        sumup_dict_one_level(res_data['demand']['demand_elec'])))
    print('Generation of each technology:')
    print('\t Generation in kWh \t\t share')
    for c in res_data['generation'].keys():
        print('\t' + c + ': ' + str(sumup_dict_one_level(
            res_data['generation'][c])) + '\t' + str(sumup_dict_one_level(
            res_data['generation'][c]) / sumup_dict_one_level(res_data['demand']['demand_elec'])))
    #operating hours
    print('Operating hours of each technology:')
    print('\t Operating hours \t\t share of year')
    for c in res_data['generation'].keys():
        print('\t' + c + ': ' + str(set_operation(
            res_data['generation'][c])) + ' \t\t' + str(set_operation(
            res_data['generation'][c]) / 8760.0))
    #load changes
    print('Load changes of each technology:')
    print('\t Load Changes ')
    for c in res_data['generation'].keys():
        print('\t' + c + ': ' + str(set_load_changes(
            res_data['generation'][c]))) #+ '\t' + str(set_load_changes(
            #res_data['generation'][c]) / sum(load_changes)))

    #load change_power
    #sum load_change_power:
    sum_load_change_power=0
    for c in res_data['generation'].keys():
        sum_load_change_power += set_load_change_power(res_data['generation'][c])

    print('Load change power of each technology(Sum of power that changes from timestep t-1 to t):')
    print('\t Load change power[KWh \t\t share')
    for c in res_data['generation'].keys():
        print('\t' + c + ': ' + str(set_load_change_power(
            res_data['generation'][c])) + ' \t\t' + str(set_load_change_power(
            res_data['generation'][c]) / sum_load_change_power))

    print('Demand incl. excess and ptg: ' + str(demand))
    for d in res_data['demand'].keys():
        print('\t '+ d + ': ' + str(sumup_dict_one_level(res_data['demand'][d])))
    print('Transmission: ' + str(trm_power))
    if parameter_dc['energy_system']['energy_system_transformer4gas']:
        print('PtG elec. input power: ' + str(ptg_ann_input))

    for c in res_data['charge'].keys():
        print(c + ' charge: ' + str(charge[c]))
        print(c + ' discharge: ' + str(discharge[c]))
        print(c + ' losses: ' + str(losses[c]))

    print('Balance: ' + str(balance))

    print('---------------------------------------------------')


def sumup_dict_one_level(dc):
    ''
    sum0 = 0
    for key in dc.keys():
        sum0 = sum0 + sum(dc[key])
    return sum0


def sumup_dict(dc):
    ''
    sum0 = 0
    for c in dc.keys():
        sum1 = 0
        for r in dc[c].keys():
            sum1 = sum1 + sum(dc[c][r])
        sum0 = sum0 + sum1
    return sum0


def results_to_dict_demand(basic_dc, res_data, parameter_dc):
    ''
    res_data['demand'] = res_dict_fill(parameter_dc, basic_dc,
            ['excess'], 'power_gen', res_data['demand'])
    if 'tptg' in parameter_dc['energy_system']['energy_system_transformer4gas']:
        res_data['demand'] = res_dict_fill(parameter_dc, basic_dc,
            ['tptg'], 'ptg_power_in', res_data['demand'])
    res_data['demand'].update(read_demand_data(basic_dc, parameter_dc))
    del(res_data['demand']['demand_elec_total_all'])


def results_to_dict_generation(basic_dc, res_data, parameter_dc):
    ''
    res_data['generation'] = res_dict_fill(parameter_dc, basic_dc,
            parameter_dc['energy_system']['energy_system_transformer4elec'],
            'power_gen', res_data['generation'])
    res_data['generation'] = res_dict_fill(parameter_dc, basic_dc,
            parameter_dc['energy_system']['energy_system_re'],
            'power_gen', res_data['generation'])


def results_to_dict_charge(basic_dc, res_data, parameter_dc):
    ''
    res_data['charge'] = res_dict_fill(parameter_dc, basic_dc,
            parameter_dc['energy_system']['energy_system_storages'],
            'storage_charge', res_data['charge'])
    if parameter_dc['energy_system']['energy_system_storages4gas']:
        res_data['charge'] = res_dict_fill(parameter_dc, basic_dc,
            parameter_dc['energy_system']['energy_system_storages4gas'],
            'gas_storage_charge', res_data['charge'])


def results_to_dict_soc(basic_dc, res_data, parameter_dc):
    ''
    res_data['soc'] = res_dict_fill(parameter_dc, basic_dc,
            parameter_dc['energy_system']['energy_system_storages'],
            'storage_soc', res_data['soc'])
    if parameter_dc['energy_system']['energy_system_storages4gas']:
        res_data['soc'] = res_dict_fill(parameter_dc, basic_dc,
            parameter_dc['energy_system']['energy_system_storages4gas'],
            'gas_storage_soc', res_data['soc'])


def results_to_dict_discharge(basic_dc, res_data, parameter_dc):
    ''
    res_data['discharge'] = res_dict_fill(parameter_dc, basic_dc,
            parameter_dc['energy_system']['energy_system_storages'],
            'storage_discharge', res_data['discharge'])
    if parameter_dc['energy_system']['energy_system_storages4gas']:
        res_data['discharge'] = res_dict_fill(parameter_dc, basic_dc,
            parameter_dc['energy_system']['energy_system_storages4gas'],
            'gas_storage_discharge', res_data['discharge'])


def results_to_dict_trm_power(basic_dc, res_data, parameter_dc):
    ''
    res_data['trm_power'] = {}
    try:
        for r in parameter_dc['energy_system']['energy_system_regions']:
            res_data['trm_power'][r] = db.fetch_columns(basic_dc,
                basic_dc['res_schema'],
                parameter_dc['energy_system']['name_set'] + '_' + 'trm_power',
                orderby='timestep', columns=r, where_column='id',
                where_condition=parameter_dc['id'])[r]
    except:
        res_data['trm_power'][r] = [0]
        print 'no grid installed'


def results_to_dict_splitted_gas_flow(basic_dc, res_data, parameter_dc):
    ''
    gas_pp = ([x for x in (parameter_dc['energy_system']
        ['energy_system_transformer4elec']) if x in ['tocg', 'tccg']])

    res_data['splitted_gas_flow'] = res_dict_fill(parameter_dc, basic_dc,
            gas_pp, 'splitted_gas_flow', res_data['splitted_gas_flow'])


def res_dict_fill(parameter_dc, basic_dc, c_list, res_table, res_dc):
    ''
    for i in c_list:
        res_dc[i] = {}
        for r in parameter_dc['energy_system']['energy_system_regions']:
            res_dc[i][r] = db.fetch_columns(basic_dc,
                basic_dc['res_schema'],
                parameter_dc['energy_system']['name_set'] + '_' + res_table,
                orderby='timestep', columns=i, where_string=
                "region='%s' and id='%s'" % (r, parameter_dc['id']))[i]
    return res_dc


def set_operation(dc):
    ''
    sum0 = 0
    for key in dc.keys():
        try:
            for num in dc[key]:
                if num > 0:
                    sum0 += 1
        except:
            pass
    return sum0


def set_load_changes(dc):
    ''
    sum0 = 0
    for key in dc.keys():
        num_t_minus_1 = 0
        try:
            for num in dc[key]:
                if num > num_t_minus_1:
                    sum0 += 1
                num_t_minus_1 = num
        except:
            pass
    return sum0


def set_load_change_power(dc):
    ''
    sum0 = 0
    for key in dc.keys():
        num_t_minus_1 = 0
        try:
            for num in dc[key]:
                if num != num_t_minus_1:
                    sum0 += abs(num - num_t_minus_1)
                num_t_minus_1 = num
        except:
            pass
    return sum0