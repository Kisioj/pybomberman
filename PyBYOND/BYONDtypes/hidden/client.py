from ...verb import verbs

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
        print filename, 'plays'
