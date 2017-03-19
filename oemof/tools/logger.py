# -*- coding: utf-8

import os
import shutil
import logging
import logging.config
from oemof.tools import helpers


def define_logging(inifile='logging.ini', basicpath=None,
                   subdir='log_files', log_version=True):
    r"""Initialise the logger using the logging.conf file in the local path.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    inifile : string, optional (default: logging.ini)
        Name of the configuration file to define the logger. If no ini-file
         exist a default ini-file will be copied from 'default_files' and
         used.
    basicpath : string, optional (default: '.oemof' in HOME)
        The basicpath for different oemof related information. By default
        a ".oemof' folder is created in your home directory.
    subdir : string, optional (default: 'log_files')
        The name of the subfolder of the basicpath where the log-files are
        stored.
    log_version : boolean
        If True the actual version or commit is logged while initialising the
        logger.

    Returns
    -------
    str : Place where the log file is stored.

    Notes
    -----
    By default the INFO level is printed on the screen and the debug level
    in a file, but you can easily configure the ini-file.
    Every module that wants to create logging messages has to import the
    logging module. The oemof logger module has to be imported once to
    initialise it.

    Examples
    --------
    To define the default logger you have to import the python logging
     library and this function. The first logging message should be the
     path where the log file is saved to.

    >>> import logging
    >>> from oemof.tools import logger
    >>> logger.define_logging() # doctest: +SKIP
    17:56:51-INFO-Path for logging: /HOME/.oemof/log_files
    ...
    >>> logging.debug("Hallo")

    """
    if basicpath is None:
        basicpath = helpers.get_basic_path()
    logpath = helpers.extend_basic_path(subdir)
    log_filename = os.path.join(basicpath, inifile)
    default_file = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'default_files', 'logging_default.ini')
    if not os.path.isfile(log_filename):
        shutil.copyfile(default_file, log_filename)
    logging.config.fileConfig(os.path.join(basicpath, inifile))
    try:
        returnpath = logging.getLoggerClass().root.handlers[1].baseFilename
    except AttributeError:
        returnpath = None
    logger = logging.getLogger('simpleExample')
    logger.debug('*********************************************************')
    logging.info('Path for logging: %s' % logpath)
    if log_version:
        try:
            check_git_branch()
        except FileNotFoundError:
            check_version()
    return returnpath


def check_version():
    """Returns the actual version number of the used oemof version."""
    import oemof
    try:
        version = oemof.__version__
    except AttributeError:
        version = 'No version found due to internal error.'
    logging.info("Used oemof version: {0}".format(version))


def check_git_branch():
    """Passes the used branch and commit to the logger
    """
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


def time_logging(start, text, logging_level='debug'):
    """
    Logs the time between the given start time and the actual time. A text
    and the debug level is variable.

    Parameters
    ----------
    start : float
        start time
    text : string
        text to describe the log
    logging_level : string
        logging_level [default='debug']
    """
    import time
    end_time = time.time() - start
    hours = int(end_time / 3600)
    minutes = int(end_time / 60 - hours * 60)
    seconds = int(end_time - hours * 3600 - minutes * 60)
    time_string = ' %0d:%02d:%02d hours' % (hours, minutes, seconds)
    log_str = text + time_string
    if logging_level == 'debug':
        logging.debug(log_str)
    elif logging_level == 'info':
        logging.info(log_str)
