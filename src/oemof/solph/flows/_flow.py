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

from warnings import warn

from oemof.network import network as on
from oemof.tools import debugging
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import NonNegativeIntegers
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import SimpleBlock

from oemof.solph._plumbing import sequence


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
    fix : numeric (iterable or scalar), :math:`f_{actual}`
        Normed fixed value for the flow variable. Will be multiplied with the
        :attr:`nominal_value` to get the absolute value. If :attr:`fixed` is
        set to :obj:`True` the flow variable will be fixed to `fix
        * nominal_value`, i.e. this value is set exogenous.
    positive_gradient : :obj:`dict`, default: `{'ub': None, 'costs': 0}`
        A dictionary containing the following two keys:

         * `'ub'`: numeric (iterable, scalar or None), the normed *upper
           bound* on the positive difference (`flow[t-1] < flow[t]`) of
           two consecutive flow values.
         * `'costs``: numeric (scalar or None), the gradient cost per
           unit.

    negative_gradient : :obj:`dict`, default: `{'ub': None, 'costs': 0}`

        A dictionary containing the following two keys:

          * `'ub'`: numeric (iterable, scalar or None), the normed *upper
            bound* on the negative difference (`flow[t-1] > flow[t]`) of
            two consecutive flow values.
          * `'costs``: numeric (scalar or None), the gradient cost per
            unit.

    max_capacity_factor : numeric, :math:`f_{sum,max}`
        Specific maximum value summed over all timesteps. Will be multiplied
        with the nominal_value to get the absolute limit.
    min_capacity_factor : numeric, :math:`f_{sum,min}`
        see above
    variable_costs : numeric (iterable or scalar)
        The costs associated with one unit of the flow. If this is set the
        costs will be added to the objective expression of the optimization
        problem.
    fixed : boolean
        Boolean value indicating if a flow is fixed during the optimization
        problem to its ex-ante set value. Used in combination with the
        :attr:`fix`.
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
        Note: at the moment this does not work if the investment attribute is
        set .

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph..flows.flow.FlowBlock`
     * :py:class:`~oemof.solph..flows.investment_flow.InvestmentFlowBlock`
        (additionally if Investment object is present)
     * :py:class:`~oemof.solph..flows.non_convex_flow.NonConvexFlowBlock`
        (If nonconvex  object is present, CAUTION: replaces
        :py:class:`~oemof.solph.flows.flow.FlowBlock`
        class and a MILP will be build)

    Examples
    --------
    Creating a fixed flow object:

    >>> f = Flow(fix=[10, 4, 4], variable_costs=5)
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

        super().__init__()

        scalars = [
            "nominal_value",
            "max_capacity_factor",
            "min_capacity_factor",
            "investment",
            "nonconvex",
            "integer",
        ]
        sequences = ["fix", "variable_costs", "min", "max"]
        dictionaries = ["positive_gradient", "negative_gradient"]
        defaults = {
            "variable_costs": 0,
            "positive_gradient": {"ub": None},
            "negative_gradient": {"ub": None},
        }
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
                "It is not allowed to define min/max if fix is defined."
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

        for attribute in set(scalars + sequences + dictionaries + keys):
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
        if self.investment and self.nonconvex:
            raise ValueError(
                "Investment flows cannot be combined with "
                + "nonconvex flows!"
            )

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


class FlowBlock(SimpleBlock):
    r""" FlowBlock block with definitions for standard flows.

    **The following variables are created**:

    negative_gradient :
        Difference of a flow in consecutive timesteps if flow is reduced
        indexed by NEGATIVE_GRADIENT_FLOWS, TIMESTEPS.

    positive_gradient :
        Difference of a flow in consecutive timesteps if flow is increased
        indexed by NEGATIVE_GRADIENT_FLOWS, TIMESTEPS.

    **The following sets are created:** (-> see basic sets at :class:`.Model` )

    MAX_CAPACITY_FACTOR_FLOWS
        A set of flows with the attribute :attr:`max_capacity_factor` being not
        None.
    MIN_CAPACITY_FACTOR_FLOWS
        A set of flows with the attribute :attr:`min_capacity_factor` being not
        None.
    NEGATIVE_GRADIENT_FLOWS
        A set of flows with the attribute :attr:`negative_gradient` being not
        None.
    POSITIVE_GRADIENT_FLOWS
        A set of flows with the attribute :attr:`positive_gradient` being not
        None
    INTEGER_FLOWS
        A set of flows where the attribute :attr:`integer` is True (forces flow
        to only take integer values)

    **The following constraints are build:**

    FlowBlock max sum :attr:`om.FlowBlock.max_capacity_factor[i, o]`
      .. math::
        \sum_t flow(i, o, t) \cdot \tau
            \leq summed\_max(i, o) \cdot nominal\_value(i, o), \\
        \forall (i, o) \in \textrm{SUMMED\_MAX\_FLOWS}.

    FlowBlock min sum :attr:`om.FlowBlock.min_capacity_factor[i, o]`
      .. math::
        \sum_t flow(i, o, t) \cdot \tau
            \geq summed\_min(i, o) \cdot nominal\_value(i, o), \\
        \forall (i, o) \in \textrm{SUMMED\_MIN\_FLOWS}.

    Negative gradient constraint
      :attr:`om.FlowBlock.negative_gradient_constr[i, o]`:
        .. math::
          flow(i, o, t-1) - flow(i, o, t) \geq \
          negative\_gradient(i, o, t), \\
          \forall (i, o) \in \textrm{NEGATIVE\_GRADIENT\_FLOWS}, \\
          \forall t \in \textrm{TIMESTEPS}.

    Positive gradient constraint
      :attr:`om.FlowBlock.positive_gradient_constr[i, o]`:
        .. math:: flow(i, o, t) - flow(i, o, t-1) \geq \
          positive\__gradient(i, o, t), \\
          \forall (i, o) \in \textrm{POSITIVE\_GRADIENT\_FLOWS}, \\
          \forall t \in \textrm{TIMESTEPS}.

    **The following parts of the objective function are created:**

    If :attr:`variable_costs` are set by the user:
      .. math::
          \sum_{(i,o)} \sum_t flow(i, o, t) \cdot variable\_costs(i, o, t)

    The expression can be accessed by :attr:`om.FlowBlock.variable_costs` and
    their value after optimization by :meth:`om.FlowBlock.variable_costs()` .

    """

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
        self.MAX_CAPACITY_FACTOR_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].max_capacity_factor is not None
                and g[2].nominal_value is not None
            ]
        )

        self.MIN_CAPACITY_FACTOR_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].min_capacity_factor is not None
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

        def _flow_max_capacity_factor_rule(model):
            """Rule definition for build action of max. sum flow constraint."""
            for inp, out in self.MAX_CAPACITY_FACTOR_FLOWS:
                lhs = sum(
                    m.flow[inp, out, ts] * m.timeincrement[ts]
                    for ts in m.TIMESTEPS
                )
                rhs = (
                    m.flows[inp, out].max_capacity_factor
                    * m.flows[inp, out].nominal_value
                )
                self.max_capacity_factor.add((inp, out), lhs <= rhs)

        self.max_capacity_factor = Constraint(
            self.MAX_CAPACITY_FACTOR_FLOWS, noruleinit=True
        )
        self.max_capacity_factor_build = BuildAction(
            rule=_flow_max_capacity_factor_rule
        )

        def _flow_min_capacity_factor_rule(model):
            """Rule definition for build action of min. sum flow constraint."""
            for inp, out in self.MIN_CAPACITY_FACTOR_FLOWS:
                lhs = sum(
                    m.flow[inp, out, ts] * m.timeincrement[ts]
                    for ts in m.TIMESTEPS
                )
                rhs = (
                    m.flows[inp, out].min_capacity_factor
                    * m.flows[inp, out].nominal_value
                )
                self.min_capacity_factor.add((inp, out), lhs >= rhs)

        self.min_capacity_factor = Constraint(
            self.MIN_CAPACITY_FACTOR_FLOWS, noruleinit=True
        )
        self.min_capacity_factor_build = BuildAction(
            rule=_flow_min_capacity_factor_rule
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
