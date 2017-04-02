# moze po prostu dac intrukcje, ze nalezy zrobic plik main.py gdzi beda importowane wszystkie moduly, ktore chcemy zeby sie wykonaly

from PyBYOND import *
import mappable  # bez tej linijki wywali, moze by trzeba bylo zrobic jakies manage.py do uruchamiania, zeby moduly nie musialy sie importowac?
from PyBYOND import internals, world


class Player(Mob):
    icon = 'resources/player.png'
    icon_state = ''
    pixel_x = -16
    x, y = 12, 11     # x, y i z tez zrobic jako deskryptory najlepiej i jezeli np  ustawisz x na 0 to wszystko idzie na 0
    range = 3

    def __login__(self):
        print self, 'has logged in'
        self._icon.scale(64, 64)
        # self._icon_state = self._icon.icon_states[self.icon_state]
        print 'yolo'

    def __logout__(self):
        print self, 'has logged out'

    def move(self, *args, **kwargs):
        x, y = self.x, self.y
        super(Player, self).move(*args, **kwargs)
        if (self.x, self.y) != (x, y):
            print 'move', self.x, self.y
            for powerup in get_by_type(self.loc, BYONDtypes.Powerup):
                if powerup.name == "amount":
                    pass
                elif powerup.name == "speed":
                    pass
                elif powerup.name == "range":
                    pass
                elif powerup.name == "kick":
                    pass
                elif powerup.name == "throw":
                    pass
                self.client.play('resources/powerup.wav')
                delete(powerup)


@verb
def drop_bomb(usr):
    for atom in usr.loc:
        if isinstance(atom, (BYONDtypes.Bomb, BYONDtypes.Explosion)):
            return
    print usr, 'dropped the bomb'
    bomb = mappable.Bomb(usr.x, usr.y)  # lepiej chyba loc=usr.loc lub loc=locate(usr.x, usr.y)
    bomb.range = usr.range
    bomb.owner = usr
    usr.client.play('resources/drop.wav')

world.mob = Player
client.controls[K_LCTRL] = drop_bomb
pyBYOND.run()


# manage.py
# 1 uruchamianie servera
# 2 odpalanie gry
# 3 odpalanie edytora mapy
# 4 odpalanie edytora ikon


# TODO:
# LAYERS, zeby spod spodu niszczonego boxa bylo widac bonus
# KOPANIE BOMB
# RZUCANIE BOMBAMI
# WIEKSZA MAPKA (PRZEWIJANIE MAPKI)
# CLIENT.VIEW
# KOLIZJE NA BRZEGACH
# PER PIXEL CLICK