.. _additional_constraints_label:

~~~~~~~~~~~~~~~~~~~~~~
Additional Constraints
~~~~~~~~~~~~~~~~~~~~~~

You can add additional constraints to your :py:class:`~oemof.solph.models.Model`.
See :ref:`custom_constraints_label` to learn how to do it.

Some predefined additional constraints can be found in the
:py:mod:`~oemof.solph.constraints` module.

 * Emission limit for the model -> :func:`~.oemof.solph.constraints.emission_limit`
 * Generic integral limit (general form of emission limit) -> :func:`~.oemof.solph.constraints.generic_integral_limit`
 * Coupling of two variables e.g. investment variables) with a factor -> :func:`~.oemof.solph.constraints.equate_variables`
 * Overall investment limit -> :func:`~.oemof.solph.constraints.investment_limit`
 * Generic investment limit -> :func:`~.oemof.solph.constraints.additional_investment_flow_limit`
 * Limit active flow count -> :func:`~.oemof.solph.constraints.limit_active_flow_count`
 * Limit active flow count by keyword -> :func:`~.oemof.solph.constraints.limit_active_flow_count_by_keyword`
