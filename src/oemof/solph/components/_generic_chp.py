# -*- coding: utf-8 -

"""
GenericCHP and associated individual constraints (blocks) and groupings.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: FranziPl
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: FabianTU
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

import numpy as np
from oemof.network import Node
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Binary
from pyomo.environ import Constraint
from pyomo.environ import NonNegativeReals
from pyomo.environ import Set
from pyomo.environ import Var

from oemof.solph._plumbing import sequence


class GenericCHP(Node):
    r"""
    Component `GenericCHP` to model combined heat and power plants.

    Can be used to model (combined cycle) extraction or back-pressure turbines
    and used a mixed-integer linear formulation. Thus, it induces more
    computational effort than the `ExtractionTurbineCHP` for the
    benefit of higher accuracy.

    The full set of equations is described in:
    Mollenhauer, E., Christidis, A. & Tsatsaronis, G.
    Evaluation of an energy- and exergy-based generic modeling
    approach of combined heat and power plants
    Int J Energy Environ Eng (2016) 7: 167.
    https://doi.org/10.1007/s40095-016-0204-6

    For a general understanding of (MI)LP CHP representation, see:
    Fabricio I. Salgado, P.
    Short - Term Operation Planning on Cogeneration Systems: A Survey
    Electric Power Systems Research (2007)
    Electric Power Systems Research
    Volume 78, Issue 5, May 2008, Pages 835-848
    https://doi.org/10.1016/j.epsr.2007.06.001

    Note
    ----
    * An adaption for the flow parameter `H_L_FG_share_max` has been made to
      set the flue gas losses at maximum heat extraction `H_L_FG_max` as share
      of the fuel flow `H_F` e.g. for combined cycle extraction turbines.
    * The flow parameter `H_L_FG_share_min` can be used to set the flue gas
      losses at minimum heat extraction `H_L_FG_min` as share of
      the fuel flow `H_F` e.g. for motoric CHPs.
    * The boolean component parameter `back_pressure` can be set to model
      back-pressure characteristics.

    Also have a look at the examples on how to use it.

    Parameters
    ----------
    fuel_input : dict
        Dictionary with key-value-pair of `oemof.solph.Bus` and
        `oemof.solph.Flow` objects for the fuel input.
    electrical_output : dict
        Dictionary with key-value-pair of `oemof.solph.Bus` and
        `oemof.solph.Flow` objects for the electrical output.
        Related parameters like `P_max_woDH` are passed as
        attributes of the `oemof.Flow` object.
    heat_output : dict
        Dictionary with key-value-pair of `oemof.solph.Bus`
        and `oemof.solph.Flow` objects for the heat output.
        Related parameters like `Q_CW_min` are passed as
        attributes of the `oemof.Flow` object.
    beta : list of numerical values
        beta values in same dimension as all other parameters (length of
        optimization period).
    back_pressure : boolean
        Flag to use back-pressure characteristics. Set to `True` and
        `Q_CW_min` to zero for back-pressure turbines. See paper above for more
        information.

    Note
    ----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.components._generic_chp.GenericCHPBlock`

    Examples
    --------
    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='electricityBus')
    >>> bth = solph.buses.Bus(label='heatBus')
    >>> bgas = solph.buses.Bus(label='commodityBus')
    >>> ccet = solph.components.GenericCHP(
    ...    label='combined_cycle_extraction_turbine',
    ...    fuel_input={bgas: solph.flows.Flow(
    ...        custom_attributes={"H_L_FG_share_max": [0.183]})},
    ...    electrical_output={bel: solph.flows.Flow(
    ...        custom_attributes={
    ...            "P_max_woDH": [155.946],
    ...            "P_min_woDH": [68.787],
    ...            "Eta_el_max_woDH": [0.525],
    ...            "Eta_el_min_woDH": [0.444],
    ...        })},
    ...    heat_output={bth: solph.flows.Flow(
    ...        custom_attributes={"Q_CW_min": [10.552]})},
    ...    beta=[0.122], back_pressure=False)
    >>> type(ccet)
    <class 'oemof.solph.components._generic_chp.GenericCHP'>
    """

    def __init__(
        self,
        fuel_input,
        electrical_output,
        heat_output,
        beta,
        back_pressure,
        label=None,
        custom_properties=None,
    ):
        if custom_properties is None:
            custom_properties = {}
        super().__init__(label, custom_properties=custom_properties)

        self.fuel_input = fuel_input
        self.electrical_output = electrical_output
        self.heat_output = heat_output
        self.beta = sequence(beta)
        self.back_pressure = back_pressure
        self._alphas = None

        # map specific flows to standard API
        fuel_bus = list(self.fuel_input.keys())[0]
        fuel_flow = list(self.fuel_input.values())[0]
        fuel_bus.outputs.update({self: fuel_flow})

        self.outputs.update(electrical_output)
        self.outputs.update(heat_output)

    def _calculate_alphas(self):
        """
        Calculate alpha coefficients.

        A system of linear equations is created from passed capacities and
        efficiencies and solved to calculate both coefficients.
        """
        alphas = [[], []]

        eb = list(self.electrical_output.keys())[0]

        attrs = [
            self.electrical_output[eb].P_min_woDH,
            self.electrical_output[eb].Eta_el_min_woDH,
            self.electrical_output[eb].P_max_woDH,
            self.electrical_output[eb].Eta_el_max_woDH,
        ]

        length = [len(a) for a in attrs if not isinstance(a, (int, float))]
        max_length = max(length)

        if all(len(a) == max_length for a in attrs):
            if max_length == 0:
                max_length += 1  # increment dimension for scalars from 0 to 1
            for i in range(0, max_length):
                A = np.array(
                    [
                        [1, self.electrical_output[eb].P_min_woDH[i]],
                        [1, self.electrical_output[eb].P_max_woDH[i]],
                    ]
                )
                b = np.array(
                    [
                        self.electrical_output[eb].P_min_woDH[i]
                        / self.electrical_output[eb].Eta_el_min_woDH[i],
                        self.electrical_output[eb].P_max_woDH[i]
                        / self.electrical_output[eb].Eta_el_max_woDH[i],
                    ]
                )
                x = np.linalg.solve(A, b)
                alphas[0].append(x[0])
                alphas[1].append(x[1])
        else:
            error_message = (
                "Attributes to calculate alphas "
                + "must be of same dimension."
            )
            raise ValueError(error_message)

        self._alphas = alphas

    @property
    def alphas(self):
        """Compute or return the _alphas attribute."""
        if self._alphas is None:
            self._calculate_alphas()
        return self._alphas

    def constraint_group(self):
        return GenericCHPBlock


class GenericCHPBlock(ScalarBlock):
    r"""
    Block for the relation of the :math:`n` nodes with
    type class:`.GenericCHP`.

    **The following constraints are created:**

    .. _GenericCHP-equations1-10:

    .. math::
        &
        (1)\qquad \dot{H}_F(t) = fuel\ input \\
        &
        (2)\qquad \dot{Q}(t) = heat\ output \\
        &
        (3)\qquad P_{el}(t) = power\ output\\
        &
        (4)\qquad \dot{H}_F(t) = \alpha_0(t) \cdot Y(t) + \alpha_1(t) \cdot
        P_{el,woDH}(t)\\
        &
        (5)\qquad \dot{H}_F(t) = \alpha_0(t) \cdot Y(t) + \alpha_1(t) \cdot
        ( P_{el}(t) + \beta \cdot \dot{Q}(t) )\\
        &
        (6)\qquad \dot{H}_F(t) \leq Y(t) \cdot
        \frac{P_{el, max, woDH}(t)}{\eta_{el,max,woDH}(t)}\\
        &
        (7)\qquad \dot{H}_F(t) \geq Y(t) \cdot
        \frac{P_{el, min, woDH}(t)}{\eta_{el,min,woDH}(t)}\\
        &
        (8)\qquad \dot{H}_{L,FG,max}(t) = \dot{H}_F(t) \cdot
        \dot{H}_{L,FG,sharemax}(t)\\
        &
        (9)\qquad \dot{H}_{L,FG,min}(t) = \dot{H}_F(t) \cdot
        \dot{H}_{L,FG,sharemin}(t)\\
        &
        (10)\qquad P_{el}(t) + \dot{Q}(t) + \dot{H}_{L,FG,max}(t) +
        \dot{Q}_{CW, min}(t) \cdot Y(t) = / \leq \dot{H}_F(t)\\

    where :math:`= / \leq` depends on the CHP being back pressure or not.

    The coefficients :math:`\alpha_0` and :math:`\alpha_1`
    can be determined given the efficiencies maximal/minimal load:

    .. math::
        &
        \eta_{el,max,woDH}(t) = \frac{P_{el,max,woDH}(t)}{\alpha_0(t)
        \cdot Y(t) + \alpha_1(t) \cdot P_{el,max,woDH}(t)}\\
        &
        \eta_{el,min,woDH}(t) = \frac{P_{el,min,woDH}(t)}{\alpha_0(t)
        \cdot Y(t) + \alpha_1(t) \cdot P_{el,min,woDH}(t)}\\


    **For the attribute** :math:`\dot{H}_{L,FG,min}` **being not None**,
    e.g. for a motoric CHP, **the following is created:**

        **Constraint:**

    .. _GenericCHP-equations11:

    .. math::
        &
        (11)\qquad P_{el}(t) + \dot{Q}(t) + \dot{H}_{L,FG,min}(t) +
        \dot{Q}_{CW, min}(t) \cdot Y(t) \geq \dot{H}_F(t)\\[10pt]

    The symbols used are defined as follows (with Variables (V) and Parameters (P)):

    =============================== ======================= ==== =============================================
    math. symbol                    attribute               type explanation
    =============================== ======================= ==== =============================================
    :math:`\dot{H}_{F}`             `H_F[n,t]`              V    input of enthalpy through fuel input
    :math:`P_{el}`                  `P[n,t]`                V    provided electric power
    :math:`P_{el,woDH}`             `P_woDH[n,t]`           V    electric power without district heating
    :math:`P_{el,min,woDH}`         `P_min_woDH[n,t]`       P    min. electric power without district heating
    :math:`P_{el,max,woDH}`         `P_max_woDH[n,t]`       P    max. electric power without district heating
    :math:`\dot{Q}`                 `Q[n,t]`                V    provided heat
    :math:`\dot{Q}_{CW, min}`       `Q_CW_min[n,t]`         P    minimal therm. condenser load to cooling water
    :math:`\dot{H}_{L,FG,min}`      `H_L_FG_min[n,t]`       V    flue gas enthalpy loss at min heat extraction
    :math:`\dot{H}_{L,FG,max}`      `H_L_FG_max[n,t]`       V    flue gas enthalpy loss at max heat extraction
    :math:`\dot{H}_{L,FG,sharemin}` `H_L_FG_share_min[n,t]` P    share of flue gas loss at min heat extraction
    :math:`\dot{H}_{L,FG,sharemax}` `H_L_FG_share_max[n,t]` P    share of flue gas loss at max heat extraction
    :math:`Y`                       `Y[n,t]`                V    status variable on/off
    :math:`\alpha_0`                `n.alphas[0][n,t]`      P    coefficient describing efficiency
    :math:`\alpha_1`                `n.alphas[1][n,t]`      P    coefficient describing efficiency
    :math:`\beta`                   `beta[n,t]`             P    power loss index
    :math:`\eta_{el,min,woDH}`      `Eta_el_min_woDH[n,t]`  P    el. eff. at min. fuel flow w/o distr. heating
    :math:`\eta_{el,max,woDH}`      `Eta_el_max_woDH[n,t]`  P    el. eff. at max. fuel flow w/o distr. heating
    =============================== ======================= ==== =============================================

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Create constraints for GenericCHPBlock.

        Parameters
        ----------
        group : list
            List containing `GenericCHP` objects.
            e.g. groups=[ghcp1, gchp2,..]
        """
        m = self.parent_block()

        if group is None:
            return None

        self.GENERICCHPS = Set(initialize=[n for n in group])

        # variables
        self.H_F = Var(self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals)
        self.H_L_FG_max = Var(
            self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals
        )
        self.H_L_FG_min = Var(
            self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals
        )
        self.P_woDH = Var(
            self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals
        )
        self.P = Var(self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals)
        self.Q = Var(self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals)
        self.Y = Var(self.GENERICCHPS, m.TIMESTEPS, within=Binary)

        # constraint rules
        def _H_flow_rule(block, n, t):
            """Link fuel consumption to component inflow."""
            expr = 0
            expr += self.H_F[n, t]
            expr += -m.flow[list(n.fuel_input.keys())[0], n, t]
            return expr == 0

        self.H_flow = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_H_flow_rule
        )

        def _Q_flow_rule(block, n, t):
            """Link heat flow to component outflow."""
            expr = 0
            expr += self.Q[n, t]
            expr += -m.flow[n, list(n.heat_output.keys())[0], t]
            return expr == 0

        self.Q_flow = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_Q_flow_rule
        )

        def _P_flow_rule(block, n, t):
            """Link power flow to component outflow."""
            expr = 0
            expr += self.P[n, t]
            expr += -m.flow[n, list(n.electrical_output.keys())[0], t]
            return expr == 0

        self.P_flow = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_P_flow_rule
        )

        def _H_F_1_rule(block, n, t):
            """Set P_woDH depending on H_F."""
            expr = 0
            expr += -self.H_F[n, t]
            expr += n.alphas[0][t] * self.Y[n, t]
            expr += n.alphas[1][t] * self.P_woDH[n, t]
            return expr == 0

        self.H_F_1 = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_H_F_1_rule
        )

        def _H_F_2_rule(block, n, t):
            """Determine relation between H_F, P and Q."""
            expr = 0
            expr += -self.H_F[n, t]
            expr += n.alphas[0][t] * self.Y[n, t]
            expr += n.alphas[1][t] * (self.P[n, t] + n.beta[t] * self.Q[n, t])
            return expr == 0

        self.H_F_2 = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_H_F_2_rule
        )

        def _H_F_3_rule(block, n, t):
            """Set upper value of operating range via H_F."""
            expr = 0
            expr += self.H_F[n, t]
            expr += -self.Y[n, t] * (
                list(n.electrical_output.values())[0].P_max_woDH[t]
                / list(n.electrical_output.values())[0].Eta_el_max_woDH[t]
            )
            return expr <= 0

        self.H_F_3 = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_H_F_3_rule
        )

        def _H_F_4_rule(block, n, t):
            """Set lower value of operating range via H_F."""
            expr = 0
            expr += self.H_F[n, t]
            expr += -self.Y[n, t] * (
                list(n.electrical_output.values())[0].P_min_woDH[t]
                / list(n.electrical_output.values())[0].Eta_el_min_woDH[t]
            )
            return expr >= 0

        self.H_F_4 = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_H_F_4_rule
        )

        def _H_L_FG_max_rule(block, n, t):
            """Set max. flue gas loss as share fuel flow share."""
            expr = 0
            expr += -self.H_L_FG_max[n, t]
            expr += (
                self.H_F[n, t]
                * list(n.fuel_input.values())[0].H_L_FG_share_max[t]
            )
            return expr == 0

        self.H_L_FG_max_def = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_H_L_FG_max_rule
        )

        def _Q_max_res_rule(block, n, t):
            """Set maximum Q depending on fuel and electrical flow."""
            expr = 0
            expr += self.P[n, t] + self.Q[n, t] + self.H_L_FG_max[n, t]
            expr += list(n.heat_output.values())[0].Q_CW_min[t] * self.Y[n, t]
            expr += -self.H_F[n, t]
            # back-pressure characteristics or one-segment model
            if n.back_pressure is True:
                return expr == 0
            else:
                return expr <= 0

        self.Q_max_res = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_Q_max_res_rule
        )

        def _H_L_FG_min_rule(block, n, t):
            """Set min. flue gas loss as fuel flow share."""
            # minimum flue gas losses e.g. for motoric CHPs
            if getattr(
                list(n.fuel_input.values())[0], "H_L_FG_share_min", None
            ):
                expr = 0
                expr += -self.H_L_FG_min[n, t]
                expr += (
                    self.H_F[n, t]
                    * list(n.fuel_input.values())[0].H_L_FG_share_min[t]
                )
                return expr == 0
            else:
                return Constraint.Skip

        self.H_L_FG_min_def = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_H_L_FG_min_rule
        )

        def _Q_min_res_rule(block, n, t):
            """Set minimum Q depending on fuel and eletrical flow."""
            # minimum restriction for heat flows e.g. for motoric CHPs
            if getattr(
                list(n.fuel_input.values())[0], "H_L_FG_share_min", None
            ):
                expr = 0
                expr += self.P[n, t] + self.Q[n, t] + self.H_L_FG_min[n, t]
                expr += (
                    list(n.heat_output.values())[0].Q_CW_min[t] * self.Y[n, t]
                )
                expr += -self.H_F[n, t]
                return expr >= 0
            else:
                return Constraint.Skip

        self.Q_min_res = Constraint(
            self.GENERICCHPS, m.TIMESTEPS, rule=_Q_min_res_rule
        )

    def _objective_expression(self):
        r"""Objective expression for generic CHPs with no investment.

        Note: This adds nothing as variable costs are already
        added in the Block :class:`SimpleFlowBlock`.
        """
        if not hasattr(self, "GENERICCHPS"):
            return 0

        return 0
