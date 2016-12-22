#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import os
import shutil
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
        exist a default ini-file will be copied from 'default_files' and used.
    basicpath : string, optional (default: '.oemof' in HOME)
        The basicpath for different oemof related informations. By default
        a ".oemof' folder is created in your home directory.
    subdir : string, optional (default: 'log_files')
        The name of the subfolder of the basicpath where the log-files are
        stored.

    Notes
    -----
    By default the INFO level is printed on the screen and the debug level
    in a file, but you can easily configure the ini-file.
    Every module that wants to create logging messages has to import the
    logging module. The oemof logger module has to be imported once to
    initialise it.

    Examples
    --------
    To define the default logge you have to import the python logging library
    and this function. The first logging message should be the path where the
    log file is saved to.

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
    logger = logging.getLogger('simpleExample')
    logger.debug('*********************************************************')
    logging.info('Path for logging: %s' % logpath)
    try:
        check_git_branch()
    except:
        check_version()


def check_version():
    """Returns the actual version number of the used oemof version."""
    # TODO : Please add this feature if you know how.
    pass


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

if __name__ == '__main__':
    import doctest

    OC = doctest.OutputChecker
    class AEOutputChecker(OC):
        def check_output(self, want, got, optionflags):
            from re import sub
            if optionflags & doctest.ELLIPSIS:
                want = sub(r'\[\.\.\.\]', '...', want)
            return OC.check_output(self, want, got, optionflags)

    doctest.OutputChecker = AEOutputChecker
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)