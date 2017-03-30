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

    def move(self):
        if self._moving:
            return

        world_map = world.map.fields

        x, y = self.x, self.y

        if internals.keyboard[K_UP]:
            self.dir = NORTH
            self._dir_index = NORTH_INDEX
            if True not in (obj.density for obj in world_map[y + 1][x]):
                y += 1
        elif internals.keyboard[K_DOWN]:
            self.dir = SOUTH
            self._dir_index = SOUTH_INDEX
            if True not in (obj.density for obj in world_map[y - 1][x]):
                y -= 1
        elif internals.keyboard[K_LEFT]:
            self.dir = WEST
            self._dir_index = WEST_INDEX
            if True not in (obj.density for obj in world_map[y][x - 1]):
                x -= 1
        elif internals.keyboard[K_RIGHT]:
            self.dir = EAST
            self._dir_index = EAST_INDEX
            if True not in (obj.density for obj in world_map[y][x + 1]):
                x += 1

        if (self.x, self.y) != (x, y):
            world_map[self.y][self.x].remove(self)
            self.x, self.y = x, y
            world_map[self.y][self.x].append(self)
            self._moving = True
            # print x / 32, y / 32 + 1, x, y
        else:
            self._moving = False

