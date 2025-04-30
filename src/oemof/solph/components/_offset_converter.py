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
SPDX-FileCopyrightText: Francesco Witte

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
    r"""An object with one input and multiple outputs and two coefficients
    per output to model part load behaviour.
    The output must contain a NonConvex object.

    Parameters
    ----------
    conversion_factors : dict, (:math:`m(t)`)
        Dict containing the respective bus as key and as value the parameter
        :math:`m(t)`. It represents the slope of a linear equation with
        respect to the `NonConvex` flow. The value can either be a scalar or a
        sequence with length of time horizon for simulation.

    normed_offsets : dict, (:math:`y_\text{0,normed}(t)`)
        Dict containing the respective bus as key and as value the parameter
        :math:`y_\text{0,normed}(t)`. It represents the y-intercept with respect
        to the `NonConvex` flow divided by the `nominal_capacity` of the
        `NonConvex` flow (this is for internal purposes). The value can either
        be a scalar or a sequence with length of time horizon for simulation.
    Notes
    -----

    :math:`m(t)` and :math:`y_\text{0,normed}(t)` can be calculated as follows:

    .. _OffsetConverterCoefficients-equations:

    .. math::

        m = \frac{(l_{max}/\eta_{max}-l_{min}/\eta_{min}}{l_{max}-l_{min}}

        y_\text{0,normed} = \frac{1}{\eta_{max}} - m

    Where :math:`l_{max}` and :math:`l_{min}` are the maximum and minimum
    partload share (e.g. 1.0 and 0.5) with reference to the `NonConvex` flow
    and :math:`\eta_{max}` and :math:`\eta_{min}` are the respective
    efficiencies/conversion factors at these partloads. Alternatively, you can
    use the inbuilt methods:

    - If the `NonConvex` flow is at an input of the component:
      :py:meth:`oemof.solph.components._offset_converter.slope_offset_from_nonconvex_input`,
    - If the `NonConvex` flow is at an output of the component:
      :py:meth:`oemof.solph.components._offset_converter.slope_offset_from_nonconvex_output`

    You can import these methods from the `oemof.solph.components` level:

    >>> from oemof.solph.components import slope_offset_from_nonconvex_input
    >>> from oemof.solph.components import slope_offset_from_nonconvex_output

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
    >>> slope = (l_max / eta_max - l_min / eta_min) / (l_max - l_min)
    >>> offset = 1 / eta_max - slope

    Or use the provided method as explained in the previous section:

    >>> _slope, _offset = slope_offset_from_nonconvex_output(
    ...     l_max, l_min, eta_max, eta_min
    ... )
    >>> slope == _slope
    True
    >>> offset == _offset
    True

    >>> ostf = solph.components.OffsetConverter(
    ...    label='ostf',
    ...    inputs={bel: solph.flows.Flow()},
    ...    outputs={bth: solph.flows.Flow(
    ...         nominal_capacity=l_nominal, min=l_min, max=l_max,
    ...         nonconvex=solph.NonConvex())},
    ...    conversion_factors={bel: slope},
    ...    normed_offsets={bel: offset},
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
        custom_properties=None,
    ):
        if custom_properties is None:
            custom_properties = {}

        super().__init__(
            inputs=inputs,
            outputs=outputs,
            label=label,
            custom_properties=custom_properties,
        )

        # --- BEGIN: To be removed for versions >= v0.7 ---
        # this part is used for the transition phase from the old
        # OffsetConverter API to the new one. It calcualtes the
        # conversion_factors and normed_offsets from the coefficients and the
        # outputs information on min and max.
        if coefficients is not None:
            if conversion_factors is not None or normed_offsets is not None:
                msg = (
                    "The deprecated argument `coefficients` cannot be used "
                    "in combination with its replacements "
                    "(`conversion_factors` and `normed_offsets`)."
                )
                raise TypeError(msg)

            (
                normed_offsets,
                conversion_factors,
            ) = self.normed_offset_and_conversion_factors_from_coefficients(
                coefficients
            )
        # --- END ---

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

        self._reference_flow = _reference_flow[0]

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

    # --- BEGIN: To be removed for versions >= v0.7 ---
    def normed_offset_and_conversion_factors_from_coefficients(
        self, coefficients
    ):
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
            A tuple holding the slope and the offset for the new
            OffsetConverter API.
        """
        coefficients = tuple([sequence(i) for i in coefficients])
        if len(coefficients) != 2:
            raise ValueError(
                "Two coefficients or coefficient series have to be given."
            )

        input_bus = list(self.inputs.values())[0].input
        for flow in self.outputs.values():
            if flow.max.size is not None:
                target_len = flow.max.size
            else:
                target_len = 1

            slope = []
            offset = []
            for i in range(target_len):
                eta_at_max = (
                    flow.max[i]
                    * coefficients[1][i]
                    / (flow.max[i] - coefficients[0][i])
                )
                eta_at_min = (
                    flow.min[i]
                    * coefficients[1][i]
                    / (flow.min[i] - coefficients[0][i])
                )

                c0, c1 = slope_offset_from_nonconvex_output(
                    flow.max[i], flow.min[i], eta_at_max, eta_at_min
                )
                slope.append(c0)
                offset.append(c1)

            if target_len == 1:
                slope = slope[0]
                offset = offset[0]

            conversion_factors = {input_bus: slope}
            normed_offsets = {input_bus: offset}
            msg = (
                "The usage of coefficients is depricated, use "
                "conversion_factors and normed_offsets instead."
            )
            warn(msg, DeprecationWarning)

        return normed_offsets, conversion_factors

    # --- END ---

    def plot_partload(self, bus, tstep):
        """Create a matplotlib figure of the flow to nonconvex flow relation.

        Parameters
        ----------
        bus : oemof.solph.Bus
            Bus, to which the NOT-nonconvex input or output is connected to.
        tstep : int
            Timestep to generate the figure for.

        Returns
        -------
        tuple
            A tuple with the matplotlib figure and axes objects.
        """
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(2, sharex=True)

        slope = self.conversion_factors[bus][tstep]
        offset = self.normed_offsets[bus][tstep]

        min_load = self._reference_flow.min[tstep]
        max_load = self._reference_flow.max[tstep]

        infeasible_load = np.linspace(0, min_load)
        feasible_load = np.linspace(min_load, max_load)

        y_feasible = feasible_load * slope + offset
        y_infeasible = infeasible_load * slope + offset

        _ = ax[0].plot(feasible_load, y_feasible, label="operational range")
        color = _[0].get_color()
        ax[0].plot(infeasible_load, y_infeasible, "--", color=color)
        ax[0].scatter(
            [0, feasible_load[0], feasible_load[-1]],
            [y_infeasible[0], y_feasible[0], y_feasible[-1]],
            color=color,
        )
        ax[0].legend()

        ratio = y_feasible / feasible_load
        ax[1].plot(feasible_load, ratio)
        ax[1].scatter(
            [feasible_load[0], feasible_load[-1]],
            [ratio[0], ratio[-1]],
            color=color,
        )

        ax[0].set_ylabel(f"flow from/to bus '{bus.label}'")
        ax[1].set_ylabel("efficiency $\\frac{y}{x}$")
        ax[1].set_xlabel("nonconvex flow")

        _ = [(_.set_axisbelow(True), _.grid()) for _ in ax]
        plt.tight_layout()

        return fig, ax


