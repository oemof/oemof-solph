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
SPDX-FileCopyrightText: Pierre-François Duc
SPDX-FileCopyrightText: Saeed Sayadi

SPDX-License-Identifier: MIT

"""
import math
from warnings import warn

import numpy as np
from oemof.network import network as on
from oemof.tools import debugging

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
        investment variable rather than to the nominal_value. The nominal_value
        should not be set (or set to None) if an investment object is used.
    nonconvex : :class:`NonConvex <oemof.solph.options.NonConvex>`
        If a nonconvex flow object is added here, the flow constraints will
        be altered significantly as the mathematical model for the flow
        will be different, i.e. constraint etc. from
        :class:`~oemof.solph.flows._non_convex_flow_block.NonConvexFlowBlock`
        will be used instead of
        :class:`~oemof.solph.flows._simple_flow_block.SimpleFlowBlock`.

    Notes
    -----
    See :py:class:`~oemof.solph.flows._simple_flow.SimpleFlowBlock`
    for the variables, constraints and objective parts, that are created for
    a Flow object.

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
    """  # noqa: E501

    def __init__(self, **kwargs):
        # TODO: Check if we can inherit from pyomo.core.base.var _VarData
        # then we need to create the var object with
        # pyomo.core.base.IndexedVarWithDomain before any SimpleFlowBlock
        # is created. E.g. create the variable in the energy system and
        # populate with information afterwards when creating objects.

        # --- BEGIN: The following code can be removed for versions >= v0.6 ---
        msg = (
            "\nThe parameter 'summed_{0}' is deprecated and will be removed "
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
        defaults = {
            "variable_costs": 0,
            "positive_gradient": {"ub": None},
            "negative_gradient": {"ub": None},
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

            if self.nonconvex.negative_gradient["ub"][0] is not None and (
                self.positive_gradient["ub"][0] is not None
                or self.negative_gradient["ub"][0] is not None
            ):
                raise ValueError(
                    "You specified a negative gradient in your nonconvex "
                    "option. This cannot be combined with a positive or a "
                    "negative gradient for a standard flow!"
                )

        if (
            self.investment
            and self.nonconvex
            and not np.isfinite(self.investment.maximum)
        ):
            raise AttributeError(
                "Investment into a non-convex flows needs a maximum "
                + "investment to be set."
            )
