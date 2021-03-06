import logging
import sys
import time

from .icon_state import IconStateDescriptor
from .mappable_meta import MappableMeta

from PyBYOND import constants
from PyBYOND.base_types.icon import IconDescriptor
from PyBYOND import singletons as si

DIR_TO_DIR_INDEX_MAP = {
    constants.SOUTH: constants.SOUTH_INDEX,
    constants.NORTH: constants.NORTH_INDEX,
    constants.WEST: constants.WEST_INDEX,
    constants.EAST: constants.EAST_INDEX,
}


class Atom(metaclass=MappableMeta):
    _icon = ''
    _icon_state = ''
    icon = IconDescriptor()
    icon_state = IconStateDescriptor()
    x = 0
    y = 0
    z = 0
    density = False

    layer = 0
    pixel_x = 0
    pixel_y = 0

    _dir = constants.SOUTH
    _dir_index = constants.SOUTH_INDEX
    _frame_no = 0
    _loop_no = 0  # how many loops animation has done
    _time_diff = 0
    _deleted = False

    _is_gliding = False  # atoms cannot move but need this object for icon with movable states

    def __repr__(self):
        return 'the {}'.format(self.__class__.__name__.lower())

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, direction):
        self._dir = direction
        self._dir_index = DIR_TO_DIR_INDEX_MAP[direction]

    def __init__(self, x=None, y=None):
        self.name = self.__class__.__name__.lower()
        self._last_time = time.time()
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self._screen_x = self.x * si.world.icon_size
        self._screen_y = (si.world.map.height - self.y) * si.world.icon_size
        si.world.map.fields[self.y][self.x].append(self)

        self.dots = 1

    def __remove__(self):
        if self not in si.world.map.fields[self.y][self.x]:
            logging.info(self, self.x, self.y, si.world.map.fields[self.y][self.x])
        assert self in si.world.map.fields[self.y][self.x]
        si.world.map.fields[self.y][self.x].remove(self)
        self._deleted = True
        if self in si.walking:
            del si.walking[self]

    @property
    def loc(self):
        from PyBYOND import base_types  # FIXME circular import
        return base_types.Location(self.x, self.y, self.z)

    def draw(self):
        if self.icon:
            self.animate()
            self.render()

    def animate(self):
        icon_state = self._icon_state
        try:
            frames_count = icon_state._frames_count
        except AttributeError:
            raise

        # animate_more = icon_state.attr_loop == constants.INFINITE or self._loop_no < icon_state.attr_loop

        if frames_count > 1:
            is_animation_on = True
            movement_animation = icon_state.attr_movement
            if movement_animation and not self._is_gliding:
                is_animation_on = False
            if is_animation_on:
                if icon_state.attr_loop != constants.INFINITE and self._loop_no >= icon_state.attr_loop:
                    return
                now_time = si.world.time
                self._time_diff += now_time - self._last_time
                last_time_diff = self._time_diff
                self._last_time = now_time

                total_delay_in_seconds = icon_state.total_delay / 10.0
                current_delay_in_seconds = icon_state.delay[self._frame_no] / 10.0

                if self._time_diff > total_delay_in_seconds:
                    self._time_diff %= total_delay_in_seconds
                    self._loop_no += 1
                    logging.info('ROUGH')

                changed_frame = False
                while self._time_diff > current_delay_in_seconds:
                     current_delay_in_seconds = icon_state.delay[self._frame_no] / 10.0
                     self._time_diff -= current_delay_in_seconds
                     self._frame_no += 1
                     self._frame_no %= icon_state._frames_count
                     changed_frame = True
                     if self._frame_no == (icon_state._frames_count - 1):
                         self._loop_no += 1

                if movement_animation and changed_frame:
                     logging.info('frame: {}, time_diff: {}, si.world.time: {}, delay_in_sec: {}, total_delay_in_sec: {}'.format(self._frame_no, last_time_diff, now_time, current_delay_in_seconds, total_delay_in_seconds))
            else:
                if movement_animation:
                    self._loop_no = 0
                    self._frame_no = 0
                    self._last_time = si.world.time
                    sys.stdout.write('\r' + ((self.dots // 100) + 1) * '.')
                    self.dots += 1
                    if self.dots >= 300:
                        self.dots = 1


    def render(self):
        if self.icon:

            dir_index = self._dir_index if self._dir_index < self._icon_state.attr_dirs else 0
            current_frame = self._icon_state.frames[dir_index][self._frame_no]
            rect = current_frame.get_rect()

            if self.name == "bomb":
                logging.info(current_frame,  self._screen_x + self.pixel_x, self._screen_y + self.pixel_y - rect.height)


            eye = si.client.eye
            # view = si.client.view or si.world.view
            # if isinstance(view, int):
            #     view_width = view_height = 1 + (view * 2)
            # elif isinstance(view, str):
            #     view_width, view_height = view.split('x')
            #     view_width = int(view_width)
            #     view_height = int(view_height)
            #
            # viewport_width = view_width * si.world.icon_size
            # viewport_height = view_height * si.world.icon_size

            # eye._screen_x, eye._screen_y
            # viewport_width//2
            # viewport_height//2

            si.screen.blit(
                current_frame,
                (
                    self._screen_x - eye._screen_x + 208 + self.pixel_x,
                    self._screen_y - eye._screen_y + 208 + self.pixel_y - rect.height
                )
            )

    def Enter(self, movable, old_location):
        logging.info(self, "__Enter__")
        return True

    def Entered(self, movable, old_location):
        logging.info(self, "__Entered__")
        return True

    def Exit(self, movable, new_location):
        logging.info(self, "__Exit__")
        return True

    def Exited(self, movable, new_location):
        logging.info(self, "__Exited__")
        return True
