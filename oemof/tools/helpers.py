# -*- coding: utf-8 -*-
"""
This is a collection of helper functions which work on their own and can be
used by various classes. If there are too many helper-functions, they will
be sorted in different modules.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/tools/helpers.py

SPDX-License-Identifier: MIT
"""

import os
from collections import MutableMapping


def get_basic_path():
    """Returns the basic oemof path and creates it if necessary.
    The basic path is the '.oemof' folder in the $HOME directory.
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


def flatten(d, parent_key='', sep='_'):
    """
    Flatten dictionary by compressing keys.

    See: https://stackoverflow.com/questions/6027558/
         flatten-nested-python-dictionaries-compressing-keys

    d : dictionary
    sep : separator for flattening keys

    Returns
    -------
    dict
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + str(k) if parent_key else str(k)
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
