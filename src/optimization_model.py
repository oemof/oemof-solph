import pyomo.environ as po
import components as cp

#@profile


def opt_model(buses, components, timesteps, invest):
    """Create Pyomo model of the energy system.

    **Mathematical equations (should be a "sphinx-headline") later**

    The model equations are described as follows:

    .. math::

        I_{SF} = \\{ i | i \\subset E_B, (i,e) \\in \\vec{E},
        e \\in E_{SF}\\} \\\\

        O_{SF} = \\{ o | o \\subset E_B, (e,o) \\in \\vec{E},
        e \\in E_{SF}\\} \\\\

        w(I_{SF}(e), e,t) \cdot \eta_(e) - w(e,O_{SF}(e),t) = 0,
        \\forall e \\in E_{SF}, \\forall t \\in T

    Parameters
    ----------
    buses : list with all bus objects
    components : list with all component objects
    timesteps : list with all timesteps as integer values
    invest : boolean

    Returns
    -------
    m : pyomo.ConcreteModel
    """

    # create lists with objects of component subclasses
    s_transformers = [e for e in components
                      if isinstance(e, cp.SimpleTransformer)]
    s_chps = [e for e in components
              if isinstance(e, cp.SimpleCombinedHeatPower)]
    renew_sources = [e for e in components
                     if isinstance(e, cp.RenewableSource)]
    sinks = [e for e in components if isinstance(e, cp.Sink)]
    simple_storages = [e for e in components
                       if isinstance(e, cp.SimpleStorage)]
    commodities = [e for e in components if isinstance(e, cp.Commodity)]

    # create pyomo model instance
    m = po.ConcreteModel()

    # parameter flag for investment models
    m.invest = invest

    # set for timesteps
    m.timesteps = timesteps

    # entity sets using uids
    m.buses = [b.uid for b in buses]
    m.s_transformers = [c.uid for c in s_transformers]
    m.s_chps = [c.uid for c in s_chps]
    m.renew_sources = [c.uid for c in renew_sources]
    m.simple_storages = [c.uid for c in simple_storages]
    m.sinks = [c.uid for c in sinks]
    m.commodities = [c.uid for c in commodities]

    # calculate all edges ([('coal', 'pp_coal'),...])
    m.edges = get_edges(components)
    # variable for edges
    m.w = po.Var(m.edges, m.timesteps, within=po.NonNegativeReals)
    # additional variable for investment models
    if(m.invest is True):
        m.w_add = po.Var(m.edges, within=po.NonNegativeReals)

    def bus(m):
        """Create bus balance for all buses.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        # slack variable that assures a feasible problem
        m.bus_slack = po.Var(m.buses, m.timesteps, within=po.NonNegativeReals)

        # constraint for bus balance:
        # component inputs/outputs are negative/positive in the bus balance
        def bus_rule(m, e, t):
            expr = 0
            expr += -sum(m.w[(i, j), t] for (i, j) in m.edges if i == e)
            expr += sum(m.w[(i, j), t] for (i, j) in m.edges if j == e)
            expr += -m.bus_slack[e, t]
            return(0, expr, 0)
        m.bus_constr = po.Constraint(m.buses, m.timesteps, rule=bus_rule)

    def simple_transformer_model(m):
        """Simple transformer model containing the constraints
        for simple transformers.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        # temp set with input uids for every simple chp e in s_transformers
        I = {obj.uid: obj.inputs[0].uid for obj in s_transformers}
        # set with output uids for every simple transformer e in s_transformers
        O = {obj.uid: obj.outputs[0].uid for obj in s_transformers}
        eta = {obj.uid: obj.eta for obj in s_transformers}

        # constraint for simple transformers: input * efficiency = output
        def eta_rule(m, e, t):
            expr = 0
            expr += m.w[I[e], e, t] * eta[e]
            expr += - m.w[e, O[e], t]
            return(expr, 0)
        m.s_transformer_eta_constr = po.Constraint(m.s_transformers,
                                                   m.timesteps,
                                                   rule=eta_rule)

        # set variable bounds (out_max = in_max * efficiency):
        # m.i_max = {'pp_coal': 51794.8717948718, ... }
        # m.o_max = {'pp_coal': 20200, ... }
        m.i_max = {obj.uid: obj.in_max for obj in s_transformers}
        m.o_max = {obj.uid: obj.out_max for obj in s_transformers}

        # set bounds for basic/investment models
        if(m.invest is False):
            # edges for simple transformers ([('coal', 'pp_coal'),...])
            ee = get_edges(s_transformers)
            for (e1, e2) in ee:
                for t in m.timesteps:
                    # transformer output <= m.o_max
                    if e1 in m.s_transformers:
                        m.w[e1, e2, t].setub(m.o_max[e1])
                    # transformer input <= m.i_max
                    if e2 in m.s_transformers:
                        m.w[e1, e2, t].setub(m.i_max[e2])
        else:
            # constraint for additional capacity
            def w_max_invest_rule(m, e, t):
                return(m.w[I[e], e, t] <= m.i_max[e] + m.w_add[I[e], e])
            m.s_transformer_w_max = po.Constraint(m.s_transformers,
                                                  m.timesteps,
                                                  rule=w_max_invest_rule)

    def simple_chp_model(m):
        """Simple chp model containing the constraints for simple chps.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        # temp set with input uids for every simple chp e in s_chps:
        # {'pp_chp': 'gas'}
        I = {obj.uid: obj.inputs[0].uid for obj in s_chps}
        # set with output uids for every simple chp e in s_chps:
        # {'pp_chp': ['b_th', 'b_el']}
        O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in s_chps}
        # efficiencies for simple chps
        eta = {obj.uid: obj.eta for obj in s_chps}

        # constraint for transformer energy balance:
        # E = P + Q / (eta_el + eta_th) = P / eta_el = Q/ eta_th
        # (depending on the position of the outputs and eta)
        def eta_rule(m, e, t):
            expr = 0
            expr += m.w[I[e], e, t]
            expr += -sum(m.w[e, o, t] for o in O[e]) / (eta[e][0] + eta[e][1])
            return(expr, 0)
        m.s_chp_eta_constr = po.Constraint(m.s_chps, m.timesteps,
                                           rule=eta_rule)

        # additional constraint for power to heat ratio of simple chp comp:
        # P/eta_el = Q/eta_th
        def power_to_heat_rule(m, e, t):
            expr = 0
            expr += m.w[e, O[e][0], t] / eta[e][0]
            expr += -m.w[e, O[e][1], t] / eta[e][1]
            return(expr, 0)
        m.s_chp_pth_constr = po.Constraint(m.s_chps, m.timesteps,
                                           rule=power_to_heat_rule)
        # set variable bounds
        if(m.invest is False):
            m.i_max = {obj.uid: obj.in_max for obj in s_chps}
            # yields nested dict e.g: {'chp': {'home_th': 40, 'region_el': 30}}
            m.o_max = {obj.uid: dict(zip(O[obj.uid], obj.out_max))
                       for obj in s_chps}
            # edges for simple chps ([('gas', 'pp_chp'), ('pp_chp', 'b_th'),..)
            ee = get_edges(s_chps)
            for (e1, e2) in ee:
                for t in m.timesteps:
                    # chp input <= m.i_max
                    if e2 in m.s_chps:
                        m.w[e1, e2, t].setub(m.i_max[e2])
                    # chp outputs <= m.o_max
                    if e1 in m.s_chps:
                        m.w[e1, e2, t].setub(m.o_max[e1][e2])

    def renewable_source(m):
        """Simple model containing the constraints for renewable sources.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        m.source_val = {obj.uid: obj.val for obj in renew_sources}
        m.out_max = {obj.uid: obj.out_max for obj in renew_sources}

        # set bounds for basic/investment models
        if(m.invest is False):
            # edges for renewables ([('wind_on', 'b_el'), ...)
            ee = get_edges(renew_sources)
            # fixed value
            for (e1, e2) in ee:
                for t in m.timesteps:
                    m.w[(e1, e2), t].setub(m.source_val[e1][t]*m.out_max[e1])
                    m.w[(e1, e2), t].setlb(m.source_val[e1][t]*m.out_max[e1])
        else:
            # outputs: {'pv': 'b_el', 'wind_off': 'b_el', ... }
            O = {obj.uid: obj.outputs[0].uid for obj in renew_sources}

            # constraint to allow additional capacity for renewables
            def source_rule(m, e, t):
                expr = 0
                expr += m.w[e, O[e], t]
                expr += -(m.out_max[e] + m.w_add[e, O[e]]) * m.source_val[e][t]
                return(0, expr, 0)
            m.source_constr = po.Constraint(m.renew_sources, m.timesteps,
                                            rule=source_rule)

    def commodity(m):
        """Simple model containing the constraints for commodities.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        m.yearly_limit = {obj.uid: obj.yearly_limit for obj in commodities}
        # outputs: {'rcoal': ['coal'], 'rgas': ['gas'],...}
        O = {obj.uid: [obj.outputs[0].uid] for obj in commodities}

        # set upper bounds: sum(yearly commodity output) <= yearly_limit
        def commodity_limit_rule(m, e):
            expr = 0
            expr += sum(m.w[e, o, t] for t in m.timesteps for o in O[e])
            ub = m.yearly_limit[e]
            return(0, expr, ub)
        m.commodity_limit_constr = po.Constraint(m.commodities,
                                                 rule=commodity_limit_rule)

    def sink(m):
        """Simple model containing the constraints for sinks.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        m.sink_val = {obj.uid: obj.val for obj in sinks}
        ee = get_edges(sinks)
        for (e1, e2) in ee:
            # fixed value
            for t in m.timesteps:
                m.w[(e1, e2), t].setub(m.sink_val[e2][t])
                m.w[(e1, e2), t].setlb(m.sink_val[e2][t])

    def simple_storage_model(m):
        """Simple model containing the constraints for storages.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        m.soc_max = {obj.uid: obj.opt_param['soc_max']
                     for obj in simple_storages}
        m.soc_min = {obj.uid: obj.opt_param['soc_min']
                     for obj in simple_storages}

        O = {obj.uid: obj.outputs[0].uid for obj in simple_storages}
        I = {obj.uid: obj.inputs[0].uid for obj in simple_storages}

        # set bounds for basic/investment models
        if(m.invest is False):
            ij = get_edges(simple_storages)
            # installed input/output capacity
            for (i, j) in ij:
                for t in m.timesteps:
                    m.w[i, j, t].setub(10)
                    m.w[i, j, t].setlb(1)

            def soc_bounds(m, e, t):
                return(m.soc_min[e], m.soc_max[e])
            m.soc = po.Var(m.simple_storages, m.timesteps, bounds=soc_bounds)
        else:
            def soc_bounds(m, e, t):
                return(0,  None)
            m.soc = po.Var(m.simple_storages, m.timesteps, bounds=soc_bounds)
            m.soc_add = po.Var(m.simple_storages, within=po.NonNegativeReals)

            # constraint for additional capacity in investment models
            def soc_max_rule(m, e, t):
                return(m.soc[e, t] <= m.soc_max[e] + m.soc_add[e])
            m.soc_max_constr = po.Constraint(m.simple_storages, m.timesteps,
                                             rule=soc_max_rule)

        # storage energy balance
        def simple_storage_rule(m, e, t):
            if(t == 0):
                expr = 0
                expr += m.soc[e, t] - 0.5 * m.soc_max[e]
                return(expr, 0)
            else:
                expr = m.soc[e, t]
                expr += - m.soc[e, t-1] - m.w[I[e], e, t] + m.w[e, O[e], t]
                return(expr, 0)
            m.simple_storage_constr = po.Constraint(m.simple_storages,
                                                    m.timesteps,
                                                    rule=simple_storage_rule)

    def objective(m):
        """Function that creates the objective function of the LP model.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        # create a combine list of all cost-related components
        objective_components = s_chps + s_transformers + simple_storages
        m.objective_components = m.s_chps + m.s_transformers
        I = {obj.uid: obj.inputs[0].uid for obj in objective_components}
        # operational costs
        m.opex_var = {obj.uid: obj.opex_var for obj in objective_components}

        # objective function
        def obj_rule(m):
            expr = 0
            expr += sum(m.w[I[e], e, t] * m.opex_var[e]
                        for e in m.objective_components
                        for t in m.timesteps)
            expr += sum(m.bus_slack[e, t]*10e4 for e in m.buses for t in m.timesteps)
            # add additional capacity & capex for investment models
            if(m.invest is True):
                m.capex = {obj.uid: obj.capex for obj in objective_components}

                expr += sum(m.w_add[I[e], e] * m.capex[e]
                            for e in m.objective_components)
                expr += sum(m.soc_add[e] * m.capex[e]
                            for e in m.simple_storages)
            return(expr)
        m.objective = po.Objective(rule=obj_rule)

    # "call" the models to add the constraints to opt-problem
    bus(m)
    simple_chp_model(m)
    renewable_source(m)
    simple_transformer_model(m)
    simple_storage_model(m)
    commodity(m)
    objective(m)
    sink(m)

    return(m)


