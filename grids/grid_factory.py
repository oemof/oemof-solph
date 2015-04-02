"""

This module provides a bunch of functions for creating whole grids from a datasource.

"""

import oemof.iolib.csv_io as csv
import oemof.iolib.config as cfg
from oemof.grids.base_grid import Grid
from oemof.entities.base_entity import Entity
from oemof.grids.base_grid import Connection

def create_grid(scenario):
    entity_source = cfg.get("entity", "source")
    grid_source = cfg.get("grid", "source")

    if grid_source == "csv":
        grid = load_grid_from_csv(scenario)
    elif grid_source == "postgis":
        pass
    if entity_source == "csv":
        load_entities_from_csv_to_grid(grid, scenario)
    elif entity_source == "postgis":
        pass
    return grid

def load_grid_from_csv(scenario):

    file_name = cfg.get("csv", "root") + "grid.csv"
    grid_csv = csv.load_dict_from_csv(file_name)
    grid = Grid("0")

    for k, line in grid_csv.items():
        g = Grid(line["id"])
        fields = line.keys()

        for field in fields:
            g[field] = line[field]


        if line["parent_id"] == "0":
            grid.add_node(g)
        else:
            grid.find_node_by_id(line["parent_id"]).add_node(g)

    return grid

def load_entities_from_csv_to_grid(grid, scenario):

    file_name = cfg.get("csv", "root") + "entity.csv"
    entity_csv = csv.load_dict_from_csv(file_name)


    for k, line in entity_csv.items():
        e = Entity(line["id"])
        fields = line.keys()
        # TODO: Add all other properties
        for field in fields:
            e[field] = line[field]

        g = grid.find_node_by_id(line["parent_id"])
        g.add_entity(e)

