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
        # print '3'
        # yield sleep(2)
        # print '2'
        # yield sleep(2)
        # print '1'
        # yield sleep(3)
        yield sleep(7)
        delete(self)


class Explosion(Object):
    icon = 'resources/explosion.png'
    icon_state = ''
    @sleepy
    def start(self):
        # for direction in self.possible_directions:
        # for direction in (NORTH, SOUTH, EAST, WEST):
        #     for obj in get_step(self, direction):
        #         if isinstance(obj, BYONDtypes.Box):
        #             if not obj.exploding:
        #                 obj.explode()
        #         elif isinstance(obj, BYONDtypes.Bomb):
        #             if not obj.exploded:
        #                 print self, 'triggers explosion of', obj
        #                 obj.explode(explosion_source)
        yield sleep(4)
        delete(self)



class Bomb(Object):
    icon = 'resources/bomb.png'
    icon_state = ''
    density = True

    explosion_source = None
    exploded = False
    range = 1

    def __init__(self, *args, **kwargs):
        super(Bomb, self).__init__(*args, **kwargs)
        self._icon.scale(32, 32)
        spawn(30, self.explode)   # opcjonalny 3ci argument dodac z parametrami

    def explode(self, explosion_source=None):
        self.explosion_source = explosion_source

        self.exploded = True
        if self.explosion_source is None:
            print self, 'explodes'
        else:
            print self, 'chain explodes from', self.explosion_source

        for obj in self.loc:
            if isinstance(obj, BYONDtypes.Mob):
                print obj, 'got hurt'
        print 'self.range', self.range

        for direction in (NORTH, SOUTH, EAST, WEST):
            for step_size in xrange(1, self.range + 1):
                if not self.continue_explosion(direction, step_size):
                    break
        delete(self)

    def continue_explosion(self, direction, step_size):
        """

        :param direction:
        :param step_size:
        :return: True if explosion should continue further, else False
        """
        location = get_step(self, direction, step_size)
        for obj in location:
            if isinstance(obj, BYONDtypes.Turf) and obj.density:
                return False
            elif isinstance(obj, BYONDtypes.Box):
                if not obj.exploding:
                    obj.explode()
                Explosion(location.x, location.y)
                return False
            elif isinstance(obj, BYONDtypes.Bomb):
                if not obj.exploded:
                    print self, 'triggers explosion of', obj
                    obj.explode(self.explosion_source)

        Explosion(location.x, location.y)
        return True

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
