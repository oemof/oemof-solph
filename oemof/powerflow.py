# -*- coding: utf-8 -*-
"""

Open questions:
 - We usually have transformers for lines. We need to decide where to put
   physical properties of the pypsa line (node, inflow or ouflow?).
 - How do we differentiate between 'carrier' and 'bus' ? do we use ElectricalBus
 - If we had HUB, this would be easier: Hub -> Bus, Hub -> CommodityHub
 - Creating generator as source? would be enough for pyPSA, but we should
   probably stick with transformer
 - How do we handle timeseries? Especially multiplication of normed values
   with absolute value for specific pypsa attributes ?

oemof feedback questions
 - Why does the energysystem not hold the optimization model? I think it might
   make sense to put it together etc.

"""
import network
import energy_system
from solph import Investment
from oemof.solph.plumbing import Sequence
import pypsa

class EnergySystem(energy_system.EnergySystem):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        self.timeindex = kwargs.get('timeindex')

    def _create_network(self):
        self.network = pypsa.Network()
        if self.timeindex is not None:
            self.network.set_snapshots(self.timeindex)

    def _populate_network(self):
        """
        """
        for n in self.groups.get(Bus, []):
            self.network.add('Bus', n.label)

        for n in self.groups.get(Line, []):
            self.network.add('Line', n.label,
                             bus0=list(n.inputs.keys())[0].label,
                             bus1=list(n.outputs.keys())[0].label,
                             x=n.reactance,
                             s_nom=list(n.outputs.values())[0].nominal_value)

        for n in self.groups.get(Generator, []):
            # get the output bus
            out = list(n.outputs.keys())[0]
            self.network.add('Generator', n.label,
                             bus=out.label,
                             p_nom=n.outputs[out].nominal_value,
                             marginal_cost=n.outputs[out].variable_costs)

        for n in self.groups.get(Demand, []):
            # get the output bus
            b = list(n.inputs.keys())[0]
            # this works but we need to make that better because otherwise
            # we loop a lot everywhere
            p_set = [n.inputs[b].actual_value[t] * n.inputs[b].nominal_value
                     for t in range(len(self.timeindex))]

            self.network.add('Load', n.label,
                             bus=b.label,
                             p_set=p_set)

        for n in self.groups.get(Storage, []):
            if isinstance(n.investment, Investment) :
                invest = True
            else:
                invest = False
            b = list(n.outputs.keys())[0]

            self.network.add("Store", n.label,
                             bus=b.label,
                             e_nom = n.nominal_capacity,
                             e_cyclic=True,  # Whats this for ????
                             e_nom_extendable=invest,
                             standing_loss=n.capacity_loss,
                             capital_cost=n.investment.ep_costs)

    def linear_optimal_power_flow(self):
        """
        This mehtod will take the oemof object and fill the pypsa network
        to perform
        """
        # where can we put this?

        self.generators = {(source.label, target.label): source.outputs[target]
                           for source in es.groups[Generator]
                           for target in source.outputs}
        self._create_network()
        self._populate_network()
        self.network.lopf()

        # TODO: extract pyomo model results to produc
        # 'standard oemof result dict'
        self.lopf_results = {}

class Flow:
    """
    """
    def __init__(self, *args, **kwargs):
        self.nominal_value = kwargs.get('nominal_value', 1)
        self.variable_costs = kwargs.get('variable_costs', 0)
        self.actual_value = kwargs.get('actual_value', Sequence(1))

class Bus(network.Bus):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)


class Line(network.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        self.reactance = kwargs.get('reactance')


class Storage(network.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        self.nominal_capacity = kwargs.get('nominal_capacity', 0.0)
        self.capacity_loss = kwargs.get('capacity_loss', 0.0)
        self.investment = kwargs.get('investment', False)

class Generator(network.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(self, *args, **kwargs)
        self.conversion_factors = {
            k: v
            for k, v in kwargs.get('conversion_factors', {}).items()}

class Demand(network.Sink):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(self, *args, **kwargs)

# just for now, we wil have commitybus or something similar later
commodities = ['Coal', 'gas', 'lignite']
def node_grouping(node):
    """
    """
    if isinstance(node, Bus) and node.label not in commodities:
        return Bus
    if isinstance(node, Demand):
        return Demand
    if isinstance(node, Generator):
        return Generator
    if isinstance(node, Line):
        return Line
    if isinstance(node, Storage):
        return Storage


if __name__ == "__main__":
    import pandas as pd

    GROUPINGS = [node_grouping]
    es = EnergySystem(groupings=GROUPINGS,
                      timeindex=pd.date_range('2014', periods=3, freq='H'))
    # do not now why this must be added explicitly, usally it should work
    # without explicit adding
    es.add(Bus(label='Coal'))

    for i in range(3):
        es.add(Bus(label="My Bus {}".format(i)))

    for i in range(3):
        es.add(Line(label='My Line {}'.format(i), reactance=0.001,
                    inputs={
                        es.groups['My Bus {}'.format(i)]: Flow()},
                    outputs={
                        es.groups['My Bus {}'.format((i+1)%3)]:
                            Flow(nominal_value=60)}
                    )
                )
    es.add(Generator(label='My gen 0',
                     inputs={
                         es.groups['Coal']: Flow()},
                     outputs={
                         es.groups['My Bus 0']: Flow(nominal_value=100,
                                                     variable_costs=50)},
                     conversion_factors = {es.groups['My Bus 0']: 0.4}
                     )
                )
    es.add(Generator(label='My gen 1',
                     inputs={
                         es.groups['Coal']: Flow()},
                     outputs={
                         es.groups['My Bus 1']: Flow(nominal_value=100,
                                                     variable_costs=25)}
                     )
                )
    es.add(Storage(label='My stor 1',
                     inputs={
                         es.groups['My Bus 0']: Flow()},
                     outputs={
                         es.groups['My Bus 0']: Flow(variable_costs=25)},
                     nominal_capacity = 1,
                     capacity_loss  = 0.009,
                     investment = Investment(ep_costs=10)
                     )
                )
    es.add(Demand(label='My load 0',
                  inputs={
                      es.groups['My Bus 2']: Flow(nominal_value=100,
                                                  actual_value=[0.1, 0.3, 0.4])},
                  outputs={}
                     )
                )
    #es._create_network()
    #es._populate_network()
    es.linear_optimal_power_flow()

    print(es.network.generators_t.p)
