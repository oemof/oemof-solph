class Scenario(object):

    def __init__(self, **parameters):
        self.parameters = parameters

        self.name = self.parameters['name']