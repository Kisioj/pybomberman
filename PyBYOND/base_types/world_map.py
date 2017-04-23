import configparser

from PyBYOND import constants
from PyBYOND import singletons as si
from .location import Location




class MappableTypesRegister:
    types = {}

    def __getitem__(self, type_name):
        return self.types[type_name]

    def __getattr__(self, type_name):
        return self.__getitem__(type_name)

    def add(self, cls):
        MappableTypesRegister.types[cls.__name__] = cls

    def __iter__(self):
        return self.types.keys()


class WorldMap:
    types = MappableTypesRegister()

    def __init__(self, world, filename):
        world.map = self
        config = configparser.ConfigParser()
        config.read(filename)
        raw_map = config.get('level', 'map').split('\n')
        self.width, self.height = len(raw_map[0]), len(raw_map)

        self.fields = [[[] for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                cell = self.fields[y][x]

                symbol = raw_map[self.height - y - 1][x]
                cell_conent = config.get('level', symbol)
                if ', ' in cell_conent:
                    cell_conent = cell_conent.split(', ')
                else:
                    cell_conent = [cell_conent]

                for atom_type in cell_conent:
                    WorldMap.types[atom_type](x=x, y=y)

    def __draw__(self):
        for y in range(self.height):
            for x in range(self.width):
                for atom in sorted(self.fields[y][x], key=lambda atom: atom.layer):
                    atom.draw()

    # def locate(self, x, y, z=1):  # probably should also give possibility to pass class Turf argument here, z
    #     return Location(x, y)