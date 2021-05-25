# -*- coding: utf-8 -*-

"""
In-development transfomer with piecewise linar efficiencies.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: jakob-wo
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: jnnr

SPDX-License-Identifier: MIT

"""

from oemof.network import network as on
from pyomo.core.base.block import SimpleBlock
from pyomo.environ import BuildAction
from pyomo.environ import Constraint
from pyomo.environ import Piecewise
from pyomo.environ import Set
from pyomo.environ import Var


class PiecewiseLinearTransformer(on.Transformer):
    """Component to model a transformer with one input and one output
    and an arbitrary piecewise linear conversion function.

    Parameters
    ----------
    in_breakpoints : list
        List containing the domain breakpoints, i.e. the breakpoints for the
        incoming flow.

    conversion_function : func
        The function describing the relation between incoming flow and outgoing
        flow which is to be approximated.

    pw_repn : string
        Choice of piecewise representation that is passed to
        pyomo.environ.Piecewise

    Examples
    --------
    >>> import oemof.solph as solph

    >>> b_gas = solph.Bus(label='biogas')
    >>> b_el = solph.Bus(label='electricity')

    >>> pwltf = solph.custom.PiecewiseLinearTransformer(
    ...    label='pwltf',
    ...    inputs={b_gas: solph.Flow(
    ...    nominal_value=100,
    ...    variable_costs=1)},
    ...    outputs={b_el: solph.Flow()},
    ...    in_breakpoints=[0,25,50,75,100],
    ...    conversion_function=lambda x: x**2,
    ...    pw_repn='CC')

    >>> type(pwltf)
    <class 'oemof.solph.custom.piecewise_linear_transformer.\
PiecewiseLinearTransformer'>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.in_breakpoints = list(kwargs.get("in_breakpoints"))
        self.conversion_function = kwargs.get("conversion_function")
        self.pw_repn = kwargs.get("pw_repn")

        if len(self.inputs) > 1 or len(self.outputs) > 1:
            raise ValueError(
                "Component `PiecewiseLinearTransformer` cannot have "
                + "more than 1 input and 1 output!"
            )

        nominal_value = [a.nominal_value for a in self.inputs.values()][0]
        if max(self.in_breakpoints) < nominal_value:
            raise ValueError(
                "Largest in_breakpoint must be larger or equal "
                + "nominal value"
            )

    def constraint_group(self):
        return PiecewiseLinearTransformerBlock


class PiecewiseLinearTransformerBlock(SimpleBlock):
    r"""Block for the relation of nodes with type
    :class:`~oemof.solph.custom.piecewise_linear_transformer.PiecewiseLinearTransformer`

    **The following constraints are created:**

    """
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the relation for the class:`PiecewiseLinearTransformer`.

        Parameters
        ----------
        group : list
            List of oemof.solph.custom.PiecewiseLinearTransformer objects
            for which the relation of inputs and outputs is created
            e.g. group = [pwltf1, pwltf2, pwltf3, ...].

        """
        if group is None:
            return None

        m = self.parent_block()

        self.PWLINEARTRANSFORMERS = Set(initialize=[n for n in group])

        pw_repns = [n.pw_repn for n in group]
        if all(x == pw_repns[0] for x in pw_repns):
            self.pw_repn = pw_repns[0]
        else:
            print(
                "Cannot different piecewise representations ",
                [n.pw_repn for n in group],
            )

        self.breakpoints = {}

        def build_breakpoints(block, n):
            for t in m.TIMESTEPS:
                self.breakpoints[(n, t)] = n.in_breakpoints

        self.breakpoint_build = BuildAction(
            self.PWLINEARTRANSFORMERS, rule=build_breakpoints
        )

        def _conversion_function(block, n, t, x):
            expr = n.conversion_function(x)
            return expr

        # bounds are min/max of breakpoints
        lower_bound_in = {n: min(n.in_breakpoints) for n in group}
        upper_bound_in = {n: max(n.in_breakpoints) for n in group}
        lower_bound_out = {
            n: n.conversion_function(bound)
            for (n, bound) in lower_bound_in.items()
        }
        upper_bound_out = {
            n: n.conversion_function(bound)
            for (n, bound) in upper_bound_in.items()
        }

        def get_inflow_bounds(model, n, t):
            return lower_bound_in[n], upper_bound_in[n]

        def get_outflow_bounds(model, n, t):
            return lower_bound_out[n], upper_bound_out[n]

        self.inflow = Var(
            self.PWLINEARTRANSFORMERS, m.TIMESTEPS, bounds=get_inflow_bounds
        )
        self.outflow = Var(
            self.PWLINEARTRANSFORMERS, m.TIMESTEPS, bounds=get_outflow_bounds
        )

        def _in_equation(block, n, t):
            """Link binary input and output flow to component outflow."""
            expr = 0
            expr += -m.flow[list(n.inputs.keys())[0], n, t]
            expr += self.inflow[n, t]
            return expr == 0

        self.equate_in = Constraint(
            self.PWLINEARTRANSFORMERS, m.TIMESTEPS, rule=_in_equation
        )

        def _out_equation(block, n, t):
            """Link binary input and output flow to component outflow."""
            expr = 0
            expr += -m.flow[n, list(n.outputs.keys())[0], t]
            expr += self.outflow[n, t]
            return expr == 0

        self.equate_out = Constraint(
            self.PWLINEARTRANSFORMERS, m.TIMESTEPS, rule=_out_equation
        )

        self.piecewise = Piecewise(
            self.PWLINEARTRANSFORMERS,
            m.TIMESTEPS,
            self.outflow,
            self.inflow,
            pw_repn=self.pw_repn,
            pw_constr_type="EQ",
            pw_pts=self.breakpoints,
            f_rule=_conversion_function,
        )
