import time

import pygame

from ..constants import SOUTH, SOUTH_INDEX
from ..internals import screen

from .hidden.icon import IconDescriptor
from .hidden.icon_state import IconStateDescriptor
from .hidden.mappable import Mappable


class Atom(object):
    __metaclass__ = Mappable
    icon = IconDescriptor()
    icon_state = IconStateDescriptor()
    x = 0
    y = 0
    def __init__(self):
        self.dir = SOUTH
        self._dir_index = SOUTH_INDEX
        self._frame_no = 0
        self._last_time = time.time()
        self._time_diff = 0
        self.x, self.y = 0, 0

    def draw(self):
        now_time = time.time()
        self._time_diff += int(round((now_time - self._last_time) * 1000))
        self._last_time = now_time

        if self._time_diff > 200:
            self._time_diff %= 100
            self._frame_no += 1
            self._frame_no %= self.__dict__['icon_state'].attr_frames

        if self.__dict__.get('icon'):
            icon_state = self.__dict__['icon_state']
            # screen.blit(icon_state.frames[self.dir][self._frame_no], (self.x, self.y))

            screen.blit(
                pygame.transform.scale(
                    icon_state.frames[self._dir_index][self._frame_no], (32, 32)
                ),
                (self.x, self.y)
            )