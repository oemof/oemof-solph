import pyomo.environ as po
import components as cp


class OptimizationModel(po.ConcreteModel):
    """Create Pyomo model of the energy system.

    Parameters
    ----------
    entities : list with all entity objects
    timesteps : list with all timesteps as integer values
    invest : boolean

    Returns
    -------
    m : pyomo.ConcreteModel

    """

    def __init__(self, entities, timesteps, options=None):

        super().__init__()

        self.entities = entities
        self.timesteps = timesteps
        self.invest = options.get("invest", False)
        self.slack = options.get("slack", True)

        # calculate all edges ([('coal', 'pp_coal'),...])
        self.all_edges = self.edges([e for e in self.entities
                                     if isinstance(e, cp.Component)])
        # list with all necessary classes
        classes = ([cp.Bus] +
                   cp.Transformer.__subclasses__() +
                   cp.Sink.__subclasses__() +
                   cp.Source.__subclasses__() +
                   cp.Transport.__subclasses__())

        # set attributes lists per class with objects and uids for opt model
        for cls in classes:
            objs = [e for e in self.entities if isinstance(e, cls)]
            uids = [e.uid for e in objs]
            setattr(self, cls.__lower_name__ + "_objs", objs)
            setattr(self, cls.__lower_name__ + "_uids", uids)

        # "call" methods to add the constraints and variables to opt. problem
        self.variables()
        self.bus_model()
        self.simple_chp_model(objs=self.simple_chp_objs,
                              uids=self.simple_chp_uids)
        self.simple_extraction_chp_model()
        self.renewable_source_model()
        self.generic_transformer_model(objs=self.simple_transformer_objs,
                                       uids=self.simple_transformer_uids)
        self.simple_storage_model()
        self.commodity_model()
        self.simple_transport_model(objs=self.simple_transport_objs,
                                    uids=self.simple_transport_uids)
        self.simple_sink_model()
        # set objective function
        self.objective()

    def variables(self):
        """ variables creates all variables corresponding to the edges indexed
        by t in timesteps, (e1,e2) in all_edges
        if invest flag is set to true, an additional variable indexed by
        (e1,e2) in all_edges is created.
        """
        # variable for edges
        self.w = po.Var(self.all_edges, self.timesteps,
                        within=po.NonNegativeReals)

        # additional variable for investment models
        if(self.invest is True):
            self.w_add = po.Var(self.all_edges, within=po.NonNegativeReals)

    def bus_model(self):
        """bus model creates bus balance for all buses using pyomo.Constraint

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """

        # slack variables that assures a feasible problem
        if self.slack is True:
            self.shortage_slack = po.Var(self.bus_uids, self.timesteps,
                                         within=po.NonNegativeReals)
            self.excess_slack = po.Var(self.bus_uids, self.timesteps,
                                       within=po.NonNegativeReals)

        I = {b.uid: [i.uid for i in b.inputs] for b in self.bus_objs}
        O = {b.uid: [o.uid for o in b.outputs] for b in self.bus_objs}

        # constraint for bus balance:
        # component inputs/outputs are negative/positive in the bus balance
        def bus_rule(self, e, t):
            expr = 0
            expr += -sum(self.w[e, o, t] for o in O[e])
            expr += sum(self.w[i, e, t] for i in I[e])
            if self.slack is True:
                expr += -self.excess_slack[e, t] + self.shortage_slack[e, t]
            return(expr, 0)
        self.bus = po.Constraint(self.bus_uids, self.timesteps, rule=bus_rule)

    def generic_transformer_model(self, objs, uids):
        """Generic transformer model containing the constraints
        for generic transformer components.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """

        # temp set with input uids for every simple transformer
        I = {obj.uid: obj.inputs[0].uid for obj in objs}
        # set with output uids for every simple transformer
        O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in objs}
        eta = {obj.uid: obj.param['eta'] for obj in objs}

        # constraint for simple transformers: input * efficiency = output
        def in_out_rule(self, e, t):
            expr = self.w[I[e], e, t] * eta[e][0] - self.w[e, O[e][0], t]
            return(expr == 0)
        setattr(self, "generic_in_out_"+objs[0].__lower_name__,
                po.Constraint(uids, self.timesteps, rule=in_out_rule))

        # set variable bounds (out_max = in_max * efficiency):
        # m.in_max = {'pp_coal': 51794.8717948718, ... }
        # m.out_max = {'pp_coal': 20200, ... }
        in_max = {obj.uid: obj.param['in_max'] for obj in objs}
        out_max = {obj.uid: obj.param['out_max'] for obj in objs}

        # set bounds for basic/investment models
        if(self.invest is False):
            # edges for simple transformers ([('coal', 'pp_coal'),...])
            ee = self.edges(objs)
            for (e1, e2) in ee:
                for t in self.timesteps:
                    # transformer output <= self.out_max
                    if e1 in uids:
                        self.w[e1, e2, t].setub(out_max[e1][e2])
                    # transformer input <= self.in_max
                    if e2 in uids:
                        self.w[e1, e2, t].setub(in_max[e2][e1])
        else:
            # constraint for additional capacity
            def invest_rule(self, e, t):
                expr = self.w[I[e], e, t] - in_max[e][I[e]] - \
                    self.w_add[I[e], e]
                return(expr <= 0)
            setattr(self, "generic_invest_" + objs[0].__lower_name__,
                    po.Constraint(uids, self.timesteps,
                                  rule=invest_rule))

    def simple_chp_model(self, objs, uids):
        """Simple chp model containing the constraints for simple chp
        components.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel

        """
        # use generic_transformer model for in-out relation and
        # upper/lower bounds
        self.generic_transformer_model(objs=objs, uids=uids)

        # set with output uids for every simple chp
        # {'pp_chp': ['b_th', 'b_el']}
        O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in objs}
        # efficiencies for simple chps
        eta = {obj.uid: obj.param['eta'] for obj in objs}

        # additional constraint for power to heat ratio of simple chp comp:
        # P/eta_el = Q/eta_th
        def chp_rule(self, e, t):
            expr = self.w[e, O[e][0], t] / eta[e][0]
            expr += -self.w[e, O[e][1], t] / eta[e][1]
            return(expr == 0)
        self.simple_chp_c2 = po.Constraint(uids, self.timesteps,
                                           rule=chp_rule)

    def simple_extraction_chp_model(self):
        """Simple extraction chp model containing the constraints for
        objects of class cp.SimpleExtractionCHP().

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel

        """
        # {'pp_chp': 'gas'}
        I = {obj.uid: obj.inputs[0].uid
             for obj in self.simple_extraction_chp_objs}
        # set with output uids for every simple chp
        # {'pp_chp': ['b_th', 'b_el']}
        O = {obj.uid: [o.uid for o in obj.outputs[:]]
             for obj in self.simple_extraction_chp_objs}
        k = {obj.uid: obj.k for obj in self.simple_extraction_chp_objs}
        c = {obj.uid: obj.c for obj in self.simple_extraction_chp_objs}
        beta = {obj.uid: obj.beta for obj in self.simple_extraction_chp_objs}
        p = {obj.uid: obj.p for obj in self.simple_extraction_chp_objs}
        out_min = {obj.uid: obj.out_min
                   for obj in self.simple_extraction_chp_objs}

        # constraint for transformer energy balance:
        # 1) P <= p[0] - beta[0]*Q
        def c1_rule(self, e, t):
            expr = self.w[e, O[e][0], t]
            rhs = p[e][0] - beta[e][0] * self.w[e, O[e][1], t]
            return(expr <= rhs)
        self.simple_extraction_chp_1 = \
            po.Constraint(self.simple_extraction_chp_uids, self.timesteps,
                          rule=c1_rule)

        # 2) P = c[0] + c[1] * Q
        def c2_rule(self, e, t):
            expr = self.w[e, O[e][1], t]
            rhs = (self.w[e, O[e][0], t] - c[e][0]) / c[e][1]
            return(expr <= rhs)
        self.simple_extraction_chp_2 = \
            po.Constraint(self.simple_extraction_chp_uids, self.timesteps,
                          rule=c2_rule)

        # 3) P >= p[1] - beta[1]*Q
        def c3_rule(self, e, t):
            if out_min[e] > 0:
                expr = self.w[e, O[e][0], t]
                rhs = p[e][1] - beta[e][1] * self.w[e, O[e][1], t]
                return(expr >= rhs)
            else:
                return(po.Constraint.Skip)
        self.simple_extraction_chp_3 = \
            po.Constraint(self.simple_extraction_chp_uids, self.timesteps,
                          rule=c3_rule)

        # H = k[0] + k[1]*P + k[2]*Q
        def in_out_rule(self, e, t):
            expr = 0
            expr += self.w[I[e], e, t]
            expr += - (k[e][0] + k[e][1]*self.w[e, O[e][0], t] +
                       k[e][2]*self.w[e, O[e][1], t])
            return(expr, 0)
        self.simple_extraction_chp_io = \
            po.Constraint(self.simple_extraction_chp_uids, self.timesteps,
                          rule=in_out_rule)

    def renewable_source_model(self):
        """Simple renewable source model containing the constraints for
        renewable source sources.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """
        # outputs: {'pv': 'b_el', 'wind_off': 'b_el', ... }
        O = {obj.uid: obj.outputs[0].uid
             for obj in self.renewable_source_objs}
        # normed value of renewable source (0 <= value <=1)
        self.source_val = {obj.uid: obj.val
                           for obj in self.renewable_source_objs}
        # maximal ouput of renewable source (in general installed capacity)
        self.out_max = {obj.uid: obj.out_max
                        for obj in self.renewable_source_objs}
        # flag if dispatch is true or false for each object
        self.dispatch = {obj.uid: obj.dispatch
                         for obj in self.renewable_source_objs}

        # if one one RenewableSource() instance attribute is dispatch=True
        if(True in self.dispatch.values()):
            # get only the RenewableSource() instance that have dispatch
            self.renewable_sources_dispatch_uids = [k for (k, v) in
                                                    self.dispatch.items()
                                                    if v is True]
            # Set to define dispatch variable
            self.renewable_dispatch_v = \
                po.Var(self.renewable_sources_dispatch_uids, self.timesteps,
                       within=po.NonNegativeReals)

            # constraint to determine how much renewable energy is dispatched
            def dispatch_rule(self, e, t):
                expr = self.renewable_dispatch_v[e, t]
                expr += - self.source_val[e][t] * self.out_max[e] + \
                    self.w[e, O[e], t]
                return(expr, 0)
            self.renewable_source_dispatch_c = \
                po.Constraint(self.renewable_sources_dispatch_uids,
                              self.timesteps, rule=dispatch_rule)
        # set bounds for basic/investment models
        # TODO: include dispatch if invest=True
        if(self.invest is False):
            # edges for renewables ([('wind_on', 'b_el'), ...)
            ee = self.edges(self.renewable_source_objs)
            # fixed value
            for (e1, e2) in ee:
                for t in self.timesteps:
                    self.w[(e1, e2), t].setub(self.source_val[e1][t] *
                                              self.out_max[e1])
                    self.w[(e1, e2), t].setlb(self.source_val[e1][t] *
                                              self.out_max[e1] *
                                              (1-self.dispatch[e1]))

        else:
            if(True in self.dispatch.values()):
                raise ValueError("Dispatchable renewables not implemented for"
                                 "investment models.\n Please reset flag from"
                                 "True to False")

            # constraint to allow additional capacity for renewables
            def invest_rule(self, e, t):
                expr = 0
                expr += self.w[e, O[e], t]
                rhs = (self.out_max[e] + self.w_add[e, O[e]]) * \
                    self.source_val[e][t]
                return(expr <= rhs)
            self.source_c = po.Constraint(self.renewable_source_uids,
                                          self.timesteps, rule=invest_rule)

    def commodity_model(self):
        """Simple commdity model containing the constraints for commodity
        sources.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """

        self.yearly_limit = {obj.uid: obj.yearly_limit
                             for obj in self.commodity_objs}

        # outputs: {'rcoal': ['coal'], 'rgas': ['gas'],...}
        O = {obj.uid: [obj.outputs[0].uid] for obj in self.commodity_objs}

        # set upper bounds: sum(yearly commodity output) <= yearly_limit
        def commodity_limit_rule(self, e):
            expr = 0
            expr += sum(self.w[e, o, t] for t in self.timesteps
                        for o in O[e])
            rhs = self.yearly_limit[e]
            return(expr <= rhs)
        self.commodity_limit_c = po.Constraint(self.commodity_uids,
                                               rule=commodity_limit_rule)

    def simple_sink_model(self):
        """simple sink model containing the constraints for simple sinks
        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """

        self.simple_sink_val = {obj.uid: obj.val
                                for obj in self.simple_sink_objs}
        ee = self.edges(self.simple_sink_objs)
        for (e1, e2) in ee:
            # setting upper and lower bounds for variable corresponding to
            # edge from buses to simple_sinks
            for t in self.timesteps:
                self.w[(e1, e2), t].setub(self.simple_sink_val[e2][t])
                self.w[(e1, e2), t].setlb(self.simple_sink_val[e2][t])

    def simple_storage_model(self):
        """Simple storage model containing the constraints for simple storage
        components.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        self.soc_max = {obj.uid: obj.soc_max
                        for obj in self.simple_storage_objs}
        self.soc_min = {obj.uid: obj.soc_min
                        for obj in self.simple_storage_objs}

        O = {obj.uid: obj.outputs[0].uid for obj in self.simple_storage_objs}
        I = {obj.uid: obj.inputs[0].uid for obj in self.simple_storage_objs}

        # set bounds for basic/investment models
        if(self.invest is False):
            ee = self.edges(self.simple_storage_objs)
            # installed input/output capacity
            for (e1, e2) in ee:
                for t in self.timesteps:
                    self.w[e1, e2, t].setub(10)
                    self.w[e1, e2, t].setlb(1)

            # rule for creating upper and lower bounds for
            # storage state of charge variable (soc_v) for operational mode
            def soc_var_bounds(self, e, t):
                return(self.soc_min[e], self.soc_max[e])
            self.soc_v = po.Var(self.simple_storage_uids, self.timesteps,
                                bounds=soc_var_bounds)
        else:
            self.soc_v = po.Var(self.simple_storage_uids, self.timesteps,
                                within=po.NonNegativeReals)
            # creating additional variable for planning models used
            self.soc_add_v = po.Var(self.simple_storage_uids,
                                    within=po.NonNegativeReals)

            # constraint for additional capacity in investment models
            def invest_rule(self, e, t):
                return(self.soc_v[e, t] <= self.soc_max[e] + self.soc_add_v[e])
            self.soc_max_c = po.Constraint(self.simple_storage_uids,
                                           self.timesteps,
                                           rule=invest_rule)

        # storage energy balance
        def storage_balance_rule(self, e, t):
            if(t == 0):
                expr = 0
                expr += self.soc_v[e, t] - 0.5 * self.soc_max[e]
                return(expr, 0)
            else:
                expr = self.soc_v[e, t]
                expr += - self.soc_v[e, t-1] - self.w[I[e], e, t] + \
                    self.w[e, O[e], t]
                return(expr, 0)
            self.simple_storage_c = po.Constraint(self.simple_storage_uids,
                                                  self.timesteps,
                                                  rule=storage_balance_rule)

    def simple_transport_model(self, objs, uids):
        """Simple transport model building the constraints
        for simple transport components

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        self.generic_transformer_model(objs=objs, uids=uids)

    def objective(self):
        """Function that creates the objective function of the optimization
        model.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        # create a combine list of all cost-related components
        objective_objs = (
            self.simple_chp_objs +
            self.simple_transformer_objs +
            self.simple_storage_objs +
            self.simple_transport_objs)

        self.objective_uids = (
            self.simple_chp_uids +
            self.simple_transformer_uids +
            self.simple_transport_uids)

        I = {obj.uid: obj.inputs[0].uid for obj in objective_objs}
        # operational costs
        self.opex_var = {obj.uid: obj.opex_var for obj in objective_objs}
        # get dispatch expenditure for renewable energies with dispatch
        self.dispatch_ex = {obj.uid: obj.dispatch_ex
                            for obj in self.renewable_source_objs
                            if obj.dispatch is True}

        # objective function
        def obj_rule(self):
            expr = 0
            expr += sum(self.w[I[e], e, t] * self.opex_var[e]
                        for e in self.objective_uids
                        for t in self.timesteps)
            if self.slack is True:
                expr += sum(self.shortage_slack[e, t] * 10e10
                            for e in self.bus_uids for t in self.timesteps)

            # costs for dispatchable renewables
            if(True in self.dispatch.values()):
                expr += sum(self.renewable_dispatch_v[e, t] *
                            self.dispatch_ex[e]
                            for e in self.renewable_sources_dispatch_uids
                            for t in self.timesteps)
            # add additional capacity & capex for investment models
            if(self.invest is True):
                self.capex = {obj.uid: obj.capex for obj in objective_objs}

                expr += sum(self.w_add[I[e], e] * self.capex[e]
                            for e in self.objective_uids)
                expr += sum(self.soc_add[e] * self.capex[e]
                            for e in self.simple_storage_uids)
            return(expr)
        self.objective = po.Objective(rule=obj_rule)

    def solve(self, solver='glpk', solver_io='lp', debug=False, **kwargs):
        """Method that creates the instance of the model and solves it.

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
        self : solved pyomo.ConcreteModel instance
        """

        from pyomo.opt import SolverFactory

        # create model instance
        instance = self.create()

        # write lp-file
        if(debug is True):
            instance.write('problem.lp',
                           io_options={'symbolic_solver_labels': True})
            # print instance
            #instance.pprint()
        # solve instance
        opt = SolverFactory(solver, solver_io=solver_io)
        # store results
        results = opt.solve(instance, **kwargs)
        # load results back in instance
        instance.load(results)

        return(instance)

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


def results_to_objects(entities, instance):
    """Function that writes the results for po.ConcreteModel instance to
    objects.

    Parameters
    ----------
    components : list of component objects

    Returns
    -------
    results : dictionary with results for every instance of a class
    """
    for e in entities:
        if (isinstance(e, cp.Transformer) or isinstance(e, cp.SimpleTransport)
           or isinstance(e, cp.Source)):
            # write outputs
            e.results['Output'] = {}
            O = [e.uid for e in e.outputs[:]]
            for o in O:
                e.results['Output'][o] = []
                for t in instance.timesteps:
                    e.results['Output'][o].append(instance.w[e.uid,
                                                  o, t].value)

        if (isinstance(e, cp.Transformer) or
                isinstance(e, cp.SimpleTransport)):
            # write inputs
            e.results['Input'] = []
            for t in instance.timesteps:
                e.results['Input'].append(
                    instance.w[e.inputs[0].uid, e.uid, t].value)

        if isinstance(e, cp.SimpleStorage):
            for t in instance.timesteps:
                e.results['Input'].append(instance.w[e.inputs[0].uid,
                                          e.uid, o, t].value)
        # write results to self.simple_sink_objs
        # (will be the value of simple sink in general)
        if isinstance(e, cp.SimpleSink):
            e.results['Input'] = []
            for t in instance.timesteps:
                e.results['Input'].append(instance.w[e.inputs[0].uid,
                                          e.uid, t].value)

    if(instance.invest is True):
        for e in entities:
            if isinstance(e, cp.Transformer):
                e.results['Invest'] = instance.w_add[e.inputs[0].uid,
                                                     e.uid].value
            if isinstance(e, cp.Source):
                e.results['Invest'] = instance.w_add[e.uid,
                                                     e.outputs[0].uid].value
            if isinstance(e, cp.SimpleStorage):
                e.results['Invest'] = instance.soc_add[e.uid].value


def io_sets(components):
    """Function that gets inputs and outputs for given components.

    Parameters
    ----------
    components : list of component objects

    Returns
    -------
    (I, O) : lists with tupels that represent the edges
    """
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in components}
    I = {obj.uid: [i.uid for i in obj.inputs[:]] for obj in components}
    return(I, O)
