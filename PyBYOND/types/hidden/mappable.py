from ... import internals


class Mappable(type):
    # def __new__(mcs, name, bases, dct):
    #     print '-----------------------------------'
    #     print "Allocating memory for class", name
    #     print mcs
    #     print bases
    #     print dct
    #     return super(Mappable, mcs).__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        # print '-----------------------------------'
        # print "Initializing class", name
        # print cls
        # print bases
        # print dct
        internals.mappable_types[name] = cls
        super(Mappable, cls).__init__(name, bases, dct)