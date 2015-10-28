# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""
import logging
import pandas as pd
import calendar

from . import energy_weather as w
from . import energy_power_plants as pp
from .. tools import helpers

from feedinlib import powerplants as plants
from feedinlib import models
from matplotlib import pyplot as plt
from descartes import PolygonPatch


class region2solph():
    r"""A class to define a region of an energy system.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
        (e.g. ``int``), or describe the type of the variable in more
        detail, e.g. ``(N,) ndarray`` or ``array_like``.
    Long_variable_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.

    Attributes
    ----------

    Attributes that are properties and have their own docstrings
    can be simply listed by name

    place : list of strings
        Containing the name of the state [0] and the name of the country
    weather : instance of class Weather
        Containing the weather data of all raster fields touching the region
    tz : str
        Timezone of the region
    name : str
        Name of the region. Default: 'No name'.
    year : int
        Year for the data sets of the region
    connection : sqlalchemy.connection object
        Containing a connection to an aktive database

    Other Parameters
    ----------------
    only_seldom_used_keywords : type
        Explanation
    common_parameters_listed_above : type
        Explanation

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    otherfunc : relationship (optional)
    newfunc : Relationship (optional), which could be fairly long, in which
              case the line wraps here.
    thirdfunc, fourthfunc, fifthfunc

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a greek symbol like :math:`omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a=[1,2,3]
    >>> print [x + 3 for x in a]
    [4, 5, 6]
    >>> print "a\n\nb"
    a
    b

    """

    def __init__(self, **kwargs):
        ''
        self.regions = kwargs.get('regions', None)  # list of region objects
        self.multi_geom
