# -*- coding: utf-8 -*-

"""
General description
-------------------

A basic example to show how to get the dual variables from the system. Try
to understand the plot.

Code
----
Download source code: :download:`dual_variable_example.py
</../examples/dual_variable_example/dual_variable_example.py>`

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

from oemof.solph import Facade


class DSO(Facade):
    def __init__(self, label, el_bus, *args, energy_price, feedin_tariff):
        self.energy_price = energy_price
        self.feedin_tariff = feedin_tariff
        self.el_bus = el_bus
        super().__init__(*args, label=label, facade_type=type(self))

    def define_subnetwork(self):
        internal_bus = self.subnode(Bus, local_name="internal_bus")

        self.subnode(
            Converter,
            inputs={self.el_bus: Flow(variable_costs=self.feedin_tariff * -1)},
            outputs={internal_bus: Flow()},
            local_name="feedin_converter",
        )
        self.subnode(
            Sink, inputs={internal_bus: Flow()}, local_name="feedin_sink"
        )

        self.subnode(
            Converter,
            inputs={internal_bus: Flow()},
            outputs={self.el_bus: Flow(variable_costs=self.energy_price)},
            local_name="consumption_converter",
        )

        self.subnode(
            Source,
            outputs={internal_bus: Flow()},
            local_name="consumption_source",
        )
