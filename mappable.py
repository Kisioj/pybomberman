from PyBYOND import *
from PyBYOND import internals


class Box(Object):
    name = "wall1"
    icon = 'resources/map.png'
    icon_state = "wall1"
    density = True


class Bomb(Object):
    icon = 'resources/bomb.png'
    icon_state = ''
    density = True

    def __init__(self, **kwargs):
        super(Bomb, self).__init__(**kwargs)
        self.exploded = False
        spawn(3, self.explode)   # opcjonalny 3ci argument dodac z parametrami

    def explode(self, explosion_source=None):
        if not explosion_source:
            explosion_source = self

        self.exploded = True
        if explosion_source is self:
            print self, 'explodes'
        else:
            print self, 'chain explodes from', explosion_source

        for direction in (NORTH, SOUTH, WEST, EAST):
            for obj in get_step(self, direction):
                if isinstance(obj, Box):
                    delete(obj)
                elif isinstance(obj, Bomb):
                    if not obj.exploded:
                        print self, 'triggers explosion of', obj
                        obj.explode(explosion_source)
        delete(self)



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
