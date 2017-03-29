import os
import time

import pygame

from .. import constants
from .. import internals
from ..internals import world

from .hidden.icon import IconDescriptor
from .hidden.icon_state import IconStateDescriptor
from .hidden.mappable_meta import MappableMeta
from .hidden.world_map import WorldMap


dir_to_dir_index_map = {
    constants.SOUTH: constants.SOUTH_INDEX,
    constants.NORTH: constants.NORTH_INDEX,
    constants.WEST: constants.WEST_INDEX,
    constants.EAST: constants.EAST_INDEX,
}


class Atom(object):
    __metaclass__ = MappableMeta
    _icon = ''
    _icon_state = ''
    icon = IconDescriptor()
    icon_state = IconStateDescriptor()
    x = 0
    y = 0
    density = False
    dir = constants.SOUTH
    pixel_x = 0
    pixel_y = 0

    _dir_index = constants.SOUTH_INDEX
    _frame_no = 0
    _time_diff = 0
    _deleted = False

    def __init__(self, x=None, y=None):
        self._last_time = time.time()
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self._screen_x = self.x * world.icon_size
        self._screen_y = (world.map.height - self.y) * world.icon_size
        world.map.fields[self.y][self.x].append(self)

    def __remove__(self):
        assert self in world.map.fields[self.y][self.x]
        world.map.fields[self.y][self.x].remove(self)
        self._deleted = True

    @property
    def loc(self):
        return world.map.locate(self.x, self.y)

    def draw(self):
        self._screen_x = self.x * world.icon_size
        self._screen_y = (world.map.height - self.y) * world.icon_size

        now_time = time.time()
        self._time_diff += int(round((now_time - self._last_time) * 1000))
        self._last_time = now_time

        if self._time_diff > 200:
            self._time_diff %= 100
            self._frame_no += 1
            self._frame_no %= self._icon_state.attr_frames

        if self.icon:
            icon_state = self._icon_state
            current_frame = icon_state.frames[self._dir_index][self._frame_no]
            rect = current_frame.get_rect()
            # screen.blit(icon_state.frames[self.dir][self._frame_no], (self.x, self.y))

            internals.screen.blit(
                pygame.transform.scale(
                    current_frame, (32, 32)
                ),
                (
                    self._screen_x,
                    self._screen_y-rect.height*2
                )
            )
