# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Edge including base constraints

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga

SPDX-License-Identifier: MIT

"""
import math
from warnings import warn

from oemof.network import network as on
from oemof.tools import debugging
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import NonNegativeIntegers
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import ScalarBlock

from oemof.solph._plumbing import sequence
from oemof.solph._exceptions import (
    FlowOptionWarning,
    WrongOptionCombinationError,
)


class Flow(on.Edge):
    r"""Defines a flow between two nodes.

    Keyword arguments are used to set the attributes of this flow. Parameters
    which are handled specially are noted below.
    For the case where a parameter can be either a scalar or an iterable, a
    scalar value will be converted to a sequence containing the scalar value at
    every index. This sequence is then stored under the paramter's key.

    Parameters
    ----------
    nominal_value : numeric, :math:`P_{nom}`
        The nominal value of the flow. If this value is set the corresponding
        optimization variable of the flow object will be bounded by this value
        multiplied with min(lower bound)/max(upper bound).
    max : numeric (iterable or scalar), :math:`f_{max}`
        Normed maximum value of the flow. The flow absolute maximum will be
        calculated by multiplying :attr:`nominal_value` with :attr:`max`
    min : numeric (iterable or scalar), :math:`f_{min}`
        Normed minimum value of the flow (see :attr:`max`).
    fix : numeric (iterable or scalar), :math:`f_{fix}`
        Normed fixed value for the flow variable. Will be multiplied with the
        :attr:`nominal_value` to get the absolute value.
    positive_gradient : :obj:`dict`, default: `{'ub': None}`
        A dictionary containing the following key:

         * `'ub'`: numeric (iterable, scalar or None), the normed *upper
           bound* on the positive difference (`flow[t-1] < flow[t]`) of
           two consecutive flow values.

    negative_gradient : :obj:`dict`, default: `{'ub': None}`

        A dictionary containing the following key:

          * `'ub'`: numeric (iterable, scalar or None), the normed *upper
            bound* on the negative difference (`flow[t-1] > flow[t]`) of
            two consecutive flow values.

    full_load_time_max : numeric, :math:`t_{full\_load,max}`
        Upper bound on the summed flow expressed as the equivalent time that
        the flow would have to run at full capacity to yield the same sum. The
        value will be multiplied with the nominal_value to get the absolute
        limit.
    full_load_time_min : numeric, :math:`t_{full\_load,min}`
        Lower bound on the summed flow expressed as the equivalent time that
        the flow would have to run at full capacity to yield the same sum. The
        value will be multiplied with the nominal_value to get the absolute
        limit.
    variable_costs : numeric (iterable or scalar)
        The costs associated with one unit of the flow. If this is set the
        costs will be added to the objective expression of the optimization
        problem.
    fixed : boolean
        Boolean value indicating if a flow is fixed during the optimization
        problem to its ex-ante set value. Used in combination with the
        :attr:`fix`.
    integer : boolean
        Set True to bound the flow values to integers.
    investment : :class:`Investment <oemof.solph.options.Investment>`
        Object indicating if a nominal_value of the flow is determined by
        the optimization problem. Note: This will refer all attributes to an
        investment variable instead of to the nominal_value. The nominal_value
        should not be set (or set to None) if an investment object is used.
    nonconvex : :class:`NonConvex <oemof.solph.options.NonConvex>`
        If a nonconvex flow object is added here, the flow constraints will
        be altered significantly as the mathematical model for the flow
        will be different, i.e. constraint etc. from
        :class:`NonConvexFlowBlock <oemof.solph.blocks.NonConvexFlowBlock>`
        will be used instead of
        :class:`FlowBlock <oemof.solph.blocks.FlowBlock>`.
    allow_nonconvex_investment: :bool:
        If set to True, then the combinaison of nonconvex and investment flows
        is possible

    Notes
    -----
    See :py:class:`~oemof.solph.flows._flow.FlowBlock` for the variables,
    constraints and objective parts, that are created for a FLow object.

    Examples
    --------
    Creating a fixed flow object:

    >>> f = Flow(nominal_value=2, fix=[10, 4, 4], variable_costs=5)
    >>> f.variable_costs[2]
    5
    >>> f.fix[2]
    4

    Creating a flow object with time-depended lower and upper bounds:

    >>> f1 = Flow(min=[0.2, 0.3], max=0.99, nominal_value=100)
    >>> f1.max[1]
    0.99
    """

    def __init__(self, **kwargs):
        # TODO: Check if we can inherit from pyomo.core.base.var _VarData
        # then we need to create the var object with
        # pyomo.core.base.IndexedVarWithDomain before any FlowBlock is created.
        # E.g. create the variable in the energy system and populate with
        # information afterwards when creating objects.

        # --- BEGIN: The following code can be removed for versions >= v0.6 ---
        msg = (
            "\nThe parameter 'summed_{0}' ist deprecated and will be removed "
            "in version v0.6.\nRename the parameter to 'full_load_time_{0}', "
            "to avoid this warning and future problems. "
        )
        if "summed_max" in kwargs:
            warn(msg.format("max"), FutureWarning)
            kwargs["full_load_time_max"] = kwargs["summed_max"]
        if "summed_min" in kwargs:
            warn(msg.format("min"), FutureWarning)
            kwargs["full_load_time_min"] = kwargs["summed_min"]
        # --- END ---

        super().__init__()

        scalars = [
            "nominal_value",
            "full_load_time_max",
            "full_load_time_min",
            "investment",
            "nonconvex",
            "integer",
        ]
        sequences = ["fix", "variable_costs", "min", "max"]
        dictionaries = ["positive_gradient", "negative_gradient"]
        booleans = ["allow_nonconvex_investment"]
        defaults = {
            "variable_costs": 0,
            "positive_gradient": {"ub": None},
            "negative_gradient": {"ub": None},
            "allow_nonconvex_investment": False,
        }
        need_nominal_value = [
            "fix",
            "full_load_time_max",
            "full_load_time_min",
            "max",
            "min",
            # --- BEGIN: To be removed for versions >= v0.6 ---
            "summed_max",
            "summed_min",
            # --- END ---
        ]
        keys = [k for k in kwargs if k != "label"]

        if "fixed_costs" in keys:
            raise AttributeError(
                "The `fixed_costs` attribute has been removed" " with v0.2!"
            )

        if "actual_value" in keys:
            raise AttributeError(
                "The `actual_value` attribute has been renamed"
                " to `fix` with v0.4. The attribute `fixed` is"
                " set to True automatically when passing `fix`."
            )

        if "fixed" in keys:
            msg = (
                "The `fixed` attribute is deprecated.\nIf you have defined "
                "the `fix` attribute the flow variable will be fixed.\n"
                "The `fixed` attribute does not change anything."
            )
            warn(msg, debugging.SuspiciousUsageWarning)

        # It is not allowed to define min or max if fix is defined.
        if kwargs.get("fix") is not None and (
            kwargs.get("min") is not None or kwargs.get("max") is not None
        ):
            raise AttributeError(
                "It is not allowed to define `min`/`max` if `fix` is defined."
            )

        # Set default value for min and max
        if kwargs.get("min") is None:
            if "bidirectional" in keys:
                defaults["min"] = -1
            else:
                defaults["min"] = 0
        if kwargs.get("max") is None:
            defaults["max"] = 1

        # Check gradient dictionaries for non-valid keys
        for gradient_dict in ["negative_gradient", "positive_gradient"]:
            if gradient_dict in kwargs:
                if list(kwargs[gradient_dict].keys()) != list(
                    defaults[gradient_dict].keys()
                ):
                    msg = (
                        "Only the key 'ub' is allowed for the '{0}' attribute"
                    )
                    raise AttributeError(msg.format(gradient_dict))

        for attribute in set(
            scalars + sequences + dictionaries + booleans + keys
        ):
            value = kwargs.get(attribute, defaults.get(attribute))
            if attribute in dictionaries:
                setattr(
                    self,
                    attribute,
                    {"ub": sequence(value["ub"])},
                )

            else:
                setattr(
                    self,
                    attribute,
                    sequence(value) if attribute in sequences else value,
                )

        # Checking for impossible attribute combinations
        if self.investment and self.nominal_value is not None:
            raise ValueError(
                "Using the investment object the nominal_value"
                " has to be set to None."
            )

        # Checking for misuse of nonconvex and investment options of
        # <class 'solph.flows.Flow'> instead of using
        # <class 'solph.flows.NonConvexInvestFlow'>
        if self.allow_nonconvex_investment is False:
            if self.investment and self.nonconvex:
                raise WrongOptionCombinationError(
                    "Investment flows cannot be combined with "
                    + "nonconvex flows using the class "
                    + "<class 'solph.flows.Flow'>! Please consider using"
                    + " <class 'solph.flows.NonConvexInvestFlow'>"
                )
        else:
            warn(
                "You are using the class <class 'solph.flows.Flow'> "
                "with option `allow_nonconvex_investment`, please consider "
                "using <class 'solph.flows.NonConvexInvestFlow'> instead.",
                FlowOptionWarning,
            )

        infinite_error_msg = (
            "{} must be a finite value. Passing an infinite "
            "value is not allowed."
        )
        if not self.investment:
            if self.nominal_value is None:
                for attr in need_nominal_value:
                    if kwargs.get(attr) is not None:
                        raise AttributeError(
                            "If {} is set in a flow (except InvestmentFlow), "
                            "nominal_value must be set as well.\n"
                            "Otherwise, it won't have any effect.".format(attr)
                        )
            elif not math.isfinite(self.nominal_value):
                raise ValueError(infinite_error_msg.format("nominal_value"))
        if not math.isfinite(self.max[0]):
            raise ValueError(infinite_error_msg.format("max"))

        # Checking for impossible gradient combinations
        if self.nonconvex:
            if self.nonconvex.positive_gradient["ub"][0] is not None and (
                self.positive_gradient["ub"][0] is not None
                or self.negative_gradient["ub"][0] is not None
            ):
                raise ValueError(
                    "You specified a positive gradient in your nonconvex "
                    "option. This cannot be combined with a positive or a "
                    "negative gradient for a standard flow!"
                )

        if self.nonconvex:
            if self.nonconvex.negative_gradient["ub"][0] is not None and (
                self.positive_gradient["ub"][0] is not None
                or self.negative_gradient["ub"][0] is not None
            ):
                raise ValueError(
                    "You specified a negative gradient in your nonconvex "
                    "option. This cannot be combined with a positive or a "
                    "negative gradient for a standard flow!"
                )


class FlowBlock(ScalarBlock):
    r"""Flow block with definitions for standard flows.

    See :class:`~oemof.solph.flows._flow.Flow` class for all parameters of the *Flow*.

    **Variables**

    All *Flow* objects are indexed by a starting and ending node
    :math:`(i, o)`, which is omitted in the following for the sake of
    convenience. The creation of some variables depend on the values of
    *Flow* attributes. The following variables are created:

    * :math:`P(t)`
        Actual flow value (created in :class:`~oemof.solph._models.Model`).
        The variable is bound to: :math:`f_{min}(t) \cdot P_{nom} \ge P(t) \le f_{max}(t) \cdot P_{nom}`.

        If `Flow.fix` is not None the variable is bound to
        :math:`P(t) = f_{fix}`.

    * :math:`ve_n` (`Flow.negative_gradient` is not `None`)
        Difference of a flow in consecutive timesteps if flow is reduced. The
        variable is bound to: :math:`0 \ge ve_n \ge ve_n^{max}`.

    * :math:`ve_p` (`Flow.positive_gradient` is not `None`)
        Difference of a flow in consecutive timesteps if flow is increased. The
        variable is bound to: :math:`0 \ge ve_p \ge ve_p^{max}`.

    The following variable is build for Flows with the attribute
    `integer_flows` being not None.

    * :math:`i`(`Flow.integer` is `True`)
        All flow values are integers. Variable is bound to non-negative
        integers.

    **Constraints**

    The following constraints are created, if the appropriate attribute of the
    *Flow* (see :class:`oemof.solph.network.Flow`) object is set:

    * `Flow.full_load_time_max` is not `None` (full_load_time_max_constr):
        .. math::
            \sum_t P(t) \cdot \tau \leq F_{max} \cdot P_{nom}

    * `Flow.full_load_time_min` is not `None` (full_load_time_min_constr):
        .. math::
            \sum_t P(t) \cdot \tau \geq F_{min} \cdot P_{nom}


    * `Flow.negative_gradient` is not `None` (negative_gradient_constr):
        .. math::
          P(t-1) - P(t) \geq ve_n(t)

    * `Flow.positive_gradient` is not `None` (positive_gradient_constr):
        .. math::
          P(t) - P(t-1) \geq ve_p(t)

    * `Flow.integer` is `True`
        .. math::
          P(t) = i(t)

    **Objective function**

    Depending on the attributes of the `Flow` object the following parts of
    the objective function are created:

    * `Flow.variable_costs` is not `None`:
        .. math::
          \sum_{(i,o)} \sum_t P(t) \cdot c_{var}(i, o, t)

    .. csv-table:: List of Variables
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P(t)`", ":command:`flow[i, o][t]`", "Actual flow value"
        ":math:`ve_n`", ":command:`negative_gradient[n, o, t]`", "Negative gradient of the flow"
        ":math:`ve_p`", ":command:`positive_gradient[n, o, t]`", "Positive gradient of the flow"
        ":math:`i`", ":command:`integer_flow[i, o, t]`","Integer flow"


    .. csv-table:: List of Parameters
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P_{nom}`", ":command:`flows[i, o].nominal_value`","Nominal value of the flow"
        ":math:`F_{max}`",":command:`flow[i, o].full_load_time_max`", "Maximal full
        load time"
        ":math:`F_{min}`",":command:`flow[i, o].full_load_time_min`", "Minimal full
        load time"
        ":math:`c_{var}`", ":command:`variable\_costs[t]`", "Variable cost of the flow"
        ":math:`f_{max}`", ":command:`flows[i, o].max[t]`", "Normed maximum value of the flow, the absolute maximum is :math:`f_{max} \cdot P_{nom}`"
        ":math:`f_{min}`", ":command:`flows[i, o].min[t]`", "Normed minimum value of the flow, the absolute minimum is :math:`f_{min} \cdot P_{nom}`"
        ":math:`f_{fix}`", ":command:`flows[i, o].min[t]`", "Normed fixed value of the flow, the absolute fixed value is :math:`f_{fix} \cdot P_{nom}`"
        ":math:`ve_n^{max}`",":command:`flows[i, o].negative_gradient`","Normed maximal negative gradient of the flow, the absolute maximum gradient is :math:`ve_n^{max} \cdot P_{nom}`"
        ":math:`ve_p^{max}`",":command:`flows[i, o].positive_gradient`","Normed maximal positive gradient of the flow, the absolute maximum gradient is :math:`ve_n^{max} \cdot P_{nom}`"

    Note
    ----
    See the :class:`~oemof.solph.flows._flow.Flow` class for the definition of
    all parameters from the "List of Parameters above.

    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        r"""Creates sets, variables and constraints for all standard flows.

        Parameters
        ----------
        group : list
            List containing tuples containing flow (f) objects and the
            associated source (s) and target (t)
            of flow e.g. groups=[(s1, t1, f1), (s2, t2, f2),..]
        """
        if group is None:
            return None

        m = self.parent_block()

        # ########################## SETS #################################
        # set for all flows with an global limit on the flow over time
        self.FULL_LOAD_TIME_MAX_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].full_load_time_max is not None
                and g[2].nominal_value is not None
            ]
        )

        self.FULL_LOAD_TIME_MIN_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].full_load_time_min is not None
                and g[2].nominal_value is not None
            ]
        )

        self.NEGATIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].negative_gradient["ub"][0] is not None
            ]
        )

        self.POSITIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].positive_gradient["ub"][0] is not None
            ]
        )

        self.INTEGER_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].integer]
        )
        # ######################### Variables  ################################

        self.positive_gradient = Var(self.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS)

        self.negative_gradient = Var(self.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS)

        self.integer_flow = Var(
            self.INTEGER_FLOWS, m.TIMESTEPS, within=NonNegativeIntegers
        )
        # set upper bound of gradient variable
        for i, o, f in group:
            if m.flows[i, o].positive_gradient["ub"][0] is not None:
                for t in m.TIMESTEPS:
                    self.positive_gradient[i, o, t].setub(
                        f.positive_gradient["ub"][t] * f.nominal_value
                    )
            if m.flows[i, o].negative_gradient["ub"][0] is not None:
                for t in m.TIMESTEPS:
                    self.negative_gradient[i, o, t].setub(
                        f.negative_gradient["ub"][t] * f.nominal_value
                    )

        # ######################### CONSTRAINTS ###############################

        def _flow_full_load_time_max_rule(model):
            """Rule definition for build action of max. sum flow constraint."""
            for inp, out in self.FULL_LOAD_TIME_MAX_FLOWS:
                lhs = sum(
                    m.flow[inp, out, ts] * m.timeincrement[ts]
                    for ts in m.TIMESTEPS
                )
                rhs = (
                    m.flows[inp, out].full_load_time_max
                    * m.flows[inp, out].nominal_value
                )
                self.full_load_time_max_constr.add((inp, out), lhs <= rhs)

        self.full_load_time_max_constr = Constraint(
            self.FULL_LOAD_TIME_MAX_FLOWS, noruleinit=True
        )
        self.full_load_time_max_build = BuildAction(
            rule=_flow_full_load_time_max_rule
        )

        def _flow_full_load_time_min_rule(model):
            """Rule definition for build action of min. sum flow constraint."""
            for inp, out in self.FULL_LOAD_TIME_MIN_FLOWS:
                lhs = sum(
                    m.flow[inp, out, ts] * m.timeincrement[ts]
                    for ts in m.TIMESTEPS
                )
                rhs = (
                    m.flows[inp, out].full_load_time_min
                    * m.flows[inp, out].nominal_value
                )
                self.full_load_time_min_constr.add((inp, out), lhs >= rhs)

        self.full_load_time_min_constr = Constraint(
            self.FULL_LOAD_TIME_MIN_FLOWS, noruleinit=True
        )
        self.full_load_time_min_build = BuildAction(
            rule=_flow_full_load_time_min_rule
        )

        def _positive_gradient_flow_rule(model):
            """Rule definition for positive gradient constraint."""
            for inp, out in self.POSITIVE_GRADIENT_FLOWS:
                for ts in m.TIMESTEPS:
                    if ts > 0:
                        lhs = m.flow[inp, out, ts] - m.flow[inp, out, ts - 1]
                        rhs = self.positive_gradient[inp, out, ts]
                        self.positive_gradient_constr.add(
                            (inp, out, ts), lhs <= rhs
                        )

        self.positive_gradient_constr = Constraint(
            self.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.positive_gradient_build = BuildAction(
            rule=_positive_gradient_flow_rule
        )

        def _negative_gradient_flow_rule(model):
            """Rule definition for negative gradient constraint."""
            for inp, out in self.NEGATIVE_GRADIENT_FLOWS:
                for ts in m.TIMESTEPS:
                    if ts > 0:
                        lhs = m.flow[inp, out, ts - 1] - m.flow[inp, out, ts]
                        rhs = self.negative_gradient[inp, out, ts]
                        self.negative_gradient_constr.add(
                            (inp, out, ts), lhs <= rhs
                        )

        self.negative_gradient_constr = Constraint(
            self.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.negative_gradient_build = BuildAction(
            rule=_negative_gradient_flow_rule
        )

        def _integer_flow_rule(block, ii, oi, ti):
            """Force flow variable to NonNegativeInteger values."""
            return self.integer_flow[ii, oi, ti] == m.flow[ii, oi, ti]

        self.integer_flow_constr = Constraint(
            self.INTEGER_FLOWS, m.TIMESTEPS, rule=_integer_flow_rule
        )

    def _objective_expression(self):
        r"""Objective expression for all standard flows with fixed costs
        and variable costs.
        """
        m = self.parent_block()

        variable_costs = 0

        for i, o in m.FLOWS:
            if m.flows[i, o].variable_costs[0] is not None:
                for t in m.TIMESTEPS:
                    variable_costs += (
                        m.flow[i, o, t]
                        * m.objective_weighting[t]
                        * m.flows[i, o].variable_costs[t]
                    )

        return variable_costs
