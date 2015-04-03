"""
This module contains a bunch of plotters for different kinds of data.

version: 0.1

"""

import matplotlib.pyplot as plt


def simple_plot(dictionary, fields):
    """
    Plots lineplots for for a dict of timeseries.
    Provide a dictionary in the following form:
    dictionary = { "input" : {1:15, 2:23, 3:45, ...}, "output": {1:33, 2:45, 3:22, ...}, "price" : {...} }.
    and specify the fields you want to get plotted in the following way:
    fields = ["input", "output"].

    :param dictionary: the dict with the data.
    :param fields: a list of strings containing the fields to get plotted.
    """

    #TODO: label the plots with the field names
    for f in fields:
        list = [v for k,v in dictionary[f].items()]
        plt.plot(list)
    plt.show()