# -*- coding: utf-8 -*-
""" This module is desined to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application.
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
