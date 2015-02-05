#!/usr/bin/python
# -*- coding: utf-8

import logging
import numpy as np


def remove_from_list(orig_list, remove_list):
    '''
    Removes the values inside the remove_list from the orig_list.
    '''
    for item in remove_list:
        if item in orig_list:
            try:
                orig_list.remove(item)
            except:
                logging.debug('Cannot remove %s from list %s' % (
                    item, orig_list))
    return orig_list


def cut_lists(list_a, list_b):
    '''
    Returns a list with the values of list_a AND list_b.
    '''
    return [x for x in list(list_a) if x in set(list_b)]


def unique_list(seq):
    '''
    Returns a unique list without preserving the order
    '''
    return list({}.fromkeys(seq).keys())


def time_logging(start, text, logging_level='debug'):
    '''
    Logs the time between the given start time and the actual time. A text
    and the debug level is variable.

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters
        start : start time : float
        text : text to describe the log : string

    Keyword arguments
        logging_level : logging_level [default='debug'] : string
    '''
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


def get_timesteps(parameter_dc):
    '''
    Returns a list with the range of timesteps.
    '''
    return xrange(parameter_dc['simulation']['timestep_end'] -
        parameter_dc['simulation']['timestep_start'])


def get_prev_timsteps(parameter_dc):
    '''
    Returns the
    '''
    return list(np.roll(get_timesteps(parameter_dc), 1))