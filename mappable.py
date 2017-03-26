from PyBYOND import *


class Box(Object):
    name = "wall1"
    icon = 'resources/map.png'
    icon_state = "wall1"
    density = True


class Bomb(Object):
    icon = 'resources/bomb.png'
    icon_state = ''
    density = True
    # def __init__(self):
    #     pass




Turf.icon = 'resources/map.png'
print Turf.icon
Turf.create(name='grass', icon_state='grass')
Turf.create(name='wall2', icon_state='wall2', density=True)
for i in xrange(1, 18):
    Turf.create(
        name='map_edge_{:0>2}'.format(i),
        icon_state='map_edge_{:0>2}'.format(i),
        density=True
    )
