from PyBYOND import singletons as si
from PyBYOND import base_types


class World:
    def __init__(self):
        self.mob = None # base_types.Mob()  # Mob
        self.icon_size = 32  #  TODO mozliwosc dodania "32x32"
        self.maps = []  # moze byc wiecej map
        self.map = None


# si.world = World()
