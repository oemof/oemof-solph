# -*- coding: utf-8 -*-
"""
This is a collection of helper functions which work on there own and can be
used by various classes. If there are too many helper-functions, they will
be sorted in different modules.
"""

import os


def get_basic_path():
    """Returns the basic oemof path and creates it if necessary.
    """
    basicpath = os.path.join(os.path.expanduser('~'), '.oemof')
    if not os.path.isdir(basicpath):
        os.mkdir(basicpath)
    return basicpath


def extend_basic_path(subfolder):
    """Returns a path based on the basic oemof path and creates it if
     necessary. The subfolder is the name of the path extension.
    """
    extended_path = os.path.join(get_basic_path(), subfolder)
    if not os.path.isdir(extended_path):
        os.mkdir(extended_path)
    return extended_path


def get_fullpath(path, filename):
    """Combines path and filename to a full path.
    """
    return os.path.join(path, filename)
