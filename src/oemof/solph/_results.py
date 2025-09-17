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
from pyomo.environ import ConcreteModel
from pyomo.opt.results.container import ListContainer

import oemof.solph


class Results:
    # TODO:
    #   Defer attribute references not present as variables to
    #   attributes of `model.solver_results` in order to make `Results`
    #   instances returnable by `model.solve` and still be backwards
    #   compatible.
    def __init__(self, model: ConcreteModel):
        msg = (
            "The class 'Results' is experimental. Functionality and API can"
            " be changed without warning during any update."
        )
        warnings.warn(msg, debugging.ExperimentalFeatureWarning)

        self._solver_results = model.solver_results
        self._variables = {}
        self._model = model

        for vardata in model.component_data_objects(Var):
            for variable in [vardata.parent_component()]:
                key = str(variable).split(".")[-1]
                occurence = str(variable)[: -(len(key) + 1)]
                if (
                    key not in self._variables
                    and key not in self._solver_results
                ):
                    self._variables[key] = {occurence: variable}
                elif (
                    key in self._variables
                    and occurence not in self._variables[key]
                ):
                    self._variables[key][occurence] = variable
                elif self._variables[key][occurence] == variable:
                    # For debugging purposes.
                    # We should avoid useless iterations.
                    pass
                else:
                    raise ValueError(
                        f"Variable name defined multiple times: {key}"
                        + f"(last time in '{variable}')"
                    )

        # adss additional keys for the calculation of opex and capex
        # if the keyword eval_economy is True
        # checks if investment optimization is happing to add capex as key
        # TODO: add keyword for multiperiod

        self._economy = {"variable_costs": None}
        if "invest" in self._variables.keys():
            self._economy["investment_costs"] = None

    def keys(self):
        return (
            self._solver_results.keys()
            | self._variables.keys()
            | self._economy.keys()
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

        if variable == "variable_costs":
            df = self._calc_variable_costs()
        elif variable == "investment_costs":
            df = self._calc_capex()

        else:
            df = []
            for occurence in self._variables[variable]:
                dataset = self._variables[variable][occurence]
                df.append(
                    pd.DataFrame(dataset.extract_values(), index=[0]).stack(
                        future_stack=True
                    )
                )
            df = pd.concat(df, axis=1)

            # overwrite known indexes
            index_type = tuple(dataset.index_set().subsets())[-1].name
            match index_type:
                case "TIMEPOINTS":
                    df.index = self.timeindex
                case "TIMESTEPS":
                    df.index = self.timeindex[:-1]
                case _:
                    df.index = df.index.get_level_values(-1)
        return df

    def _calc_capex(self):

        # extract the the optimized investment sizes
        invest_values = self.to_df("invest")

        # Initialize an empty dictionary to collect results
        capex_data = {}

        # calculate yearly investment costs associated with investment FLOWS
        # and store data in capex_data dictionary

        # TODO: is it really necessary to loop over all flows again or is it
        # possible to use the flows of 'invest_values'?
        for i, o in self._model.FLOWS:

            # access the costs of each investment flow
            if hasattr(self._model.flows[i, o], "investment"):

                # map investment and costs and multiply
                for col in invest_values.columns:
                    if isinstance(col, oemof.solph.components.GenericStorage):
                        pass
                    else:
                        if col[0] == i and col[1] == o:
                            invest_size = invest_values[col][0]

                            investment_costs = (
                                self._model.flows[i, o].investment.ep_costs[0]
                                * invest_size
                                + self._model.flows[i, o].investment.offset[0]
                            )

                            # Save values to dictionary
                            capex_data[col] = investment_costs

            else:
                pass

        # calculate yearly investment costs associated with GenericStorages
        # and store data in capex_data dictionary
        for node in self._model.nodes:
            if isinstance(
                node,
                oemof.solph.components._generic_storage.GenericStorage,
            ):

                # map investment and costs and mulitply
                for col in invest_values.columns:
                    if isinstance(col, oemof.solph.components.GenericStorage):
                        if col == node:
                            invest_size = invest_values[col][0]

                            investment_costs = (
                                node.investment.ep_costs[0] * invest_size
                                + node.investment.offset[0]
                            )

                            # Save values to dictionary
                            capex_data[col] = investment_costs
                    else:
                        pass

        df_capex = pd.DataFrame([capex_data])

        return df_capex

    def _calc_variable_costs(self):
        df_opex = pd.DataFrame()

        # extract the the optimized flow values
        flow_values = self.to_df("flow")

        for i, o in self._model.FLOWS:
            # access the variable costs of each flow
            variable_costs = self._model.flows[i, o].variable_costs

            # map flows and variable costs and mulitply
            for col in flow_values.columns:
                if col[0] == i and col[1] == o:
                    opex = flow_values[col] * variable_costs
                    df_opex[col] = opex

        return df_opex

    @property
    def objective(self):
        return self._model.objective()

    @property
    def timeindex(self):
        return self._model.es.timeindex

    def __getattr__(self, key: str) -> pd.DataFrame | ListContainer:
        return self[key]

    def __getitem__(self, key: str) -> pd.DataFrame | ListContainer:
        # backward-compatibility with returned results object from Pyomo
        if key in self._solver_results:
            return self._solver_results[key]
        else:
            return self.to_df(key)
