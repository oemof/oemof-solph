class Entity:
  """
  """
  def __init__(self, **kwargs):
    #TODO: add default argument values to docstrings (if it's possible).
    """
    :param uid: unique component identifier
    :param inputs: list of Entities acting as input to this Entity.
    :param outputs: list of Entities acting as output from this Enity.
    """
    self.uid = kwargs["uid"]
    self.inputs = kwargs.get("inputs", [])
    self.outputs = kwargs.get("outputs", [])
    for e_in in self.inputs:
      if self not in e_in.outputs: e_in.outputs.append(self)
    for e_out in self.outputs:
      if self not in e_out.inputs: e_out.inputs.append(self)

  def __str__(self): return "<{0} #{1}>".format(type(self).__name__, self.uid)

class Component(Entity): pass

class Transformer(Component):
  """
  """
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if not self.inputs:
      raise ValueError("Transformer must have at least one input.\n" +
                       "Got: {0!r}".format([str(x) for x in self.inputs]))
    if not self.outputs:
      raise ValueError("Transformer must have at least one output.\n" +
                       "Got: {0!r}".format([str(x) for x in self.outputs]))

class Sink(Component):
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.outputs:
      raise ValueError("Sink must not have outputs.\n" +
                       "Got: {0!r}".format([str(x) for x in self.outputs]))


class Source(Component):
  """
  """
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.inputs:
      raise ValueError("Source must not have inputs.\n" +
                       "Got: {0!r}".format([str(x) for x in self.inputs]))

class Bus(Entity):
  """
  """
  def __init__(self, **kwargs):
    """
    :param type: bus type could be electricity...BLARBLAR
    """
    super().__init__(**kwargs)
    self.type = kwargs["type"]

class Transport(Component):
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if len(self.inputs) != 1:
      raise ValueError("Transport must have exactly one input.\n" +
                       "Got: {0!r}".format([str(x) for x in self.inputs]))

    if len(self.outputs) != 1:
      raise ValueError("Transport must have exactly one output.\n" +
                       "Got: {0!r}".format([str(x) for x in self.outputs]))




if __name__ == "__main__":
  #TODO: This example is missing a Transport. (Needs more escalation error.)
  coal = Bus(uid="Coal", type="coal")
  power = Bus(uid="Electricity", type="electricity")
  heat = Bus(uid="Thermal", type="thermal")
  heatpump = Transformer(uid="Heatpump", inputs=[power],
                         outputs=[heat])
  chp = Transformer(uid="CHP", inputs=[coal], outputs=[heat, power])
  wind = Source(uid="The only wind turbine on the planet.", outputs=[power])
  city = Sink(uid="Neverwhere", inputs=[heat])

  import networkx as nx

  g = nx.DiGraph()
  es = [coal, power, heat, heatpump, chp, wind, city]
  buses = [e for e in es if type(e) == Bus]
  components = [e for e in es if type(e) != Bus]
  g.add_nodes_from(es)
  for e in es:
    for e_in in e.inputs:
      a, b = e_in, e
      g.add_edge(a, b)
  graph_pos=nx.spectral_layout(g)
  nx.draw_networkx_nodes(g, graph_pos, buses, node_shape="o", node_color="r",
                         node_size = 900)
  nx.draw_networkx_nodes(g, graph_pos, components, node_shape="s",
                         node_color="b", node_size=300)
  nx.draw_networkx_edges(g, graph_pos)
  nx.draw_networkx_labels(g, graph_pos)
  # or simply nx.draw(g) but then without different node shapes etc
