import os
import sys
import time

import pygame

from .. import constants
from .. import internals
from ..internals import world

from .hidden.icon import IconDescriptor
from .hidden.icon_state import IconStateDescriptor
from .hidden.mappable_meta import MappableMeta


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
    layer = 0
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

        self.dots = 1

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
        icon_state = self._icon_state
        frames_count = icon_state._frames_count
        if frames_count > 1:
            is_animation_on = True
            movement_animation = icon_state.attr_movement
            if movement_animation and not self._moving:
                is_animation_on = False

            if is_animation_on:
                now_time = world.time
                self._time_diff += now_time - self._last_time
                last_time_diff = self._time_diff
                self._last_time = now_time

                total_delay_in_seconds = icon_state.total_delay / 10.0
                current_delay_in_seconds = icon_state.delay[self._frame_no] / 10.0

                if self._time_diff > total_delay_in_seconds:
                    self._time_diff %= total_delay_in_seconds
                    print 'ROUGH'

                changed_frame = False
                while self._time_diff > current_delay_in_seconds:
                     current_delay_in_seconds = icon_state.delay[self._frame_no] / 10.0
                     self._time_diff -= current_delay_in_seconds
                     self._frame_no += 1
                     self._frame_no %= icon_state._frames_count
                     changed_frame = True
                if movement_animation and changed_frame:
                     print 'frame: {}, time_diff: {}, world.time: {}, delay_in_sec: {}, total_delay_in_sec: {}'.format(self._frame_no, last_time_diff, now_time, current_delay_in_seconds, total_delay_in_seconds)
            else:
                self._frame_no = 0
                self._last_time = world.time

                if movement_animation:
                    sys.stdout.write('\r' + ((self.dots / 100) + 1) * '.')
                    self.dots += 1
                    if self.dots >= 300:
                        self.dots = 1


    def render(self):
        if self.icon:
            current_frame = self._icon_state.frames[self._dir_index][self._frame_no]
            rect = current_frame.get_rect()

            internals.screen.blit(
                current_frame,
                (
                    self._screen_x + self.pixel_x,
                    self._screen_y + self.pixel_y - rect.height
                )
            )
