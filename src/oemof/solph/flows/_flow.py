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
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from warnings import warn

from oemof.network import network as on
from oemof.tools import debugging
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeIntegers
from pyomo.core import NonNegativeReals
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
    every index. This sequence is then stored under the parameter's key.

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
         * `'costs'`: REMOVED!

    negative_gradient : :obj:`dict`, default: `{'ub': None, 'costs': 0}`

        A dictionary containing the following two keys:

          * `'ub'`: numeric (iterable, scalar or None), the normed *upper
            bound* on the negative difference (`flow[t-1] > flow[t]`) of
            two consecutive flow values.
          * `'costs'`: REMOVED!

    summed_max : numeric, :math:`f_{sum,max}`
        Specific maximum value summed over all timesteps. Will be multiplied
        with the nominal_value to get the absolute limit.
    summed_min : numeric, :math:`f_{sum,min}`
        see above
    variable_costs : numeric (iterable or scalar), :math:`c_{var}`
        The costs associated with one unit of the flow. If this is set the
        costs will be added to the objective expression of the optimization
        problem.
        Note: In a multi-period model, nominal costs have to be used.
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
        set.
    integer : boolean
        If True, flow is forced to take only integer values
    fixed_costs : numeric (iterable or scalar), :math:`c_{fixed}`
        The fixed costs associated with a flow.
        Note: These are only applicable for a multi-period model.
    lifetime : int, :math:`l`
        The lifetime of a flow (usually given in years);
        once it reaches its lifetime (considering also
        an initial age), the flow is forced to 0.
        Note: Only applicable for a multi-period model.
    age : int, :math:`a`
        The initial age of a flow (usually given in years);
        once it reaches its lifetime (considering also
        an initial age), the flow is forced to 0.
        Note: Only applicable for a multi-period model.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created

    * :py:class:`~oemof.solph.flows.flow.FlowBlock`
    * :py:class:`~oemof.solph.flows.investment_flow.InvestmentFlowBlock`
      (additionally if Investment object is present)
    * :py:class:`~oemof.solph.flows.non_convex_flow.NonConvexFlowBlock`
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
            "summed_max",
            "summed_min",
            "investment",
            "nonconvex",
            "integer",
            "lifetime",
            "age",
        ]
        sequences = ["fix", "variable_costs", "fixed_costs", "min", "max"]
        dictionaries = ["positive_gradient", "negative_gradient"]
        defaults = {
            "variable_costs": 0,
            "positive_gradient": {"ub": None},
            "negative_gradient": {"ub": None},
        }
        keys = [k for k in kwargs if k != "label"]

        if "fixed_costs" in keys:
            msg = (
                "Be aware that the fixed costs attribute is only\n"
                "meant to be used for multi-period models.\n"
                "If you wish to set up a multi-period model, set the"
                " multi_period attribute of your energy system to True.\n"
                "It has been decided to remove the `fixed_costs` "
                "attribute with v0.2 for regular uses.\n"
                "If you specify `fixed_costs` for a regular model, "
                "it will simply be ignored."
            )
            warn(msg, debugging.SuspiciousUsageWarning)

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

    SUMMED_MAX_FLOWS
        A set of flows with the attribute :attr:`summed_max` being not None.
    SUMMED_MIN_FLOWS
        A set of flows with the attribute :attr:`summed_min` being not None.
    NEGATIVE_GRADIENT_FLOWS
        A set of flows with the attribute :attr:`negative_gradient` being not
        None.
    POSITIVE_GRADIENT_FLOWS
        A set of flows with the attribute :attr:`positive_gradient` being not
        None
    INTEGER_FLOWS
        A set of flows where the attribute :attr:`integer` is True (forces flow
        to only take integer values)
    LIFETIME_FLOWS
        All flows with a given attribute :attr:`lifetime`, but no initial
        :attr:`age` given
    LIFETIME_AGE_FLOWS
        All flows with a given attribute :attr:`lifetime` and an initial
        :attr:`age` given

    **The following constraints are build:**

    FlowBlock max sum :attr:`om.FlowBlock.summed_max[i, o]`
      .. math::
        \sum_{p, t \in \textrm{TIMEINDEX}} flow(i, o, p, t) \cdot \tau
            \leq summed\_max(i, o) \cdot nominal\_value(i, o), \\
        \forall (i, o) \in \textrm{SUMMED\_MAX\_FLOWS}.

    FlowBlock min sum :attr:`om.FlowBlock.summed_min[i, o]`
      .. math::
        \sum_{p, t \in \textrm{TIMEINDEX}} flow(i, o, p, t) \cdot \tau
            \geq summed\_min(i, o) \cdot nominal\_value(i, o), \\
        \forall (i, o) \in \textrm{SUMMED\_MIN\_FLOWS}.

    Negative gradient constraint
      :attr:`om.FlowBlock.negative_gradient_constr[i, o]`:
        .. math::
          &
          if \quad t > 0:\\
          &
          flow(i, o, p, t-1) - flow(i, o, p, t) \geq \
          negative\_gradient(i, o, t), \\
          &\\
          &
          else:\\
          &
          flow(i, o, p, t) = 0\\
          &\\
          &
          \forall (i, o) \in \textrm{NEGATIVE\_GRADIENT\_FLOWS}, \\
          &
          p, t \in \textrm{TIMEINDEX}\\.

    Positive gradient constraint
      :attr:`om.FlowBlock.positive_gradient_constr[i, o]`:
        .. math::
          &
          if \quad t > 0:\\
          &
          flow(i, o, p t) - flow(i, o, p, t-1) \geq \
          positive\_gradient(i, o, t), \\
          &\\
          &
          else:\\
          &
          flow(i, o, p, t) = 0\\
          &\\
          &
          \forall (i, o) \in \textrm{POSITIVE\_GRADIENT\_FLOWS}, \\
          &
          p, t \in \textrm{TIMEINDEX}\\.

    Note
    ----
    The gradient implementations combine a timestep and its predecessor.
    This predecessor might also lie in the previous period. For the sake
    of readability, this is not represented in the mathematical
    formulation above, but taken care of by
    checking the previous index of the TIMEINDEX set.


    Integer constraint
      :attr:`om.FlowBlock.integer_flow_constr[i, o]`:
        .. math::
          integer\_flow(i, o, t) = flow(i, o, p, t) \\
          \forall p, t \in \textrm{TIMEINDEX}, integer\_flow(i, o, t)
          \in \textrm{N}

    Lifetime output constraint: Force flow to 0 once it exceeds its lifetime
      :attr:`om.FlowBlock.lifetime_output[i, o]`:
        .. math::
          &
          if \quad lifetime(i, o) < year(p):\\
          &
          flow(i, o, p, t) = 0 \\
          &
          \forall p, t \in \textrm{TIMEINDEX},
          (i, o) \in \textrm{LIFETIME\_FLOWS}

    Lifetime age output constraint:
    Force flow to 0 once it exceeds its lifetime, considering its initial age
    :attr:`om.FlowBlock.lifetime_age_output[i, o]`:

        .. math::
          &
          if \quad lifetime(i, o) - age(i, o) < year(p):\\
          &
          flow(i, o, p, t) = 0 \\
          &
          \forall p, t \in \textrm{TIMEINDEX},
          (i, o) \in \textrm{LIFETIME\_AGE\_FLOWS}

    Whereby:

    * :math:`year(p)` is the year corresponding to period p
    * :math:`lifetime(i, o)` is the expected technical lifetime of flow (i, o)
    * :math:`age(i, o)` is the initial age of flow (i, o)

    **The following parts of the objective function are created:**

    *Standard model*

    If :attr:`variable_costs` is set by the user:
      .. math::
          \sum_{(i,o)} \sum_{p, t \in \textrm{TIMEINDEX}}
          flow(i, o, p, t) \cdot weight(t) \cdot variable\_costs(i, o, t)

    The expression can be accessed by :attr:`om.FlowBlock.variable_costs` and
    their value after optimization by :meth:`om.FlowBlock.variable_costs()`.

    *Multi-period model*

    If :attr:`variable_costs` is set by the user:
      .. math::
          \sum_{(i,o)} \sum_{p, t \in \textrm{TIMEINDEX}}
          flow(i, o, p, t) \cdot weight(t) \cdot variable\_costs(i, o, t)
          \cdot DF^{-p}

    If :attr:`fixed_costs` is set by the user and no lifetime limitation:
      .. math::
          \sum_{(i,o)} \sum_{p \in {PERIODS}}
          nominal\_value(i, o) \cdot fixed\_costs(i, o, p)
          \cdot DF^{-p}

    If :attr:`fixed_costs` is set by the user and flow
    has a :attr:`lifetime` attribute defined:

      .. math::
          \sum_{(i,o)} \sum_{pp=0}^{lifetime(i, o)}
          nominal\_value(i, o) \cdot fixed\_costs(i, o, pp)
          \cdot DF^{-pp}

    If :attr:`fixed_costs` is set by the user and flow has a :attr:`lifetime`
    and an :attr:`age` attribute defined:

      .. math::
          \sum_{(i,o)} \sum_{pp=0}^{lifetime(i, o) - age(i, o)}
          nominal\_value(i, o) \cdot fixed\_costs(i, o, pp)
          \cdot DF^{-pp}

    Whereby:

    * :math:`DF=(1+dr)` is the discount factor with discount rate :math:`dr`
    * :math:`weight(t)` is the objective weighting term for timestep t

    Cost expressions can be accessed by

    * :attr:`om.FlowBlock.variable_costs`,
    * :attr:`om.FlowBlock.fixed_costs` and
    * :attr:`om.FlowBlock.costs`.

    Their values  after optimization can be retrieved by

    * :meth:`om.FlowBlock.variable_costs()`,
    * :meth:`om.FlowBlock.fixed_costs()` and
    * :meth:`om.FlowBlock.costs()`

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
        self.SUMMED_MAX_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].summed_max is not None
                and g[2].nominal_value is not None
            ]
        )

        self.SUMMED_MIN_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].summed_min is not None
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

        self.LIFETIME_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].lifetime is not None and g[2].age is None
            ]
        )

        self.LIFETIME_AGE_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].lifetime is not None and g[2].age is not None
            ]
        )
        # ######################### Variables  ################################

        self.positive_gradient = Var(
            self.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS, within=NonNegativeReals
        )

        self.negative_gradient = Var(
            self.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS, within=NonNegativeReals
        )

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

        def _flow_summed_max_rule(model):
            """Rule definition for build action of max. sum flow constraint."""
            for inp, out in self.SUMMED_MAX_FLOWS:
                lhs = sum(
                    m.flow[inp, out, p, ts] * m.timeincrement[ts]
                    for p, ts in m.TIMEINDEX
                )
                rhs = (
                    m.flows[inp, out].summed_max
                    * m.flows[inp, out].nominal_value
                )
                self.summed_max.add((inp, out), lhs <= rhs)

        self.summed_max = Constraint(self.SUMMED_MAX_FLOWS, noruleinit=True)
        self.summed_max_build = BuildAction(rule=_flow_summed_max_rule)

        def _flow_summed_min_rule(model):
            """Rule definition for build action of min. sum flow constraint."""
            for inp, out in self.SUMMED_MIN_FLOWS:
                lhs = sum(
                    m.flow[inp, out, p, ts] * m.timeincrement[ts]
                    for p, ts in m.TIMEINDEX
                )
                rhs = (
                    m.flows[inp, out].summed_min
                    * m.flows[inp, out].nominal_value
                )
                self.summed_min.add((inp, out), lhs >= rhs)

        self.summed_min = Constraint(self.SUMMED_MIN_FLOWS, noruleinit=True)
        self.summed_min_build = BuildAction(rule=_flow_summed_min_rule)

        def _positive_gradient_flow_rule(model):
            """Rule definition for positive gradient constraint."""
            for inp, out in self.POSITIVE_GRADIENT_FLOWS:
                for index in range(1, len(m.TIMEINDEX) + 1):
                    if m.TIMEINDEX[index][1] > 0:
                        lhs = (
                            m.flow[
                                inp,
                                out,
                                m.TIMEINDEX[index][0],
                                m.TIMEINDEX[index][1],
                            ]
                            - m.flow[
                                inp,
                                out,
                                m.TIMEINDEX[index - 1][0],
                                m.TIMEINDEX[index - 1][1],
                            ]
                        )
                        rhs = self.positive_gradient[
                            inp, out, m.TIMEINDEX[index][1]
                        ]
                        self.positive_gradient_constr.add(
                            (
                                inp,
                                out,
                                m.TIMEINDEX[index][0],
                                m.TIMEINDEX[index][1],
                            ),
                            lhs <= rhs,
                        )
                    else:
                        lhs = self.positive_gradient[inp, out, 0]
                        rhs = 0
                        self.positive_gradient_constr.add(
                            (
                                inp,
                                out,
                                m.TIMEINDEX[index][0],
                                m.TIMEINDEX[index][1],
                            ),
                            lhs == rhs,
                        )

        self.positive_gradient_constr = Constraint(
            self.POSITIVE_GRADIENT_FLOWS, m.TIMEINDEX, noruleinit=True
        )
        self.positive_gradient_build = BuildAction(
            rule=_positive_gradient_flow_rule
        )

        def _negative_gradient_flow_rule(model):
            """Rule definition for negative gradient constraint."""
            for inp, out in self.NEGATIVE_GRADIENT_FLOWS:
                for index in range(1, len(m.TIMEINDEX) + 1):
                    if m.TIMEINDEX[index][1] > 0:
                        lhs = (
                            m.flow[
                                inp,
                                out,
                                m.TIMEINDEX[index - 1][0],
                                m.TIMEINDEX[index - 1][1],
                            ]
                            - m.flow[
                                inp,
                                out,
                                m.TIMEINDEX[index][0],
                                m.TIMEINDEX[index][1],
                            ]
                        )
                        rhs = self.negative_gradient[
                            inp, out, m.TIMEINDEX[index][1]
                        ]
                        self.negative_gradient_constr.add(
                            (
                                inp,
                                out,
                                m.TIMEINDEX[index][0],
                                m.TIMEINDEX[index][1],
                            ),
                            lhs <= rhs,
                        )
                    else:
                        lhs = self.negative_gradient[inp, out, 0]
                        rhs = 0
                        self.negative_gradient_constr.add(
                            (
                                inp,
                                out,
                                m.TIMEINDEX[index][0],
                                m.TIMEINDEX[index][1],
                            ),
                            lhs == rhs,
                        )

        self.negative_gradient_constr = Constraint(
            self.NEGATIVE_GRADIENT_FLOWS, m.TIMEINDEX, noruleinit=True
        )
        self.negative_gradient_build = BuildAction(
            rule=_negative_gradient_flow_rule
        )

        def _integer_flow_rule(block, ii, oi, pi, ti):
            """Force flow variable to NonNegativeInteger values."""
            return self.integer_flow[ii, oi, ti] == m.flow[ii, oi, pi, ti]

        self.integer_flow_constr = Constraint(
            self.INTEGER_FLOWS, m.TIMEINDEX, rule=_integer_flow_rule
        )

        if m.es.multi_period:

            def _lifetime_output_rule(block):
                """Force flow value to zero when lifetime is reached"""
                for inp, out in self.LIFETIME_FLOWS:
                    for p, ts in m.TIMEINDEX:
                        if m.flows[inp, out].lifetime <= m.es.periods_years[p]:
                            lhs = m.flow[inp, out, p, ts]
                            rhs = 0
                            self.lifetime_output.add(
                                (inp, out, p, ts), (lhs == rhs)
                            )

            self.lifetime_output = Constraint(
                self.LIFETIME_FLOWS, m.TIMEINDEX, noruleinit=True
            )
            self.lifetime_output_build = BuildAction(
                rule=_lifetime_output_rule
            )

            def _lifetime_age_output_rule(block):
                """Force flow value to zero when lifetime is reached
                considering initial age
                """
                for inp, out in self.LIFETIME_AGE_FLOWS:
                    for p, ts in m.TIMEINDEX:
                        if (
                            m.flows[inp, out].lifetime - m.flows[inp, out].age
                            <= m.es.periods_years[p]
                        ):
                            lhs = m.flow[inp, out, p, ts]
                            rhs = 0
                            self.lifetime_age_output.add(
                                (inp, out, p, ts), (lhs == rhs)
                            )

            self.lifetime_age_output = Constraint(
                self.LIFETIME_AGE_FLOWS, m.TIMEINDEX, noruleinit=True
            )
            self.lifetime_age_output_build = BuildAction(
                rule=_lifetime_age_output_rule
            )

    def _objective_expression(self):
        r"""Objective expression for all standard flows with fixed costs
        and variable costs.
        """
        m = self.parent_block()

        variable_costs = 0
        fixed_costs = 0

        if not m.es.multi_period:
            for i, o in m.FLOWS:
                if m.flows[i, o].variable_costs[0] is not None:
                    for p, t in m.TIMEINDEX:
                        variable_costs += (
                            m.flow[i, o, p, t]
                            * m.objective_weighting[t]
                            * m.flows[i, o].variable_costs[t]
                        )

        else:
            for i, o in m.FLOWS:
                if m.flows[i, o].variable_costs[0] is not None:
                    for p, t in m.TIMEINDEX:
                        variable_costs += (
                            m.flow[i, o, p, t]
                            * m.objective_weighting[t]
                            * m.flows[i, o].variable_costs[t]
                            * ((1 + m.discount_rate) ** -m.es.periods_years[p])
                        )

                # Include fixed costs of units operating "forever"
                if (
                    m.flows[i, o].fixed_costs[0] is not None
                    and m.flows[i, o].nominal_value is not None
                    and (i, o) not in self.LIFETIME_FLOWS
                    and (i, o) not in self.LIFETIME_AGE_FLOWS
                ):
                    for p in m.PERIODS:
                        fixed_costs += (
                            m.flows[i, o].nominal_value
                            * m.flows[i, o].fixed_costs[p]
                            * ((1 + m.discount_rate) ** -m.es.periods_years[p])
                        )

            # Fixed costs for units with limited lifetime
            for i, o in self.LIFETIME_FLOWS:
                if m.flows[i, o].fixed_costs[0] is not None:
                    fixed_costs += sum(
                        m.flows[i, o].nominal_value
                        * m.flows[i, o].fixed_costs[pp]
                        * ((1 + m.discount_rate) ** (-pp))
                        for pp in range(0, m.flows[i, o].lifetime)
                    )

            for i, o in self.LIFETIME_AGE_FLOWS:
                if m.flows[i, o].fixed_costs[0] is not None:
                    fixed_costs += sum(
                        m.flows[i, o].nominal_value
                        * m.flows[i, o].fixed_costs[pp]
                        * ((1 + m.discount_rate) ** (-pp))
                        for pp in range(
                            0, m.flows[i, o].lifetime - m.flows[i, o].age
                        )
                    )

        self.variable_costs = Expression(expr=variable_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.costs = Expression(expr=variable_costs + fixed_costs)

        return self.costs
