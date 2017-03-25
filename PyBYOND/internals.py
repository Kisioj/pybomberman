import sys
import ConfigParser

import pygame
from pygame.constants import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    QUIT,
    KEYDOWN,
    KEYUP,
    K_ESCAPE,
)

from types.hidden.world import World

world = World()
SCREEN_WIDTH, SCREEN_HEIGHT = 400*2, 368*2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
keyboard = {
    K_LEFT: False,
    K_RIGHT: False,
    K_UP: False,
    K_DOWN: False
}

icon_key_types = {
    'width': int,
    'height': int,
    'state': str,
    'dirs': int,
    'frames': int,
    'delay': lambda delay: map(int, delay.split(',')),
    'loop': bool,
}

map_object_attribute_types = {
    'density': lambda density: density == 'True'
}

icons = {}
mappable_types = {}

FPS = 30
tile_width, tile_height = 32, 32

world_map = None
map_width = None
map_height = None

class PyBYOND(object):
    def run(self):
        self._load_map()

        player = world.mob()
        player.__login__()

        pygame.init()
        pygame.font.init()
        fpsClock = pygame.time.Clock()
        pygame.display.set_caption('PyBomberman')

        while True:
            player.moving()
            player.move()
            for y in xrange(map_height):
                for x in xrange(map_width):
                    for atom in world_map[y][x]:
                        atom.draw()

            player.draw()
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    keyboard[event.key] = True
                elif event.type == KEYUP:
                    keyboard[event.key] = False

            pygame.display.update()
            fpsClock.tick(FPS)

    def _get_atom_data(self, atom_type):
        result = dict(self.fields_data[atom_type])
        for key, value in result.iteritems():
            # key, value = line.split(' = ')
            key_type = map_object_attribute_types.get(key)
            if key_type:
                result[key] = key_type(value)
        return result

    def _load_map(self):
        global world_map, map_width, map_height
        config = ConfigParser.ConfigParser()
        config.read('map.ini')
        raw_map = config.get('level', 'map').split('\n')
        map_width, map_height = len(raw_map[0]), len(raw_map)

        self.fields_data = {}
        world_map = []
        for y in xrange(map_height):
            row = []
            world_map.append(row)
            for x in xrange(map_width):
                cell = []
                row.append(cell)

                symbol = raw_map[y][x]
                cell_conent = config.get('level', symbol)
                if ', ' in cell_conent:
                    cell_conent = cell_conent.split(', ')
                else:
                    cell_conent = [cell_conent]

                for atom_type in cell_conent:
                    if atom_type not in self.fields_data:
                        attrs = {}
                        for attr in config.options(atom_type):
                            attrs[attr] = config.get(atom_type, attr)
                            self.fields_data[atom_type] = attrs

                    atom_data = self._get_atom_data(atom_type)
                    atom_class = mappable_types[atom_data.pop('type')]
                    atom = atom_class(**atom_data)
                    atom.x, atom.y = x*32, y*32
                    cell.append(atom)
                    # print atom_data

                # print cell_conent

        # print self.fields_data
        # print 'map_width, map_height', map_width, map_height
        map_width, map_height = len(world_map[0]), len(world_map)


pyBYOND = PyBYOND()

# map_tiles = load_tiles('resources/map.png', 16, 16)
# print len(map_tiles), map_tiles


# icon = Icon('resources/player.png')
# print icon.icon_states
# im2 = Image.open('resources/map.png')
# print 'info', im2.info  # http://blog.client9.com/2007/08/28/python-pil-and-png-metadata-take-2.html



