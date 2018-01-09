# -*- coding: utf-8

"""Helpers to log your modeling process with oemof.
"""

import os
import logging
from logging import handlers
import sys
from oemof.tools import helpers


def define_logging(logpath=None, logfile='oemof.log', file_format=None,
                   screen_format=None, file_datefmt=None, screen_datefmt=None,
                   screen_level=logging.INFO, file_level=logging.DEBUG,
                   log_version=True, log_path=True, timed_rotating=None):

    r"""Initialise customisable logger.

    Parameters
    ----------
    logfile : str
        Name of the log file, default: oemof.log
    logpath : str
        The path for log files. By default a ".oemof' folder is created in your
        home directory with subfolder called 'log_files'.
    file_format : str
        Format of the file output.
        Default: "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    screen_format : str
        Format of the screen output.
        Default: "%(asctime)s-%(levelname)s-%(message)s"
    file_datefmt : str
        Format of the datetime in the file output. Default: None
    screen_datefmt : str
        Format of the datetime in the screen output. Default: "%H:%M:%S"
    screen_level : int
        Level of logging to stdout. Default: 20 (logging.INFO)
    file_level : int
        Level of logging to file. Default: 10 (logging.DEBUG)
    log_version : boolean
        If True the actual version or commit is logged while initialising the
        logger.
    log_path : boolean
        If True the used file path is logged while initialising the logger.
    timed_rotating : dict
        Option to pass parameters to the TimedRotatingFileHandler.


    Returns
    -------
    str : Place where the log file is stored.

    Notes
    -----
    By default the INFO level is printed on the screen and the DEBUG level
    in a file, but you can easily configure the logger.
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
    >>> mypath = logger.define_logging(log_path=False, log_version=False,
    ...                                screen_datefmt = "no_date")
    >>> mypath[-9:]
    'oemof.log'
    >>> logging.debug("Hallo")
    """

    if logpath is None:
        logpath = helpers.extend_basic_path('log_files')

    file = os.path.join(logpath, logfile)

    log = logging.getLogger('')

    # Remove existing handlers to avoid interference.
    log.handlers = []
    log.setLevel(logging.DEBUG)

    if file_format is None:
        file_format = (
            "%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    file_formatter = logging.Formatter(file_format, file_datefmt)

    if screen_format is None:
        screen_format = "%(asctime)s-%(levelname)s-%(message)s"
    if screen_datefmt is None:
        screen_datefmt = "%H:%M:%S"
    screen_formatter = logging.Formatter(screen_format, screen_datefmt)

    tmp_formatter = logging.Formatter("%(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(screen_formatter)
    ch.setLevel(screen_level)
    log.addHandler(ch)

    timed_rotating_p = {
        'when': 'midnight',
        'backupCount': 10}

    if timed_rotating is not None:
        timed_rotating_p.update(timed_rotating)

    fh = handlers.TimedRotatingFileHandler(file, **timed_rotating_p)
    fh.setFormatter(tmp_formatter)
    fh.setLevel(file_level)
    log.addHandler(fh)

    logging.debug("******************************************************")
    fh.setFormatter(file_formatter)
    if log_path:
        logging.info("Path for logging: {0}".format(file))

    if log_version:
        try:
            check_git_branch()
        except FileNotFoundError:
            check_version()
    return file


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
