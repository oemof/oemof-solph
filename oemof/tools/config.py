# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 12:26:40 2014

:module-author: steffen
:filename: config.py


This module provides a highlevel layer for reading and writing config files.
There must be a file called "config.ini" in the root-folder of the project.
The file has to be of the following structure to be imported correctly.

# this is a comment \n
# the filestructure is like: \n
 \n
[netCDF] \n
RootFolder = c://netCDF \n
FilePrefix = cd2- \n
 \n
[mySQL] \n
host = localhost \n
user = guest \n
password = root \n
database = znes \n
 \n
[SectionName] \n
OptionName = value \n
Option2 = value2 \n


"""
import os.path as path

try:
    import configparser as cp
except:
    # to be compatible with Python2.7
    import ConfigParser as cp

FILENAME = 'config.ini'
FILE = path.join(path.expanduser("~"), '.oemof', FILENAME)

cfg = cp.RawConfigParser()
_loaded = False


def main():
    pass


def init():
    try:
        cfg.read(FILE)
        global _loaded
        _loaded = True
    except:
        print("configfile not found.")


def get(section, key):
    """
    returns the value of a given key of a given section of the main
    config file.

    :param section: the section.
    :type section: str.
    :param key: the key.
    :type key: str.

    :returns: the value which will be casted to float, int or boolean.
              if no cast is successfull, the raw string will be returned.

    """
    if not _loaded:
        init()
    try:
        return cfg.getfloat(section, key)
    except Exception:
        try:
            return cfg.getint(section, key)
        except:
            try:
                return cfg.getboolean(section, key)
            except:
                return cfg.get(section, key)


def set(section, key, value):
    """
    sets a value to a [section] key - pair.
    if the section doesn't exist yet, it will be created.

    :param section: the section.
    :type section: str.
    :param key: the key.
    :type key: str.
    :param value: the value.
    :type value: float, int, str.
    """

    if not _loaded:
        init()

    if not cfg.has_section(section):
        cfg.add_section(section)

    cfg.set(section, key, value)

    with open(FILE, 'w') as configfile:
        cfg.write(configfile)

if __name__ == "__main__":
    main()
