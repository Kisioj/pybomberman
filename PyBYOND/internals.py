import sys
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
from .base_types import world_map
from .base_types.client import Client
from .base_types.world import World
from . import singletons as si

from PyBYOND import api
from .verb import verbs


# si.client = Client()
# si.world = World()
# world_map.world = world
SCREEN_WIDTH, SCREEN_HEIGHT = 400*2, 368*2
si.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
si.keyboard = {
    K_LEFT: False,
    K_RIGHT: False,
    K_UP: False,
    K_DOWN: False
}


map_object_attribute_types = {
    'density': lambda density: density == 'True'
}
BYONDtypes = world_map.WorldMap.types


FPS = 30


import types

si.world = World()
si.client = Client()


class PyBYOND(object):
    def run(self):
        def spawned_function_time(spawned_function):
            run_time, function = spawned_function
            return run_time

        print('verbs', verbs.items())
        world_map.WorldMap(si.world, 'map.ini')

        player = si.world.mob()
        player.client = si.client
        si.client.mob = player

        player.__login__()

        pygame.init()
        pygame.font.init()
        fpsClock = pygame.time.Clock()
        pygame.display.set_caption('PyBomberman')

        while True:
            now_time = time.time()
            si.world.time = now_time
            for spawned_function in sorted(si.functions_queue, key=spawned_function_time):
                run_time, function = spawned_function

                if hasattr(function, '__self__') and function.__self__._deleted:
                    si.functions_queue.remove(spawned_function)
                elif now_time >= run_time:
                    si.functions_queue.remove(spawned_function)
                    if isinstance(function, types.GeneratorType):
                        try:
                            next(function)
                        except StopIteration:
                            pass
                    else:
                        function()
                else:
                    break

            player.moving()
            player.movement()
            si.world.map.__draw__()

            player.draw()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    si.client.__keydown__(event.key)
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    si.keyboard[event.key] = True
                elif event.type == KEYUP:
                    si.keyboard[event.key] = False

            pygame.display.update()
            fpsClock.tick(FPS)

pyBYOND = PyBYOND()

