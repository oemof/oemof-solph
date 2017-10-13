# -*- coding: utf-8 -*-

import logging
import time
import os
import sys
import nose
from oemof.tools import logger

sys.path.append(os.path.join(os.path.dirname(__file__), 'solph'))
from storage_investment import storage_investment
from simple_dispatch import simple_dispatch
from flexible_modelling import add_constraints
from csv_reader.dispatch import dispatch
from csv_reader.investment import investment
from variable_chp import variable_chp

tolerance = 0.001  # percent
show_messages = True
testdict = {}
PASSED = True
basic_path = os.path.dirname(__file__)


def check(cdict, runcheck, subdict, new_results=None):
    global PASSED
    print("Check {0}...".format(subdict['name']))
    if runcheck and new_results is not None:
        count = 0
        subdict['run'] = "Okay"
        subdict.setdefault('messages', {})
        for key, value in new_results.items():
            maxval = cdict[key] + abs(cdict[key]) * tolerance
            minval = cdict[key] - abs(cdict[key]) * tolerance

            if not ((float(value) >= minval) and (float(value) <= maxval)):
                count += 1
                subdict['messages'][count] = (
                    "{0}: {1} not between {2} and {3}".format(
                        key, float(value), minval, maxval))
                PASSED = False
        if count < 1:
            subdict['results'] = "Okay"
        else:
            subdict['results'] = "{0} error(s)".format(count)
        skip = list(set(cdict.keys()) - set(new_results.keys()))
        if len(skip):
            count += 1
            subdict['messages'][count] = (
                "The following tests were skipped: {0}.".format(skip))
    elif runcheck and new_results is None:
        subdict['run'] = "Okay"
        subdict['results'] = "No results to check - Okay"
    else:
        subdict['run'] = "Failed"
        subdict['results'] = "Failed"
        PASSED = False


def check_nosetests():
    testdir = os.path.join(os.path.dirname(__file__), os.pardir)
    argv = sys.argv[:]
    argv.insert(1, "--with-doctest")
    argv.insert(1, "-w{0}".format(testdir))
    if nose.run(argv=argv):
        time.sleep(0.3)
        print("All nosetests passed!")
    else:
        msg = "Some nosetests failed."
        msg += "See the output above for more information!"
        print(msg)


