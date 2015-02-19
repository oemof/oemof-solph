from oemof.scenariolib.base_scenario import Scenario
from oemof.grids.base_grid import Grid
from oemof.feedinlib.feedin import Feedin
from oemof.solverlib.base_solph import Solph

class Handler(object):

    def __init__(self, **parameters):
        self.parameters = parameters

        self.scenario = Scenario(**self.parameters)
        self.grid = Grid("Germany")
        Feedin(self.grid)                           # TODO: komischer aufruf
        solph = Solph()                             # TODO: echt alles komoisch, sollte nich so laufen
        self.results = solph.solph(self.grid)


    def run(self):
        print(self.scenario.name)

    def get_results(self):
        return self.results