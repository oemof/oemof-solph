#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import os
import logging
import logging.config
from oemof.tools import helpers


def define_logging(inifile='logging.ini', basicpath=None, subdir='log_files'):
    r"""Initialise the logger using the logging.conf file in the local path.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    inifile : string, optional (default: logging.ini)
        Name of the configuration file to define the logger. If no ini-file
        exist a default ini-file will be downloaded from
        'http://vernetzen.uni-flensburg.de/~git/logging_default.ini' and used.
    basicpath : string, optional (default: '.oemof' in HOME)
        The basicpath for different oemof related informations. By default
        a ".oemof' folder is created in your home directory.
    subdir : string, optional (default: 'log_files')
        The name of the subfolder of the basicpath where the log-files are
        stored.

    Notes
    -----
    By default the INFO level is printed on the screen and the debug level
    in a file.

    Examples
    --------
    To define the default logge you have to import the python logging library
    and this function.

    >>> import logging
    >>> from oemof.tools import logger
    >>> logger.define_logging()
    [...]INFO-Path for logging:...
    [...]INFO-Used oemof version:...
    >>> logging.debug("Hallo")
    
    """
    url = 'http://vernetzen.uni-flensburg.de/~git/logging_default.ini'
    if basicpath is None:
        basicpath = helpers.get_basic_path()
    logpath = helpers.extend_basic_path(subdir)
    log_filename = os.path.join(basicpath, 'logging.ini')
    if not os.path.isfile(log_filename):
        helpers.download_file(log_filename, url)
    logging.config.fileConfig(os.path.join(basicpath, 'logging.ini'))
    logger = logging.getLogger('simpleExample')
    logger.debug('*********************************************************')
    logging.info('Path for logging: %s' % logpath)
    check_git_branch()


def check_git_branch():
    '''
    Passes the used brance and commit to the logger
    '''
    path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), os.pardir,
        os.pardir, '.git')

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

    logging.info("Used oemof version: {0}@{1}".format(
        last_commit,
        name_branch))