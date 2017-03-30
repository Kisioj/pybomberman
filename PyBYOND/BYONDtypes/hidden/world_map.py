import ConfigParser
from ... import constants


# class Location(object):
#     def __init__(self, x, y):
#         self.x, self.y = x, y
#         self.cell = world.map.fields[y][x]
#
#     def __repr__(self):
#         return [
#             atom for atom
#             in self.map_cell
#             if isinstance(atom, Turf)
#         ][0]
#
#     def __iter__(self):
#         return [] # powinnismy zwrocic moby i obiekty


class MappableTypesRegister(object):
    types = {}

    def __getitem__(self, type_name):
        return self.types[type_name]

    def __getattr__(self, type_name):
        return self.__getitem__(type_name)

    def add(self, cls):
        MappableTypesRegister.types[cls.__name__] = cls

    def __iter__(self):
        return self.types.iterkeys()


class WorldMap(object):
    types = MappableTypesRegister()

    def __init__(self, world, filename):
        world.map = self
        config = ConfigParser.ConfigParser()
        config.read(filename)
        raw_map = config.get('level', 'map').split('\n')
        self.width, self.height = len(raw_map[0]), len(raw_map)

        self.fields = [[[] for _ in xrange(self.width)] for _ in xrange(self.height)]
        for y in xrange(self.height):
            for x in xrange(self.width):
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
        for y in xrange(self.height):
            for x in xrange(self.width):
                for atom in self.fields[y][x]:
                    atom.draw()

    def get_step(self, ref, direction):
        x, y = ref.x, ref.y
        result = None
        if direction == constants.NORTH:
            result = self.fields[y + 1][x]
        elif direction == constants.SOUTH:
            result = self.fields[y - 1][x]
        elif direction == constants.WEST:
            result = self.fields[y][x - 1]
        elif direction == constants.EAST:
            result = self.fields[y][x + 1]
        return list(result)

    def locate(self, x, y, z=1):  # probably should also give possibility to pass class Turf argument here, z
        return self.fields[y][x]