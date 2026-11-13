# -*- coding: utf-8 -*-

"""linopy builder for the bus balance.

SPDX-License-Identifier: MIT
"""

from oemof.solph._linopy._indexing import ragged_sum
from oemof.solph._linopy._registry import register_builder
from oemof.solph.buses._bus import BusBlock


@register_builder(BusBlock)
def build_bus_balance(model, group):
    """Balance of every bus: sum of inflows == sum of outflows.

    As in the Pyomo block, the constraint is written as inflows - outflows
    == 0, so that the duals have the same sign. Buses without any flow get
    no constraint.
    """
    buses, rows = [], []
    for bus in group:
        row = [(model.flow_position(i, bus), 1.0) for i in bus.inputs]
        row += [(model.flow_position(bus, o), -1.0) for o in bus.outputs]
        if row:
            buses.append(bus)
            rows.append(row)
    if not buses:
        return
    lhs = ragged_sum(
        model.linopy,
        model.flow.labels.values,
        rows,
        "bus",
        tail_dims=("timestep",),
    )
    model.add_constraints("BusBlock.balance", lhs, "=", 0)
    model.balance_buses = buses
