from PyBYOND import *
import mappable
from PyBYOND import internals, world


class Player(Mob):
    def __login__(self):
        self.icon = 'resources/player.png'
        self.icon_state = ''
        self.x, self.y = 3, 2
        self.pixel_x = -16
        # b = Bomb()
        # b.x, b.y = 10, 10

        # b = mappable.Bomb()
        # b.x, b.y = 220, 220
        # internals.world_map[12][10].append(b)

    def __logout__(self):
        pass


@verb
def drop_bomb(usr):
    print usr, 'dropped the bomb'
    b = mappable.Bomb()
    b.x, b.y = usr.x, usr.y
    world.map.fields[usr.y][usr.x].append(b)

    # usr.play('Drop.wav')
    # b = Bomb()
    # b.loc = usr.x, usr.y, usr.z
    # b.range = usr.range
    # b.owner = usr

world.mob = Player
client.controls[K_LCTRL] = drop_bomb
pyBYOND.run()


# manage.py
# 1 uruchamianie servera
# 2 odpalanie gry
# 3 odpalanie edytora mapy
# 4 odpalanie edytora ikon