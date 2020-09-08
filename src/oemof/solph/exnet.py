# -*- coding: utf-8 -*-
'''
General description
-------------------
The goal of GasBus and GasLine is to implement a piecewise linear model.
The gas flow is the result of a pressure difference and
has a non-linear relationship.

Installation requirements
-------------------------
This example depends on an installation of oemof

02.03.2020 - philipp.gradl@stud.unileoben.ac.at
'''
from oemof.solph.network import Bus, Transformer
from pyomo.core import *


class GasBus(Bus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slack = kwargs.get('slack', False)
        self.p_max = kwargs.get('p_max', 1)
        self.p_min = kwargs.get('p_min', -1)


class GasLineBlock(SimpleBlock):
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        self.GASLINE_PL = Set(initialize=[n for n in group])

        self.GAS_BUSES = Set(initialize=[s for s in m.es.nodes
                                         if isinstance(s, GasBus)])

        self.pressure = Var(self.GAS_BUSES, m.TIMESTEPS, bounds=(0, 1))

        self.delta_pressure = Var(self.GASLINE_PL, m.TIMESTEPS, bounds=(-1, 1))

        self.energy_flow = Var(self.GASLINE_PL, m.TIMESTEPS)

        for n in self.GASLINE_PL:
            for t in m.TIMESTEPS:
                for ob in list(n.outputs.keys()):
                    if ob.slack is True:
                        self.pressure[ob, t].value = 1
                        self.pressure[ob, t].fix()

                for ob in list(n.inputs.keys()):
                    if ob.slack is True:
                        self.pressure[ob, t].value = 1
                        self.pressure[ob, t].fix()

        self.piecewise = Piecewise(self.GASLINE_PL,
                                   m.TIMESTEPS,
                                   self.energy_flow,
                                   self.delta_pressure,
                                   pw_pts=n.input_list,
                                   pw_constr_type='EQ',
                                   pw_repn='CC',
                                   f_rule=n.output_list)

        def flow_eq_pressure(block, n, t):
            expr = 0
            expr += (self.pressure[list(n.outputs.keys())[0], t] -
                     self.pressure[list(n.inputs.keys())[0], t])
            expr += self.delta_pressure[n, t]

            return expr == 0

        self.flow_eq_pressure = Constraint(self.GASLINE_PL,
                                           m.TIMESTEPS,
                                           rule=flow_eq_pressure)

        def energy_flow_out(block, n, t):
            expr = 0
            expr += - m.flow[n, list(n.outputs.keys())[0], t]
            expr += self.energy_flow[n, t]*n.K_1

            return expr == 0

        self.energy_flow_out = Constraint(self.GASLINE_PL,
                                          m.TIMESTEPS,
                                          rule=energy_flow_out)

        def energy_flow_in(block, n, t):
            expr = 0
            expr += - m.flow[list(n.inputs.keys())[0], n, t]*n.conv_factor
            expr += self.energy_flow[n, t]*n.K_1

            return expr == 0

        self.energy_flow_in = Constraint(self.GASLINE_PL,
                                         m.TIMESTEPS,
                                         rule=energy_flow_in)


class GasLine(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conv_factor = kwargs.get('conv_factor', 1)
        self.K_1 = kwargs.get('K_1')
        self.input_list = list(kwargs.get('input_list', []))
        self.output_list = list(kwargs.get('output_list', []))

    def constraint_group(self):
        return GasLineBlock
