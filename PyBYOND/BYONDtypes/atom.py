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

    _moving = False  # atoms cannot move but need this object for icon with movable states

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
        if self not in world.map.fields[self.y][self.x]:
            print self, self.x, self.y, world.map.fields[self.y][self.x]
        assert self in world.map.fields[self.y][self.x]
        world.map.fields[self.y][self.x].remove(self)
        self._deleted = True

    @property
    def loc(self):
        return world.map.locate(self.x, self.y)

    def draw(self):
        self.animate()
        self.render()

    def animate(self):
        frames_count = self._icon_state._frames_count
        if frames_count > 1:
            is_animation_on = True
            movement_animation = self._icon_state.attr_movement
            if movement_animation and not self._moving:
                is_animation_on = False

            if is_animation_on:
                now_time = world.time
                self._time_diff += int(round((now_time - self._last_time) * 1000))
                self._last_time = now_time
                if self._time_diff > 200:
                    self._time_diff %= 100
                    self._frame_no += 1
                    self._frame_no %= self._icon_state._frames_count
            else:
                self._frame_no = 0

    def render(self):
        if self.icon:
            icon_state = self._icon_state
            current_frame = icon_state.frames[self._dir_index][self._frame_no]
            rect = current_frame.get_rect()

            internals.screen.blit(
                current_frame,
                (
                    self._screen_x + self.pixel_x,
                    self._screen_y + self.pixel_y - rect.height
                )
            )
