# -*- coding: utf-8 -*-

"""
General description
-------------------

A basic example to show how to get the dual variables from the system. Try
to understand the plot.

Code
----
Download source code: :download:`dual_variable_example.py </../examples/dual_variable_example/dual_variable_example.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/dual_variable_example/dual_variable_example.py
        :language: python
        :lines: 34-297


Installation requirements
-------------------------

This example requires the version v0.6.x of oemof.solph:

.. code:: bash

    pip install 'oemof.solph[examples]>=0.6,<0.7'

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Pierre-François Duc

SPDX-License-Identifier: MIT
"""

from oemof.solph.components import Converter, Source, Sink
from oemof.solph.flows import Flow
from oemof.solph.buses import Bus

from oemof.solph._facades import Facade

class DSO(Facade):
    def __init__(self,label, el_bus, *args, energy_price, feedin_tariff):
        super().__init__(*args,label=label)
        self.facade_type = "dso"
        self.energy_price = energy_price
        self.feedin_tariff = feedin_tariff

        self.el_bus = el_bus
    def build_subnetwork(self):
        internal_bus = Bus(label="internal_bus")
        self.add_subnode(internal_bus)

        feedin = Converter(
            inputs={self.el_bus: Flow(variable_costs=self.feedin_tariff)},
            outputs={internal_bus: Flow()},
            label="feedin_converter"
        )
        sink = Sink(inputs={internal_bus: Flow()}, label="feedin_sink")
        self.add_subnode(sink, feedin)

        bus_c = Bus()
        consumption = Converter(
            inputs={bus_c: Flow()},
            outputs={self.el_bus: Flow(variable_costs=self.energy_price)},
            label="consumption_converter"
        )
        source = Source(outputs={internal_bus: Flow()}, label="consumption_sink")
        self.add_subnode(source, consumption)


