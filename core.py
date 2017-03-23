import pygame
from collections import OrderedDict
from PIL import Image
import time
from pygame.constants import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
)

tile_width = 32
tile_height = 32
map_height = 23

SCREEN_WIDTH, SCREEN_HEIGHT = 400*2, 368*2
FPS = 30
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

icons = {

}

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

        if state:
            icon_states_data.append((state, values))

        self.icon_states = OrderedDict()
        start_frame = 0
        for name, attrs in icon_states_data:
            attrs = dict(attrs)
            icon_state = IconState(self, start_frame, name, **dict(attrs))
            self.icon_states[name] = icon_state
            start_frame += icon_state.total_frames

        # print icon_states_data


class IconState(object):
    def __init__(self, icon, start_frame, name, **kwargs):
        self.width = icon.tile_width
        self.height = icon.tile_height
        self.name = name

        self.attr_frames = kwargs.get('frames', 1)
        self.attr_dirs = kwargs.get('dirs', 1)
        self.attr_loop = kwargs.get('loop', False)
        self.attr_delay = kwargs.get('delay')
        self.attr_movement = kwargs.get('movement', False)
        self.total_frames = self.attr_dirs * self.attr_frames

        frames_to_start = start_frame
        frames_left = self.total_frames
        frames = []
        for tile_y in xrange(0, icon.height / self.height):
            for tile_x in xrange(0, icon.width / self.width):
                if frames_to_start == 0:
                    if frames_left > 0:
                        frames_left -= 1
                        rect = (tile_x * self.width, tile_y * self.height, self.width, self.height)
                        frames.append(icon.image.subsurface(rect))
                else:
                    frames_to_start -= 1

        self.frames = [[] for _ in xrange(self.attr_dirs)]
        for i, frame in enumerate(frames):
            idx = i % self.attr_dirs
            self.frames[idx].append(frame)

        # print name, kwargs


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


class IconStateDescriptor(object):
    def __set__(self, src, state_name):
        # print 'src', src, 'state_name', state_name

        icon = src.__dict__.get('icon')
        if icon:
            src.__dict__['icon_state'] = icon.icon_states[state_name]
        else:
            src.__dict__['icon_state'] = state_name

    def __get__(self, src, cls):
        # print 'src', src, 'cls', cls

        icon = src.__dict__.get('icon')
        icon_state = src.__dict__.get('icon_state', '')
        if icon and icon_state:
            icon_state = icon_state.name
        return icon_state


SOUTH = 0
NORTH = 1
EAST = 2
WEST = 3

# http://qq.readthedocs.io/en/latest/player.html
class Atom(object):
    icon = IconDescriptor()
    icon_state = IconStateDescriptor()
    x = 0
    y = 0
    def __init__(self):
        self.dir = SOUTH
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
                    icon_state.frames[self.dir][self._frame_no], (32, 32)
                ),
                (self.x, self.y)
            )


class Turf(Atom):
    def __init__(self, icon, icon_state, density=False):
        super(Turf, self).__init__()
        self.icon = icon
        self.icon_state = icon_state
        self.density = density


class Object(Atom):
    def __init__(self, icon, icon_state, density=False):
        super(Object, self).__init__()
        self.icon = icon
        self.icon_state = icon_state
        self.density = density


class Mob(Atom):
    def __init__(self):
        self.dir = SOUTH
        self._frame_no = 0
        self._last_time = time.time()
        self._time_diff = 0
        self.x, self.y = 0, 0
        self._moving = False
        self.pixel_x, self.pixel_y = 0, 0

        self._screen_x, self._screen_y = 0, 0
        print 'trolo'

    def moving(self):
        if self._moving:
            x, y = self.x, self.y
            step_size = 4
            to_screen_x = x * tile_width
            to_screen_y = (map_height - y) * tile_width
            if self._screen_x < to_screen_x:
                self._screen_x += step_size
            elif self._screen_x > to_screen_x:
                self._screen_x -= step_size

            if self._screen_y < to_screen_y:
                self._screen_y += step_size
            elif self._screen_y > to_screen_y:
                self._screen_y -= step_size

            if self._screen_x == to_screen_x and self._screen_y == to_screen_y:
                self._moving = False

    def move(self):
        if self._moving:
            return

        x, y = self.x, self.y

        if keyboard[K_UP]:
            self.dir = NORTH
            y += 1
        elif keyboard[K_DOWN]:
            self.dir = SOUTH
            y -= 1
        elif keyboard[K_LEFT]:
            self.dir = WEST
            x -= 1
        elif keyboard[K_RIGHT]:
            self.dir = EAST
            x += 1

        if (self.x, self.y) != (x, y):
            self.x, self.y = x, y
            self._moving = True
            print x/32, y/32 + 1, x, y
        else:
            self._moving = False

    def draw(self):
        animation_only_while_moving = self.__dict__['icon_state'].attr_movement
        should_progress_animation = True
        if animation_only_while_moving and not self._moving:
            should_progress_animation = False

        now_time = time.time()
        if should_progress_animation:
            self._time_diff += int(round((now_time - self._last_time) * 1000))
        self._last_time = now_time

        if should_progress_animation:
            if self._time_diff > 200:
                self._time_diff %= 100
                self._frame_no += 1
                self._frame_no %= self.__dict__['icon_state'].attr_frames
        else:
            self._frame_no = 0



        # time_diff_millis = int(round(time_diff * 1000))
        # print 'time_diff_millis', time_diff_millis

        if self.__dict__.get('icon'):
            icon_state = self.__dict__['icon_state']
            # screen.blit(icon_state.frames[self.dir][self._frame_no], (self.x, self.y))


            y = map_height - self.y

            current_frame = icon_state.frames[self.dir][self._frame_no]
            rect = current_frame.get_rect()

            screen.blit(
                pygame.transform.scale(current_frame, (64, 64)),
                (
                    self.x*tile_width+self.pixel_x,
                    y*tile_height+self.pixel_y-rect.height*2  # FIXME *2 chwilowo bo generalnie sprity powinny byc skalowane podczas tworzenia, a nie przy wyswietlaniu
                )
            )

            # screen.blit(pygame.transform.scale2x(icon_state.frames[0][0]), (0, 0))
            # screen.blit(pygame.transform.scale(icon_state.frames[0][0], (64, 64)), (0, 0))




# def load_tiles(filename, width, height):
#     image = pygame.image.load('resources/map.png')
#     image_width, image_height = image.get_size()
#     tiles = []
#     for tile_x in range(0, image_width/width):
#         for tile_y in range(0, image_height/height):
#             rect = (tile_x*width, tile_y*height, width, height)
#             tiles.append(image.subsurface(rect))
#     return tiles