from network.entities.components import Sink


class Simple(Sink):
    """
    """
    lower_name = "simple_sink"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.val = kwargs['val']
