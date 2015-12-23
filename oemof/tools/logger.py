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


def define_logging(logging_dir='log_files'):
    '''
    Initialise the logger using the logging.conf file in the local path

    Uwe Krien (uwe.krien@rl-institut.de)
    '''
    url = 'http://vernetzen.uni-flensburg.de/~git/logging_default.ini'
    basicpath = os.path.join(os.environ['HOME'], '.oemof')
    logpath = os.path.join(basicpath, logging_dir)
    if not os.path.isdir(basicpath):
        os.mkdir(basicpath)
    if not os.path.isdir(logpath):
        os.mkdir(logpath)
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

    logging.info("Used oemof version: {0} @ {1}".format(
        last_commit,
        name_branch))
