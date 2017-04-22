import configparser
from ... import constants


world = None


class Location:
    def __init__(self, x, y):
        from ..turf import Turf  # FIXME, tutaj przez circual import
        from ..area import Area
        self.x, self.y = x, y
        self.cell = world.map.fields[y][x]
        self.turfs = []
        self.areas = []
        self.areas_classes = []
        for atom in self.cell:
            if isinstance(atom, Turf):
                self.turfs.append(atom)
            elif isinstance(atom, Area):
                self.areas.append(atom)
                self.areas_classes.append(atom.__class__)

    def __repr__(self):
        from ..turf import Turf  #FIXME, tutaj przez circual import
        return '{} ({}, {})'.format([
            atom for atom
            in self.cell
            if isinstance(atom, Turf)
        ][0].__class__.__name__, self.x, self.y)

    def __iter__(self):
        """
        :return: iterator to copy of self.cell
        so it is safe to remove elements
        from map while iterating
        """
        return iter(list(self.cell))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def Exit(self, movable, new_location):
        for turf in self.turfs:
            if not turf.Exit(movable, new_location):
                return False

        for area in self.areas:
            if area.__class__ not in new_location.areas_classes:
                # print 'area.__class__ ({}) VS new_location.areas_classes ({})'.format(area.__class__, new_location.areas_classes)
                if not area.Exit(movable, new_location):
                    return False

        return True

    def Enter(self, movable, old_location):
        result = True
        for turf in self.turfs:
            if not turf.Enter(movable, old_location):
                result = False

        for area in self.areas:
            if area.__class__ not in old_location.areas_classes:
                # print 'area.__class__ ({}) VS old_location.areas_classes ({})'.format(area.__class__, old_location.areas_classes)
                if not area.Enter(movable, old_location):
                    result = False

        return result

    def Exited(self, movable, new_location):
        for turf in self.turfs:
            turf.Exited(movable, new_location)

        for area in self.areas:
            if area.__class__ not in new_location.areas_classes:
                area.Exited(movable, new_location)


    def Entered(self, movable, old_location):
        for turf in self.turfs:
            turf.Entered(movable, old_location)

        for area in self.areas:
            if area.__class__ not in old_location.areas_classes:
                area.Entered(movable, old_location)


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

    def get_step(self, ref, direction, steps):
        x, y = ref.x, ref.y
        if direction == constants.NORTH:
            y += steps
        elif direction == constants.SOUTH:
            y -= steps
        elif direction == constants.WEST:
            x -= steps
        elif direction == constants.EAST:
            x += steps
        return Location(x, y)

    def locate(self, x, y, z=1):  # probably should also give possibility to pass class Turf argument here, z
        return Location(x, y)