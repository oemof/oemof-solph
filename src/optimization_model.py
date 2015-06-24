
import pyomo.environ as po


def opt_model(buses, components, timesteps, invest):
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

  s_transformers = [e for e in components if isinstance(e, cp.SimpleTransformer)]
  s_chps = []#[e for e in components if isinstance(e, cp.Transformer)]
  sources = [e for e in components if isinstance(e, cp.Source)]
  sinks = [e for e in components if isinstance(e, cp.Sink)]
  simple_storages = [e for e in components if isinstance(e, cp.SimpleStorage)]

  # create pyomo model instance
  m = po.ConcreteModel()

  # parameter simulation
  m.invest = invest
  # create pyomo sets
  # timesteps
  m.timesteps = timesteps

  # entity sets using uids
  m.buses = [b.uid for b in buses]
  m.s_transformers = [c.uid for c in s_transformers]
  m.s_chps = [c.uid for c in s_chps]
  m.sources = [c.uid for c in sources]
  m.simple_storages = [c.uid for c in simple_storages]
  m.sinks = [c.uid for c in sinks]
  # could be calculated inside this function
  m.edges = get_edges(components)

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
    eta = {obj.uid:obj.opt_param['eta'] for obj in s_transformers}
    def eta_rule(m, e, t):
      expr = 0
      expr += m.w[I[e], e, t] * eta[e]
      expr += - m.w[e, O[e], t]
      return(expr,0)
    m.s_transformer_eta_constr = po.Constraint(m.s_transformers, m.timesteps,
                                               rule=eta_rule)
    # set variable bounds
    m.i_max = {obj.uid:obj.opt_param['in_max'] for obj in s_transformers}
    m.o_max = {obj.uid:obj.opt_param['out_max'] for obj in s_transformers}

    if(m.invest is False):
      ee = get_edges(s_transformers)
      for (e1,e2) in ee:
        for t in m.timesteps:
          if e1 in m.s_transformers:
            m.w[e1,e2,t].setub(m.o_max[e1])
          if e2 in m.s_transformers:
            m.w[e1,e2,t].setub(m.i_max[e2])
    else:
      def w_max_invest_rule(m, e, t):
        return(m.w[I[e],e,t] <= m.i_max[e] + m.w_add[I[e],e])
      m.s_transformer_w_max = po.Constraint(m.s_transformers, m.timesteps,
                                            rule=w_max_invest_rule)

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
      expr += -m.w[e, O[e][1], t] * 1
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
      ee = get_edges(sources)
      for (e1,e2) in ee:
        for t in m.timesteps:
          m.w[(e1,e2),t].setub(m.source_val[e1][t])
          m.w[(e1,e2),t].setlb(0)#m.source_val[e1][t])
    else:
      O = {obj.uid:obj.outputs[0].uid for obj in sources}
      def source_rule(m, e, t):
        return(m.w[e,O[e],t] == (888 + m.w_add[e,O[e]]) * m.source_val[e][t])
      m.source_constr = po.Constraint(m.sources, m.timesteps, rule=source_rule)

  def sink(m):
    m.sink_val = {obj.uid:obj.val for obj in sinks}
    ee = get_edges(sinks)
    for (e1,e2) in ee:
      for t in m.timesteps:
        m.w[(e1,e2),t].setub(m.sink_val[e2][t])
        m.w[(e1,e2),t].setlb(m.sink_val[e2][t])

  def simple_storage_model(m):
    """
    """
    m.soc_max = {obj.uid:obj.opt_param['soc_max'] for obj in simple_storages}
    m.soc_min = {obj.uid:obj.opt_param['soc_min'] for obj in simple_storages}

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
  sink(m)

  return(m)

def solve_opt_model(instance, solver='glpk', options={'stream':False},
                    debug=False):
 """
 :param model: pyomo concreteModel() instance
 :param str solver: solver specification as string 'glpk','gurobi','clpex' ...
 """
 from pyomo.opt import SolverFactory

 if(debug==True):
   instance.write('problem.lp',
                  io_options={'symbolic_solver_labels':True})
 # solve instance
 opt = SolverFactory(solver, solver_io='lp')
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
  import components as cp
  import random

  timesteps = [t for t in range(5)]

  # Busses (1 Coal, 2 Elec, 1 Thermal)
  bus_coal = cp.Bus(uid="coal_bus", type="coal")
  bus_el1 = cp.Bus(uid="region_1", type="elec")
  bus_el2 = cp.Bus(uid="region_2", type="elec")
  bus_th1 = cp.Bus(uid="district_heating", type="th")

  # Renewable sources
  wind_r1 = cp.Source(uid="wind_r1", outputs=[bus_el1],
                      val=[random.gauss(15,1) for i in timesteps])
  wind_r2 = cp.Source(uid="wind_r2", outputs=[bus_el2],
                      val=[random.gauss(10,1) for i in timesteps])
  solar = cp.Source(uid="solar_heat", outputs=[bus_th1],
                    val=[random.gauss(3,1) for i in timesteps])

  # (Re) sources
  r_coal = cp.Source(uid="r_coal", outputs=[bus_coal], val=[float('inf') for t in timesteps])

  # Sinks
  demand_r1 = cp.Sink(uid="demand_r1", inputs=[bus_el1],
                      val=[random.gauss(30,4) for i in timesteps])
  demand_r2 = cp.Sink(uid="demand_r2", inputs=[bus_el2],
                      val=[random.gauss(50,4) for i in timesteps])
  demand_th = cp.Sink(uid="demand_th", inputs=[bus_th1],
                      val=[random.gauss(50,4) for i in timesteps])

  # Simple Transformer for region_1
  SF_region_1 = [cp.SimpleTransformer(uid='SFr1'+str(i), inputs=[bus_coal],
                                      outputs=[bus_el1],
                                      opt_param={'eta':0.5, 'in_max':200, 'out_max':100}) for i in range(2)]
  # Simple Transformer for region_2
  SF_region_2 = [cp.SimpleTransformer(uid='SFr2'+str(i), inputs=[bus_coal],
                                      outputs=[bus_el2],
                                      opt_param={'eta':0.3, 'in_max':1000, 'out_max':300}) for i in range(2)]

  # Boiler for district heating
  SF_district_heating = [cp.SimpleTransformer(uid='Boiler'+str(i),
                                              inputs=[bus_coal], outputs=[bus_th1],
                                              opt_param={'eta':0.9, 'in_max':200, 'out_max':None}) for i in range(2)]
  # Storage electric for region_1
  SS_region_1 = cp.SimpleStorage(uid="Storage", outputs=[bus_el1],
                                 inputs=[bus_th1],
                                 opt_param={'soc_max':10, 'soc_min':1})

  # group all components
  buses = [bus_coal, bus_el1, bus_el2, bus_th1]
  components = [wind_r1, wind_r2, solar, r_coal] + [demand_r1, demand_r2] + \
                SF_region_1 + SF_region_2 + SF_district_heating + [SS_region_1]
  #I, O = io_sets(objs_schp)

  from time import time
  t0 = time()
  # create optimization model
  om = opt_model(buses, components,
                 timesteps=timesteps, invest=False)
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