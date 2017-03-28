import time

import pygame
from pygame.constants import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
)

from ..constants import (
    SOUTH,
    NORTH,
    WEST,
    EAST,
    SOUTH_INDEX,
    NORTH_INDEX,
    EAST_INDEX,
    WEST_INDEX,
)
from .. import internals
from ..internals import world
from .atom import Atom


class Mob(Atom):
    def __init__(self):
        self.dir = SOUTH
        self._dir_index = SOUTH_INDEX
        self._frame_no = 0
        self._last_time = time.time()
        self._time_diff = 0
        self.x, self.y = 0, 0
        self._moving = False
        self.pixel_x, self.pixel_y = 0, 0
        self.client = None

        self._screen_x, self._screen_y = 0, 0
        print 'trolo'

    def __login__(self):
        pass

    def __logout__(self):
        pass

    def moving(self):
        if self._moving:
            x, y = self.x, self.y
            step_size = 4
            to_screen_x = x * world.icon_size
            to_screen_y = (world.map.height - y) * world.icon_size
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

        world_map = world.map.fields

        x, y = self.x, self.y

        if internals.keyboard[K_UP]:
            self.dir = NORTH
            self._dir_index = NORTH_INDEX
            if True not in (obj.density for obj in world_map[y+1][x]):
                y += 1
        elif internals.keyboard[K_DOWN]:
            self.dir = SOUTH
            self._dir_index = SOUTH_INDEX
            if True not in (obj.density for obj in world_map[y - 1][x]):
                y -= 1
        elif internals.keyboard[K_LEFT]:
            self.dir = WEST
            self._dir_index = WEST_INDEX
            if True not in (obj.density for obj in world_map[y][x-1]):
                x -= 1
        elif internals.keyboard[K_RIGHT]:
            self.dir = EAST
            self._dir_index = EAST_INDEX
            if True not in (obj.density for obj in world_map[y][x + 1]):
                x += 1

        if (self.x, self.y) != (x, y):
            self.x, self.y = x, y
            self._moving = True
            print x/32, y/32 + 1, x, y
        else:
            self._moving = False

    def draw(self):
        animation_only_while_moving = self._icon_state.attr_movement
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
                self._frame_no %= self._icon_state.attr_frames
        else:
            self._frame_no = 0



        # time_diff_millis = int(round(time_diff * 1000))
        # print 'time_diff_millis', time_diff_millis

        if self.icon:
            icon_state = self._icon_state
            # screen.blit(icon_state.frames[self.dir][self._frame_no], (self.x, self.y))

            y = world.icon_size - self.y

            current_frame = icon_state.frames[self._dir_index][self._frame_no]
            rect = current_frame.get_rect()

            internals.screen.blit(
                pygame.transform.scale(current_frame, (64, 64)),
                (
                    self._screen_x+self.pixel_x,
                    self._screen_y+self.pixel_y-rect.height*2  # FIXME *2 chwilowo bo generalnie sprity powinny byc skalowane podczas tworzenia, a nie przy wyswietlaniu
                )
            )

            # screen.blit(pygame.transform.scale2x(icon_state.frames[0][0]), (0, 0))
            # screen.blit(pygame.transform.scale(icon_state.frames[0][0], (64, 64)), (0, 0))