class OffsetConverterBlock(ScalarBlock):
    r"""Block for the relation of nodes with type
    :class:`~oemof.solph.components._offset_converter.OffsetConverter`

    **The following constraints are created:**

    .. _OffsetConverter-equations:

    .. math::
        &
        P(p, t) = P_\text{ref}(p, t) \cdot m(t)
        + P_\text{nom,ref}(p) \cdot Y_\text{ref}(t) \cdot y_\text{0,normed}(t) \\


    The symbols used are defined as follows (with Variables (V) and Parameters (P)):

    +------------------------------+--------------------------------------------------------------+------+-----------------------------------------------------------------------------+
    | symbol                       | attribute                                                    | type | explanation                                                                 |
    +==============================+==============================================================+======+=============================================================================+
    | :math:`P(t)`                 | `flow[i,n,p,t]` or `flow[n,o,p,t]`                           | V    | **Non**-nonconvex flows at input or output                                  |
    +------------------------------+--------------------------------------------------------------+------+-----------------------------------------------------------------------------+
    | :math:`P_{in}(t)`            | `flow[i,n,p,t]` or `flow[n,o,p,t]`                           | V    | nonconvex flow of converter                                                 |
    +------------------------------+--------------------------------------------------------------+------+-----------------------------------------------------------------------------+
    | :math:`Y(t)`                 |                                                              | V    | Binary status variable of nonconvex flow                                    |
    +------------------------------+--------------------------------------------------------------+------+-----------------------------------------------------------------------------+
    | :math:`P_{nom}(t)`           |                                                              | V    | Nominal value (max. capacity) of the nonconvex flow                         |
    +------------------------------+--------------------------------------------------------------+------+-----------------------------------------------------------------------------+
    | :math:`m(t)`                 | `conversion_factors[i][n,t]` or `conversion_factors[o][n,t]` | P    | Linear coefficient 1 (slope) of a **Non**-nonconvex flows                   |
    +------------------------------+--------------------------------------------------------------+------+-----------------------------------------------------------------------------+
    | :math:`y_\text{0,normed}(t)` | `normed_offsets[i][n,t]` or `normed_offsets[o][n,t]`         | P    | Linear coefficient 0 (y-intersection)/P_{nom}(t) of **Non**-nonconvex flows |
    +------------------------------+--------------------------------------------------------------+------+-----------------------------------------------------------------------------+

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
                (n, reference_node[n], f, t)
                for t in m.TIMESTEPS
                for n in group
                for f in in_flows[n] + out_flows[n]
            ],
            noruleinit=True,
        )

        def _relation_rule(block):
            """Link binary input and output flow to component outflow."""
            for t in m.TIMESTEPS:
                for n in group:
                    if reference_node_at_input[n]:
                        ref_flow = m.flow[reference_node[n], n, t]
                        status_nominal_idx = reference_node[n], n, t
                    else:
                        ref_flow = m.flow[n, reference_node[n], t]
                        status_nominal_idx = n, reference_node[n], t

                    try:
                        ref_status_nominal = (
                            m.InvestNonConvexFlowBlock.status_nominal[
                                status_nominal_idx
                            ]
                        )
                    except (AttributeError, KeyError):
                        ref_status_nominal = (
                            m.NonConvexFlowBlock.status_nominal[
                                status_nominal_idx
                            ]
                        )

                    for f in in_flows[n] + out_flows[n]:
                        rhs = 0
                        if f in in_flows[n]:
                            rhs += m.flow[f, n, t]
                        else:
                            rhs += m.flow[n, f, t]

                        lhs = 0
                        lhs += ref_flow * n.conversion_factors[f][t]
                        lhs += ref_status_nominal * n.normed_offsets[f][t]
                        block.relation.add(
                            (n, reference_node[n], f, t), (lhs == rhs)
                        )

        self.relation_build = BuildAction(rule=_relation_rule)


def slope_offset_from_nonconvex_input(
    max_load, min_load, eta_at_max, eta_at_min
):
    r"""Calculate the slope and the offset with max and min given for input

    The reference is the input flow here. That means, the `NonConvex` flow
    is specified at one of the input flows. The `max_load` and the `min_load`
    are the `max` and the `min` specifications for the `NonConvex` flow.
    `eta_at_max` and `eta_at_min` are the efficiency values of a different
    flow, e.g. an output, with respect to the `max_load` and `min_load`
    operation points.

    .. math::

        \text{slope} =
        \frac{
            \text{max} \cdot \eta_\text{at max}
            - \text{min} \cdot \eta_\text{at min}
        }{\text{max} - \text{min}}\\

        \text{offset} = \eta_\text{at,max} - \text{slope}

    Parameters
    ----------
    max_load : float
        Maximum load value, e.g. 1
    min_load : float
        Minimum load value, e.g. 0.5
    eta_at_max : float
        Efficiency at maximum load.
    eta_at_min : float
        Efficiency at minimum load.

    Returns
    -------
    tuple
        slope and offset

    Example
    -------
    >>> from oemof import solph
    >>> max_load = 1
    >>> min_load = 0.5
    >>> eta_at_min = 0.4
    >>> eta_at_max = 0.3

    With the input load being at 100 %, in this example, the efficiency should
    be 30 %. With the input load being at 50 %, it should be 40 %. We can
    calcualte slope and the offset which is normed to the nominal capacity of
    the referenced flow (in this case the input flow) always.

    >>> slope, offset = solph.components.slope_offset_from_nonconvex_input(
    ...     max_load, min_load, eta_at_max, eta_at_min
    ... )
    >>> input_flow = 10
    >>> input_flow_nominal = 10
    >>> output_flow = slope * input_flow + offset * input_flow_nominal

    We can then calculate with the `OffsetConverter` input output relation,
    what the resulting efficiency is. At max operating conditions it should be
    identical to the efficiency we put in initially. Analogously, we apply this
    to the minimal load point.

    >>> round(output_flow / input_flow, 3) == eta_at_max
    True
    >>> input_flow = 5
    >>> output_flow = slope * input_flow + offset * input_flow_nominal
    >>> round(output_flow / input_flow, 3) == eta_at_min
    True
    """
    slope = (max_load * eta_at_max - min_load * eta_at_min) / (
        max_load - min_load
    )
    offset = eta_at_max - slope
    return slope, offset


def slope_offset_from_nonconvex_output(
    max_load, min_load, eta_at_max, eta_at_min
):
    r"""Calculate the slope and the offset with max and min given for output.

    The reference is the output flow here. That means, the `NonConvex` flow
    is specified at one of the output flows. The `max_load` and the `min_load`
    are the `max` and the `min` specifications for the `NonConvex` flow.
    `eta_at_max` and `eta_at_min` are the efficiency values of a different
    flow, e.g. an input, with respect to the `max_load` and `min_load`
    operation points.

    .. math::

        \text{slope} =
        \frac{
            \frac{\text{max}}{\eta_\text{at max}}
            - \frac{\text{min}}{\eta_\text{at min}}
        }{\text{max} - \text{min}}\\

        \text{offset} = \frac{1}{\eta_\text{at,max}} - \text{slope}

    Parameters
    ----------
    max_load : float
        Maximum load value, e.g. 1
    min_load : float
        Minimum load value, e.g. 0.5
    eta_at_max : float
        Efficiency at maximum load.
    eta_at_min : float
        Efficiency at minimum load.

    Returns
    -------
    tuple
        slope and offset

    Example
    -------
    >>> from oemof import solph
    >>> max_load = 1
    >>> min_load = 0.5
    >>> eta_at_min = 0.7
    >>> eta_at_max = 0.8

    With the output load being at 100 %, in this example, the efficiency should
    be 80 %. With the input load being at 50 %, it should be 70 %. We can
    calcualte slope and the offset, which is normed to the nominal capacity of
    the referenced flow (in this case the output flow) always.

    >>> slope, offset = solph.components.slope_offset_from_nonconvex_output(
    ...     max_load, min_load, eta_at_max, eta_at_min
    ... )
    >>> output_flow = 10
    >>> output_flow_nominal = 10
    >>> input_flow = slope * output_flow + offset * output_flow_nominal

    We can then calculate with the `OffsetConverter` input output relation,
    what the resulting efficiency is. At max operating conditions it should be
    identical to the efficiency we put in initially. Analogously, we apply this
    to the minimal load point.

    >>> round(output_flow / input_flow, 3) == eta_at_max
    True
    >>> output_flow = 5
    >>> input_flow = slope * output_flow + offset * output_flow_nominal
    >>> round(output_flow / input_flow, 3) == eta_at_min
    True
    """
    slope = (max_load / eta_at_max - min_load / eta_at_min) / (
        max_load - min_load
    )
    offset = 1 / eta_at_max - slope
    return slope, offset
