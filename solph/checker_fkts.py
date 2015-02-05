#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import logging


#def check_if_results_exist(main_dc, overwrite):
    #'''
    #'''
    #tester = db.fetch_columns(main_dc['basic'], main_dc['basic']['res_schema'],
        #'info', columns='id', where_column='id',
        #where_condition=main_dc['info']['id'])['id']
    #if tester:
        #tester = True
        #if overwrite:
            #logging.warning('System will overwrite existing results for ' +
                #'scenario: %s.' % (main_dc['info']['id']))
        #else:
            #logging.warning('System will try to create subscenario to save ' +
                #'the existing results of scenario %s.' % main_dc['info']['id'])
            #logging.warning('This mode is unsecure and might cause data' +
                #' losses. Try to avoid this by using a new scenario.')
    #else:
        #tester = False
    #return tester


def check_heat(main_dc):
    '''
    Checks if there are any heat producing transformers including chp.
    '''
    if (main_dc['energy_system']['transformer']['heat'] or
            main_dc['energy_system']['transformer']['chp']):
        main_dc['check']['heat'] = True
    else:
        main_dc['check']['heat'] = False


def check_extend_nat_gas_bus(m_dc):
    '''
    Checks for components that make it necessary to extend the natural gas bus.
    '''
    if (m_dc['simulation']['re_share']):
        m_dc['check']['extend_nat_gas_bus'] = True
    else:
        m_dc['check']['extend_nat_gas_bus'] = False


def check_biogas(m_dc):
    '''
    Checks if the resource 'biogas (rbig)' is needed.
    '''
    if 'rbig' in list(m_dc['energy_system']['resources'].keys()):
        m_dc['check']['biogas'] = True
    else:
        m_dc['check']['biogas'] = False


def check_input(main_dc, overwrite):
    '''
    '''
    #main_dc['check']['results_exist'] = check_if_results_exist(main_dc,
        #overwrite)
    if not 'check' in main_dc:
        main_dc['check'] = {}
    check_heat(main_dc)
    check_extend_nat_gas_bus(main_dc)
    check_biogas(main_dc)
    info_parameter_check = ("Heat = %s, " % main_dc['check']['heat'] +
        "Invest = %s" % main_dc['simulation']['investment'])
    logging.info(info_parameter_check)


def check_domestic_resources(main_dc):
    '''
    Checks the yealy limit of resources for domestic heating systems.
    '''
    tmp_dc = {}
    for r in main_dc['energy_system']['regions']:
        for c in main_dc['energy_system']['domestic']:
            tmp_dc.setdefault(main_dc['energy_system']['resources'][c], 0)
            tmp_dc[main_dc['main_dc']['resource'][c]] += (
                sum(main_dc['timeseries']['demand'][r][c]) *
                (1 / main_dc['energy_system']['eff4heat'][c]))
        for i in list(tmp_dc.keys()):
            yearly_limit = ((main_dc['parameter']['resources'][r][i]
                ['yearly_limit']) * ((main_dc['simulation']['timestep_end'] -
                main_dc['simulation']['timestep_start']) / 8760.))
            if tmp_dc[i] > yearly_limit:
                logging.warning(
                    "Yearly limit lower than demand for {0}.".format(i))
                logging.warning("Yearly limit: {0}".format(yearly_limit))
                logging.warning("LP-problem might be infeasible.")


def check_biogas_installed_cap(main_dc):
    '''
    Checks if the installed capacity of all transformers that use biogas is
    sufficient to process the biogas.
    '''
    logging.warning('Function check_biogas_installed_cap is disabled.')

    main_dc['check']['biogas_ratio_inst_pot'] = 'disabled'

    #!!!!!!This function causes errors in some configurations!!!!!

    #biogas_ratio_inst_pot = {}

    #if basic_dc['check']['biogas']:
        #for r in p_dc['parameter']['parameter_regions']:
            #daily_limit = (p_dc['parameter']['parameter_resources'][r]['rbig']
                #['yearly_limit'] / 8760)
            #p_inst_tot = 0.0
            #for key in basic_dc['transformer_keys']:
                #for c in p_dc['lists']['resources2plant']['rbig'][key]:
                    #p_inst_tot += data_dc['presetting'][c][r] / (
                        #p_dc['parameter']['parameter_transformer4' + key][r][c]
                        #['efficiency'])
            #biogas_ratio_inst_pot[r] = p_inst_tot / daily_limit
            #if biogas_ratio_inst_pot < 0:
                #logging.error('The biogas production is higher than the ' +
                    #'installed capacity.')
        #check_str = str(biogas_ratio_inst_pot).replace("'", "")
        #basic_dc['check']['biogas_ratio_inst_pot'] = check_str
    #else:
        #basic_dc['check']['biogas_ratio_inst_pot'] = 'no biogas'


def check_data(main_dc):
    '''
    Checks some data sets.
    '''

    check_domestic_resources(main_dc)
    check_biogas_installed_cap(main_dc)


def start_check():
    '''
    '''
    check_dc = {}
    check_dc['sim_check'] = 'okay'
    return check_dc


def isNoneOrEmptyOrBlankString(myString):
    ''
    if myString:
        if not myString.strip():
            return True
    else:
        return True
    return False
