# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/facades.py

SPDX-License-Identifier: GPL-3.0-or-later
"""
from oemof.solph import Source, Flow, Investment, Sink, Transformer, Bus
from oemof.solph.components import GenericStorage
from oemof.solph.custom import Link
from oemof.solph.plumbing import sequence


class Facade:
    """
    """
    def __init__(**kwargs):
        pass

    def __str__(self):
        return self.__name__
        
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


class Reservoir(GenericStorage, Facade):
    """ Reservoir storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    capacity: numeric
        The total capacity of the storage (e.g. in MWh)
    inflow: array-like
        Absolute profile of water inflow into the storage
    investment_cost: numeric
        Investment costs for the storage capacity! unit e.g in €/MW-capacity
    spillage: boolean
        If True, spillage of water will be possible, otherwise water is forced
        to storage. Default: True
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.capacity = kwargs.get('capacity')

        self.nominal_capacity = self.capacity

        self.investment_cost = kwargs.get('investment_cost')

        self.bus = kwargs.get('bus')

        self.inflow = kwargs.get('inflow')

        self.spillage = kwargs.get('spillage', True)

        self.investment = self._investment()

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})

        if self.investment:
            investment = Investment()
        else:
            investment = None

        # TODO: Ensure automatic adding of
        water = Bus(label="water-bus")
        water_inflow = Source(
            label='water-inflow',
            outputs={
                water: Flow(nominal_value=max(self.inflow),
                            #i/max(self.inflow) for i in self.inflow
                            actual_value=[1])})
        if self.spillage:
            water_spillage = Sink(label='water-spillage',
                                  inputs={water: Flow()})
        else:
            water_spillage = None

        self.inputs.update({water: Flow(investment=investment,
                                        **self.input_edge_parameters)})

        self.outputs.update({self.bus: Flow(investment=investment,
                                            **self.output_edge_parameters)})

        self.subnodes = (water, water_inflow, water_spillage)



class Generator(Source, Facade):
    """ Generator unit with one output, e.g. gas-turbine, wind-turbine, etc.

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the generator is connected to
    capacity: numeric
        The capacity of the generator (e.g. in MW).
    dispatchable: boolean
        If False the generator will be must run based on the specified
        `profile` and (default is True).
    profile: array-like
        Profile of the output such that profile[t] * capacity yields output for
        timestep t
    marginal_cost: numeric
        Marginal cost for one unit of produced output
        E.g. for a powerplant:
        marginal cost =fuel cost + operational cost + co2 cost (in Euro / MWh)
        if timestep length is one hour.
    investment_cost: numeric
        Investment costs per unit of capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        generators capacity.
    amount: numeric
        Total amount of produced energy for the time horizon of the model e.G.
        in MWh (optional). Note: Either set `amount` or `capacity`!
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bus = kwargs.get('bus', None)

        self.capacity = kwargs.get('capacity', None)

        self.amount = kwargs.get('amount', None)

        if self.capacity and not self.amount:
            nominal_value = self.capacity
        elif self.amount and not self.capacity:
            nominmal_value = self.amount
        else:
            msg = ("Either set the capacity OR the amount for the generator" +
                  " with name {}!")
            raise ValueError(msg.format(self.label))

        self.dispatchable = kwargs.get('dispatchable', True)

        self.profile = kwargs.get('profile', None)

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.investment_cost = kwargs.get('investment_cost', None)

        self.edge_parameters = kwargs.get('edge_parameters', {})

        investment = self._investment()

        f = Flow(nominal_value=nominal_value,
                 variable_costs=self.marginal_cost,
                 actual_value=self.profile,
                 investment=investment,
                 fixed=not self.dispatchable,
                 **self.edge_parameters)

        self.outputs.update({self.bus: f})


class CHP(Transformer):
    """ Combined Heat and Power (backpressure) unit with one input and
    two outputs.

    Parameters
    ----------
    bus_el: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        electrical output
    bus_th: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        thermal output
    bus_fuel: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        intput
    capacity: numeric
        The electrical capacity of the chp unit (e.g. in MW).
    efficiency_el:
        Electrical efficiency of the chp unit
    efficiency_th
        Thermal efficiency of the chp unit
    marginal_cost: numeric
        Marginal cost for one unit of produced electrical output
        E.g. for a powerplant:
        marginal cost =fuel cost + operational cost + co2 cost (in Euro / MWh)
        if timestep length is one hour.
    investment_cost: numeric
        Investment costs per unit of electrical capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bus_fuel = kwargs.get('bus_fuel', None)

        self.bus_th = kwargs.get('bus_th', None)

        self.bus_el = kwargs.get('bus_el', None)

        self.capacity = kwargs.get('capacity', None)

        self.efficiency_el = kwargs.get('efficiency_el', None)

        self.efficiency_th = kwargs.get('efficiency_th', None)

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.investment_cost = kwargs.get('investment_cost', None)

        investment = self._investment()

        self.conversion_factors.update({
            self.bus_el: sequence(self.efficiency_el),
            self.bus_th: sequence(self.efficiency_th)})

        self.inputs.update({
            self.bus_fuel: Flow()})

        self.outputs.update({
            self.bus_el: Flow(nominal_value=self.capacity,
                              variable_costs=self.marginal_cost,
                              investment=investment),
            self.bus_th: Flow()})


class Conversion(Transformer, Facade):
    """ Conversion unit with one input and one output.

    Parameters
    ----------
    from_bus: oemof.solph.Bus
        An oemof bus instance where the conversion unit is connected to with
        its input.
    to_bus: oemof.solph.Bus
        An oemof bus instance where the conversion unit is connected to with
        its output.
    capacity: numeric
        The conversion capacity (output side) of the unit.
    efficiency:
        Efficiency of the conversion unit (0 <= efficiency <= 1).
    marginal_cost: numeric
        Marginal cost for one unit of produced output.
    investment_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
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
            self.from_bus: sequence(1),
            self.to_bus: sequence(self.efficiency)})

        self.inputs.update({
            self.from_bus: Flow(**self.input_edge_parameters)})

        self.outputs.update({
            self.to_bus: Flow(nominal_value=self.capacity,
                              variable_costs=self.marginal_cost,
                              **self.output_edge_parameters)})


class Demand(Sink):
    """ Demand object with one input

     Parameters
     ----------
     bus: oemof.solph.Bus
         An oemof bus instance where the demand is connected to.
     amount: numeric
         The total amount for the timehorzion (e.g. in MWh)
     profile: array-like
          Demand profile with normed values such that `profile[t] * amount`
          yields the demand in timestep t
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
    """ Storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    capacity: numeric
        The total capacity of the storage (e.g. in MWh)
    c_rate: numeric
        Ratio between energy and power output of the storage
    investment_cost: numeric
        Investment costs for the storage unit e.g in €/MW-capacity
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
    """ Bi-direction connection for two buses (e.g. to model transshipment)

    Parameters
    ----------
    from_bus: oemof.solph.Bus
        An oemof bus instance where the connection unit is connected to with
        its input.
    to_bus: oemof.solph.Bus
        An oemof bus instance where the connection unit is connected to with
        its output.
    capacity: numeric
        The maximal capacity (output side each) of the unit.
    loss:
        Relative loss through the connection
    investment_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
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
