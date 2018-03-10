# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/facades.py

SPDX-License-Identifier: GPL-3.0-or-later
"""
from oemof.solph import Source, Flow, Investment, NonConvex


class Generator(Source):
    """
    """
    def __init__(self, **kwargs):
        super().__init__()

        self.Pmax = kwargs.get('Pmax', None)

        self.Pmin = kwargs.get('Pmin', None)

        self.bus = kwargs.get('bus', None)

        self.opex = kwargs.get('opex', 0)

        self.capex = kwargs.get('capex', None)

        # TODO: set summed_min / max correct for fullloadhours
        # self.flh = kwargs.get('flh', (None, None))

        if self.Pmax is not None:
            if self.capex is None:
                msg = ("If you don't set `Pmax`, you need to set attribute " +
                       "`capex` of component {}!")
                raise ValueError(msg.format(self.label))
            else:
                # TODO: calculate ep_costs from specific capex
                investment = Investment(ep_costs=self.capex)
        else:
            investment = None

        if self.Pmin is not None:
            nonconvex = NonConvex()
        else:
            nonconvex = None

        #
        self.outputs.update({self.bus: Flow(nominal_value=self.Pmax,
                                            variable_costs=self.opex,
                                            investment=investment,
                                            nonconvex=nonconvex)})
