"""
Contains the class hierarchy used to model energy systems. An energy
system is modelled as a graph/network of entities with very specific
constraints on which types of entities are allowed to be connected.

TODO: Adhere to PEP 0257 by listing the exported classes with a short
      summary.

"""
class Entity:
  """
  The most abstract type of vertex in an energy system graph. Since each
  entity in an energy system has to be uniquely identifiable and
  connected (either via input or via output) to at least one other
  entity, these properties are collected here so that they are shared
  with descendant classes.
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

class Component(Entity):
  """
  Components are one specific type of entity comprising an energy system
  graph, the other being Buses. The important thing is, that connections
  in an energy system graph are only allowed between Buses and
  Components and not between Entities of equal subtypes. This class
  exists only to facilitate this distinction and is empty otherwise.

  """
  pass

class Transformer(Component):
  """
  A Transformer is a specific type of Component which transforms
  (possibly m) inputs into (possibly n) outputs. As such neither its
  list of inputs, nor its list of outputs are allowed to be empty.
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

class SimpleTransformer(Transformer):
  """
  Simple Transformers always have a simple input output relation with a
  constant efficiency
  """
  def __init__(self,**kwargs):
    """
    :param eta: eta as constant efficiency for simple transformer
    """
    super().__init__(**kwargs)
    self.eta = kwargs['eta']

class Sink(Component):
  """
  A Sink is special Component which only consumes some source commodity.
  Therefore its list of outputs has to be either None or empty (i.e. logically
  False).
  """
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.outputs:
      raise ValueError("Sink must not have outputs.\n" +
                       "Got: {0!r}".format([str(x) for x in self.outputs]))


class Source(Component):
  """
  The opposite of a Sink, i.e. a Component which only produces and as a
  consequence has no input.
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
  The other type of entity in an energy system graph (besides
  Components). A Bus acts as a kind of mediator between producers and
  consumers of a commodity of the same kind. As such it has a type,
  which signifies what kind of commodity goes through the bus.
  """
  def __init__(self, **kwargs):
    """
    :param type: the type of the bus. Can be a meaningful value like e.g.
                 "electricity" but may be anything that can be tested for
                 equality and is distinct for incompatible Buses.
    """
    super().__init__(**kwargs)
    self.type = kwargs["type"]

class Transport(Component):
  """
  A Transport is a simple connection transporting a commodity from one
  Bus to a different one. It is different from a Transformer in that it
  may not change the type of commodity being transported. But since the
  transfer can still change things about the commodity other than the
  type (loss, gain, time delay, etc.) this class exists to encapsulate
  such changes.
  """
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
  st = SimpleTransformer(uid="st1",inputs=[coal],outputs=[power], eta=0.4)
  heat = Bus(uid="Thermal", type="thermal")
  heatpump = Transformer(uid="Heatpump", inputs=[power],
                         outputs=[heat])
  chp = Transformer(uid="CHP", inputs=[coal], outputs=[heat, power])
  wind = Source(uid="The only wind turbine on the planet.", outputs=[power])
  city = Sink(uid="Neverwhere", inputs=[heat])

  import networkx as nx

  g = nx.DiGraph()
  es = [coal, power, heat, heatpump, chp, wind, city]
  buses = [e for e in es if isinstance(e, Bus)]
  components = [e for e in es if isinstance(e, Component)]
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
