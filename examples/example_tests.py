# -*- coding: utf-8 -*-

import logging
import os
import sys
from oemof.tools import logger

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'solph'))
from storage_optimization import storage_invest

tolerance = 0.001  # percent
show_messages = True
testdict = {}


def check(cdict, runcheck, subdict, new_results):
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


# ********* storage invest example ******************************************
testdict['stor_inv'] = {'name': "Storage invest example",
                        'solver': 'cbc'}

number_of_timesteps = 8760

try:
    esys = storage_invest.initialise_energysystem(number_of_timesteps)
    filepath = os.path.join('solph/storage_optimization', 'storage_invest.csv')
    esys = storage_invest.optimise_storage_size(
        esys, filename=filepath, solvername=testdict['stor_inv']['solver'])
    results = storage_invest.get_result_dict(esys)
    stor_invest_run = True

except Exception as e:
    testdict['stor_inv']['messages'] = {'error': e}
    stor_invest_run = False

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

logger.define_logging()
for tests in testdict.values():
    logging.info(tests['name'])
    logging.info("Used solver: {0}".format(tests['solver']))
    logging.info("Run check: {0}".format(tests['run']))
    logging.info("Result check: {0}".format(tests['results']))
    if show_messages and 'messages' in tests:
        for message in tests['messages'].values():
            logging.error(message)
