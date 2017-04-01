from ..atom import Atom
from pygame.constants import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
)

from ...constants import (
    SOUTH,
    NORTH,
    WEST,
    EAST,
    SOUTH_INDEX,
    NORTH_INDEX,
    EAST_INDEX,
    WEST_INDEX,
)
from ...internals import world
from ... import internals


class Movable(Atom):
    _moving = False

    def moving(self):
        if self._moving:
            x, y = self.x, self.y
            pixel_step_size = 4
            to_screen_x = x * world.icon_size
            to_screen_y = (world.map.height - y) * world.icon_size
            if self._screen_x < to_screen_x:
                self._screen_x += pixel_step_size
            elif self._screen_x > to_screen_x:
                self._screen_x -= pixel_step_size

            if self._screen_y < to_screen_y:
                self._screen_y += pixel_step_size
            elif self._screen_y > to_screen_y:
                self._screen_y -= pixel_step_size

            if self._screen_x == to_screen_x and self._screen_y == to_screen_y:
                self._moving = False

    def movement(self):
        if self._moving:
            return

        key_up = internals.keyboard[K_UP]
        key_down = internals.keyboard[K_DOWN]
        key_right = internals.keyboard[K_RIGHT]
        key_left = internals.keyboard[K_LEFT]

        if key_up and not key_down:
            direction = NORTH
            location = internals.get_step(ref=self, direction=direction)
            if True not in (obj.density for obj in location):
                self.move(location=location, direction=direction)

        elif key_down and not key_up:
            direction = SOUTH
            location = internals.get_step(ref=self, direction=direction)
            if True not in (obj.density for obj in location):
                self.move(location=location, direction=direction)

        elif key_left and not key_right:
            direction = WEST
            location = internals.get_step(ref=self, direction=direction)
            if True not in (obj.density for obj in location):
                self.move(location=location, direction=direction)

        elif key_right and not key_left:
            direction = EAST
            location = internals.get_step(ref=self, direction=direction)
            if True not in (obj.density for obj in location):
                self.move(location=location, direction=direction)

    def move(self, location, direction):
        self.dir = direction
        world_map = world.map.fields
        world_map[self.y][self.x].remove(self)
        self.x, self.y = location.x, location.y
        world_map[self.y][self.x].append(self)
        self._moving = True

