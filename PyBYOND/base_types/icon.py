from collections import OrderedDict
from PIL import Image

import pygame

from .icon_state import IconState
from PyBYOND import singletons as si


icon_key_types = {
    'width': int,
    'height': int,
    'state': str,
    'dirs': int,
    'frames': int,
    'delay': lambda delay: [int(x) for x in delay.split(',')],  # delay in 1/10s
    'loop': int,
}


class Icon:
    def scale(self, width, height):
        # self.image = pygame.transform.scale(self.image, (width, height))
        for name, icon_state in self.icon_states.items():
            for i, frames in enumerate(icon_state.frames):
                icon_state.frames[i] = [
                    pygame.transform.scale(frame, (width, height))
                    for frame in frames
                ]
        print('scale', width, height)

    def load_metadata(self, filename):
        image = Image.open(filename)
        desc = image.info.get('Description')
        print(image.info)
        print('desc', desc)
        image.close()

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
        return icon_states_data

    def load(self, filename):
        self.filename = filename
        self.image = pygame.image.load(filename)#.convert()  # z convertem niby szybciej ale niektore ikonki maja hujowe kolorki
        self.width, self.height = self.image.get_size()
        icon_states_data = self.load_metadata(filename)
        self.icon_states = OrderedDict()
        start_frame = 0
        for name, attrs in icon_states_data:
            attrs = dict(attrs)
            icon_state = IconState(self, start_frame, name, **dict(attrs))
            self.icon_states[name] = icon_state
            start_frame += icon_state.total_frames


    def __init__(self, filename):
        self.load(filename)


class IconDescriptor(object):
    def __set__(self, src, filename):
        # print 'src', src, 'filename', filename
        if filename not in si.icons:
            si.icons[filename] = Icon(filename)
        src._icon = si.icons[filename]
        src._icon_state = src._icon.icon_states.get(src.icon_state, '')

    def __get__(self, src, cls):
        # print 'src', src, 'cls', cls
        # if issubclass(cls, type):
        #     return self
        icon = src._icon
        if src._icon:
            icon = icon.filename
        return icon

