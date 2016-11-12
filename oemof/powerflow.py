# -*- coding: utf-8 -*-
"""

Open questions:
 - We usually have transformers for lines. We need to decide where to put
   physical properties of the pypsa line (node, inflow or ouflow?).


"""
import network
import energy_system
import pypsa

class EnergySystem(energy_system.EnergySystem):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        self.network = pypsa.Network()


    def populate_network(self):
        """
        """

        for n in self.groups.get(Bus, []):
            self.network.add('Bus', n.label)

        for n in self.groups.get(Line, []):
            self.network.add('Line', n.label,
                             bus0=list(n.inputs.keys())[0].label,
                             bus1=list(n.outputs.keys())[0].label,
                             x=n.reactance)
        for n in self.groups.get(Generator, []):
            # get the output bus
            out = list(n.outputs.keys())[0]
            self.network.add('Generator', n.label,
                             bus=out.label,
                             p_nom=n.outputs[out].nominal_value,
                             marginal_cost=n.outputs[out].variable_costs)

        for n in self.groups.get(Demand, []):
            # get the output bus
            k = list(n.inputs.keys())[0]
            self.network.add('Load', n.label,
                             bus=k.label,
                             p_set=n.inputs[k].nominal_value)


class Flow:
    """
    """
    def __init__(self, *args, **kwargs):
        self.nominal_value = kwargs.get('nominal_value', 1)
        self.variable_costs = kwargs.get('variable_costs', 0)


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



class Generator(network.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(self, *args, **kwargs)



class Demand(network.Sink):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(self, *args, **kwargs)


def node_grouping(node):
    """
    """
    if isinstance(node, Bus):
        return Bus
    if isinstance(node, Demand):
        return Demand
    if isinstance(node, Generator):
        return Generator
    if isinstance(node, Line):
        return Line


if __name__ == "__main__":
    GROUPINGS = [node_grouping]
    es = EnergySystem(groupings=GROUPINGS)
    # do not now why this must be added explicitly, usally it should work
    # without explicit adding
    es.add(Bus(label='Coal'))

    for i in range(3):
        es.add(Bus(label="My Bus {}".format(i)))

    for i in range(3):
        es.add(Line(label='My Line {}'.format(i), reactance=10+i,
                    inputs={
                        es.groups['My Bus {}'.format(i)]: Flow()},
                    outputs={
                        es.groups['My Bus {}'.format((i+1)%3)]: Flow()}
                    )
                )
    es.add(Generator(label='My gen 0',
                     inputs={
                         es.groups['Coal']: Flow()},
                     outputs={
                         es.groups['My Bus 0']: Flow(nominal_value=100,
                                                     variable_costs=50)}
                     )
                )
    es.add(Demand(label='My load 0',
                  inputs={
                      es.groups['My Bus 2']: Flow(nominal_value=100)},
                  outputs={}
                     )
                )

    es.populate_network()
