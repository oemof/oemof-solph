"""

@contact Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""
import pyomo.environ as po
import logging
try:
    import variables as var
    import linear_mixed_integer_constraints as milc
    import linear_constraints as lc
    import predefined_objectives as predefined_objectives
    import objective_expressions as objfuncexprs
    from oemof.core.network.entities import Bus, Component
    from oemof.core.network.entities import components as cp
except:
    from . import variables as var
    from . import linear_mixed_integer_constraints as milc
    from . import linear_constraints as lc
    from . import predefined_objectives as predefined_objectives
    from . import objective_expressions as objfuncexprs
    from ..core.network.entities import Bus, Component
    from ..core.network.entities import components as cp


class OptimizationModel(po.ConcreteModel):
    """Create Pyomo model of the energy system.

    Parameter
    ----------
    entities : list with all entity objects
    timesteps : list with all timesteps as integer values
    options : nested dictionary with options to set.


    Returns
    -------
    m : pyomo.ConcreteModel

    """

    # TODO Cord: Take "next(iter(self.dict.values()))" where the first value of
    #            dict has to be selected
    def __init__(self, entities, timesteps, options=None):
        super().__init__()

        self.entities = entities
        self.timesteps = timesteps
        self.objective_name = options.get('objective_name', 'individual')

        self.T = po.Set(initialize=timesteps, ordered=True)
        # calculate all edges ([('coal', 'pp_coal'),...])
        self.components = [e for e in self.entities
                           if isinstance(e, Component)]
        self.all_edges = self.edges(self.components)
        var.add_continuous(model=self, edges=self.all_edges)

        # list with all necessary classes
        component_classes = (cp.Transformer.__subclasses__() +
                             cp.Sink.__subclasses__() +
                             cp.Source.__subclasses__() +
                             cp.Transport.__subclasses__())


        self.I = {c.uid: c.inputs[0].uid for c in self.components
                  if not isinstance(c, cp.Source)}
        self.O = {c.uid: [o.uid for o in c.outputs[:]] for c in self.components
                  if not isinstance(c, cp.Sink)}

        self.objfuncexpr = 0
        # set attributes lists per class with objects and uids for opt model
        for cls in component_classes:
            objs = [e for e in self.entities if isinstance(e, cls)]
            # "call" methods to add the constraints opt. problem
            if objs:
                uids = [e.uid for e in objs]
                # add pyomo block per cls to OptimizationModel instance
                block = po.Block()
                block.uids = po.Set(initialize=uids)
                block.indexset = po.Set(initialize=block.uids*self.T)
                block.objs = objs
                block.model_param = cls.model_param
                self.add_component(cls.lower_name, block)
                getattr(self, cls.lower_name + '_assembler')(block=block)

        self.uids = {}
        self.bus_assembler()

        # create objective function
        if self.objective_name == 'individual':
            self.objective = po.Objective(expr=self.objfuncexpr)
        else:
            self.objective_assembler(objective_name=self.objective_name)


    def bus_assembler(self):
        """ Method creates bus balance for all buses.

        The bus model creates all full balance around the energy buses using
        the :func:`lc.generic_bus_constraint` function.
        Additionally it sets constraints to model limits over the timehorizon
        for resource buses using :func:`lc.generic_limit`

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """
        # get all bus objects
        self.bus_objs = [e for e in self.entities if isinstance(e, Bus)]

        # get uids from bus objects
        self.bus_uids = [e.uid for e in self.bus_objs]


        # slack variables that assures a feasible problem
        # get uids for busses that allow excess
        self.uids.update({'excess': [b.uid for b in self.bus_objs
                                     if b.excess == True]})
        # get uids for busses that allow shortage
        self.uids.update({'shortage': [b.uid for b in self.bus_objs
                                       if b.shortage == True]})
        # create variables for 'slack' of shortage and excess
        if self.uids['excess']:
            self.excess_slack = po.Var(self.uids['excess'],
                                       self.timesteps,
                                       within=po.NonNegativeReals)
        if self.uids['shortage']:
            self.shortage_slack = po.Var(self.uids['shortage'],
                                         self.timesteps,
                                         within=po.NonNegativeReals)

        # select only "energy"-bus objects for bus balance constraint
        energy_bus_objs = [obj for obj in self.bus_objs
                           if any([obj.type == "el", obj.type == "th"])]
        energy_bus_uids = [obj.uid for obj in energy_bus_objs]

        print('Creating bus balance constraints ...')
        # bus balance constraint for energy bus objects
        lc.add_bus_balance(self, objs=energy_bus_objs, uids=energy_bus_uids,
                           balance_type="==")

        # select only buses that are resources (gas, oil, etc.)
        resource_bus_objs = [obj for obj in self.bus_objs
                             if all([obj.type != "el", obj.type != "th"])]
        resource_bus_uids = [e.uid for e in resource_bus_objs]

        # set limits for resource buses
        lc.add_bus_output_limit(model=self, objs=resource_bus_objs,
                                uids=resource_bus_uids)

        if self.objective_name == 'individual':
            if self.uids['shortage']:
                self.objfuncexpr += objfuncexprs.add_shortage_slack_costs(self)
            if self.uids['excess']:
                 self.objfuncexpr += objfuncexprs.add_excess_slack_costs(self)

    def simple_transformer_assembler(self, block):
        """ Method containing the constraints functions for simple
        transformer components.

        Constraints are selected by the `model_param` variable of
        transformer.Simple().


        Parameter
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()

        Returns
        -------
        self : OptimizationModel() instance
        """
        # TODO: This should be dependent on objs classes not fixed if assembler
        # method is used by another assemlber method...

        param = block.model_param

        if param.get('investment', False) == True and param['milp_constr']:
            raise ValueError('Component can not be modeled with milp-constr ' +
                             'in investment mode! Please change `model_param`')

        # additional variable for investment models
        if param.get('investment', False) == True:
            block.add_out = po.Var(block.uids, within=po.NonNegativeReals)

        # input output relation for simple transformer
        if 'io_relation' in param['linear_constr']:
            print('Creating simple input-output linear constraints for: ',
                  block.name, '...')
            lc.add_simple_io_relation(self, block)
        # 'pmax' constraint/bounds for output of component
        if 'out_max' in param['linear_constr']:
            print('Setting output bounds for components: ',
                  block.name, '...')
            var.set_bounds(self, block, side='output')
        #'pmax' constraint/bounds for input of component
        if 'in_max' in param['linear_constr']:
            var.set_bounds(self, block, side='input')
        # gradient calculation dGrad
        if 'ramping' in param['linear_constr']:
            lc.add_output_gradient_calc(self, block, grad_direc="both")
        if 'outages' in param['linear_constr']:
            var.set_outages(self, block, outagetype='period', side='output')
        if param['investment'] == False:
            # binary status variables
            if param['milp_constr']:
                var.add_binary(self, block)
            # (pmax)/pmin constraints for output of component
            if 'out_min' in param['milp_constr']:
                milc.set_bounds(self, block, side='output')
            # (pmax)/pmin constraints for input of component
            if 'in_min' in param['milp_constr']:
                print('Creating minimum input milp constraints for',
                      block.name, '...')
                milc.set_bounds(self, block, side='input')
            # additional ramping constraint for milp-models
            if 'ramping' in param['milp_constr']:
                print('Creating ramping milp constraints for',
                      block.name, '...')
                milc.add_output_gradient_constraints(self, block,
                                                     grad_direc='both')
            # startup constraints
            if 'startup' in param['milp_constr']:
                milc.add_startup_constraints(self, block)
                # startup constraints
            if 'shutdown' in param['milp_constr']:
                milc.add_shutdown_constraints(self, block)

        # objective expressions
        if self.objective_name == 'individual':
            # add variable costs (opex_var)
            if 'opex_var' in param['objective']:
                self.objfuncexpr += objfuncexprs.add_opex_var(self, block)
            # add fix costs (opex_fix, refers to the output side e.g. el Power)
            if 'opex_fix' in param['objective']:
                self.objfuncexpr += objfuncexprs.add_opex_fix(self, block,
                                                              ref='output')
            # add fuel costs (input_costs, if not included in opex)
            if 'fuel_ex' in param['objective']:
                self.objfuncexpr += objfuncexprs.add_input_costs(self, block)
            # add revenues generated by output (busprice from output)
            if 'rsell' in param['objective']:
                self.objfuncexpr += objfuncexprs.add_revenues(self, block,
                                                              ref='output')
            if 'ramping' in param['linear_constr']:
                self.objfuncexpr += objfuncexprs.add_ramping_costs(self, block)
            # add startup costs
            if 'startup' in param['milp_constr']:
                self.objfuncexpr += objfuncexprs.add_startup_costs(self, block)
            # add shutbown costs
            if 'shutdown' in param['milp_constr']:
                self.objfuncexpr += objfuncexprs.add_shutdown_costs(self, block)
            # investment costs (capex) if in component can be invested
            if param['investment'] == True:
                self.objfuncexpr += objfuncexprs.add_capex(self, block,
                                                           ref='output')

    def simple_chp_assembler(self, block):
        """ Method grouping the constraints for simple chp components.

        The methdo uses the simple_transformer_assembler() method. The
        model_param comes from the transfomer.CHP()

        Parameters
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()

        Returns
        -------
        self : OptimizationModel() instance
        """
        param = block.model_param

        # additional variable for investment models
        if param.get('investement', False) == True:
            block.add_out = po.Var(block.uids, within=po.NonNegativeReals)

        # simple_transformer assebmler for in-out relation, pmin,.. etc.
        self.simple_transformer_assembler(block)

        # add constraint for PQ relation (P/eta_el = Q/eta_th)
        if 'simple_chp_relation' in param['linear_constr']:
            lc.add_simple_chp_relation(self, block)

    def simple_extraction_chp_assembler(self, block):
        """Method grouping the constraints for simple chp components.

        Parameters
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()

        Returns
        -------
        self : OptimizationModel() instance
        """
        param = block.model_param

        if param.get('investment', False) == True:
           raise ValueError('Investment models can not be calculated' +
                        'with extraction chps.')

        self.simple_transformer_assembler(block)
        # relations for P/Q-field of extraction turbine
        if 'simple_extraction_relation' in param['linear_constr']:
            lc.add_simple_extraction_chp_relation(self, block)
        else:
            logging.warning('Necessary constraint for extraction chp missing!')

    def fixed_source_assembler(self, block):
        """Method containing the constraints for
        fixed sources.

        Parameters
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()

        Returns
        -------
        self : OptimizationModel() instance
        """
        param = block.model_param

        self.simple_transformer_assembler(block)

        # add constraints
        if 'fixvalues' in param['linear_constr']:
            lc.add_fix_source(self, block)

    def dispatch_source_assembler(self, block):
        """Method containing the constraints for dispatchable sources.

        Parameters
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()

        Returns
        -------
        self : OptimizationModel() instance
        """
        param = block.model_param
        # add constraints
        if param.get('investment', False) == True:
            raise ValueError('Dispatch source investment is not possible')

        self.simple_transformer_assembler(block)

        if 'dispatch' in param['linear_constr']:
             lc.add_dispatch_source(self, block)

        if self.objective_name == 'individual':
            # add dispatch costs (dispatch_ex) to objective
            if 'dispatch_ex' in param['objective']:
                self.objfuncexpr += objfuncexprs.add_curtailment_costs(self,
                                                                      block)

    def simple_sink_assembler(self, block):
        """Method containing the constraints for simple sinks

        Simple sinks are modeled with a fixed output value set for the
        variable of the output.

        Parameters
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()

        Returns
        -------
        self : OptimizationModel() instance
        """
        var.set_fixed_sink_value(self, block)

    def simple_storage_assembler(self, block):
        """Simple storage assembler containing the constraints for simple
        storage components.

         Parameters
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()

        Returns
        -------
        self : OptimizationModel() instance
        """
        # add capacity variable
        block.cap = po.Var(block.uids, self.timesteps,
                           within=po.NonNegativeReals)

        param = block.model_param

        # add addictional capacity variable
        if param.get('investment', False) == True:
            block.add_cap = po.Var(block.uids, within=po.NonNegativeReals)

        lc.add_storage_balance(self, block)
        var.set_storage_cap_bounds(self, block)

        # optimization model with no investment
        if param.get('investment', False) == False:
            var.set_bounds(self, block, side='output')
            var.set_bounds(self, block, side='input')
        # investment
        else:
            # constraint that limits discharge power by using the c-rate
            c_rate_out = {obj.uid: obj.c_rate_out for obj in block.objs}
            cap_max = {obj.uid: obj.cap_max for obj in block.objs}

            def storage_discharge_limit_rule(block, e, t):
                expr = 0
                expr += self.w[e, self.O[e][0], t]
                expr += -(cap_max[e] + block.add_cap[e]) \
                    * c_rate_out[e]
                return(expr <= 0)
            block.discharge_limit_invest = po.Constraint(block.uids,
                                                         self.timesteps,
                                             rule=storage_discharge_limit_rule)

            # constraint that limits charging power by using the c-rate
            c_rate_in = {obj.uid: obj.c_rate_in for obj in block.objs}

            def storage_charge_limit_rule(block, e, t):
                expr = 0
                expr += self.w[e, self.I[e], t]
                expr += -(cap_max[e] + block.add_cap[e]) \
                    * c_rate_in[e]
                return(expr <= 0)
            block.charge_limit_invest = po.Constraint(block.uids, self.timesteps,
                                           rule=storage_charge_limit_rule)

    def simple_transport_assembler(self, block):
        """Simple transport assembler grouping the constraints
        for simple transport components

        The method uses the simple_transformer_assembler() method.

        Parameters
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()

        Returns
        -------
        self : OptimizationModel() instance
        """

        # input output relation for simple transport
        lc.add_simple_io_relation(self, block)
        # bounds
        var.set_bounds(self, block, side='output')

    def objective_assembler(self, objective_name="minimize_costs"):
        """ calls functions to add predefined objective functions

        """
        if objective_name == "minimize_costs":
            print('Creating predefined objective with name:', objective_name)
            predefined_objectives.minimize_cost(self)

    def solve(self, solver='glpk', solver_io='lp', debug=False,
              duals=False, **kwargs):
        """ Method that takes care of the communication with the solver
        to solve the optimization model

        Parameters
        ----------

        self : pyomo.ConcreteModel
        solver str: solver to be used e.g. 'glpk','gurobi','cplex'
        solver_io str: str that defines the solver interaction
        (file or interface) 'lp','nl','python'
        **kwargs: other arguments for the pyomo.opt.SolverFactory.solve()
        method

        Returns
        -------
        self : solved pyomo.ConcreteModel() instance
        """

        from pyomo.opt import SolverFactory
        # Create a 'dual' suffix component on the instance
        # so the solver plugin will know which suffixes to collect
        if duals is True:
            # dual variables (= shadow prices)
            self.dual = po.Suffix(direction=po.Suffix.IMPORT)
            # reduced costs
            self.rc = po.Suffix(direction=po.Suffix.IMPORT)
        # write lp-file
        if debug == True:
            self.write('problem.lp',
                       io_options={'symbolic_solver_labels': True})
            # print instance
            # instance.pprint()

        # solve instance
        opt = SolverFactory(solver, solver_io=solver_io)
        # store results
        results = opt.solve(self, **kwargs)
        if debug == True:
            if (results.solver.status == "ok") and \
               (results.solver.termination_condition == "optimal"):
                # Do something when the solution in optimal and feasible
                self.solutions.load_from(results)

            elif (results.solver.termination_condition == "infeasible"):
                print("Model is infeasible",
                      "Solver Status: ", results.solver.status)
            else:
                # Something else is wrong
                print("Solver Status: ", results.solver.status, "\n"
                      "Termination condition: ",
                      results.solver.termination_condition)

    def edges(self, components):
        """Method that creates a list with all edges for the objects in
        components.

        Parameters
        ----------
        self :
        components : list of component objects

        Returns
        -------
        edges : list with tupels that represent the edges
        """

        edges = []
        # create a list of tuples
        # e.g. [('coal', 'pp_coal'), ('pp_coal', 'b_el'),...]
        for c in components:
            for i in c.inputs:
                ei = (i.uid, c.uid)
                edges.append(ei)
            for o in c.outputs:
                ej = (c.uid, o.uid)
                edges.append(ej)
        return(edges)