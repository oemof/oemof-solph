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

from oemof.solph.components import VariableSplitConverter


class ExtractionTurbineCHP(VariableSplitConverter):
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
        parent_node=None,
        conversion_factors=None,
        custom_properties=None,
    ):
        # super().__init__(
        #     label=label,
        #     inputs=inputs,
        #     outputs=outputs,
        #     parent_node=parent_node,
        #     conversion_factors=conversion_factors,
        #     custom_properties=custom_properties,
        # )
        bus2 = set(conversion_factors).difference(
            set(conversion_factor_full_condensation)
        ).pop()
        conversion_factor_full_condensation[bus2] = 0

        super().__init__(
            label=label,
            inputs=inputs,
            outputs=outputs,
            parent_node=parent_node,
            conversion_factors=conversion_factors,
            custom_properties=custom_properties,
            allow_equal_states=False,
            conversion_factors_secondary_state=conversion_factor_full_condensation,
        )
