#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import sys
import os
import shutil
import logging


def create_default_init_file(initpath, initfile):
    '''
    Creates a default initfile file if it doesn't exist. The file will be
    located in the initpath.
    The default version will not necessarily work. You might need to adept it.

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters
        initpath : path where the initfile is located : string
        initfile : the name of the initfile
    '''
    default_path = os.path.join(os.path.dirname(os.path.realpath(
        __file__)), os.pardir, os.pardir, 'default')
    default_file = 'init_local_default.py'
    default_file_path = os.path.join(default_path, default_file)
    init_file_path = os.path.join(initpath, initfile)
    if not os.path.isdir(initpath):
        os.mkdir(initpath)
    shutil.copy2(default_file_path, init_file_path)
    logging.info('Created default file for init_local.py')


def create_default_log_conf_file(initpath, initfile):
    '''
    Creates a default log_conf file if it doesn't exist. The file will be
    located in the pahesmf folder in the initpath.
    The default version will not necessarily work. You might need to adept it.

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters
        initpath : path where the pahesmf/log_conf file is located : string
        initfile : the name of the initfile
    '''
    default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            os.pardir, os.pardir, 'default')
    default_file = 'logging_default.conf'
    if not os.path.isdir(initpath):
        os.mkdir(initpath)
    initpath = os.path.join(initpath, 'pahesmf')
    default_file_path = os.path.join(default_path, default_file)
    init_file_path = os.path.join(initpath, initfile)
    if not os.path.isdir(initpath):
        os.mkdir(initpath)
    shutil.copy2(default_file_path, init_file_path)


def get_init_path():
    '''
    Returns the path to the local inti file 'init_local.py' and will
    create it if it doesn't exist.

    Uwe Krien (uwe.krien@rl-institut.de)

    Returns:
        path to the local init file : string
    '''
    initpath = os.path.join(os.environ['HOME'], '.python_local')
    initfile = 'init_local.py'
    if not os.path.isfile(os.path.join(initpath, initfile)):
        create_default_init_file(initpath, initfile)
    return initpath


def get_basic_dc():
    '''
    Returns the basic dictionary from the local directory

    Uwe Krien (uwe.krien@rl-institut.de)

    Returns:
        basic parameters : dictionary
    '''
    main_dc = {}
    initpath = get_init_path()
    sys.path.append(initpath)
    import init_local as init
    main_dc['basic'] = init.pahesmf()
    main_dc['basic']['initpath'] = initpath
    logging.debug('Basic dictionary initialised')
    return main_dc


def define_logging(logging_dir='pahesmf'):
    '''
    Initialise the logger using the logging.conf file in the local path

    Uwe Krien (uwe.krien@rl-institut.de)
    '''
    import logging.config
    basicpath = os.path.join(os.environ['HOME'], '.python_local')
    logpath = os.path.join(basicpath, logging_dir)
    logging.debug('Path for logging: %s' % logpath)
    if not os.path.isfile(os.path.join(logpath, 'logging.conf')):
        create_default_log_conf_file(basicpath, 'logging.conf')
    log_config_path = os.path.join(logpath, 'logging.conf')
    logging.config.fileConfig(log_config_path)
    logger = logging.getLogger('simpleExample')
    logger.debug('*********************************************************')


def check_git_branch(basic_dc):
    '''
    Passes the used brance and commit to the logger
    '''
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
        os.pardir, '.git')

    if not 'check' in basic_dc:
        basic_dc['check'] = {}

    # Reads the name of the branch
    f_branch = os.path.join(path, 'HEAD')
    f = open(f_branch, "r")
    first_line = f.readlines(1)
    name_full = first_line[0].replace("\n", "")
    name_branch = name_full.replace("ref: refs/heads/", "")
    f.close()

    # Reads the code of the last commit used
    f_commit = os.path.join(path, 'refs', 'heads', name_branch)
    f = open(f_commit, "r")
    last_commit = f.read(8)
    f.close()

    basic_dc['check']['last_commit'] = last_commit
    basic_dc['check']['name_branch'] = name_branch

    logging.info("Used pahesmf version: {0} @ {1}".format(last_commit,
        name_branch))

    #if basic_dc['check']['name_branch'] in basic_dc['list_of_masters_in_db']:
        #basic_dc['schema'] = basic_dc['master_schema']
        #basic_dc['res_schema'] = basic_dc['master_res_schema']
        #logging.info('DB schema "master" is used.')
    #else:
        #logging.info('DB schema "dev" is used.')


def check_parameter(var):
    '''
    Check if the scenario variable is given as an integer (id of scenario) or
    a string (name of scenario) and gives back the name of the connected column
    in the database.

    by Uwe Krien (uwe.krien@rl-institut.de)

    Parameters
        var : name or id of the chosen scenario : string/integer

    Returns
        name of column, where the var argument can be found : string

    '''
    # Check if scenario name or ID is given
    if type(var).__name__ == 'int':
        tmp_var = 'id'
        logging.debug('Scenario with ID %s chosen.' % var)
    elif type(var).__name__ == 'str':
        tmp_var = 'name_set'
        logging.debug('Scenario with name "%s" chosen.' % var)
    else:
        tmp_var = type(var)
        logging.warning('Unknown type for input variable: %s' % tmp_var)
        logging.critical(('Wrong input type! Please make sure that you entered'
            + 'a valid scenario name or a valid scenario ID'))
    return tmp_var


def create_maindt():
    '''
    Initialises a main_dt including switch branch
    '''
    main_dt = {}
    main_dt['switch'] = {}
    main_dt['switch']['read_re_data'] = True
    main_dt['switch']['read_demand_data'] = True
    return main_dt