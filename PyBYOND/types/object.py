from .atom import Atom

class Object(Atom):
    def __init__(self, icon, icon_state='', density=False):
        super(Object, self).__init__()
        self.icon = icon
        self.icon_state = icon_state
        self.density = density
