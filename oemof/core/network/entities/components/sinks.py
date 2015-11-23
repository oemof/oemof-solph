from . import Sink


class Simple(Sink):
    """
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.val = kwargs['val']
