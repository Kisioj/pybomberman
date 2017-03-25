from PyBYOND import *


class Box(Object):
    def __init__(self, *args, **kwargs):
        super(Box, self).__init__(*args, **kwargs)

class Bomb(Object):
    # icon = 'resources/bomb.png'
    # icon_state = ""

# class Wall1(Object):
#     icon = 'resources/map.png'
#     icon_state = "wall1"
#

    def __init__(self, *args, **kwargs):
        super(Bomb, self).__init__(*args, **kwargs)




class Player(Mob):
    def __login__(self):
        self.icon = 'resources/player.png'
        self.icon_state = ''
        self.x, self.y = 3, 2
        self.pixel_x = -16
        # b = Bomb()
        # b.x, b.y = 10, 10

    def __logout__(self):
        pass


world.mob = Player
pyBYOND.run()

# manage.py
# 1 uruchamianie servera
# 2 odpalanie gry
# 3 odpalanie edytora mapy
# 4 odpalanie edytora ikon