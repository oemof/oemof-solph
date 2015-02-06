# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 14:09:06 2014

:module-author: stfn
:filename: netCDF.py


"""
print("/iolib/netcdf.py imported")

import config as cfg
#from netCDF4 import Dataset



def inspect_dataset(filename, variable=None):
    """
    let's you inspect a netCDF file: either the whole set of variables or
    a single variable. It prints out the structure of the dataset(s).
    
    :param filename: the filename. file has to be located in the netCDF folder
        specified in the config.ini.
    :type filename: string.
    :param variable: (optional) a variable name.
    :type variable: str.
    
    
    """
    nc = Dataset(cfg.get("netCDF", "root") + filename)
    
    if variable is not None:
        print nc.variables[variable]
    
    else:
        for var in nc.variables:
            print nc.variables[var]


def get_data(filename, variable=None):
    """
    extracts data from a netCDF file.
    Returns all the data for the specified variable, or the whole dataset
    if no variable is specified.
    
    Parameters
    ----------
    :param filename: the filename. file has to be located in the netCDF folder
        specified in the config.ini.
    :type filename; string.
    :param variable: (optional) a variable name.
    :type variable: string.

    see also
    --------
    :py:class:`Location`
    """
    
    nc = Dataset(cfg.get("netCDF", "root") + filename)
    
    if variable is not None:
        return nc.variables[variable]
    
    else:
        return nc


###################################################


def main():
    pass



if __name__ == "__main__":
    main()