"""

This module provides a bunch of functions for creating whole grids from a datasource.

"""

import oemof.iolib.csv_io as csv
import oemof.iolib.config as cfg
from oemof.grids.base_grid import Grid
from oemof.entities.base_entity import Entity



def create_grid(scenario):
    """
    Create your grid here.
    Pass the Scenario-parameters and retrieve the full grid incl. entites.
    Configure the Datasource inside the config.cfg

    :param scenario: the parameter-dict
    :return: the grid.
    """
    entity_source = cfg.get("entity", "source")
    grid_source = cfg.get("grid", "source")

    if grid_source == "csv":
        grid = _load_grid_from_csv(scenario)
    elif grid_source == "postgis":
        pass
    if entity_source == "csv":
        _load_entities_from_csv_to_grid(grid, scenario)
    elif entity_source == "postgis":
        pass
    return grid


def _load_grid_from_csv(scenario):
    """
    Loads the grid-data from a csv-file
    :param scenario: the scenario.parameter.dict
    :return: the grid.
    """

    file_name = scenario["name"] + "/" + scenario["year"] + "/grid.csv"
    grid_csv = csv.load_dict_from_csv(file_name)
    grid = Grid("0")

    for element in grid_csv:
        g = Grid(element["id"])
        fields = element.keys()

        for field in fields:
            g[field] = element[field]


        if element["parent_id"] == "0":
            grid.add_node(g)
        else:
            grid.find_node_by_id(element["parent_id"]).add_node(g)

    return grid

def _load_entities_from_csv_to_grid(grid, scenario):
    """
    loads entities from a csv-source and positions them inside a grid.
    :param grid: the grid to put the entities into.
    :param scenario: the scenario-parameter-doct.
    :return:
    """

    file_name = scenario["name"] + "/" + scenario["year"] + "/entity.csv"
    entity_csv = csv.load_dict_from_csv(file_name)


    for element in entity_csv:
        e = Entity(element["id"])
        fields = element.keys()
        # TODO: Add all other properties
        for field in fields:
            e[field] = element[field]

        g = grid.find_node_by_id(element["parent_id"])
        g.add_entity(e)

