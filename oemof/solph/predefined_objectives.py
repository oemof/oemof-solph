# -*- coding: utf-8 -*-
"""
This module contains predefined objectives that can be used to model
energy systems.

@author: Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""
try:
    import objective_expressions as objexpr
except:
    from . import objective_expressions as objexpr

import pyomo.environ as po
import oemof.solph as solph

from ..core.network.entities import Bus, ExcessSlack, ShortageSlack
from ..core.network.entities.components import transformers as transformer
from ..core.network.entities.components import sources as source


def minimize_cost(self, cost_objects=None, revenue_objects=None):
    """ Builds objective function that minimises the total costs.

    Costs included are:
                        opex_var,
                        opex_fix,
                        curtailment_costs (dispatch sources),
                        annualised capex (investment components)

    Parameters
    ----------
    self : pyomo model instance
    cost_blocks : array like
       list containing classes of objects that are included in
               cost terms of objective function
    revenue_blocks : array like
       list containing classes of objects that are included in revenue
               terms of objective function
    """
    expr = 0
    # TODO: Fix naming
    c_blocks = cost_objects
    r_blocks = revenue_objects

    if cost_objects is None:
        c_blocks = [str(transformer.Simple),
                    str(transformer.TwoInputsOneOutput),
                    str(transformer.VariableEfficiencyCHP),
                    str(transformer.SimpleExtractionCHP),
                    str(transformer.Storage),
                    str(transformer.CHP),
                    str(source.FixedSource),
                    str(source.Commodity)]
    if revenue_objects is None:
        r_blocks = []

    blocks = [block for block in self.block_data_objects(active=True)
              if not isinstance(block,
                                solph.optimization_model.OptimizationModel)]

    for block in blocks:
        if block.name in c_blocks:
            if block.name == str(transformer.Storage):
                ref = 'capacity'
                expr += objexpr.add_opex_var(self,
                                             getattr(self,
                                                     str(transformer.Storage)),
                                             ref='input')
            else:
                ref = 'output'
            # variable costs
            expr += objexpr.add_opex_var(self, block, ref='output')
            # fix costs
            if block != str(source.Commodity):
                expr += objexpr.add_opex_fix(self, block, ref=ref)
            # investment costs
            if block.optimization_options.get('investment', False):
                expr += objexpr.add_capex(self, block, ref=ref)
            if hasattr(block, 'z_start'):
                expr += objexpr.add_startup_costs(self, block)

            # revenues
        if block.name in r_blocks:
            expr += objexpr.add_revenues(self, block, ref='output')

    # costs for dispatchable sources
    if hasattr(self, str(source.DispatchSource)):
        expr += \
            objexpr.add_curtailment_costs(self,
                                          getattr(self,
                                                  str(source.DispatchSource)))

    # artificial costs for excess or shortage
    if hasattr(self, str(ExcessSlack)):
        expr += objexpr.add_excess_slack_costs(self,
                                               getattr(self, str(ExcessSlack)))
    if hasattr(self, str(ShortageSlack)):
        expr += objexpr.add_shortage_slack_costs(self,
                                                 getattr(self, str(ShortageSlack)))


    self.objective = po.Objective(expr=expr)

