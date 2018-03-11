# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/facades.py

SPDX-License-Identifier: GPL-3.0-or-later
"""
from oemof.solph import Source, Flow, Investment, Sink, Transformer
from oemof.solph.components import GenericStorage
from oemof.solph.custom import Link
from oemof.solph.plumbing import sequence


class Facade:
    """
    """
    def __init__():
        pass

    def _investment(self):
        if self.capacity is None:
            if self.capex is None:
                msg = ("If you don't set `capacity`, you need to set attribute " +
                       "`capex` of component {}!")
                raise ValueError(msg.format(self.label))
            else:
                # TODO: calculate ep_costs from specific capex
                investment = Investment(ep_costs=self.capex)
        else:
            investment = None

        return investment

class Generator(Source, Facade):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bus = kwargs.get('bus', None)

        self.capacity = kwargs.get('capacity', None)

        self.dispatchable = kwargs.get('dispatchable', True)

        self.profile = kwargs.get('profile', None)

        self.opex = kwargs.get('opex', 0)

        self.capex = kwargs.get('capex', None)

        investment = self._investment()

        self.outputs.update({self.bus: Flow(nominal_value=self.capacity,
                                            variable_costs=self.opex,
                                            actual_value=self.profile,
                                            investment=investment,
                                            fixed=not self.dispatchable)})


class CHP(Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bus_fuel = kwargs.get('bus_fuel', None)

        self.bus_th = kwargs.get('bus_th', None)

        self.bus_el = kwargs.get('bus_el', None)

        self.capacity = kwargs.get('capacity', None)

        self.eta_el = kwargs.get('eta_el', None)

        self.eta_th = kwargs.get('eta_th', None)

        self.opex = kwargs.get('opex', None)

        self.conversion_factors.update({
            self.bus_el: sequence(self.eta_el),
            self.bus_th: sequence(self.eta_th)})

        self.inputs.update({
            self.bus_fuel: Flow()})

        self.outputs.update({
            self.bus_el: Flow(nominal_value=self.capacity,
                              variable_costs=self.opex),
            self.bus_th: Flow()})


class Demand(Sink):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.amount = kwargs.get('amount', None)

        self.bus = kwargs.get('bus', None)

        self.profile = kwargs.get('profile', None)

        self.inputs.update({self.bus: Flow(nominal_value=self.amount,
                                           actual_value=self.profile,
                                           fixed=True, **kwargs)})


class Storage(GenericStorage, Facade):
    """
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.capacity = kwargs.get('capacity')

        self.nominal_capacity = self.capacity

        self.nominal_input_capacity_ratio = kwargs.get('c_rate', 1/6)

        self.nominal_output_capacity_ratio = kwargs.get('c_rate', 1/6)

        self.capex = kwargs.get('capex')

        self.bus = kwargs.get('bus')

        self.investment = self._investment()

        if self.investment:
            investment = Investment()
        else:
            investment = None
        self.inputs.update({self.bus: Flow(investment=investment)})

        self.outputs.update({self.bus: Flow(investment=investment)})


class Connector(Link, Facade):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.from_bus = kwargs.get('from_bus')

        self.capacity = kwargs.get('capacity')

        self.to_bus = kwargs.get('to_bus')

        self.loss = kwargs.get('loss')

        self.capex = kwargs.get('capex')

        investment = self._investment()

        self.inputs.update({
            self.from_bus: Flow(),
            self.to_bus: Flow()})

        self.outputs.update({
            self.from_bus: Flow(nominal_value=self.capacity,
                                investment=investment),
            self.to_bus: Flow(nominal_value=self.capacity,
                              investment=investment)})

        self.conversion_factors.update({
            (self.from_bus, self.to_bus): sequence((1 - self.loss)),
            (self.to_bus, self.from_bus): sequence((1 - self.loss))})
