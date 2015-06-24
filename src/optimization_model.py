
import pyomo.environ as po


def opt_model(entities, edges, timesteps, invest):
  """
  :param entities: dictionary containing all entities grouped by classtypes

  **Mathematical equations:**
    .. math::
      I_{SF} = \\{ i | i \\subset E_B, (i,e) \\in \\vec{E}, e \\in E_{SF}\\} \\\\
      O_{SF} = \\{ o | o \\subset E_B, (e,o) \\in \\vec{E}, e \\in E_{SF}\\} \\\\
      w(I_{SF}(e), e,t) \cdot \eta_(e) - w(e,O_{SF}(e),t) = 0,
      \\forall e \\in E_{SF}, \\forall t \\in T
  """
  # objects
  buses = entities['buses']
  s_transformers = entities['s_transformers']
  s_chps = entities['s_chps']
  sources = entities['sources']
  simple_storages = entities['simple_storages']

  # create pyomo model instance
  m = po.ConcreteModel()

  # parameter simulation
  m.invest = invest
  # create pyomo sets
  # timesteps
  m.timesteps = timesteps

  # entity sets using uids
  m.buses = [b.uid for b in buses]
  m.s_transformers = [t.uid for t in s_transformers]
  m.s_chps = [t.uid for t in s_chps]
  m.sources = [s.uid for s in sources]
  m.simple_storages = [s.uid for s in simple_storages]

  # could be calculated inside this function
  m.edges = edges

  m.w = po.Var(m.edges, m.timesteps, within=po.NonNegativeReals)
  if(m.invest==True):
      m.w_add = po.Var(m.edges, within=po.NonNegativeReals)

  ## bus balance forall b in buses
  def bus_rule(m, e, t):
    expr = 0
    expr += -sum(m.w[(i,j),t] for (i,j) in m.edges if i==e)
    expr +=  sum(m.w[(i,j),t] for (i,j) in m.edges if j==e)
    return(expr, 0)
  m.bus_constr = po.Constraint(m.buses, m.timesteps, rule=bus_rule)


  # simple transformer model containing the constraints for simple transformers
  def simple_transformer_model(m):
    """
    :param m: pyomo model instance
    """


    # temp set with input uids for every simple chp e in s_transformers
    I = {obj.uid:obj.inputs[0].uid for obj in s_transformers}
    # set with output uids for every simple transformer e in s_transformers
    O = {obj.uid:obj.outputs[0].uid for obj in s_transformers}
    eta = {t.uid:t.eta for t in s_transformers}
    def eta_rule(m, e, t):
      expr = 0
      expr += m.w[I[e], e, t] * eta[e]
      expr += - m.w[e, O[e], t]
      return(expr,0)
    m.s_transformer_eta_constr = po.Constraint(m.s_transformers, m.timesteps,
                                               rule=eta_rule)
    # set variable bounds
    if(m.invest is False):
      ij = get_edges(s_transformers)
      for (i,j) in ij:
        for t in m.timesteps:
          m.w[i,j,t].setub(99999)
    else:
      def w_bound_investment(m, e, t):
        return(m.w[I[e],e,t] <= 8888 + m.w_add[I[e],e])
      m.s_transformer_w_max = po.Constraint(m.s_transformers, m.timesteps,
                                            rule=w_bound_investment)

  # simple chp model containing the constraints for simple chps
  def simple_chp_model(m):
    """
    """

    # temp set with input uids for every simple chp e in s_chps
    I = {obj.uid:obj.inputs[0].uid for obj in s_chps}
    # set with output uids for every simple chp e in s_chps
    O = {obj.uid : [o.uid for o in obj.outputs[:]] for obj in s_chps}
    # constraint for transformer energy balance
    def eta_rule(m, e, t):
      expr = 0
      expr += m.w[I[e], e, t]
      expr += -sum(m.w[e, o, t] for o in O[e]) / 0.8
      return(expr,0)
    m.s_chp_eta_constr = po.Constraint(m.s_chps, m.timesteps, rule=eta_rule)

    # additional constraint for power to heat ratio of simple chp components
    def power_to_heat_rule(m, e, t):
      expr = 0
      expr += m.w[e, O[e][0], t]
      expr += -m.w[e, O[e][1], t] * 0.6
      return(expr,0)
    m.s_chp_pth_constr = po.Constraint(m.s_chps, m.timesteps,
                                       rule=power_to_heat_rule)
    # set variable bounds
    if(m.invest is False):
      ij = get_edges(s_chps)
      for (i,j) in ij:
        for t in m.timesteps:
          m.w[i,j,t].setub(1000)

  def source(m):
    """
    """
    m.source_val = {obj.uid:obj.val for obj in sources}
    # set variable bounds
    if(m.invest is False):
      ij = get_edges(sources)
      for (i,j) in ij:
        for t in m.timesteps:
          print(i,j)
          m.w[(i,j),t].setub(m.source_val[i][t])
          m.w[(i,j),t].setlb(m.source_val[i][t])
    else:
      O = {obj.uid:obj.outputs[0].uid for obj in sources}
      def source_rule(m, e, t):
        return(m.w[e,O[e],t] == (888 + m.w_add[e,O[e]]) * m.source_val[e][t])
      m.source_constr = po.Constraint(m.sources, m.timesteps, rule=source_rule)

  def simple_storage_model(m):
    """
    """
    m.soc_max = {obj.uid:obj.soc_max for obj in simple_storages}
    m.soc_min = {obj.uid:obj.soc_min for obj in simple_storages}

    O = {obj.uid:obj.outputs[0].uid for obj in simple_storages}
    I = {obj.uid:obj.inputs[0].uid for obj in simple_storages}

    if(m.invest is False):
      ij = get_edges(simple_storages)
      for (i,j) in ij:
        for t in m.timesteps:
          m.w[i,j,t].setub(10)
          m.w[i,j,t].setlb(1)
      def soc_bounds(m, e, t):
        return(m.soc_min[e], m.soc_max[e])
      m.soc = po.Var(m.simple_storages, m.timesteps, bounds=soc_bounds)

    else:
      def soc_bounds(m, e, t):
        return(0,  None)
      m.soc = po.Var(m.simple_storages, m.timesteps, bounds=soc_bounds)
      m.soc_add = po.Var(m.simple_storages, within=po.NonNegativeReals)

      def soc_max_rule(m, e, t):
        return(m.soc[e,t] <= m.soc_max[e] + m.soc_add[e])
      m.soc_max_constr = po.Constraint(m.simple_storages, m.timesteps,
                                       rule=soc_max_rule)

    # storage energy balance
    def simple_storage_rule(m, e, t):
      if(t==0):
        return(m.soc[e,t] == 0.5 * m.soc_max[e])
      else:
        return(m.soc[e,t] == m.soc[e,t-1] - m.w[I[e],e,t] + m.w[e,O[e],t])
    m.simple_storage_constr = po.Constraint(m.simple_storages, m.timesteps,
                                              rule=simple_storage_rule)

  def objective(m):

    def obj_rule(m):
      expr = 0
      expr += sum(m.w[i,j,t] for (i,j) in m.edges for t in m.timesteps)
      return(expr)
    m.objective = po.Objective(rule=obj_rule)

  # "call" the models to add the constraints to opt-problem
  simple_chp_model(m)
  source(m)
  simple_transformer_model(m)
  simple_storage_model(m)
  objective(m)

  return(m)

