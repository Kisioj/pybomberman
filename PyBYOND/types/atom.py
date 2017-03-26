import os
import time

import pygame

from .. import constants
from .. import internals

from .hidden.icon import IconDescriptor
from .hidden.icon_state import IconStateDescriptor
from .hidden.mappable import MappableMeta

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
    def __init__(self, **kwargs):
        dct = dict(self.__class__.__dict__)
        dct.update(self.__dict__)

        self.name = kwargs.get('name', dct.get('name'))
        self.icon = kwargs.get('icon', self.icon)
        self.icon_state = kwargs.get('icon_state', self.icon_state)
        self.density = kwargs.get('density', dct.get('density', False))
        self.dir = kwargs.get('dir', dct.get('dir')) or constants.SOUTH
        self._dir_index = dir_to_dir_index_map[self.dir]
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
            self._frame_no %= self._icon_state.attr_frames

        if self.icon:
            icon_state = self._icon_state
            # screen.blit(icon_state.frames[self.dir][self._frame_no], (self.x, self.y))

            internals.screen.blit(
                pygame.transform.scale(
                    icon_state.frames[self._dir_index][self._frame_no], (32, 32)
                ),
                (self.x, self.y)
            )

    @classmethod
    def create(cls, **kwargs):
        name = kwargs.get('name')
        if not name:
            raise AttributeError('name attribute cannot be empty')
        elif name in internals.mappable_types:
            raise AttributeError("'{}' mappable type is already registered".format(name))

        icon = kwargs.get('icon', cls.icon)
        if not icon:
            raise AttributeError('icon attribute cannot be empty')
        elif not os.path.isfile(icon):
            raise AttributeError("Could not find file: '{}'".format(icon))

        attributes = {
            'name': name,
            'icon': icon,
            'icon_state': kwargs.get('icon_state', name),
            'density': kwargs.get('density'),
            'dir': kwargs.get('dir'),
        }
        internals.mappable_types[name] = cls, attributes
