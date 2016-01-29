from . import Sink


class Simple(Sink):
    """A simple sink. Use this if you do not know which sink to use."""
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.val = kwargs.get('val', None)