def run_example_checks():
    # ********* storage invest example ****************************************
    key = 'stor_inv'
    testdict[key] = {'name': "Storage invest example", 'solver': 'cbc'}

    try:
        results = storage_investment.optimise_storage_size(
            number_timesteps=500,
            solver=testdict[key]['solver'], debug=False,
            tee_switch=False, silent=True)

        testdict[key]['run'] = True

    except Exception as e:
        testdict[key]['messages'] = {'error': e}
        testdict[key]['run'] = False
        results = None

    stor_invest_dict = {
        'storage_invest': 615506.93999999994,
        (('electricity', 'demand'), 'flow'): 133997181.20832705,
        (('electricity', 'excess_bel'), 'flow'): 273149694.8592003,
        (('electricity', 'storage'), 'flow'): 1559331.1879999998,
        (('pp_gas', 'electricity'), 'flow'): 6435517.1424000021,
        (('pv', 'electricity'), 'flow'): 9806339.1483599972,
        (('storage', 'electricity'), 'flow'): 1247464.9504000004,
        (('wind', 'electricity'), 'flow'): 391216886.0}

    # der = {
    #         'objective': 2.806796142614384e+17,
    #     }

    check(stor_invest_dict, testdict[key]['run'], testdict[key], results)
    # ********* end of storage invest example *********************************

    # *********** simple dispatch example *************************************
    key = 'least_costs'
    testdict[key] = {'name': "Simple dispatch optimization",
                     'solver': 'cbc'}

    try:
        results = simple_dispatch.run_simple_dispatch_example()
        testdict[key]['run'] = True
    except Exception as e:
        testdict[key]['messages'] = {'error': e}
        testdict[key]['run'] = False
        results = None

    test_results = {
        (('wind', 'bel'), 'flow'): 19504.415509800005,
        (('pv', 'bel'), 'flow'): 4205.0081990299996,
        (('bel', 'demand_el'), 'flow'): 95893.690674837926,
        (('bel', 'excess_el'), 'flow'): 353.30769076999997,
        (('pp_chp', 'bel'), 'flow'): 7043.259944773984,
        (('pp_lig', 'bel'), 'flow'): 16320.727254279591,
        (('pp_gas', 'bel'), 'flow'): 23848.364613840022,
        (('pp_coal', 'bel'), 'flow'): 25958.774628000549,
        (('pp_oil', 'bel'), 'flow'): 2.2872602799999999,
        (('bel', 'heat_pump'), 'flow'): 635.8390440710001
    }

    check(test_results, testdict[key]['run'], testdict[key], results)
    # *********** end of simple dispatch example ******************************

    # *********** flexible modelling example **********************************
    key = 'flexible_modelling'
    testdict[key] = {'name': "Flexible Modelling",
                     'solver': 'cbc'}

    try:
        add_constraints.run_add_constraints_example(testdict[key]['solver'],
                                                    nologg=True)
        testdict[key]['run'] = True
    except Exception as e:
        testdict[key]['messages'] = {'error': e}
        testdict[key]['run'] = False

    test_results = {}

    check(test_results, testdict[key]['run'], testdict[key])
    # *********** end of flexible modelling example ***************************

    # *********** csv reader dispatch example *********************************
    key = 'csv_reader_dispatch'
    testdict[key] = {
        'name': "Dispatch model with csv reader",
        'solver': 'cbc',
        'verbose': False,
        'scenario_path': os.path.join(basic_path, 'solph', 'csv_reader',
                                      'dispatch', 'scenarios'),
        'date_from': '2030-01-01 00:00:00',
        'date_to': '2030-01-14 23:00:00',
        'nodes_flows': 'example_energy_system.csv',
        'nodes_flows_sequences': 'example_energy_system_seq.csv',
        'results_path': os.path.join(os.path.expanduser("~"), 'csv_dispatch')
    }

    if not os.path.isdir(testdict[key]['results_path']):
        os.mkdir(testdict[key]['results_path'])

    try:
        results = dispatch.run_csv_reader_dispatch_example(config=testdict[key], )
        testdict[key]['run'] = True
    except Exception as e:
        testdict[key]['messages'] = {'error': e}
        testdict[key]['run'] = False
        results = None

    test_results = {
        (('R1_pp_gas', 'R1_bus_el'), 'flow'): 0.0,
        (('R1_pp_hard_coal', 'R1_bus_el'), 'flow'): 1031265.0381399998,
        (('R1_pp_oil', 'R1_bus_el'), 'flow'): 0.0,
        (('R1_pp_uranium', 'R1_bus_el'), 'flow'): 1428000.0,
        (('R1_pp_lignite', 'R1_bus_el'), 'flow'): 1410321.1378500001,
        (('R1_bus_el', 'R1_excess'), 'flow'): 0.0,
        (('R1_bus_el', 'R1_load'), 'flow'): 8326012.1175384959,
        (('R1_bus_el', 'R1_R2_powerline'), 'flow'): 0.0,
        (('R1_solar', 'R1_bus_el'), 'flow'): 109133.28500000003,
        (('R1_run_of_river', 'R1_bus_el'), 'flow'): 1092000.0,
        (('R1_wind', 'R1_bus_el'), 'flow'): 472390.93500000017,
        (('R1_bus_el',), 'duals'): 13325.791131000004,
        (('R2_R1_powerline', 'R1_bus_el'), 'flow'): 2209649.7471529995,
        (('R1_shortage', 'R1_bus_el'), 'flow'): 0.0,
        (('R1_pp_biomass', 'R1_bus_el'), 'flow'): 180136.44901700001,
        (('R1_pp_mixed_fuels', 'R1_bus_el'), 'flow'): 393115.52601000009}


    check(test_results, testdict[key]['run'], testdict[key], results)
    # *********** end of csv reader dispatch example **************************

    # *********** csv reader investment example *******************************
    key = 'csv_reader_investment'
    testdict[key] = {'name': "Investment model with csv reader",
                     'solver': 'cbc'}

    try:
        investment.run_investment_example(solver=testdict[key]['solver'],
                                          verbose=False, nologg=True)
        testdict[key]['run'] = True
    except Exception as e:
        testdict[key]['messages'] = {'error': e}
        testdict[key]['run'] = False

    test_results = {}

    check(test_results, testdict[key]['run'], testdict[key])
    # *********** end of csv reader investment example ************************

    # ********* variable chp example ******************************************
    key = 'variable_chp'
    testdict[key] = {'name': "Variable CHP example", 'solver': 'cbc'}

    try:
        esys = variable_chp.initialise_energy_system(192)
        esys = variable_chp.optimise_storage_size(
            esys, solver=testdict[key]['solver'], tee_switch=False)
        results = variable_chp.get_result_dict(esys)
        testdict[key]['run'] = True

    except Exception as e:
        testdict[key]['messages'] = {'error': e}
        testdict[key]['run'] = False
        results = None

    variable_chp_dict = {
        'objective': 14267160965.0,
        'input_fixed_chp': 157717049.49999994,
        'natural_gas': 285343219.29999995,
        'input_variable_chp': 127626169.47000004}

    check(variable_chp_dict, testdict[key]['run'], testdict[key], results)
    # ********* end of variable chp example ***********************************

    logger.define_logging()
    for tests in testdict.values():
        logging.info('*********************************************')
        logging.info(tests['name'])
        logging.info("Used solver: {0}".format(tests['solver']))
        logging.info("Run check: {0}".format(tests['run']))
        logging.info("Result check: {0}".format(tests['results']))
        if show_messages and 'messages' in tests:
            for message in tests['messages'].values():
                logging.error(message)

    if PASSED:
        check_nosetests()
        print("All example tests passed!")
    else:
        check_nosetests()
        text = "Some example tests failed."
        text += "See the output above for more information!"
        print(text)


if __name__ == "__main__":
    run_example_checks()
