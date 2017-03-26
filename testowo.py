class MappableMeta(type):
    atrybut1 = 'MappableMeta.atrybut1'
    atrybut2 = 'MappableMeta.atrybut2'
    atrybut3 = 'MappableMeta.atrybut3'
    atrybut4 = 'MappableMeta.atrybut4'
    def __init__(cls, name, bases, dct):
        print cls, name, bases, dct
        super(MappableMeta, cls).__init__(name, bases, dct)


class Atom(object):
    __metaclass__ = MappableMeta
    atrybut1 = 'Atom.atrybut1'
    atrybut2 = 'Atom.atrybut2'
    atrybut3 = 'Atom.atrybut3'


class Turf(Atom):
    atrybut1 = 'Turf.atrybut1'
    atrybut2 = 'Turf.atrybut2'
    def __init__(self):
        self.atrybut1 = 'Turf.instance.atrybut1'

t = Turf()
print t.atrybut1, t.atrybut2, t.atrybut3
print dir(t)