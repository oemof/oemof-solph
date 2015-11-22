from . import Sink


class Simple(Sink):
    """
    """
    optimization_options = {}
    lower_name = "simple_sink"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.val = kwargs['val']
