from PyBYOND import *
from PyBYOND import internals
import random
# import byteplay
# import base_types
# byteplay.Code.from_code(obj.explode.im_func.func_code)
# import inspect

directions = (NORTH, SOUTH, EAST, WEST)


class Floor(Area):
    pass

class House(Area):
    pass

class Box(Obj):
    icon = 'resources/map.png'
    icon_state = "wall1"
    density = True
    exploded = False

    @sleepy
    def explode(self):
        self.exploded = True
        self.icon_state = "wall1_fired"
        # print '3'
        # yield sleep(20)
        # print '2'
        # yield sleep(20)
        # print '1'
        # yield sleep(30)

        yield sleep(40)
        # self.density = False
        self.drop_powerup()
        yield sleep(30)
        delete(self)

    def drop_powerup(self):
        if random.randint(1, 100) <= 90:
            powerup_class = random.choice([Amount, Speed, Range])
            powerup_class(self.x, self.y)


class Explosion(Obj):
    icon = 'resources/explosion.png'
    icon_state = 'NSEW'

    owner = None
    DIRECTION_TO_CHAR_MAP = {
        NORTH: 'N',
        SOUTH: 'S',
        EAST: 'E',
        WEST: 'W',
    }

    def __init__(self, *args, **kwargs):
        super(Explosion, self).__init__(*args, **kwargs)
        self.id = world.time
        self._icon.scale(32, 32)

    @sleepy
    def start(self):
        icon_state = ''
        for direction in directions:
            for atom in get_step(ref=self, direction=direction):
                if isinstance(atom, Explosion) and self.id == atom.id:
                    icon_state += Explosion.DIRECTION_TO_CHAR_MAP[direction]
                    break
        if not icon_state:
            icon_state = 'NSEW'
        self.icon_state = icon_state
        print(self.id, self.x, self.y, self.icon_state, icon_state)
        yield sleep(40)
        delete(self)


class Locations(list):
    def __contains__(self, item):
        for location in self:
            if location == item:
                return True
        return False


class Bomb(Obj):
    icon = 'resources/bomb.png'
    icon_state = ''
    density = True

    owner = None
    explosion_source = None
    exploded = False
    range = 1

    def __init__(self, *args, **kwargs):
        super(Bomb, self).__init__(*args, **kwargs)
        self._icon.scale(32, 32)
        self.explosion_locations = Locations()
        spawn(self.explode, delay=30)   # opcjonalny 3ci argument dodac z parametrami

    def explode(self, explosion_source=None):
        self.explosion_source = explosion_source

        self.exploded = True
        if self.explosion_source is None:
            self.explosion_locations.append(self.loc)
            print(self, 'explodes')
        else:
            print(self, 'chain explodes from', self.explosion_source)

        for obj in self.loc:
            if isinstance(obj, BYONDtypes.Mob):
                print(obj, 'got hurt')
        print('self.range', self.range)

        for direction in directions:
            for step_size in range(1, self.range + 1):
                if not self.continue_explosion(direction, step_size):
                    break

        if not self.explosion_source:
            explosions = []
            for loc in self.explosion_locations:
                explosions.append(Explosion(loc.x, loc.y))
            for expl in explosions:
                expl.start()
            self.owner.client.play('resources/explosion.wav')
        delete(self)

    def continue_explosion(self, direction, step_size):
        def add_explosion_location():
            if location not in explosion_source.explosion_locations:
                explosion_source.explosion_locations.append(location)

        explosion_source = self.explosion_source
        if not explosion_source:
            explosion_source = self
        location = get_step(self, direction, step_size)
        for atom in location:
            if isinstance(atom, BYONDtypes.Turf) and atom.density:
                return False
            elif isinstance(atom, BYONDtypes.Box):
                if not atom.exploded:
                    atom.explode()
                add_explosion_location()
                return False
            elif isinstance(atom, BYONDtypes.Powerup):
                delete(atom)
            elif isinstance(atom, BYONDtypes.Bomb) and not atom.exploded:
                atom.explode(explosion_source=explosion_source)
        add_explosion_location()
        return True

Turf.icon = 'resources/map.png'
Turf._icon.scale(32, 32)


class Grass(Turf):
    icon_state = 'grass'


class DarkGrass(Turf):
    icon_state = 'grass'


class Wall2(Turf):
    icon_state = 'wall2'
    density = True


class MapEdge(Turf):
    density = True

for i in range(1, 18):
    type(
        'MapEdge{:0>2}'.format(i),
        (MapEdge, ),
        {'icon_state': 'map_edge_{:0>2}'.format(i)}
    )


class Powerup(Obj):
    icon = 'resources/powerups.png'
    layer = TURF_LAYER

    def __init__(self, *args, **kwargs):
        super(Powerup, self).__init__(*args, **kwargs)
        self._icon.scale(32, 32)


class Amount(Powerup):
    icon_state = 'amount'


class Speed(Powerup):
    icon_state = 'speed'


class Range(Powerup):
    icon_state = 'range'


class Kick(Powerup):
    icon_state = 'kick'


class Throw(Powerup):
    icon_state = 'throw'
