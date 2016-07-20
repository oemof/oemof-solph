# -*- coding: utf-8 -*-

import logging
import time
import os
import sys
import nose
from oemof.tools import logger

# add path for solph examples
sys.path.append(os.path.join(os.path.dirname(__file__), 'solph'))
from storage_optimization import storage_invest
from simple_least_costs import simple_least_costs


tolerance = 0.001  # percent
show_messages = True
testdict = {}
PASSED = True
basic_path = os.path.dirname(__file__)


def check(cdict, runcheck, subdict, new_results):
    global PASSED
    if runcheck:
        count = 0
        subdict['run'] = "Okay"
        subdict.setdefault('messages', {})
        for key, value in new_results.items():
            maxval = cdict[key] + abs(cdict[key]) * tolerance
            minval = cdict[key] - abs(cdict[key]) * tolerance

            if not ((float(value) > minval) and (float(value) < maxval)):
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
    else:
        subdict['run'] = "Failed"
        subdict['results'] = "Failed"
        PASSED = False


def check_nosetests():
    testdir = os.path.join(os.path.dirname(__file__), os.pardir)
    os.chdir(testdir)
    argv = sys.argv[:]
    argv.insert(1, "--with-doctest")
    if nose.run(argv=argv):
        time.sleep(0.3)
        print("All nosetests passed!")
    else:
        msg = "Some nosetests failed."
        msg += "See the output above for more information!"
        print(msg)


# ********* storage invest example ******************************************
testdict['stor_inv'] = {'name': "Storage invest example",
                        'solver': 'cbc'}

number_of_timesteps = 8760

try:
    filepath = os.path.join(basic_path, 'solph', 'storage_optimization',
                            'storage_invest.csv')
    esys = storage_invest.optimise_storage_size(
        number_timesteps=number_of_timesteps, filename=filepath,
        solvername=testdict['stor_inv']['solver'], debug=False)
    results = storage_invest.get_result_dict(esys)
    stor_invest_run = True

except Exception as e:
    testdict['stor_inv']['messages'] = {'error': e}
    stor_invest_run = False
    results = None

stor_invest_dict = {8760: {
        'pp_gas_sum': 112750260.00000007,
        'demand_sum': 2255000000.000008,
        'demand_max': 368693.14440990007,
        'wind_sum': 3085699499.7,
        'wind_inst': 1000000,
        'pv_sum': 553984766.734176,
        'pv_inst': 582000,
        'storage_cap': 10805267,
        'objective': 8.93136532898235e+19}}

check(stor_invest_dict[number_of_timesteps], stor_invest_run,
      testdict['stor_inv'], results)
# ********* end of storage invest example *************************************


# *********** simple least cost  example **************************************
testdict['least_costs'] = {'name': "Simple least costs optimization",
                           'solver': 'cbc'}

filename = os.path.join(basic_path, 'solph', 'simple_least_costs',
                        'example_data.csv')

try:
    esys = simple_least_costs.initialise_energysystem(periods=2000)
    om = simple_least_costs.simulate(esys,
                                     filename=filename,
                                     solver=testdict['least_costs']['solver'])
    results = simple_least_costs.get_results(esys)
    least_costs_run = True
except Exception as e:
    testdict['least_costs']['messages'] = {'error': e}
    least_costs_run = False
    results = None

test_results = {
    'objective': 2947725.249402091,
    ('b_el', 'input', 'pp_chp', 'val'): 11161.357450000065,
    ('b_el', 'input', 'pp_coal', 'val'): 33723.047672110595,
    ('b_el', 'input', 'pp_gas', 'val'): 30412.377779000046,
    ('b_el', 'input', 'pp_lig', 'val'): 22066.451080999268,
    ('b_el', 'input', 'pp_oil', 'val'): 2.2872599999999998,
    ('b_el', 'input', 'pv', 'val'): 7796.8431880300122,
    ('b_el', 'input', 'wind', 'val'): 28009.549502999955,
    ('b_el', 'output', 'demand_el', 'val'): 132243.7904593189,
    ('b_el', 'output', 'excess', 'val'): 928.12139200000013,
    ('b_th', 'input', 'pp_chp', 'val'): 14881.810039999958,
    ('b_th', 'output', 'demand_th', 'val'): 14881.80983624002,
    ('coal', 'output', 'pp_coal', 'val'): 86469.394787298472,
    ('gas', 'output', 'pp_chp', 'val'): 37204.525720000034,
    ('gas', 'output', 'pp_gas', 'val'): 60824.751778000136,
    ('lignite', 'output', 'pp_lig', 'val'): 53820.634704001102,
    ('oil', 'output', 'pp_oil', 'val'): 8.1687949999999994}

check(test_results, least_costs_run, testdict['least_costs'], results)
# *********** end of simple least cost  example *******************************


logger.define_logging()
for tests in testdict.values():
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
