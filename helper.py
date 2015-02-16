"""
helper.py

This module contains a bunch of small helperclasse, functions etc., that can be used within the framework and
your applications.


"""

class Timeseries(dict):
    """
    List of timestep : value pairs for Timeseries of arbitrary data.
    Use ist just like a dictionary.
    """
    def __init__(self):
        super(Timeseries, self).__init__()