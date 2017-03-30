from PyBYOND import *
from PyBYOND import internals
# import byteplay
# import types
# byteplay.Code.from_code(obj.explode.im_func.func_code)
# import inspect



class Box(Object):
    icon = 'resources/map.png'
    icon_state = "wall1"
    density = True
    exploding = False

    @sleepy
    def explode(self):
        self.exploding = True
        self.icon_state = "wall1_fired"
        print '3'
        yield sleep(0.1)
        print '2'
        yield sleep(0.1)
        print '1'
        yield sleep(0.1)
        delete(self)


class Bomb(Object):
    icon = 'resources/bomb.png'
    icon_state = ''
    density = True
    exploded = False

    def __init__(self, *args, **kwargs):
        super(Bomb, self).__init__(*args, **kwargs)
        self._icon.scale(32, 32)
        spawn(3, self.explode)   # opcjonalny 3ci argument dodac z parametrami

    def explode(self, explosion_source=None):
        if not explosion_source:
            explosion_source = self

        self.exploded = True
        if explosion_source is self:
            print self, 'explodes'
        else:
            print self, 'chain explodes from', explosion_source

        for obj in self.loc:
            if isinstance(obj, BYONDtypes.Mob):
                print obj, 'got hurt'

        for direction in (NORTH, SOUTH, WEST, EAST):
            for obj in get_step(self, direction):
                if isinstance(obj, BYONDtypes.Box):
                    if not obj.exploding:
                        obj.explode()
                elif isinstance(obj, BYONDtypes.Bomb):
                    if not obj.exploded:
                        print self, 'triggers explosion of', obj
                        obj.explode(explosion_source)
        delete(self)

Turf.icon = 'resources/map.png'
Turf._icon.scale(32, 32)


class Grass(Turf):
    icon_state = 'grass'


class Wall2(Turf):
    icon_state = 'wall2'
    density = True


class MapEdge(Turf):
    density = True

for i in xrange(1, 18):
    type(
        'MapEdge{:0>2}'.format(i),
        (MapEdge, ),
        {'icon_state': 'map_edge_{:0>2}'.format(i)}
    )
