import sys
import ConfigParser
import time

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

from types.hidden.client import Client
from types.hidden.world import World
from types.hidden.world_map import WorldMap
from verb import verbs
import constants

spawned_functions = []


def spawn(seconds, method):
    spawned_functions.append([time.time() + seconds, method])


def get_step(ref, direction):
    return world.map.get_step(ref, direction)


def delete(atom):
    atom.__remove__()


client = Client()
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


FPS = 30
world_map = None
map_width = None
map_height = None


class PyBYOND(object):
    def run(self):
        print 'verbs', verbs.items()
        self._load_map()

        player = world.mob()
        player.client = client
        client.mob = player

        player.__login__()

        pygame.init()
        pygame.font.init()
        fpsClock = pygame.time.Clock()
        pygame.display.set_caption('PyBomberman')

        while True:
            now_time = time.time()
            for spawned_function in list(spawned_functions):
                run_time, function = spawned_function
                if function.__self__.deleted:
                    spawned_functions.remove(spawned_function)
                elif now_time >= run_time:
                    spawned_functions.remove(spawned_function)
                    function()

            player.moving()
            player.move()
            world.map.__draw__()

            player.draw()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    client.__keydown__(event.key)
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    keyboard[event.key] = True
                elif event.type == KEYUP:
                    keyboard[event.key] = False

            pygame.display.update()
            fpsClock.tick(FPS)

    def _load_map(self):
        global world
        world.map = WorldMap('map.ini')

pyBYOND = PyBYOND()

