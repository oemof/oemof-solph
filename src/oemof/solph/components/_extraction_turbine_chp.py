# -*- coding: utf-8 -

"""
ExtractionTurbineCHP and associated individual constraints (blocks)
and groupings.

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

from pyomo.core.base.block import ScalarBlock
from pyomo.environ import BuildAction
from pyomo.environ import Constraint

from oemof.solph._plumbing import sequence
from oemof.solph.components import Converter


class ExtractionTurbineCHP(Converter):
    r"""
    A CHP with an extraction turbine in a linear model. For a more
    detailled modelling approach providing more options, also see
    the :class:`.GenericCHP` class.

    One main output flow has to be defined and is tapped by the remaining flow.
    The conversion factors have to be defined for the maximum tapped flow (
    full CHP mode) and for no tapped flow (full condensing mode). Even though,
    it is possible to limit the variability of the tapped flow, so that the
    full condensing mode will never be reached.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.
    conversion_factor_full_condensation : dict
        The efficiency of the main flow if there is no tapped flow. Only one
        key is allowed. Use one of the keys of the conversion factors. The key
        indicates the main flow. The other output flow is the tapped flow.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.components.extraction_turbine_chp.ExtractionTurbineCHPBlock`

    Examples
    --------
    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='electricityBus')
    >>> bth = solph.buses.Bus(label='heatBus')
    >>> bgas = solph.buses.Bus(label='commodityBus')
    >>> et_chp = solph.components.ExtractionTurbineCHP(
    ...    label='variable_chp_gas',
    ...    inputs={bgas: solph.flows.Flow(nominal_capacity=10e10)},
    ...    outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
    ...    conversion_factors={bel: 0.3, bth: 0.5},
    ...    conversion_factor_full_condensation={bel: 0.5})
    """  # noqa: E501

    def __init__(
        self,
        conversion_factor_full_condensation,
        label=None,
        inputs=None,
        outputs=None,
        conversion_factors=None,
        custom_properties=None,
    ):
        super().__init__(
            label=label,
            inputs=inputs,
            outputs=outputs,
            conversion_factors=conversion_factors,
            custom_properties=custom_properties,
        )
        self.conversion_factor_full_condensation = {
            k: sequence(v)
            for k, v in conversion_factor_full_condensation.items()
        }

    def constraint_group(self):
        return ExtractionTurbineCHPBlock


class ExtractionTurbineCHPBlock(ScalarBlock):
    r"""Block for all instances of
    :class:`~oemof.solph.components.experimental._ExtractionTurbineCHP`

    **Variables**

    The following variables are used:

    * :math:`\dot H_{Fuel}`

        Fuel input flow, represented in code as `flow[i, n, t]`

    * :math:`P_{el}`

        Electric power outflow, represented in code as
        `flow[n, main_output, t]`

    * :math:`\dot Q_{th}`

        Thermal output flow, represented in code as
        `flow[n, tapped_output, t]`

    **Parameters**

    The following parameters are created as attributes of
    :attr:`om.ExtractionTurbineCHP`:

    * :math:`\eta_{el,woExtr}`

        Electric efficiency without heat extraction, represented in code as
        `conversion_factor_full_condensation[n, t]`

    * :math:`\eta_{el,maxExtr}`

        Electric efficiency with maximal heat extraction, represented in code
        as `conversion_factors[main_output][n, t]`

    * :math:`\eta_{th,maxExtr}`

        Thermal efficiency with maximal heat extraction, represented in code
        as `conversion_factors[tapped_output][n, t]`

    **Constraints**

    The following constraints are created for all
    instances of :class:`oemof.solph.components.ExtractionTurbineCHP`:

    .. _ETCHP-equations:

        .. math::
            &
            (1)\dot H_{Fuel}(t) =
               \frac{P_{el}(t) + \dot Q_{th}(t) \cdot \beta(t)}
                 {\eta_{el,woExtr}(t)} \\
            &
            (2)P_{el}(t) \geq \dot Q_{th}(t) \cdot C_b

    where:

    .. math::

        \beta(t) = \frac{\eta_{el,woExtr}(t) -
            \eta_{el,maxExtr}(t)}{\eta_{th,maxExtr}(t)}

    and:

    .. math::

        C_b = \frac{\eta_{el,maxExtr}(t)}{\eta_{th,maxExtr}(t)}

    The first equation is the result of the relation between the input
    flow and the two output flows, the second equation stems from how the two
    output flows relate to each other, and the symbols used are defined as
    follows (with Variables (V) and Parameters (P)):

    ========================= ============================================ ==== =========
    symbol                    attribute                                    type explanation
    ========================= ============================================ ==== =========
    :math:`\dot H_{Fuel}`     `flow[i, n, t]`                              V    fuel input flow

    :math:`P_{el}`            `flow[n, main_output, t]`                    V    electric power

    :math:`\dot Q_{th}`       `flow[n, tapped_output, t]`                  V    thermal output

    :math:`\beta`             `main_flow_loss_index[n, t]`                 P    power loss index

    :math:`\eta_{el,woExtr}`  `conversion_factor_full_condensation[n, t]`  P    electric efficiency
                                                                                        without heat extraction
    :math:`\eta_{el,maxExtr}` `conversion_factors[main_output][n, t]`      P    electric efficiency
                                                                                        with max heat extraction
    :math:`\eta_{th,maxExtr}` `conversion_factors[tapped_output][n, t]`    P    thermal efficiency with
                                                                                        maximal heat extraction
    ========================= ============================================ ==== =========

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the constraints for
        :class:`oemof.solph.components.experimental._extraction_turbine_chp.ExtractionTurbineCHPBlock`.

        Parameters
        ----------
        group : list
            List of
            :class:`oemof.solph.components.experimental._extraction_turbine_chp.ExtractionTurbineCHP`
            (trsf) objects for which the linear relation of inputs
            and outputs is created e.g. group = [trsf1, trsf2, trsf3, ...].
            Note that the relation is created for all existing relations
            of the inputs and all outputs of the converter-like object.
            The components inside the list need to hold all needed attributes.
        """
        if group is None:
            return None

        m = self.parent_block()

        for n in group:
            n.inflow = list(n.inputs)[0]
            n.main_flow = [
                k for k, v in n.conversion_factor_full_condensation.items()
            ][0]
            n.main_output = [o for o in n.outputs if n.main_flow == o][0]
            n.tapped_output = [o for o in n.outputs if n.main_flow != o][0]
            n.conversion_factor_full_condensation_sq = (
                n.conversion_factor_full_condensation[n.main_output]
            )
            n.flow_relation_index = [
                n.conversion_factors[n.main_output][t]
                / n.conversion_factors[n.tapped_output][t]
                for t in m.TIMESTEPS
            ]
            n.main_flow_loss_index = [
                (
                    n.conversion_factor_full_condensation_sq[t]
                    - n.conversion_factors[n.main_output][t]
                )
                / n.conversion_factors[n.tapped_output][t]
                for t in m.TIMESTEPS
            ]

        def _input_output_relation_rule(block):
            """Connection between input, main output and tapped output."""
            for t in m.TIMESTEPS:
                for g in group:
                    lhs = m.flow[g.inflow, g, t]
                    rhs = (
                        m.flow[g, g.main_output, t]
                        + m.flow[g, g.tapped_output, t]
                        * g.main_flow_loss_index[t]
                    ) / g.conversion_factor_full_condensation_sq[t]
                    block.input_output_relation.add((g, t), (lhs == rhs))

        self.input_output_relation = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        def _out_flow_relation_rule(block):
            """Relation between main and tapped output in full chp mode."""
            for t in m.TIMESTEPS:
                for g in group:
                    lhs = m.flow[g, g.main_output, t]
                    rhs = (
                        m.flow[g, g.tapped_output, t]
                        * g.flow_relation_index[t]
                    )
                    block.out_flow_relation.add((g, t), (lhs >= rhs))

        self.out_flow_relation = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.out_flow_relation_build = BuildAction(
            rule=_out_flow_relation_rule
        )
