import pyomo.environ as po
try:
    import variables as var
    import linear_mixed_integer_constraints as milc
    import linear_constraints as lc
    import objectives as predefined_objectives
    import objective_expressions as objfuncexprs
    from oemof.core.network.entities import Bus, Component
    from oemof.core.network.entities import components as cp
except:
    from . import variables as var
    from . import linear_mixed_integer_constraints as milc
    from . import linear_constraints as lc
    from . import objectives as predefined_objectives
    from . import objective_expressions as objfuncexprs
    from ..core.network.entities import Bus, Component
    from ..core.network.entities import components as cp


class OptimizationModel(po.ConcreteModel):
    """Create Pyomo model of the energy system.

    Parameters
    ----------
    entities : list with all entity objects
    timesteps : list with all timesteps as integer values
    options : nested dictionary with options to set. possible options are:
      invest, slack

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

        # get options
        self.invest = options.get('invest', False)
        self.milp = options.get('milp', False)
        self.slack = options.get('slack', {'excess': True,
                                           'shortage': False})

        # calculate all edges ([('coal', 'pp_coal'),...])
        components = [e for e in self.entities if isinstance(e, Component)]
        self.all_edges = self.edges(components)

        var.add_continuous(model=self, edges=self.all_edges)
        # list with all necessary classes
        component_classes = (cp.Transformer.__subclasses__() +
                             cp.Sink.__subclasses__() +
                             cp.Source.__subclasses__() +
                             cp.Transport.__subclasses__())
        self.objfuncexpr = 0
        self.I = {c.uid: c.inputs[0].uid for c in components
                  if not isinstance(c, cp.Source)}
        self.O = {c.uid: [o.uid for o in c.outputs[:]] for c in components
                  if not isinstance(c, cp.Sink)}

        self.objs = {}
        self.uids = {}
        # set attributes lists per class with objects and uids for opt model
        for cls in component_classes:
            objs = [e for e in self.entities if isinstance(e, cls)]
            uids = [e.uid for e in objs]
            self.objs[cls.lower_name] = objs
            self.uids[cls.lower_name] = uids
            # "call" methods to add the constraints opt. problem
            if objs:
                getattr(self, cls.lower_name + '_assembler')(objs=objs,
                                                             uids=uids)

        self.bus_assembler()


        if True:
            print('Creating predefined objective ...')
            self.objective_assembler()
        if False:
            self.objective = po.Objective(expr=self.objfuncexpr)

        print('Model created!')

    def bus_assembler(self):
        """Meethod creates bus balance for all buses using pyomo.Constraint

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
        if self.slack["excess"] is True:
            self.excess_slack = po.Var(self.bus_uids, self.timesteps,
                                       within=po.NonNegativeReals)
        if self.slack["shortage"] is True:
            self.shortage_slack = po.Var(self.bus_uids, self.timesteps,
                                         within=po.NonNegativeReals)

        # select only "energy"-bus objects for bus balance constraint
        energy_bus_objs = [obj for obj in self.bus_objs
                           if any([obj.type == "el", obj.type == "th"])]
        energy_bus_uids = [obj.uid for obj in energy_bus_objs]

        print('Creating bus balance constraints ...')
        # bus balance constraint for energy bus objects
        lc.add_bus_balance(self, objs=energy_bus_objs, uids=energy_bus_uids)

        # select only buses that are resources (gas, oil, etc.)
        resource_bus_objs = [obj for obj in self.bus_objs
                             if all([obj.type != "el", obj.type != "th"])]
        resource_bus_uids = [e.uid for e in resource_bus_objs]

        # set limits for resource buses
        lc.add_bus_output_limit(model=self, objs=resource_bus_objs,
                                uids=resource_bus_uids)

        if self.slack['shortage']:
            self.objfuncexpr += objfuncexprs.add_shortage_slack_costs(self)
        if self.slack['excess']:
             self.objfuncexpr += objfuncexprs.add_excess_slack_costs(self)

    def simple_transformer_assembler(self, objs, uids):
        """Method containing the constraints for simple transformer components.

        Parameters
        ----------
        self : OptimizationModel() instance
        objs : oemof objects for which the constraints etc. are created
        uids : unique ids of `objs`

        Returns
        -------
        self : OptimizationModel() instance
        """
        # TODO: This should be dependent on objs classes not fixed if assembler
        # method is used by another assemlber method...
        constr = cp.transformers.Simple.constr
        objfunc = cp.transformers.Simple.objfunc

        # input output relation for simple transformer
        if constr['io_relation']:
            print('Creating simple input-output linear constraints for',
                  objs[0].lower_name, '...')
            lc.add_simple_io_relation(model=self, objs=objs, uids=uids)

        # 'pmax' constraint/bounds for output of component
        if constr['out_max']:
            var.set_bounds(model=self, objs=objs, uids=uids, side='output')
        #'pmax' constraint/bounds for input of component
        if constr['in_max']:
            var.set_bounds(model=self, objs=objs, uids=uids, side='input')
        # gradient calculation dGrad for objective function
        if constr['ramping']:
            lc.add_output_gradient_calc(model=self, objs=objs, uids=uids,
                                        grad_direc="both")
        # set bounds for milp-models
        if self.invest is False and self.milp is True:
            # binary status variables
            var.add_binary(model=self, objs=objs, uids=uids)
            # pmax/pmin constraints
            if constr['out_min']:
                milc.set_bounds(model=self, objs=objs, uids=uids,
                                side='output')
            if constr['in_min']:
                print('Creating minimum input milp constraints for',
                      objs[0].lower_name, '...')
                milc.set_bounds(model=self, objs=objs, uids=uids,
                                side='input')
            if constr['ramping']:
                print('Creating ramping milp constraints for',
                      objs[0].lower_name, '...')
                milc.add_output_gradient_constraints(model=self, objs=objs,
                                                     uids=uids,
                                                     grad_direc='both')
            # pmin constraints
            if constr['startup']:
                milc.add_startup_constraints(model=self, objs=objs, uids=uids)
                # add start costs
                self.objfuncexpr += objfuncexprs.add_startup_costs(self,
                                                                 objs=objs,
                                                                 uids=uids)
        if objfunc['opex_var']:
            self.objfuncexpr += objfuncexprs.add_opex_var(self, objs=objs,
                                                          uids=uids)
        if objfunc['opex_fix']:
            self.objfuncexpr += objfuncexprs.add_opex_fix(self, objs=objs,
                                                          uids=uids,
                                                          ref='output')
        if objfunc['input_costs']:
            self.objfuncexpr += objfuncexprs.add_input_costs(self, objs=objs,
                                                             uids=uids)

        if self.invest is True and self.milp is True:
           raise ValueError("Investment models can not be calculated as \
                            mixed integer problems. \n  \
                            Please set options 'milp' = False")

    def simple_chp_assembler(self, objs, uids):
        """Method grouping the constraints for simple chp components.

        Parameters
        ----------
        self : OptimizationModel() instance
        objs : oemof objects for which the constraints etc. are created
        uids : unique ids of `objs`

        Returns
        -------
        self : OptimizationModel() instance
        """

        # use simple_transformer assebmler for in-out relation and
        # upper / lower bounds
        self.simple_transformer_assembler(objs=objs, uids=uids)

        # use linear constraint to model PQ relation (P/eta_el = Q/eta_th)
        lc.add_simple_chp_relation(model=self, objs=objs, uids=uids)

    def extrac_chp_const_assembler(self, objs, uids):
        """Method grouping the constraints for simple chp components.

        Parameters
        ----------
        self : OptimizationModel() instance
        objs : oemof objects for which the constraints etc. are created
        uids : unique ids of `objs`

        Returns
        -------
        self : OptimizationModel() instance
        """
        if self.invest is True:
           raise ValueError('Investment models can not be calculated' +
                            'with extraction chps.')
        else:
            # use simple_transformer assebmler for in-out relation and
            # upper / lower bounds
            var.set_bounds(model=self, objs=objs, uids=uids, side='input')
            var.set_bounds(model=self, objs=objs, uids=uids, side='output')
            # gradient calculation dGrad for objective function
            lc.add_gradient_calc(model=self, objs=objs, uids=uids)

            out_max = {}
            beta = {}
            sigma = {}
            eta = {}
            for e in objs:
                out_max[e.uid] = e.out_max
                beta[e.uid] = e.beta
                sigma[e.uid] = e.sigma
                eta[e.uid] = e.eta

            def equiv_out_rule(model, e, t):
                lhs = model.w[model.I[e], e, t]
                rhs = (model.w[e, model.O[e][0], t] +
                      beta[e] * model.w[e, model.O[e][1], t]) / eta[e][0]
                return(lhs == rhs)
            self.extrac_chp_const_equ_out = po.Constraint(uids,self.timesteps,
                                                          rule=equiv_out_rule)

            def power_heat_rule(model, e, t):
                lhs = model.w[e, model.O[e][1], t]
                rhs = model.w[e, model.O[e][0], t] / sigma[e]
                return(lhs <= rhs)
            self.extrac_chp_const_pth = po.Constraint(uids, self.timesteps,
                                                      rule=power_heat_rule)
        # set bounds for milp-models
        if self.milp is True:
            # binary status variables
            var.add_binary(model=self, objs=objs, uids=uids)
            # pmax/pmin constraints
            milc.set_bounds(model=self, objs=objs, uids=uids, side="input")
            # pmin constraints
            milc.add_startup_constraints(model=self, objs=objs, uids=uids)

    def fixed_source_assembler(self, objs, uids):
        """Method containing the constraints for
        fixed sources.

        Parameters
        ----------
        self : OptimizationModel() instance
        objs : oemof objects for which the constraints etc. are created
        uids : unique ids of `objs`

        Returns
        -------
        self : OptimizationModel() instance
        """
        lc.add_fixed_source(model=self, objs=objs, uids=uids)


    def dispatch_source_assembler(self, objs, uids):
        """
        """
        if self.invest is False:
            lc.add_dispatch_source(model=self, objs=objs, uids=uids)

    def simple_sink_assembler(self, objs, uids):
        """Method containing the constraints for simple sinks

        Simple sinks are modeled with a fixed output value set for the
        variable of the output.

        Parameters
        ----------
        self : OptimizationModel() instance
        objs : oemof objects for which the constraints etc. are created
        uids : unique ids of `objs`

        Returns
        -------
        self : OptimizationModel() instance
        """
        var.set_fixed_sink_value(model=self, objs=objs, uids=uids)

    def simple_storage_assembler(self, objs, uids):
        """Simple storage assembler containing the constraints for simple
        storage components.

         Parameters
        ----------
        self : OptimizationModel() instance
        objs : oemof objects for which the constraints etc. are created
        uids : unique ids of `objs`

        Returns
        -------
        self : OptimizationModel() instance
        """

        # optimization model with no investment
        if(self.invest is False):
            var.set_bounds(model=self, objs=objs, uids=uids, side='output')
            var.set_bounds(model=self, objs=objs, uids=uids, side='input')
            var.set_storage_cap_bounds(model=self, objs=objs, uids=uids)
            lc.add_storage_balance(model=self, objs=objs, uids=uids)

        # investment
        else:
            lc.add_storage_balance(model=self, objs=objs, uids=uids)

            # constraint that limits discharge power by using the c-rate
            c_rate_out = {obj.uid: obj.c_rate_out for obj in objs}
            out_max = {obj.uid: obj.out_max for obj in objs}
            cap_max = {obj.uid: obj.cap_max for obj in objs}
            print(out_max)
            print(cap_max)

            def storage_discharge_limit_rule(self, e, t):
                expr = 0
                expr += self.w[e, self.O[e][0], t]
                expr += -(cap_max[e] + self.add_cap[e]) \
                    * c_rate_out[e]
                return(expr <= 0)
            setattr(self, objs[0].lower_name+"_discharge_limit_invest",
                    po.Constraint(uids, self.timesteps,
                                  rule=storage_discharge_limit_rule))

            # constraint that limits charging power by using the c-rate
            c_rate_in = {obj.uid: obj.c_rate_in for obj in objs}

            def storage_charge_limit_rule(self, e, t):
                expr = 0
                expr += self.w[e, self.I[e], t]
                expr += -(cap_max[e] + self.add_cap[e]) \
                    * c_rate_in[e]
                return(expr <= 0)
            setattr(self,objs[0].lower_name+"_charge_limit_invest",
                    po.Constraint(uids, self.timesteps,
                                  rule=storage_charge_limit_rule))

    def simple_transport_assembler(self, objs, uids):
        """Simple transport assembler grouping the constraints
        for simple transport components

        The method uses the simple_transformer_assembler() method.

        Parameters
        ----------
        self : OptimizationModel() instance
        objs : oemof objects for which the constraints etc. are created
        uids : unique ids of `objs`

        Returns
        -------
        self : OptimizationModel() instance
        """

        # input output relation for simple transport
        lc.add_simple_io_relation(model=self, objs=objs, uids=uids)
        # bounds
        var.set_bounds(model=self, objs=objs, uids=uids, side='output')

    def objective_assembler(self, objective_name="minimize_costs"):
        """ calls functions to add predefined objective functions

        """
        if objective_name == "minimize_costs":
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
        if(debug is True):
            self.write('problem.lp',
                       io_options={'symbolic_solver_labels': True})
            # print instance
            # instance.pprint()

        # solve instance
        opt = SolverFactory(solver, solver_io=solver_io)
        # store results
        results = opt.solve(self, **kwargs)

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