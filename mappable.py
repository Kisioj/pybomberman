from PyBYOND import *
from PyBYOND import internals
import random
# import byteplay
# import types
# byteplay.Code.from_code(obj.explode.im_func.func_code)
# import inspect

directions = (NORTH, SOUTH, EAST, WEST)


class Box(Obj):
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
        self.drop_powerup()
        delete(self)

    def drop_powerup(self):
        if random.randint(1, 100) <= 50:
            powerup_class = random.choice([Amount, Speed, Range])
            powerup_class(self.x, self.y)

class Explosion(Obj):
    icon = 'resources/explosion.png'
    icon_state = 'NSEW'

    CENTER = 1
    BODY = 2
    TAIL = 3
    DIRECTION_TO_CHAR_MAP = {
        NORTH: 'N',
        SOUTH: 'S',
        EAST: 'E',
        WEST: 'W',
    }

    def __init__(self, *args, **kwargs):
        super(Explosion, self).__init__(*args, **kwargs)
        self._icon.scale(32, 32)

    @sleepy
    def start(self, direction=None, fire_type=None):
        def check_neighbour(direction):
            for obj in get_step(self, direction):
                if isinstance(obj, Turf) and obj.density:
                    print 'dense', obj
                    return ''
            return Explosion.DIRECTION_TO_CHAR_MAP[direction]

        self.dir = direction
        if fire_type == Explosion.CENTER:
            self.layer = OBJ_LAYER + 1
            icon_state = ''
            for direction in directions:
                icon_state += check_neighbour(direction)
            self.icon_state = icon_state

        elif fire_type == Explosion.BODY:
            self.layer = OBJ_LAYER + 2
            if self.dir in [NORTH, SOUTH]:
                self.icon_state = 'NS'
            else:
                self.icon_state = 'EW'
        elif fire_type == Explosion.TAIL:
            self.icon_state = Explosion.DIRECTION_TO_CHAR_MAP[self.dir]

        yield sleep(4)
        delete(self)


class Bomb(Obj):
    icon = 'resources/bomb.png'
    icon_state = ''
    density = True

    explosion_source = None
    exploded = False
    _range = None
    ranges = None

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        self._range = value
        self.ranges = dict(zip(directions, [value] * len(directions)))

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

        for direction in directions:
            for step_size in xrange(1, self.ranges[direction] + 1):
                if not self.continue_explosion(direction, step_size):
                    break
        expl = Explosion(self.x, self.y)
        expl.start(fire_type=Explosion.CENTER)
        delete(self)

    def continue_explosion(self, direction, step_size):
        """

        :param direction:
        :param step_size:
        :return: True if explosion should continue further, else False
        """
        location = get_step(self, direction, step_size)
        distance = get_dist(self, location)
        range_left = self.ranges[direction] - distance
        if range_left:
            fire_type = Explosion.BODY
        else:
            fire_type = Explosion.TAIL

        # if range_left:
        #     for obj in get_step(ref=location, direction=direction):
        #
        #     fire_type = Explosion.TAIL

        for obj in location:
            if isinstance(obj, BYONDtypes.Turf) and obj.density:
                return False
            elif isinstance(obj, BYONDtypes.Powerup):
                delete(obj)
            elif isinstance(obj, BYONDtypes.Box):
                if not obj.exploding:
                    obj.explode()
                expl = Explosion(location.x, location.y)
                expl.start(direction=direction, fire_type=Explosion.TAIL)
                return False
            elif isinstance(obj, BYONDtypes.Bomb):
                if not obj.exploded:
                    print self, 'triggers explosion of', obj
                    obj.ranges[direction] = max(obj.range, range_left)
                    obj.explode(self.explosion_source)
                return False
        expl = Explosion(location.x, location.y)
        expl.start(direction=direction, fire_type=fire_type)
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


class Powerup(Obj):
    icon = 'resources/powerups.png'

    def __init__(self, *args, **kwargs):
        super(Powerup, self).__init__(*args, **kwargs)
        self._icon.scale(32, 32)


class Amount(Powerup):
    icon_state = 'amount'

    def pick_up(self):
        pass


class Speed(Powerup):
    icon_state = 'speed'

    def pick_up(self):
        pass


class Range(Powerup):
    icon_state = 'range'

    def pick_up(self):
        pass


class Kick(Powerup):
    icon_state = 'kick'


class Throw(Powerup):
    icon_state = 'throw'
