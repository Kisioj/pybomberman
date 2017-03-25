from collections import OrderedDict
from PIL import Image

import pygame

from ...internals import (
    icon_key_types,
    icons,
)

from .icon_state import IconState


class Icon(object):
    def __init__(self, filename):
        self.filename = filename

        self.image = pygame.image.load(filename).convert()
        self.width, self.height = self.image.get_size()

        image = Image.open(filename)
        desc = image.info.get('Description')
        image.close()
        # print desc

        icon_states_data = []
        state = None
        values = []
        for line in desc.split('\n')[2:-2]:
            if line.startswith('\t'):
                line = line.lstrip('\t')
                key, value = line.split(' = ')
                key_type = icon_key_types.get(key)
                if key_type:
                    value = key_type(value)

                if key == 'width':
                    self.tile_width = value
                elif key == 'height':
                    self.tile_height = value
                elif state is not None:
                    values.append((key, value))

            else:
                key, value = line.split(' = ')
                if key == 'state':
                    value = value.strip('"')
                if state is not None:
                    icon_states_data.append((state, values))
                state = value
                values = []

        if state is not None:
            icon_states_data.append((state, values))

        self.icon_states = OrderedDict()
        start_frame = 0
        for name, attrs in icon_states_data:
            attrs = dict(attrs)
            icon_state = IconState(self, start_frame, name, **dict(attrs))
            self.icon_states[name] = icon_state
            start_frame += icon_state.total_frames

        # print icon_states_data


class IconDescriptor(object):
    def __set__(self, src, filename):
        # print 'src', src, 'filename', filename
        src.__dict__['icon'] = icons.setdefault(filename, Icon(filename))
        src.__dict__['icon_state'] = src.__dict__['icon'].icon_states.get(src.icon_state, '')

    def __get__(self, src, cls):
        # print 'src', src, 'cls', cls
        icon = src.__dict__.get('icon')
        if icon:
            icon = icon.filename
        return icon
