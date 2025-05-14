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
    def __init__(self, label, el_bus, *args, energy_price, feedin_tariff):
        super().__init__(*args, label=label)
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
            label="feedin_converter",
        )
        sink = Sink(inputs={internal_bus: Flow()}, label="feedin_sink")
        self.add_subnode(sink, feedin)

        bus_c = Bus()
        consumption = Converter(
            inputs={bus_c: Flow()},
            outputs={self.el_bus: Flow(variable_costs=self.energy_price)},
            label="consumption_converter",
        )
        source = Source(
            outputs={internal_bus: Flow()}, label="consumption_sink"
        )
        self.add_subnode(source, consumption)


# class CriticalDemand(Facade):
#     """
#     Defines a non dispatchable sink to serve critical and non-critical demand.
#
#     See :py:func:`~.sink` for more information, including parameters.
#
#     Notes
#     -----
#     Tested with:
#     - test_sink_non_dispatchable_single_input_bus()
#     - test_sink_non_dispatchable_multiple_input_busses()
#
#     Returns
#     -------
#     Indirectly updated `model` and dict of asset in `kwargs` with the sink
#     object.
#
#     """
#
#     # sink_non_dispatchable(model, dict_asset, **kwargs)
#
#     def __init__(
#         self, name, el_bus, demand_reduction_factor, total_demand, *args
#     ):
#         super().__init__(*args, name=name)
#         self.facade_type = "dso"
#         self.demand_reduction_factor = demand_reduction_factor
#         self.total_demand = total_demand
#
#         self.el_bus = el_bus
#
#     def build_subnetwork(self):
#
#         demand_reduction_factor = 1 - dict_asset[EFFICIENCY][VALUE]
#         tot_demand = dict_asset[TIMESERIES]
#         non_critical_demand_ts = tot_demand * demand_reduction_factor
#         non_critical_demand_peak = non_critical_demand_ts.max()
#         if non_critical_demand_peak == 0:
#             max_non_critical = 1
#         else:
#             max_non_critical = (
#                 non_critical_demand_ts / non_critical_demand_peak
#             )
#         critical_demand_ts = tot_demand * dict_asset[EFFICIENCY][VALUE]
#
#         # # check if the sink has multiple input busses
#         # if isinstance(dict_asset[INFLOW_DIRECTION], list):
#         #     pass
#         #     # inputs_noncritical = {}
#         #     # inputs_critical = {}
#         #     # index = 0
#         #     # for bus in dict_asset[INFLOW_DIRECTION]:
#         #     #     inputs_critical[kwargs[OEMOF_BUSSES][bus]] = solph.Flow(
#         #     #         fix=dict_asset[TIMESERIES], nominal_value=1
#         #     #     )
#         #     #     index += 1
#         # else:
#         #     inputs_noncritical = {
#         #         kwargs[OEMOF_BUSSES][dict_asset[INFLOW_DIRECTION]]: solph.Flow(
#         #             min=0,
#         #             max=max_non_critical,
#         #             nominal_value=non_critical_demand_peak,
#         #             variable_costs=-1e-15,
#         #         )
#         #     }
#         #     inputs_critical = {
#         #         kwargs[OEMOF_BUSSES][dict_asset[INFLOW_DIRECTION]]: solph.Flow(
#         #             fix=critical_demand_ts, nominal_value=1
#         #         )
#         #     }
#
#         non_critical_demand = Sink(
#             inputs={
#                 self.el_bus: Flow(
#                     min=0,
#                     max=max_non_critical,
#                     nominal_value=non_critical_demand_peak,
#                     variable_costs=-1e-15,
#                 )
#             },
#         )
#         critical_demand = solph.components.Sink(
#             label=reducable_demand_name(dict_asset[LABEL], critical=True),
#             inputs=inputs_critical,
#         )
#
#         # create and add demand sink and critical demand sink
#
#         model.add(critical_demand)
#         model.add(non_critical_demand)
#         kwargs[OEMOF_SINK].update(
#             {reducable_demand_name(dict_asset[LABEL]): non_critical_demand}
#         )
#         kwargs[OEMOF_SINK].update(
#             {
#                 reducable_demand_name(
#                     dict_asset[LABEL], critical=True
#                 ): critical_demand
#             }
#         )
#         logging.debug(
#             f"Added: Reducable Non-dispatchable sink {dict_asset[LABEL]} to bus {dict_asset[INFLOW_DIRECTION]}"
#         )
