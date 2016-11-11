# -*- coding: utf-8 -*-
import network

class Bus(network.Bus):
    """
    """
    def __init__(self):
        """
        """
class Line(network.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super.__init__(self, *args, **kwargs)

        self.reactance = kwargs.get('reactance')



class Generator(network.Transformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super.__init__(self, *args, **kwargs)





class Demand(network.Sink):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super.__init__(self, *args, **kwargs)


