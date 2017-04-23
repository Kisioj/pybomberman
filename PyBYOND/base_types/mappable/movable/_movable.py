from pygame.constants import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
)

from PyBYOND.base_types.atom import Atom
from PyBYOND.constants import (
    SOUTH,
    NORTH,
    WEST,
    EAST,
)
from PyBYOND import singletons as si
from PyBYOND.api import (
    get_step,
)

class Movable(Atom):
    _moving = False

    def moving(self):
        if self._moving:
            x, y = self.x, self.y
            pixel_step_size = 4
            to_screen_x = x * si.world.icon_size
            to_screen_y = (si.world.map.height - y) * si.world.icon_size
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

        key_up = si.keyboard[K_UP]
        key_down = si.keyboard[K_DOWN]
        key_right = si.keyboard[K_RIGHT]
        key_left = si.keyboard[K_LEFT]

        movements = (
            (key_up and not key_down, NORTH),
            (key_down and not key_up, SOUTH),
            (key_right and not key_left, EAST),
            (key_left and not key_right, WEST),
        )

        for condition, direction in movements:
            if condition:
                self.Move(
                    location=get_step(ref=self, direction=direction),
                    direction=direction
                )
                print('MOVED {} {}'.format(self.x, self.y))
                break

        # if key_up and not key_down:
        #     direction = NORTH
        #     location = internals.get_step(ref=self, direction=direction)
        #     self.move(location=location, direction=direction)
        #
        # elif key_down and not key_up:
        #     direction = SOUTH
        #     location = internals.get_step(ref=self, direction=direction)
        #     self.move(location=location, direction=direction)
        #
        # elif key_left and not key_right:
        #     direction = WEST
        #     location = internals.get_step(ref=self, direction=direction)
        #     self.move(location=location, direction=direction)
        #
        # elif key_right and not key_left:
        #     direction = EAST
        #     location = internals.get_step(ref=self, direction=direction)
        #     self.move(location=location, direction=direction)

    def Move(self, location, direction):
        self.dir = direction

        dense_object = [
            obj
            for obj in location
            if obj.density is True
        ]
        if dense_object:
            self.Bump(dense_object[0])
        else:
            if not self.loc.Exit(self, location):
                return
            if not location.Enter(self, self.loc):
                return
            self.loc.Exited(self, location)
            location.Entered(self, self.loc)

            world_map = si.world.map.fields
            world_map[self.y][self.x].remove(self) ## jakos to inaczej zrobic, zby to sie w setterze robilo samo x, y
            self.x, self.y = location.x, location.y
            world_map[self.y][self.x].append(self) ## jakos to inaczej zrobic, zby to sie w setterze robilo samo x , y
            self._moving = True

    def Bump(self, obstacle):
        print(self, 'bumps into', obstacle)