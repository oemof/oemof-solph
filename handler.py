"""
This module contains the "first-example"-of the Handler-Class.
It's the entrypoint for every simulation run by the framework.
Refer to the class-documentation for usage.

Some details will change in the future.

version: 0.1
"""
from oemof.solverlib.base_solph import Solph
import oemof.feedinlib.feedin as f
import oemof.grids.grid_factory as gf


class Handler(object):
    """
    Entrypoint for every simulation. This class handles all the entity- and grid-creation, feeds of those elements,
    solves the problem and provides methods for accessing the resulted data.

    Some details will change with the final implementation!

    """
    def __init__(self, parameters):
        """
        Main Constructor. Provide a parameter dict to let the handler correctly load the appropriate data:

        parameters = {
            "name" : "minimal",
            "year" : "2013"
        }

        this configuration will make the "first-example"-implementation run, if the needed example-data is installed.
        Refer to the wiki for more details.

        :param parameters: the parameter-dict.
        """
        self.parameters = parameters

        #call the grid-factory, will return the grid defined in the exampledata
        self.grid = gf.create_grid(parameters)
        print self.grid

    def run(self):
        """
        starts the simulation.
        """

        #passes the scenario-parameters and the greed to the feeder.
        f.feed(self.grid, self.parameters)


        #create a Solph-instance and solve the problem, catch the result set if provided by the solver.
        #TODO: implement dynamic solver-instantiation for scenario-defined solvers.
        solph = Solph()
        self.results = solph.solve(self.grid)

    def get_results(self):
        """
        :return: the resultset, if provided by the solver.
        """
        return self.results

    def get_grid(self):
        """
        :return: the grid-instance. if called after run(), it will be the "solved" grid, with all fields used.
        """
        return self.grid