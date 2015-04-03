from oemof.scenariolib.base_scenario import Scenario
from oemof.grids.base_grid import Grid
from oemof.solverlib.base_solph import Solph
import oemof.feedinlib.feedin as f
import oemof.grids.grid_factory as gf


class Handler(object):

    def __init__(self, parameters):
        self.parameters = parameters
        self.grid = gf.create_grid(parameters)
        print self.grid

    def run(self):
        f.feed(self.grid, self.parameters)
        solph = Solph()                             # TODO: echt alles komoisch, sollte nich so laufen
        self.results = solph.solph(self.grid)

    def get_results(self):
        return self.results

    def get_grid(self):
        return self.grid