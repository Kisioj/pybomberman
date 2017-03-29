from PyBYOND import *
from PyBYOND import internals
import byteplay
import types
# byteplay.Code.from_code(obj.explode.im_func.func_code)
import inspect

def sleepy(func):
    def outer(self):
        # def inner(result):

        result = func(self)
        if isinstance(result, types.GeneratorType):
            seconds = next(result)
            spawn(seconds, result)
        # print result,
        return result
    return outer


def sleep(seconds):
    print 'sleep', seconds, 'seconds'
    return seconds


class Box(Object):
    icon = 'resources/map.png'
    icon_state = "wall1"
    density = True

    @sleepy
    def explode(self):
        """
        Uzywajac yielda jako sleepa oczywiscie nie bedziemy mogli nic zwrocic rowniez.
        Zastanawialem sie szczerze mowiac nad Threadami, ale uznalem, ze lepiej yieldem
        NAjpierw by trzeba bylo sprawdzic inspectorem czy tofunkcja generator i potem opakowac jezeli tak
        ewentualnie dodac yielda jezeli w zrodle funkcji znajdziemy sleepa https://pypi.python.org/pypi/byteplay
        """
        print '3'
        yield sleep(1)  # za pomoca generatorow mozna by to chyba zrobic o kurwa mac, yield vs Thready, oszukany sleep
        print '2'
        yield sleep(1)
        print '1'
        yield sleep(1)
        delete(self)  # self.delete()


class Bomb(Object):
    icon = 'resources/bomb.png'
    icon_state = ''
    density = True
    exploded = False

    def __init__(self, *args, **kwargs):
        super(Bomb, self).__init__(*args, **kwargs)
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
                    obj.explode()
                    # delete(obj)
                elif isinstance(obj, BYONDtypes.Bomb):
                    if not obj.exploded:
                        print self, 'triggers explosion of', obj
                        obj.explode(explosion_source)
        delete(self)

# obj.explode.im_func.func_code.co_code
Turf.icon = 'resources/map.png'


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

#
# class MapEdge01(MapEdge):
#     name = 'map_edge_01'
#     icon_state = 'map_edge_01'
#
#
# class MapEdge02(MapEdge):
#     name = 'map_edge_02'
#     icon_state = 'map_edge_02'
#
#
# class MapEdge03(MapEdge):
#     name = 'map_edge_03'
#     icon_state = 'map_edge_03'
#
#
# class MapEdge04(MapEdge):
#     name = 'map_edge_04'
#     icon_state = 'map_edge_04'
#
#
# class MapEdge05(MapEdge):
#     name = 'map_edge_05'
#     icon_state = 'map_edge_05'
#
#
# class MapEdge06(MapEdge):
#     name = 'map_edge_06'
#     icon_state = 'map_edge_06'
#
#
# class MapEdge07(MapEdge):
#     name = 'map_edge_07'
#     icon_state = 'map_edge_07'
#
#
# class MapEdge08(MapEdge):
#     name = 'map_edge_08'
#     icon_state = 'map_edge_08'
#
#
# class MapEdge09(MapEdge):
#     name = 'map_edge_09'
#     icon_state = 'map_edge_09'
#
#
# class MapEdge10(MapEdge):
#     name = 'map_edge_10'
#     icon_state = 'map_edge_10'
#
#
# class MapEdge11(MapEdge):
#     name = 'map_edge_11'
#     icon_state = 'map_edge_11'
#
#
# class MapEdge12(MapEdge):
#     name = 'map_edge_12'
#     icon_state = 'map_edge_12'
#
#
# class MapEdge13(MapEdge):
#     name = 'map_edge_13'
#     icon_state = 'map_edge_13'
#
#
# class MapEdge14(MapEdge):
#     name = 'map_edge_14'
#     icon_state = 'map_edge_14'
#
#
# class MapEdge15(MapEdge):
#     name = 'map_edge_15'
#     icon_state = 'map_edge_15'
#
#
# class MapEdge16(MapEdge):
#     name = 'map_edge_16'
#     icon_state = 'map_edge_16'
#
#
# class MapEdge17(MapEdge):
#     name = 'map_edge_17'
#     icon_state = 'map_edge_17'


