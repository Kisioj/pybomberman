from .hidden.movable import Movable
from ..constants import MOB_LAYER


class Mob(Movable):
    client = None
    layer = MOB_LAYER

    def __login__(self):    # Login vs __login__
        pass

    def __logout__(self):
        pass
