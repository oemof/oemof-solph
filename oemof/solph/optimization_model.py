import pyomo.environ as po
try:
    import linear_variables as lv
    import linear_constraints as lc
    import objectives as objfunc
    from oemof.core.network.entities import Bus, Component
    from oemof.core.network.entities import components as cp
except:
    from . import linear_variables as lv
    from . import linear_constraints as lc
    from . import objectives as objfunc
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
        """

        """
        super().__init__()

        self.entities = entities
        self.timesteps = timesteps

        # get options
        self.invest = options.get("invest", False)
        self.slack = options.get("slack", {"excess": True,
                                           "shortage": False})

        # calculate all edges ([('coal', 'pp_coal'),...])
        components = [e for e in self.entities if isinstance(e, Component)]
        self.all_edges = self.edges(components)

        lv.add(model=self, edges=self.all_edges)

        # list with all necessary classes
        component_classes = (cp.Transformer.__subclasses__() +
                             cp.Sink.__subclasses__() +
                             cp.Source.__subclasses__() +
                             cp.Transport.__subclasses__())
        components
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
                getattr(self, cls.lower_name + "_assembler")(objs=objs,
                                                             uids=uids)

        self.bus_assembler()
        self.objective_assembler()

    def bus_assembler(self):
        """Meethod creates bus balance for all buses using pyomo.Constraint

        The bus model creates all full balance around the energy buses using
        the `linear_constraints.generic_bus_constraint()` function.
        Additionally it sets constraints to model limits over the timehorizon
        for resource buses using `linear_constraints.generic_limit()

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

        # bus balance constraint for energy bus objects
        lc.add_bus_balance(self, objs=energy_bus_objs, uids=energy_bus_uids)

        # select only buses that are resources (gas, oil, etc.)
        resource_bus_objs = [obj for obj in self.bus_objs
                             if all([obj.type != "el", obj.type != "th"])]
        resource_bus_uids = [e.uid for e in resource_bus_objs]

        # set limits for resource buses
        lc.add_bus_output_limit(model=self, objs=resource_bus_objs,
                                uids=resource_bus_uids)

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
        lc.add_simple_io_relation(model=self, objs=objs, uids=uids)

        lv.set_output_bounds(model=self, objs=objs, uids=uids)


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
        lv.set_fixed_sink_value(model=self, objs=objs, uids=uids)

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
            lv.set_output_bounds(model=self, objs=objs, uids=uids)
            lv.set_storage_cap_bounds(model=self, objs=objs, uids=uids)
            lc.add_storage_balance(model=self, objs=objs, uids=uids)

        # investment
        else:
            lc.add_storage_balance(model=self, objs=objs, uids=uids)

            # constraint that limits discharge power by using the c-rate
            c_rate_out = {obj.uid: obj.c_rate_out for obj in objs}
            out_max = {obj.uid: obj.out_max for obj in objs}

            def storage_discharge_limit_rule(self, e, t):
                expr = 0
                expr += self.w[e, self.O[e][0], t]
                expr += -(out_max[e][self.O[e][0]] + self.add_cap[e]) \
                    * c_rate_out[e]
                return(expr <= 0)
            setattr(self, objs[0].lower_name+"_discharge_limit_invest",
                    po.Constraint(uids, self.timesteps,
                                  rule=storage_discharge_limit_rule))

            # constraint that limits charging power by using the c-rate
            c_rate_in = {obj.uid: obj.c_rate_in for obj in objs}
            in_max = {obj.uid: obj.in_max for obj in objs}

            def storage_charge_limit_rule(self, e, t):
                expr = 0
                expr += self.w[e, self.I[e], t]
                expr += -(in_max[e][self.I[e]] + self.add_cap[e]) \
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

        self.simple_transformer_assembler(objs=objs, uids=uids)

    def objective_assembler(self, objective_type="min_costs"):
        """Objective assembler creates builds objective function of the
        optimization model.

        Parameters
        ----------
        self : OptimizationModel() instance

        Returns
        -------
        self : OptimizationModel() instance
        """
        if objective_type == "min_costs":
            objfunc.minimize_cost(self)

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