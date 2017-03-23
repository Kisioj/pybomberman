import pygame
from pygame.constants import (
    QUIT,
    KEYDOWN,
    KEYUP,
    K_ESCAPE,
)
import sys
from core import Icon, Mob, screen, FPS, keyboard, Turf, Object
import ConfigParser
from collections import OrderedDict


class Box(Object):
    def __init__(self, *args, **kwargs):
        super(Box, self).__init__(*args, **kwargs)


mappable_types = {
    'Turf': Turf,
    'Object': Object,
    'Mob': Mob,
    'Box': Box,
}

def make_map():
    config = ConfigParser.ConfigParser()
    config.read('map.ini')
    raw_map = config.get('level', 'map').split('\n')
    map_width, map_height = len(raw_map[0]), len(raw_map)

    fields_data = {}
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
                if atom_type not in fields_data:
                    attrs = {}
                    for attr in config.options(atom_type):
                        attrs[attr] = config.get(atom_type, attr)
                    fields_data[atom_type] = attrs

                atom_data = dict(fields_data[atom_type])
                atom_class = mappable_types[atom_data.pop('type')]
                atom = atom_class(**atom_data)
                atom.x, atom.y = x*32, y*32
                cell.append(atom)
                # print atom_data

            # print cell_conent

    # print fields_data
    # print 'map_width, map_height', map_width, map_height
    return world_map

world_map = make_map()
map_width, map_height = len(world_map[0]), len(world_map)
print map_width, map_height, world_map

pygame.init()
pygame.font.init()
fpsClock = pygame.time.Clock()
pygame.display.set_caption('PyBomberman')


# map_tiles = load_tiles('resources/map.png', 16, 16)
# print len(map_tiles), map_tiles


# icon = Icon('resources/player.png')
# print icon.icon_states
# im2 = Image.open('resources/map.png')
# print 'info', im2.info  # http://blog.client9.com/2007/08/28/python-pil-and-png-metadata-take-2.html

class Player(Mob):
    def __init__(self):
        super(Player, self).__init__()
        self.icon = 'resources/player.png'
        self.icon_state = ''
        self.x, self.y = 3, 2
        self.pixel_x = -16


player = Player()
print player.icon
print player.icon_state



while True:
    player.move()
    player.moving()
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