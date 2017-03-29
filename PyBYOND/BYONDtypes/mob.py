import time

import pygame
from .. import internals
from ..internals import world
from .hidden.movable import Movable


class Mob(Movable):
    client = None

    def __login__(self):    # Login vs __login__
        pass

    def __logout__(self):
        pass

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

        # self._screen_x = self.x * world.icon_size
        # self._screen_y = (world.map.height - self.y) * world.icon_size

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
