from ... import constants
import core
import pygame


class Client(object):
    def __init__(self):
        self.mob = None
        self.controls = {}

    def __keydown__(self, key):
        # print 'Client.__kedown__', key, verbs.items()
        if key in self.controls:
            self.controls[key](self.mob)

    def __keyup__(self, key):
        pass

    def play(self, filename):
        sound = pygame.mixer.Sound(filename)
        sound.play()
        print filename, 'plays'

    def __north__(self):
        self.mob.move(loc=core.get_step(self.mob, constants.NORTH), direction=constants.NORTH)

    def __south__(self):
        self.mob.move(loc=core.get_step(self.mob, constants.SOUTH), direction=constants.SOUTH)

    def __east__(self):
        self.mob.move(loc=core.get_step(self.mob, constants.EAST), direction=constants.EAST)

    def __west__(self):
        self.mob.move(loc=core.get_step(self.mob, constants.WEST), direction=constants.WEST)

    def __move__(self, location, direction):
        return self.mob.move(location=location, direction=direction)
