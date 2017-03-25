from .atom import Atom

class Turf(Atom):
    def __init__(self, icon, icon_state, density=False):
        super(Turf, self).__init__()
        self.icon = icon
        self.icon_state = icon_state
        self.density = density