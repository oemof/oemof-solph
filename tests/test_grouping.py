# -*- coding: utf-8 -

"""Grouping tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/solph_tests.py

SPDX-License-Identifier: MIT
"""

from oemof.network.energy_system import EnergySystem as EnSys

from oemof import solph as solph
from oemof.solph import Investment
from oemof.solph.flows._investment_flow_block import InvestmentFlowBlock


class TestsGrouping:
    def setup_method(self):
        self.es = EnSys(groupings=solph.GROUPINGS)

    def test_investment_flow_grouping(self):
        """Flows of investment sink should be grouped.

        The constraint tests uncovered a spurious error where the flows of an
        investment `Sink` where not put into the `InvestmentFlow` group,
        although the corresponding grouping was present in the energy system.
        The error occured in the case where the investment `Sink` was not
        instantiated directly after the `Bus` it is connected to.

        This test recreates this error scenario and makes sure that the
        `InvestmentFlow` group is not empty.
        """

        b = solph.buses.Bus(label="Bus")
        self.es.add(b)

        self.es.add(
            solph.components.Source(
                label="Source",
                outputs={
                    b: solph.flows.Flow(
                        fix=[12, 16, 14], nominal_capacity=1000000
                    )
                },
            )
        )

        self.es.add(
            solph.components.Sink(
                label="Sink",
                inputs={
                    b: solph.flows.Flow(
                        full_load_time_max=2.3,
                        variable_costs=25,
                        max=0.8,
                        nominal_capacity=Investment(
                            ep_costs=500, maximum=10e5
                        ),
                    )
                },
            )
        )

        assert self.es.groups.get(InvestmentFlowBlock), (
            "Expected InvestmentFlow group to be nonempty.\n"
            + "Got: {}".format(self.es.groups.get(InvestmentFlowBlock))
        )
