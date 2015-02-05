#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

import logging


def check_balance(res_data, parameter_dc, output='dict'):
    ''
    logging.info('Checking balances...')

    # define lists of component groups
    other_comp_list = ['twpp', 'tnuc']
    renewables_list = ['rwin', 'rpvo']
    gas_pp_list = ['tocg', 'tccg']

    k_list = ['renewables', 'other', 'gas_pp', 'gas_pp_fos']

    # calculate annual sums of component groups/ u_types ;)
    other = 0
    renewables = 0
    gas_pp = 0
    gas_pp_fos = 0
    gas_pp_fos_dc = {}
    balances = {}

    # initialise entries with zeros
    for k in k_list:
      balances[k] = 0
    balances['gas_pp_fos_dc'] = {}

    balances['generation'] = sumup_dict(res_data['generation'])
    for c in ([x for x in parameter_dc['energy_system']
            ['energy_system_re'] if x in renewables_list]):
        balances['renewables'] += sumup_dict_one_level(res_data['generation'][c])
    for c in ([x for x in parameter_dc['energy_system']
            ['energy_system_transformer4elec'] if x in other_comp_list]):
        balances['other'] += sumup_dict_one_level(res_data['generation'][c])
    for c in ([x for x in parameter_dc['energy_system']
            ['energy_system_transformer4elec'] if x in gas_pp_list]):
                balances['gas_pp'] += sumup_dict_one_level(res_data['generation'][c])
                if res_data['gas'].keys():
                    balances['gas_pp_fos_dc'][c] = (sumup_dict_one_level(res_data['gas'][c])
                        * parameter_dc['parameter']
                        ['parameter_transformer4elec']
                        [parameter_dc['energy_system']
                        ['energy_system_regions'][0]][c]['efficiency'])
                else:
                    balances['gas_pp_fos_dc'][c] = sumup_dict_one_level(
                        res_data['generation'][c])
    for c in balances['gas_pp_fos_dc'].keys():
        balances['gas_pp_fos'] += balances['gas_pp_fos_dc'][c]
    balances['fossils'] = balances['generation'] - balances['renewables'] - balances['other'] + balances['gas_pp_fos'] - balances['gas_pp']
    balances['demand_total'] = sumup_dict(res_data['demand'])  # includes ptg and excess
    balances['demand'] = sumup_dict_one_level(res_data['demand']['lele'])
    balances['trm_power'] = sumup_dict_one_level(res_data['trm_power'])
    if parameter_dc['energy_system']['energy_system_transformer4gas']:
        balances['ptg_ann_input'] = sumup_dict_one_level(res_data['demand']['rele'])

    balances['discharge'] = {}
    for c in res_data['discharge'].keys():
        balances['discharge'][c] = sumup_dict_one_level(res_data['discharge'][c])
    balances['charge'] = {}
    for c in res_data['charge'].keys():
        balances['charge'][c] = sumup_dict_one_level(res_data['charge'][c])
    balances['losses'] = {}
    balances['losses_sum'] = 0
    for c in res_data['discharge'].keys():
        balances['losses'][c] = balances['charge'][c] - balances['discharge'][c]
        balances['losses_sum'] = balances['losses_sum'] + balances['losses'][c]

    # Create balance
    balances['balance'] = (balances['generation'] - balances['demand_total'] -
        balances['losses_sum'] - balances['trm_power'])
    balances['ren_share'] = balances['renewables'] / balances['demand']


    if output == 'print':
      pass
    else:
      return balances


    ###### to be recoded according to rest of file
    ##operating hours
    #print('Operating hours of each technology:')
    #print('\t Operating hours \t\t share of year')
    #for c in res_data['generation'].keys():
        #print('\t' + c + ': ' + str(set_operation(
            #res_data['generation'][c])) + ' \t\t' + str(set_operation(
            #res_data['generation'][c]) / 8760.0))
    ##load changes
    #print('Load changes of each technology:')
    #print('\t Load Changes ')
    #for c in res_data['generation'].keys():
        #print('\t' + c + ': ' + str(set_load_changes(
            #res_data['generation'][c])))  # + '\t' + str(set_load_changes(
            ##res_data['generation'][c]) / sum(load_changes)))

    ##load change_power
    ##sum load_change_power:
    #sum_load_change_power = 0
    #for c in res_data['generation'].keys():
        #sum_load_change_power += set_load_change_power(
            #res_data['generation'][c])

    #print('Load change power of each technology(Sum of power that changes ' +
        #'from timestep t-1 to t):')
    #print('\t Load change power[KWh \t\t share')
    #for c in res_data['generation'].keys():
        #print('\t' + c + ': ' + str(set_load_change_power(
            #res_data['generation'][c])) + ' \t\t' + str(set_load_change_power(
            #res_data['generation'][c]) / sum_load_change_power))

    # has to be moved to another def in order to be printed to prompt if
    # output == 'print'
    #print('---------------------------------------------------')
    #print('Generation: ' + str(balances['generation']))
    #print('\t Renewables: ' + str(balances['renewables']) + '\t ren. share: ' +
        #str(balances['renewables'] /
            #balances['demand']))
    #print('\t Fossil: ' + str(balances['fossils']) + '\t fossil share: ' + str(balances['fossils'] /
        #balances['demand']))
    #print('\t Other: ' + str(balances['other']) + '\t other share: ' +
        #str(balances['other'] / balances['demand']))
    #print('Generation of each technology:')
    #print('\t Generation in kWh \t\t share')
    #for c in res_data['generation'].keys():
        #print('\t' + c + ': ' + str(sumup_dict_one_level(
            #res_data['generation'][c])) + '\t' + str(sumup_dict_one_level(
            #res_data['generation'][c]) / (
                #balances['demand'])))
    #print('Demand incl. excess and ptg: ' + str(balances['demand']))
    #for d in res_data['demand'].keys():
        #print('\t ' + d + ': ' + str(sumup_dict_one_level(
            #res_data['demand'][d])))
    #print('Transmission: ' + str(balances['trm_power']))
    #if parameter_dc['energy_system']['energy_system_transformer4gas']:
        #print('PtG elec. input power: ' + str(balances['ptg_ann_input']))

    #for c in res_data['charge'].keys():
        #print(c + ' charge: ' + str(balances['charge'][c]))
        #print(c + ' discharge: ' + str(balances['discharge'][c]))
        #print(c + ' losses: ' + str(balances['losses'][c]))

    #print('Balance: ' + str(balance))
    #print('Fossil share of Gas Power Plants')
    #for c in balances['gas_pp_fos_dc'].keys():
        #print('\t ' + c + ': ' + str(balances['gas_pp_fos_dc'][c] / balances['demand']))
    #print('---------------------------------------------------')


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
