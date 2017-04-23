from PyBYOND import *
from PyBYOND import internals

Turf.icon = 'resources/turfs.png'


class Grass(Turf):
    icon_state = "grass"


class Water(Turf):
    icon_state = "water"
    density = True


class Wall(Turf):
    density = True

if __name__ == '__main__':
    pyBYOND.run()
