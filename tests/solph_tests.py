from nose.tools import ok_, eq_

from oemof.energy_system import EnergySystem as ES
from oemof.solph.blocks import InvestmentFlow as IF
from oemof.solph.network import Investment
import oemof.solph as solph


class Grouping_Tests:

    def setup(self):
        self.es = ES(groupings=solph.GROUPINGS)

    def test_investment_flow_grouping(self):
        """ Flows of investment sink should be grouped.

        The constraint tests uncovered a spurious error where the flows of an
        investment `Sink` where not put into the `InvestmentFlow` group,
        although the corresponding grouping was present in the energy system.
        The error occured in the case where the investment `Sink` was not
        instantiated directly after the `Bus` it is connected to.

        This test recreates this error scenario and makes sure that the
        `InvestmentFlow` group is not empty.
        """

        b = solph.Bus(label='Bus')

        solph.Source(label='Source', outputs={b: solph.Flow(
            actual_value=[12, 16, 14], nominal_value=1000000,
            fixed=True, fixed_costs=20)})

        solph.Sink(label='Sink', inputs={b: solph.Flow(
            summed_max=2.3, variable_costs=25, max=0.8,
            investment=Investment(ep_costs=500, maximum=10e5))})

        ok_(self.es.groups.get(IF),
            ("Expected InvestmentFlow group to be nonempty.\n" +
             "Got: {}").format(self.es.groups.get(IF)))