def solve(model, solver='glpk', solver_io='lp', debug=False, **kwargs):
    """Function that creates the objective function of the LP model.

    Parameters
    ----------
    model : pyomo.ConcreteModel instance
    solver : str solver to be used e.g. 'glpk','gurobi','cplex'

    Returns
    -------
    m : pyomo.ConcreteModel
    """

    from pyomo.opt import SolverFactory

    # create model instance
    instance = model.create()

    # write lp-file
    if(debug is True):
        instance.write('problem.lp', io_options={'symbolic_solver_labels':
                                                 True})
    # solve instance
    opt = SolverFactory(solver, solver_io=solver_io)
    # store results
    results = opt.solve(instance, **kwargs)
    # load results back in instance
    instance.load(results)

    return(instance)


def get_edges(components):
    """Function that creates the objective function of the LP model.

    Parameters
    ----------
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
    """Function that converts the results.

    Parameters
    ----------
    components : list of component objects

    Returns
    -------
    edges : list with tupels that represent the edges
    """
    for e in entities:
        if isinstance(e, cp.Transformer) or isinstance(e, cp.Source):
            e.results['Output'] = {}
            O = [e.uid for e in e.outputs[:]]
            for o in O:
                e.results['Output'][o] = []
                for t in instance.timesteps:
                    e.results['Output']
                    [o].append(instance.w[e.uid, o, t].value)
        if isinstance(e, cp.SimpleStorage):
            for t in instance.timesteps:
                e.results['Input'].append(instance.w[e.inputs[0].uid,
                                          e.uid, o, t].value)
        # write results to sinks (will be the value of Sink in general)
        if isinstance(e, cp.Sink):
            e.results['Input'] = {}
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
