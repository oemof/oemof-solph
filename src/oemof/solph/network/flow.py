# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Edge

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

from warnings import warn

from oemof.network import network as on
from oemof.tools import debugging

from oemof.solph.plumbing import sequence


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
         * `'costs``: REMOVED!

    negative_gradient : :obj:`dict`, default: `{'ub': None, 'costs': 0}`

        A dictionary containing the following two keys:

          * `'ub'`: numeric (iterable, scalar or None), the normed *upper
            bound* on the negative difference (`flow[t-1] > flow[t]`) of
            two consecutive flow values.
          * `'costs``: REMOVED!

    summed_max : numeric, :math:`f_{sum,max}`
        Specific maximum value summed over all timesteps. Will be multiplied
        with the nominal_value to get the absolute limit.
    summed_min : numeric, :math:`f_{sum,min}`
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
        :class:`NonConvexFlow <oemof.solph.blocks.NonConvexFlow>`
        will be used instead of
        :class:`Flow <oemof.solph.blocks.Flow>`.
        Note: at the moment this does not work if the investment attribute is
        set .

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.flow.Flow`
     * :py:class:`~oemof.solph.blocks.investment_flow.InvestmentFlow`
        (additionally if Investment object is present)
     * :py:class:`~oemof.solph.blocks.non_convex_flow.NonConvexFlow`
        (If nonconvex  object is present, CAUTION: replaces
        :py:class:`~oemof.solph.blocks.flow.Flow`
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
        # pyomo.core.base.IndexedVarWithDomain before any Flow is created.
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
