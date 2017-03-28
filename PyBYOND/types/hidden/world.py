# from ..mob import Mob


class World(object):
    def __init__(self):
        self.mob = None  # Mob
        self.icon_size = 32  #  TODO mozliwosc dodania "32x32"
        self.maps = []  # moze byc wiecej map
        self.map = None


