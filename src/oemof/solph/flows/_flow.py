# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Edge

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Pierre-François Duc
SPDX-FileCopyrightText: Saeed Sayadi
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Lennart Schürmann

SPDX-License-Identifier: MIT

"""

import math
import numbers
from collections.abc import Iterable
from inspect import isbuiltin
from warnings import warn

import numpy as np
from oemof.network import Edge
from oemof.tools import debugging

from oemof.solph._options import Investment
from oemof.solph._plumbing import sequence


class Flow(Edge):
    r"""Defines a flow between two nodes.

    Keyword arguments are used to set the attributes of this flow. Parameters
    which are handled specially are noted below.
    For the case where a parameter can be either a scalar or an iterable, a
    scalar value will be converted to a sequence containing the scalar value at
    every index. This sequence is then stored under the parameter's key.

    Parameters
    ----------
    nominal_capacity : numeric, :math:`P_{nom}` or
            :class:`Investment <oemof.solph.options.Investment>`
        The nominal calacity of the flow, either fixed or as an investement
        optimisation. If this value is set, the corresponding optimization
        variable of the flow object will be bounded by this value
        multiplied by minimum(lower bound)/maximum(upper bound).
    variable_costs : numeric (iterable or scalar), default: 0, :math:`c`
        The costs associated with one unit of the flow per hour. The
        costs for each timestep (:math:`P_t \cdot c \cdot \delta(t)`)
        will be added to the objective expression of the optimization problem.
    maximum : numeric (iterable or scalar), default: 1, :math:`f_{maximum}`
        Normed maximum value of the flow. The flow absolute maximum will be
        calculated by multiplying :attr:`nominal_capacity` with :attr:`maximum`.
    minimum : numeric (iterable or scalar), default: 0, :math:`f_{minimum}`
        Normed minimum value of the flow (see :attr:`maximum`).
    fix : numeric (iterable or scalar), :math:`f_{fix}`
        Normed fixed value for the flow variable. Will be multiplied with the
        :attr:`nominal_capacity` to get the absolute value.
    positive_gradient_limit : numeric (iterable, scalar or None)
        the normed *upper bound* on the positive difference
        (`flow[t-1] < flow[t]`) of two consecutive flow values.
    negative_gradient_limit : numeric (iterable, scalar or None)
        the normed *upper bound* on the negative difference
        (`flow[t-1] > flow[t]`) of two consecutive flow values.
    full_load_time_max : numeric, :math:`t_{full\_load,maximum}`
        Maximum energy transported by the flow expressed as the time (in
        hours) that the flow would have to run at nominal capacity
        (`nominal_capacity`).
    full_load_time_min : numeric, :math:`t_{full\_load,minimum}`
        Minimum energy transported by the flow expressed as the time (in
        hours) that the flow would have to run at nominal capacity
        (`nominal_capacity`).
    integer : boolean
        Set True to bound the flow values to integers.
    nonconvex : :class:`NonConvex <oemof.solph.options.NonConvex>`
        If a nonconvex flow object is added here, the flow constraints will
        be altered significantly as the mathematical model for the flow
        will be different, i.e. constraint etc. from
        :class:`~oemof.solph.flows._non_convex_flow_block.NonConvexFlowBlock`
        will be used instead of
        :class:`~oemof.solph.flows._simple_flow_block.SimpleFlowBlock`.
    fixed_costs : numeric (iterable or scalar), :math:`c_{fixed}`
        The fixed costs associated with a flow.
        Note: These are only applicable for a multi-period model
        and given on a yearly basis.
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
    See :py:class:`~oemof.solph.flows._simple_flow.SimpleFlowBlock`
    for the variables, constraints and objective parts, that are created for
    a Flow object.

    Examples
    --------
    Creating a fixed flow object:

    >>> f = Flow(nominal_capacity=2, fix=[10, 4, 4], variable_costs=5)
    >>> f.variable_costs[2]
    5
    >>> f.fix[2]
    np.int64(4)

    Creating a flow object with time-depended lower and upper bounds:

    >>> f1 = Flow(minimum=[0.2, 0.3], maximum=0.99, nominal_capacity=100)
    >>> f1.maximum[1]
    0.99
    """  # noqa: E501

    def __init__(
        self,
        nominal_capacity=None,
        # --- BEGIN: To be removed for versions >= v0.7 ---
        nominal_value=None,
        min=None,
        max=None,
        # --- END ---
        variable_costs=0,
        minimum=None,
        maximum=None,
        fix=None,
        positive_gradient_limit=None,
        negative_gradient_limit=None,
        full_load_time_max=None,
        full_load_time_min=None,
        integer=False,
        # --- BEGIN: To be removed for versions >= v0.7 ---
        bidirectional=False,
        # --- END
        nonconvex=None,
        lifetime=None,
        age=None,
        fixed_costs=None,
        custom_attributes=None,  # To be removed for versions >= v0.7
        custom_properties=None,
    ):
        # TODO: Check if we can inherit from pyomo.core.base.var _VarData
        # then we need to create the var object with
        # pyomo.core.base.IndexedVarWithDomain before any SimpleFlowBlock
        # is created. E.g. create the variable in the energy system and
        # populate with information afterwards when creating objects.

        # --- BEGIN: The following code can be removed for versions >= v0.7 ---
        if nominal_value is not None:
            msg = (
                "For backward compatibility,"
                + " the option nominal_value overwrites the option"
                + " nominal_capacity."
                + " Both options cannot be set at the same time."
            )
            if nominal_capacity is not None:
                raise AttributeError(msg)
            else:
                warn(msg, FutureWarning)
            nominal_capacity = nominal_value

        if custom_attributes is not None:
            msg = (
                "For backward compatibility,"
                + " the option custom_attributes overwrites the option"
                + " custom_properties."
                + " Both options cannot be set at the same time."
            )
            if custom_properties is not None:
                raise AttributeError(msg)
            else:
                warn(msg, FutureWarning)
            custom_properties = custom_attributes

        if min is not None and isbuiltin(min) is False:
            msg = (
                "For backward compatibility,"
                + " the option min overwrites the option"
                + " minimum."
                + " Both options cannot be set at the same time."
            )
            if minimum is not None:
                raise AttributeError(msg)
            else:
                warn(msg, FutureWarning)
            minimum = min

        if max is not None and isbuiltin(max) is False:
            msg = (
                "For backward compatibility,"
                + " the option max overwrites the option"
                + " maximum."
                + " Both options cannot be set at the same time."
            )
            if maximum is not None:
                raise AttributeError(msg)
            else:
                warn(msg, FutureWarning)
            maximum = max

        if maximum is None:
            maximum = 1
        if minimum is None:
            minimum = 0
        # --- END ---
        super().__init__(custom_properties=custom_properties)
        # --- BEGIN: The following code can be removed for versions >= v0.7 ---
        if custom_attributes is not None:
            for attribute, value in custom_attributes.items():
                setattr(self, attribute, value)
        # --- END ---

        self.nominal_capacity = None
        self.investment = None

        infinite_error_msg = (
            "{} must be a finite value. Passing an infinite "
            "value is not allowed."
        )
        if isinstance(nominal_capacity, numbers.Real):
            if not math.isfinite(nominal_capacity):
                raise ValueError(infinite_error_msg.format("nominal_capacity"))
            self.nominal_capacity = nominal_capacity
        elif isinstance(nominal_capacity, Investment):
            self.investment = nominal_capacity

        if fixed_costs is not None:
            msg = (
                "Be aware that the fixed costs attribute is only\n"
                "meant to be used for multi-period models to depict "
                "fixed costs that occur on a yearly basis.\n"
                "If you wish to set up a multi-period model, explicitly "
                "set the `periods` attribute of your energy system.\n"
                "It has been decided to remove the `fixed_costs` "
                "attribute with v0.2 for regular uses.\n"
                "If you specify `fixed_costs` for a regular model, "
                "this will simply be silently ignored."
            )
            warn(msg, debugging.SuspiciousUsageWarning)

        self.fixed_costs = sequence(fixed_costs)
        self.variable_costs = sequence(variable_costs)
        self.positive_gradient_limit = sequence(positive_gradient_limit)
        self.negative_gradient_limit = sequence(negative_gradient_limit)

        self.full_load_time_max = full_load_time_max
        self.full_load_time_min = full_load_time_min
        self.integer = integer
        self.nonconvex = nonconvex
        self.lifetime = lifetime
        self.age = age

        # It is not allowed to define `minimum` or `maximum` if `fix`
        # is defined.
        # HINT: This also allows `flow`s with `fix` to be bidirectional,
        # if negative values are used in `fix`, despite `minimum` and
        # having the default values (0 and 1).
        # TODO: Is it intended to have bidirectional fixed flows?
        if fix is not None and (minimum != 0 or maximum != 1):
            msg = (
                "It is not allowed to define `minimum`/`maximum` if `fix` "
                "is defined."
            )
            raise AttributeError(msg)

        if sequence(minimum).min() < 0:
            msg = (
                "Setting `minimum` to negative values allows for the flow to "
                "become bidirectional, which is an experimental feature."
            )
            warn(msg, debugging.ExperimentalFeatureWarning)
            self.bidirectional = True
        # --- BEGIN: The following code can be removed for versions >= v0.7 ---
        elif bidirectional:
            msg = "The `bidirectional` keyword is deprecated and will be "
            "removed in a future version. It is recommended to "
            "set a negative value for `minimum` instead."
            warn(msg, FutureWarning)
            self.bidirectional = True
            if minimum == 0:
                minimum = -1
        # --- END
        else:
            self.bidirectional = False

        self.fix = sequence(fix)
        self.maximum = sequence(maximum)
        self.minimum = sequence(minimum)

        need_nominal_capacity = [
            "fix",
            "full_load_time_max",
            "full_load_time_min",
            "minimum",
            "maximum",
        ]
        need_nominal_capacity_defaults = {
            "fix": None,
            "full_load_time_max": None,
            "full_load_time_min": None,
            # --- BEGIN: The following code can be removed for versions >= v0.7
            "minimum": -1 if self.bidirectional else 0,
            # --- END
            # "minimum": 0,
            "maximum": 1,
        }
        if self.investment is None and self.nominal_capacity is None:
            for attr in need_nominal_capacity:
                if isinstance(getattr(self, attr), Iterable):
                    the_attr = getattr(self, attr)[0]
                else:
                    the_attr = getattr(self, attr)
                if the_attr != need_nominal_capacity_defaults[attr]:
                    raise AttributeError(
                        f"If {attr} is set in a flow, "
                        "nominal_capacity must be set as well."
                    )

        if self.nominal_capacity is not None and not math.isfinite(
            self.maximum[0]
        ):
            raise ValueError(infinite_error_msg.format("maximum"))

        # Checking for impossible gradient combinations
        if self.nonconvex:
            if self.nonconvex.positive_gradient_limit[0] is not None and (
                self.positive_gradient_limit[0] is not None
                or self.negative_gradient_limit[0] is not None
            ):
                raise ValueError(
                    "You specified a positive gradient in your nonconvex "
                    "option. This cannot be combined with a positive or a "
                    "negative gradient for a standard flow!"
                )

            if self.nonconvex.negative_gradient_limit[0] is not None and (
                self.positive_gradient_limit[0] is not None
                or self.negative_gradient_limit[0] is not None
            ):
                raise ValueError(
                    "You specified a negative gradient in your nonconvex "
                    "option. This cannot be combined with a positive or a "
                    "negative gradient for a standard flow!"
                )

        if (
            self.investment
            and self.nonconvex
            and not np.isfinite(self.investment.maximum.max())
        ):
            raise AttributeError(
                "Investment into a non-convex flows needs a maximum "
                + "investment to be set."
            )
