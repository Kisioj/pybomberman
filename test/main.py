from PyBYOND import *
from PyBYOND import internals

Turf.icon = 'resources/turfs.png'


class Grass(Turf):
    icon_state = "grass"


class Water(Turf):
    icon_state = "water"
    density = True


class Wall(Turf):
    icon_state = "wall"
    density = True


class Player(Mob):
    icon = 'resources/turfs.png'
    icon_state = "arrow"
    x, y = 1, 1


world.mob = Player

if __name__ == '__main__':
    pyBYOND.run()

# Mob.icon = 'resources/turfs.png'
# Mob.icon_state = "arrow"
