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
    def __init__(**kwargs):
        pass

    def _investment(self):
        if self.capacity is None:
            if self.investment_cost is None:
                msg = ("If you don't set `capacity`, you need to set attribute " +
                       "`investment_cost` of component {}!")
                raise ValueError(msg.format(self.label))
            else:
                # TODO: calculate ep_costs from specific capex
                investment = Investment(ep_costs=self.investment_cost)
        else:
            investment = None

        return investment


class Generator(Source, Facade):
    """
    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the generator is connected to
    capacity: numeric
        The capacity of the generator (e.g. in MW).
    dispatchable: boolean
        If False the generator will be must run based on the specified
        `profile` and (default is True).
    marginal_cost: numeric
        Marginal cost for one unit of produced output
        E.g. for a powerplant:
        marginal cost =fuel cost + operational cost + co2 cost (in Euro / MWh)
        if timestep length is one hour.
    investment_cost: numeric
        Investment costs per unit of capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        generators capacity.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bus = kwargs.get('bus', None)

        self.capacity = kwargs.get('capacity', None)

        self.dispatchable = kwargs.get('dispatchable', True)

        self.profile = kwargs.get('profile', None)

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.investment_cost = kwargs.get('investment_cost', None)

        self.edge_parameters = kwargs.get('edge_parameters', {})

        investment = self._investment()

        f = Flow(nominal_value=self.capacity,
                 variable_costs=self.marginal_cost,
                 actual_value=self.profile,
                 investment=investment,
                 fixed=not self.dispatchable,
                 **self.edge_parameters)

        self.outputs.update({self.bus: f})


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

        self.maringal_cost = kwargs.get('maringal_cost', None)

        self.conversion_factors.update({
            self.bus_el: sequence(self.eta_el),
            self.bus_th: sequence(self.eta_th)})

        self.inputs.update({
            self.bus_fuel: Flow()})

        self.outputs.update({
            self.bus_el: Flow(nominal_value=self.capacity,
                              variable_costs=self.marginal_cost),
            self.bus_th: Flow()})


class Conversion(Transformer, Facade):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.capacity = kwargs.get('capacity')

        self.from_bus = kwargs.get('from_bus')

        self.to_bus = kwargs.get('to_bus')

        self.efficiency = kwargs.get('efficiency', 1)

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.investment_cost = kwargs.get('investment_cost', None)

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})

        investment = self._investment()

        self.conversion_factors.update({
            self.to_bus: sequence(self.efficiency)})

        self.inputs.update({
            self.from_bus: Flow(**self.input_edge_parameters)})

        self.outputs.update({
            self.to_bus: Flow(nominal_value=self.capacity,
                              variable_costs=self.marginal_cost,
                              **self.output_edge_parameters)})


class Demand(Sink):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.amount = kwargs.get('amount', None)

        self.bus = kwargs.get('bus', None)

        self.profile = kwargs.get('profile', None)

        self.edge_parameters = kwargs.get('edge_parameters', {})

        self.inputs.update({self.bus: Flow(nominal_value=self.amount,
                                           actual_value=self.profile,
                                           fixed=True,
                                           **self.edge_parameters)})


class Storage(GenericStorage, Facade):
    """
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.capacity = kwargs.get('capacity')

        self.nominal_capacity = self.capacity

        self.nominal_input_capacity_ratio = kwargs.get('c_rate', 1/6)

        self.nominal_output_capacity_ratio = kwargs.get('c_rate', 1/6)

        self.investment_cost = kwargs.get('investment_cost')

        self.bus = kwargs.get('bus')

        self.investment = self._investment()

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})

        if self.investment:
            investment = Investment()
        else:
            investment = None

        self.inputs.update({self.bus: Flow(investment=investment,
                                            **self.input_edge_parameters)})

        self.outputs.update({self.bus: Flow(investment=investment,
                                            **self.output_edge_parameters)})


class Connection(Link, Facade):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.from_bus = kwargs.get('from_bus')

        self.capacity = kwargs.get('capacity')

        self.to_bus = kwargs.get('to_bus')

        self.loss = kwargs.get('loss')

        self.investment_cost = kwargs.get('investment_cost')

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