def solve_opt_model(instance, solver='glpk',
                      options={'stream':False}, debug=False):
 """
 :param model: pyomo concreteModel() instance
 :param str solver: solver specification as string 'glpk','gurobi','clpex' ...
 """
 from pyomo.opt import SolverFactory

 # solve instance
 if(debug==True):
   instance.write('problem.lp',
                  io_options={'symbolic_solver_labels':True})

 opt = SolverFactory(solver, solver_io='python')
 # store results
 results = opt.solve(instance, tee=options['stream'])
 # load results back in instance
 instance.load(results)

 return(instance)

def get_edges(components):
  edges= []
  for c in components:
    for i in c.inputs:
      ei =  (i.uid, c.uid)
      edges.append(ei)
    for o in c.outputs:
      ej = (c.uid, o.uid)
      edges.append(ej)
  return(edges)

def io_sets(components):
  O = {obj.uid : [o.uid for o in obj.outputs[:]] for obj in components}
  I = {obj.uid : [i.uid for i in obj.inputs[:]] for obj in components}
  return(I,O)

if __name__ == "__main__":
  # create energy system components
  timesteps = [t for t in range(3)]
  import components as cp
  import random
  bus1 = cp.Bus(uid="b1", type="coal")
  bus21 = cp.Bus(uid="b21", type="elec")
  bus22 = cp.Bus(uid="b22", type="elec")
  bus3  = cp.Bus(uid="b3", type="th")
  s21 = cp.Source(uid="s21", outputs=[bus21], val=[random.gauss(10,4) for i in timesteps])
  s3 = cp.Source(uid="s3", outputs=[bus3], val=[random.gauss(5,1) for i in timesteps])
  s22 = cp.Source(uid="s22", outputs=[bus22], val=[random.gauss(1,4) for i in timesteps])

  objs_sf = [cp.SimpleTransformer(uid='t'+str(i), inputs=[bus1],
                                  outputs=[bus21], eta=0.5) for i in range(10)]
  objs_schp = [cp.Transformer(uid='c'+str(i), inputs=[bus1],
                              outputs=[bus21,bus3]) for i in range(10)]
  objs_sf2 = [cp.SimpleTransformer(uid='t2'+str(i), inputs=[bus1],
                                   outputs=[bus22], eta=0.4) for i in range(10)]

  ss = cp.SimpleStorage(uid="ss1", outputs=[bus21], inputs=[bus21],
                        soc_max=10, soc_min=1)

  components = objs_sf + objs_sf2 + objs_schp + [s21,s22, s3] + [ss]

  edges = get_edges(components)
  I,O = io_sets(components)

  entities_dict = {'buses':[bus1, bus21, bus22, bus3],
                   's_transformers':objs_sf+objs_sf2,
                   's_chps':objs_schp,
                   'sources':[s21,s22, s3],
                   'simple_storages':[ss]}
  #I, O = io_sets(objs_schp)

  from time import time

  t0 = time()
  # create optimization model
  om = opt_model(entities=entities_dict, edges=edges,
                 timesteps=timesteps, invest=True)
  t1 = time()
  building_time = t1 - t0
  print('Building time', building_time)
  # create model instance
  print('Creating instance...')
  instance = om.create(report_timing=True)
  #instance.pprint()

  print('Solving model...')
  t0 = time()
  instance = solve_opt_model(instance=instance, solver='gurobi',
                             options={'stream':True}, debug=True)
  t1 = time()
  solving_time = t1 - t0
  print('Solving time:', solving_time)

  #instance.source_val['s1'] = [random.gauss(-10,4) for i in timesteps]
  #instance.del_component('w')
  #instance.w = po.Var(instance.edges, instance.timesteps, bounds=w_max_rule,
  #                    within=po.NonNegativeReals)

  #for idx in instance.w:
  #  print('Edge:'+str(idx), ', weight:'+str(instance.w[idx].value))