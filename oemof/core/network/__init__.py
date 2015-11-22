"""
This package (along with its subpackages) contains the classes used to model
energy systems. An energy system is modelled as a graph/network of entities
with very specific constraints on which types of entities are allowed to be
connected.

"""
# TODO: Adhere to PEP 0257 by listing the exported classes with a short
#       summary.


class Entity:
    """
    The most abstract type of vertex in an energy system graph. Since each
    entity in an energy system has to be uniquely identifiable and
    connected (either via input or via output) to at least one other
    entity, these properties are collected here so that they are shared
    with descendant classes.
    """
    optimization_options = {}
    def __init__(self, **kwargs):
        #TODO: add default argument values to docstrings (if it's possible).
        """
        :param uid: unique component identifier
        :param inputs: list of Entities acting as input to this Entity.
        :param outputs: list of Entities acting as output from this Enity.
        :param geo_data: geo-spatial data with informations for
                         location/region-shape
        """
        self.uid = kwargs["uid"]
        self.inputs = kwargs.get("inputs", [])
        self.outputs = kwargs.get("outputs", [])
        for e_in in self.inputs:
            if self not in e_in.outputs:
                e_in.outputs.append(self)
        for e_out in self.outputs:
            if self not in e_out.inputs:
                e_out.inputs.append(self)
        self.geo_data = kwargs.get("geo_data", None)

    def __str__(self):
        return "<{0} #{1}>".format(type(self).__name__, self.uid)


if __name__ == "__main__":

    #TODO: This example is missing a Transport. (Needs more escalation error.)
    coal = Bus(uid="Coal", type="coal")
    power1 = Bus(uid="Electricity1", type="electricity")
    power2 = Bus(uid="Electricity1", type="electricity")
    st = SimpleTransformer(uid="st1",inputs=[coal],outputs=[power], eta=0.4)
    heat = Bus(uid="Thermal", type="thermal")
    heatpump = Transformer(uid="Heatpump", inputs=[power],
                           outputs=[heat])
    chp = Transformer(uid="CHP", inputs=[coal], outputs=[heat, power])
    wind = Source(uid="The only wind turbine on the planet.", outputs=[power])
    city = Sink(uid="Neverwhere", val=5)
#  cable = SimpleTransport(uid="NordLink", inputs=[power1], outputs=[power2],
#                          in_max=700, out_max=630, eta=0.9)
#  print(vars(cable))

#  import networkx as nx
#
#  g = nx.DiGraph()
#  es = [coal, power, heat, heatpump, chp, wind, city]
#  buses = [e for e in es if isinstance(e, Bus)]
#  components = [e for e in es if isinstance(e, Component)]
#  g.add_nodes_from(es)
#  for e in es:
#    for e_in in e.inputs:
#      a, b = e_in, e
#      g.add_edge(a, b)
#  graph_pos=nx.spectral_layout(g)
#  nx.draw_networkx_nodes(g, graph_pos, buses, node_shape="o", node_color="r",
#                         node_size = 900)
#  nx.draw_networkx_nodes(g, graph_pos, components, node_shape="s",
#                         node_color="b", node_size=300)
#  nx.draw_networkx_edges(g, graph_pos)
#  nx.draw_networkx_labels(g, graph_pos)
#  # or simply nx.draw(g) but then without different node shapes etc
