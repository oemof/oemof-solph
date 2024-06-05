# -*- coding: utf-8 -

"""
OffsetConverter and associated individual constraints (blocks) and groupings.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: FranziPl
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: FabianTU
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: Saeed Sayadi
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from warnings import warn

from oemof.network import Node
from pyomo.core import BuildAction
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Constraint
from pyomo.environ import Set

from oemof.solph._plumbing import sequence


class OffsetConverter(Node):
    """An object with one input and multiple outputs and two coefficients
    per output to model part load behaviour.
    The output must contain a NonConvex object.

    Parameters
    ----------
    conversion_factors : dict, (:math:`C_1(t)`)
        Dict containing the respective bus as key and as value the parameter
        :math:`C_1(t)`. It represents the slope of a linear equation with
        respect to the `NonConvex` flow. The value can either be a scalar or a
        sequence with length of time horizon for simulation.

    normed_offsets : dict, (:math:`C_0(t)`)
        Dict containing the respective bus as key and as value the parameter
        :math:`C_0(t)`. It represents the y-intercept with respect to the
        `NonConvex` flow divided by the `nominal_value` of the `NonConvex` flow
        (this is for internal purposes). The value can either be a scalar or a
        sequence with length of time horizon for simulation.
    Notes
    -----
    **C_1 and C_0 can be calculated as follows:**

    .. _OffsetConverterCoefficients-equations:

    .. math::

        C_1 = \\frac{(l_{max}/\\eta_{max}-l_{min}/\\eta_{min}}{l_{max}-l_{min}}

        C_0 = \\frac{1}{\\eta_{max}} - C_1

    Where :math:`l_{max}` and :math:`l_{min}` are the maximum and minimum
    partload share (e.g. 1.0 and 0.5) with reference to the `NonConvex` flow
    and :math:`\\eta_{max}` and :math:`\\eta_{min}` are the respective
    efficiencies/conversion factors at these partloads.

    The sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.components._offset_converter.OffsetConverterBlock`

    Examples
    --------
    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='bel')
    >>> bth = solph.buses.Bus(label='bth')
    >>> l_nominal = 60
    >>> l_max = 1
    >>> l_min = 0.5
    >>> eta_max = 0.5
    >>> eta_min = 0.3
    >>> c1 = (l_max / eta_max - l_min / eta_min) / (l_max - l_min)
    >>> c0 = 1 / eta_max - c1
    >>> ostf = solph.components.OffsetConverter(
    ...    label='ostf',
    ...    inputs={bel: solph.flows.Flow()},
    ...    outputs={bth: solph.flows.Flow(
    ...         nominal_value=l_nominal, min=l_min, max=l_max,
    ...         nonconvex=solph.NonConvex())},
    ...    conversion_factors={bel: c1},
    ...    normed_offsets={bel: c0},
    ... )
    >>> type(ostf)
    <class 'oemof.solph.components._offset_converter.OffsetConverter'>

    The input required to operate at minimum load, can be computed from the
    slope and offset:

    >>> input_at_min = ostf.conversion_factors[bel][0] * l_min + ostf.normed_offsets[bel][0] * l_max
    >>> input_at_min * l_nominal
    100.0

    The same can be done for the input at nominal load:

    >>> input_at_max = l_max * (ostf.conversion_factors[bel][0] + ostf.normed_offsets[bel][0])
    >>> input_at_max * l_nominal
    120.0

    """  # noqa: E501

    def __init__(
        self,
        inputs,
        outputs,
        label=None,
        conversion_factors=None,
        normed_offsets=None,
        coefficients=None,
        custom_attributes=None,
    ):
        if custom_attributes is None:
            custom_attributes = {}

        super().__init__(
            inputs=inputs,
            outputs=outputs,
            label=label,
            custom_properties=custom_attributes,
        )

        # this part is used for the transition phase from the old OffsetConverter
        # API to the new one. It calcualtes the conversion_factors and normed_offsets
        # from the coefficients and the outputs information on min and max.
        if coefficients is not None and conversion_factors is None and normed_offsets is None:
            normed_offsets, conversion_factors = self.get_normed_offset_and_conversion_factors_from_old_style_coefficients(coefficients)

        elif coefficients is not None and (conversion_factors is not None or normed_offsets is not None):
            msg = ""
            raise TypeError(msg)

        _reference_flow = [v for v in self.inputs.values() if v.nonconvex]
        _reference_flow += [v for v in self.outputs.values() if v.nonconvex]
        if len(_reference_flow) != 1:
            raise ValueError(
                "Exactly one flow of the `OffsetConverter` must have the "
                "`NonConvex` attribute."
            )

        if _reference_flow[0] in self.inputs.values():
            self._reference_node_at_input = True
            self._reference_node = _reference_flow[0].input
        else:
            self._reference_node_at_input = False
            self._reference_node = _reference_flow[0].output

        _investment_node = [
            v.input for v in self.inputs.values() if v.investment
        ]
        _investment_node += [
            v.output for v in self.outputs.values() if v.investment
        ]

        if len(_investment_node) > 0:
            if (
                len(_investment_node) > 1
                or self._reference_node != _investment_node[0]
            ):
                raise TypeError(
                    "`Investment` attribute must be defined only for the "
                    "NonConvex flow!"
                )

        if conversion_factors is None:
            conversion_factors = {}

        if self._reference_node in conversion_factors:
            raise ValueError(
                "Conversion factors cannot be specified for the `NonConvex` "
                "flow."
            )

        self.conversion_factors = {
            k: sequence(v) for k, v in conversion_factors.items()
        }

        missing_conversion_factor_keys = (
            set(self.outputs) | set(self.inputs)
        ) - set(self.conversion_factors)

        for cf in missing_conversion_factor_keys:
            self.conversion_factors[cf] = sequence(1)

        if normed_offsets is None:
            normed_offsets = {}

        if self._reference_node in normed_offsets:
            raise ValueError(
                "Normed offsets cannot be specified for the `NonConvex` flow."
            )

        self.normed_offsets = {
            k: sequence(v) for k, v in normed_offsets.items()
        }

        missing_normed_offsets_keys = (
            set(self.outputs) | set(self.inputs)
        ) - set(self.normed_offsets)

        for cf in missing_normed_offsets_keys:
            self.normed_offsets[cf] = sequence(0)

    def constraint_group(self):
        return OffsetConverterBlock

    def get_normed_offset_and_conversion_factors_from_old_style_coefficients(self, coefficients):
        """
        Calculate slope and offset for new API from the old API coefficients.

        Parameters
        ----------
        coefficients : tuple
            tuple holding the coefficients (offset, slope) for the old style
            OffsetConverter.

        Returns
        -------
        tuple
            A tuple holding the slope and the offset for the new OffsetConverter
            API.
        """
        coefficients = tuple([sequence(i) for i in coefficients])
        if len(coefficients) != 2:
            raise ValueError(
                "Two coefficients or coefficient series have to be given."
            )

        input_bus = list(self.inputs.values())[0].input
        for flow in self.outputs.values():

            max_len = max(len(flow.max), len(flow.min), len(coefficients[0]), len(coefficients[1]))
            flow.max[max_len - 1]
            flow.min[max_len - 1]
            coefficients[0][max_len - 1]
            coefficients[1][max_len - 1]

            # this could by vectorized, but since it is an API compatibility fix
            # I will not do this here
            eta_at_max = sequence(0)
            eta_at_min = sequence(0)
            slope = []
            offset = []
            for i in range(max_len):
                eta_at_max = flow.max[i] * coefficients[1][i] / (flow.max[i] - coefficients[0][i])
                eta_at_min = flow.min[i] * coefficients[1][i] / (flow.min[i] - coefficients[0][i])

                c0, c1 = calculate_slope_and_offset_with_reference_to_output(flow.max[i], flow.min[i], eta_at_max, eta_at_min)
                slope += [c0]
                offset += [c1]

            # apparently, when coefficients are given as a list, it is assumed,
            # that the list identical in length to the timeindex
            # There should be a general check, if lenghts match then!
            if max_len == 1:
                slope = sequence(slope[0])
                offset = sequence(offset[0])

            conversion_factors = {input_bus: slope}
            normed_offsets = {input_bus: offset}
            msg = (
                "The usage of coefficients is depricated, use "
                "conversion_factors and normed_offsets instead."
            )
            warn(msg, DeprecationWarning)

        return normed_offsets, conversion_factors


# --- BEGIN: To be removed for versions >= v0.6 ---
class OffsetTransformer(OffsetConverter):
    def __init__(
        self,
        inputs,
        outputs,
        label=None,
        conversion_factors=None,
        normed_offsets=None,
        custom_attributes=None,
    ):
        super().__init__(
            label=label,
            inputs=inputs,
            outputs=outputs,
            conversion_factors=conversion_factors,
            normed_offsets=normed_offsets,
            custom_attributes=custom_attributes,
        )
        warn(
            "solph.components.OffsetTransformer has been renamed to"
            " solph.components.OffsetConverter. The transitional wrapper"
            " will be deleted in the future.",
            FutureWarning,
        )


# --- END ---


class OffsetConverterBlock(ScalarBlock):
    r"""Block for the relation of nodes with type
    :class:`~oemof.solph.components._offset_converter.OffsetConverter`

    **The following constraints are created:**

    .. _OffsetConverter-equations:

    .. math::
        &
        P_{out}(p, t) = P_{in}(p, t) \cdot C_1(t) + P_nom(p) \cdot Y(t) \cdot C_0(t) \\


    The symbols used are defined as follows (with Variables (V) and Parameters (P)):

    +--------------------+---------------------------+------+--------------------------------------------------+
    | symbol             | attribute                 | type | explanation                                      |
    +====================+===========================+======+==================================================+
    | :math:`P_{out}(t)` | `flow[n,o,p,t]`           | V    | Outflow of converter                             |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`P_{in}(t)`  | `flow[i,n,p,t]`           | V    | Inflow of converter                              |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`Y(t)`       |                           | V    | Binary status variable of nonconvex outflow      |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`P_{nom}(t)` |                           | V    | Nominal value (max. capacity) of the outflow     |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`C_1(t)`     | `coefficients[o][1][n,t]` | P    | Linear coefficient 1 (slope)                     |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`C_0(t)`     | `coefficients[o][0][n,t]` | P    | Linear coefficient 0 (y-intersection)/P_{nom}(t) |
    +--------------------+---------------------------+------+--------------------------------------------------+

    Note that :math:`P_{nom}(t) \cdot Y(t)` is merged into one variable,
    called `status_nominal[n, o, p, t]`.
    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the relation for the class:`OffsetConverter`.

        Parameters
        ----------
        group : list
            List of oemof.solph.experimental.OffsetConverter objects for
            which the relation of inputs and outputs is created
            e.g. group = [ostf1, ostf2, ostf3, ...]. The components inside
            the list need to hold an attribute `coefficients` of type dict
            containing the conversion factors for all inputs to outputs.
        """
        if group is None:
            return None

        m = self.parent_block()

        self.OFFSETCONVERTERS = Set(initialize=[n for n in group])

        reference_node = {n: n._reference_node for n in group}
        reference_node_at_input = {
            n: n._reference_node_at_input for n in group
        }
        in_flows = {
            n: [i for i in n.inputs.keys() if i != n._reference_node]
            for n in group
        }
        out_flows = {
            n: [o for o in n.outputs.keys() if o != n._reference_node]
            for n in group
        }

        self.relation = Constraint(
            [
                (n, reference_node[n], f, p, t)
                for p, t in m.TIMEINDEX
                for n in group
                for f in in_flows[n] + out_flows[n]
            ],
            noruleinit=True,
        )

        def _relation_rule(block):
            """Link binary input and output flow to component outflow."""
            for p, t in m.TIMEINDEX:
                for n in group:

                    if reference_node_at_input[n]:
                        ref_flow = m.flow[reference_node[n], n, p, t]
                        status_nominal_idx = reference_node[n], n, t
                    else:
                        ref_flow = m.flow[n, reference_node[n], p, t]
                        status_nominal_idx = n, reference_node[n], t

                    if hasattr(m.NonConvexFlowBlock, "status_nominal"):
                        status_nominal = m.NonConvexFlowBlock.status_nominal

                    if hasattr(m, "InvestNonConvexFlowBlock"):
                        if hasattr(
                            m.InvestNonConvexFlowBlock, "status_nominal"
                        ):
                            if (
                                status_nominal_idx
                                in m.InvestNonConvexFlowBlock.status_nominal
                            ):
                                status_nominal = (
                                    m.InvestNonConvexFlowBlock.status_nominal
                                )

                    ref_status_nominal = status_nominal[status_nominal_idx]

                    for f in in_flows[n] + out_flows[n]:
                        rhs = 0
                        if f in in_flows[n]:
                            rhs += m.flow[f, n, p, t]
                        else:
                            rhs += m.flow[n, f, p, t]

                        lhs = 0
                        lhs += ref_flow * n.conversion_factors[f][t]
                        lhs += ref_status_nominal * n.normed_offsets[f][t]
                        block.relation.add(
                            (n, reference_node[n], f, p, t), (lhs == rhs)
                        )

        self.relation_build = BuildAction(rule=_relation_rule)


def calculate_slope_and_offset_with_reference_to_input(
    max, min, eta_at_max, eta_at_min
):
    """Calculate the slope and the offset with max and min given for input

    The reference is the input flow here. That means, the `NonConvex` flow
    is specified at one of the input flows. Therefore the `max` and the `min`
    both reference that flow. `eta_at_max` and `eta_at_min` are the efficiency
    values at the referenced point.

    .. math::

        \text{slope} =
        \frac{
            \text{max} \cdot \eta_\text{at max}
            - \text{min} \cdot \eta_\text{at min}
        }{\text{max} - \text{min}}\\

        \text{offset} = \eta_\text{at,max} - \text{slope}

    Parameters
    ----------
    max : float
        Maximum load value, e.g. 1
    min : float
        Minimum load value, e.g. 0.5
    eta_at_max : float
        Efficiency at maximum load.
    eta_at_min : float
        Efficiency at minimum load.

    Returns
    -------
    tuple
        slope and offset
    """
    slope = (max * eta_at_max - min * eta_at_min) / (max - min)
    offset = eta_at_max - slope
    return slope, offset


def calculate_slope_and_offset_with_reference_to_output(
    max, min, eta_at_max, eta_at_min
):
    r"""Calculate the slope and the offset with max and min given for output.

    The reference is the output flow here. That means, the `NonConvex` flow
    is specified at one of the output flows. Therefore the `max` and the `min`
    both reference that flow. `eta_at_max` and `eta_at_min` are the efficiency
    values at the referenced point.

    .. math::

        \text{slope} =
        \frac{
            \frac{\text{max}}{\eta_\text{at max}}
            - \frac{\text{min}}{\eta_\text{at min}}
        }{\text{max} - \text{min}}\\

        \text{offset} = \frac{1}{\eta_\text{at,max}} - \text{slope}

    Parameters
    ----------
    max : float
        Maximum load value, e.g. 1
    min : float
        Minimum load value, e.g. 0.5
    eta_at_max : float
        Efficiency at maximum load.
    eta_at_min : float
        Efficiency at minimum load.

    Returns
    -------
    tuple
        slope and offset
    """
    slope = (max / eta_at_max - min / eta_at_min) / (max - min)
    offset = 1 / eta_at_max - slope
    return slope, offset
