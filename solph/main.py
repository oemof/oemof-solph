#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import time
import traceback
import pulp as pulp
from . import checker_fkts as check
from . import basic_functions as bf
from . import extenddc as dc
from . import lp_definition as lp_def
from . import main_model as model


def solve_problem(main_dc, prob, debug, barrieronly):
    '''
    Solves the lp problem.
    '''
    if debug:
        logging.warning(
            'WRITING LP file. This is not necessary, only for debugging')
        lp_fil_path = os.path.join(
            main_dc['simulation']['initpath'], 'pahesmf',
            'lp_files', "pahesmf_debug.lp")
        logging.info('LP-file saved in: {0}'.format(lp_fil_path))
        prob.writeLP(lp_fil_path)
    logging.info('Solving problem using %s...' % (
        main_dc['simulation']['solver']))
    solver_start = time.time()
    if barrieronly is True:
        eval_string = '''prob.solve(pulp.%s(msg=%d, options={'Method': 2,
            'Crossover': 0}))''' % (
            main_dc['simulation']['solver'],
            main_dc['simulation']['solver_verbose'])
    else:
        eval_string = '''prob.solve(pulp.%s(msg=%d))''' % (
            main_dc['simulation']['solver'],
            main_dc['simulation']['solver_verbose'])
    status = eval(eval_string)
    main_dc['lp']['info']['data']['solver_status'] = pulp.LpStatus[status]
    main_dc['lp']['info']['data']['solver_time_minutes'] = (
        time.time() - solver_start) / 60.
    if (main_dc['lp']['info']['data']['solver_status'] == 'Infeasible' or
            main_dc['lp']['info']['data']['solver_status'] == 'Not Solved'):

        main_dc['lp']['info']['data']['objective_value'] = 0

        if debug:
            # If infeasible perform IIS and write ouput to .../lp_files/...
            logging.warning(
                'Model infeasible! Tracing Irreducible Infeasible Set...')
            if (main_dc['simulation']['solver'] == "GUROBI") or (
                    main_dc['simulation']['solver'] == "GUROBI_CMD"):
                import gurobipy
                prob_inf = gurobipy.read(lp_fil_path)
                prob_inf.computeIIS()
                ilp_fil_path = os.path.join(
                    main_dc['simulation']['initpath'],
                    'pahesmf', 'lp_files', "pahesmf_iis_debug.ilp")
                logging.info('ILP-file saved in: {0}'.format(ilp_fil_path))
                prob_inf.write(ilp_fil_path)
    else:
        main_dc['lp']['info']['data']['objective_value'] = (
            pulp.value(prob.objective))

    logging.info('Simulation finished. Status: %s' % pulp.LpStatus[status])
    bf.time_logging(solver_start, 'Solver time:', 'info')

    logging.debug('Storages used: %s' % (main_dc['energy_system']['storages']))
    logging.debug('Fossil used: %s' % (
        main_dc['energy_system']['transformer']['elec']))
    logging.debug('Renewables used: %s' % (main_dc['energy_system']['re']))


def start_core(var, main_dc, overwrite, failsafe, debug, barrieronly):
    '''
    Starts solph.
    '''
    logging.info('Starting SOLPH.')
    solph_start = time.time()

    # Create lists to describe the energy-system
    dc.extend(main_dc)

    # Checks the input data
    check.check_input(main_dc, overwrite)
    #check.check_data(main_dc)

    # Create LP variables
    logging.info('Creating LP Variables.')
    lp_def.create_lp_vars_dc(main_dc)

    # Create objective function and adding constraints
    logging.info('Creating objective function and adding constraints...')
    prob = model.create_model_equations(main_dc)

    # Solve problem
    solve_problem(main_dc, prob, debug, barrieronly=barrieronly)

    bf.time_logging(solph_start, 'SOLPH finished.', 'info')


def start(var, main_dc, overwrite=True, failsafe=False, debug=False,
          barrieronly=False):
    '''
    Start pahesmf wether in normal or failsafe mode
    '''
    if failsafe:
        try:
            start_core(var, main_dc, overwrite=overwrite, failsafe=failsafe,
                       debug=debug, barrieronly=barrieronly)
        except Exception as e:
            logging.critical(e.message)
            trace = traceback.format_exc()
            logging.critical(trace)
    else:
        start_core(var, main_dc, overwrite=overwrite, failsafe=failsafe,
                   debug=debug, barrieronly=barrieronly)
