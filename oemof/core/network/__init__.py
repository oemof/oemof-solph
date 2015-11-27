"""
This package (along with its subpackages) contains the classes used to model
energy systems. An energy system is modelled as a graph/network of entities
with very specific constraints on which types of entities are allowed to be
connected.

"""
# TODO: Adhere to PEP 0257 by listing the exported classes with a short
#       summary.


class Entity:
    r"""
    The most abstract type of vertex in an energy system graph. Since each
    entity in an energy system has to be uniquely identifiable and
    connected (either via input or via output) to at least one other
    entity, these properties are collected here so that they are shared
    with descendant classes.

    Parameters
    ----------
    uid : string or tuple
        Unique component identifier of the entity.
    inputs : list
        List of Entities acting as input to this Entity.
    outputs : list
        List of Entities acting as output from this Enity.
    geo_data : shapely.geometry object
        Geo-spatial data with informations for location/region-shape. The
        geometry can be a polygon/multi-polygon for regions, a line fore
        transport objects or a point for objects such as transformer sources.
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        # TODO: @Günni:
        # add default argument values to docstrings (if it's possible).
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
        self.regions = []
        self.add_regions(kwargs.get('regions', []))

        # TODO: @Gunni Yupp!
    def add_regions(self, regions):
        'Add regions to self.regions'
        self.regions.extend(regions)
        for region in regions:
            if self not in region.entities:
                region.entities.append(self)

    def __str__(self):
        return "<{0} #{1}>".format(type(self).__name__, self.uid)
