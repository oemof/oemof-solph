# -*- coding: utf-8 -*-

"""Modules for providing a convenient data structure for solph results.

SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Patrik Schönfeldt <patrik.schoenfeldt@dlr.de>

SPDX-License-Identifier: MIT

"""

import warnings
from functools import cache

import pandas as pd
from oemof.tools import debugging
from pyomo.core.base.var import Var

from ._models import Model


class Results:
    # TODO:
    #   Defer attribute references not present as variables to
    #   attributes of `model.solver_results` in order to make `Results`
    #   instances returnable by `model.solve` and still be backwards
    #   compatible.
    def __init__(self, model: Model):
        msg = (
            "The class 'Results' is experimental. Functionality and API can"
            " be changed without warning during any update."
        )
        warnings.warn(msg, debugging.ExperimentalFeatureWarning)
        self.variables = {}
        for vardata in model.component_data_objects(Var):
            for variable in [vardata.parent_component()]:
                key = str(variable).split(".")[-1]
                if key not in self.variables:
                    self.variables[key] = variable
                else:
                    raise ValueError(
                        f"Variable name defined multiple times: {key}"
                        + f"(last time in '{variable}')"
                    )

    @cache
    def to_df(self, variable: str) -> pd.DataFrame | pd.Series:
        # TODO:
        #   - Figure out why `Results.init_content` is a `pd.Series`.
        #   - Support `Var`s as arguments?
        #   - Add column (level) and index names like:
        #       source, target, timestep etc.
        """Return a `DataFrame` view of the model's `variable`.

        This is the function that attribute and dictionary access to
        variables as `DataFrame`s is based on. Use it if you like to be
        explicit.
        For convenience you can also replace `results.to_df("variable")`
        with the equivalent `results.variable` or `results["variable"]`.
        """
        variable = self.variables[variable]
        df = pd.DataFrame(variable.extract_values(), index=[0]).stack(
            future_stack=True
        )
        df.index = df.index.get_level_values(-1)
        return df

    def __getattr__(self, variable: str) -> pd.DataFrame | pd.Series:
        return self[variable]

    def __getitem__(self, variable: str) -> pd.DataFrame | pd.Series:
        return self.to_df(variable)
